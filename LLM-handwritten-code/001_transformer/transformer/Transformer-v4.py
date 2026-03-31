class Embedding(nn.Module):
  def __init__(self, vocab_size, d_model):
    super().__init__()
    self.d_model = d_model
    self.embedding = nn.Embedding(vocab_size, d_model)
    
  def forward(self, x):
    out = self.embedding(x) * math.sqrt(self.d_model)
    return out
    
class PositionalEncoding(nn.Module):
  def __init__(self, max_len, d_model):
    super().__init__()
    pe = torch.zeros(max_len, d_model)
    position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
    div = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000) / d_model) )
    pe[:, 0::2] = torch.sin(position * div)
    pe[:, 1::2] = torch.cos(position * div)
    pe = pe.unsqueeze(0)
    self.register_buffer(pe)
    
  def forward(self, x):
    out = x + self.pe[:,:x.size(1)]
    
    return out
    
def MultiHeadAttention(nn.Module):
  def __init__(self, d_model, head):
    super().__init__()
    self.d_model = d_model
    self.head = head
    assert d_model % head==0
    self.head_dim = d_model // head
    
    self.w_q = nn.Linear(d_model, d_model)
    self.w_k = nn.Linear(d_model, d_model)
    self.w_v = nn.Linear(d_model, d_model)
    
  def forward(self, x):
    B, T, C = x.shape
    
    q = self.w_q(x).view(B, T, self.head, self.head_dim).transpose(1, 2)
    k = self.w_k(x).view(B, T, self.head, self.head_dim).transpose(1, 2)
    v = self.w_v(x).view(B, T, self.head, self.head_dim).transpose(1, 2)
    score = q @ k.transpose(-2, -1) / math.sqrt(self.d_model)
    
    causal_mask = torch.triu(
        torch.ones(T, T, device=x.device, dtype=torch.bool),
        diagonal=1,
    )
    scores = scores.masked_fill(causal_mask.unsqueeze(0).unsqueeze(0), float("-inf"))
    
    attn_weights = torch.softmax(scores, dim=-1)
    output = torch.matmul(attn_weights, V)

    output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
    output = self.Wo(output)

    return output
    
def FFN(nn.Module):
  def __init__(self, d_model, d_ff):
    super().__init__()
    self.fc1 = nn.Linear(d_model, d_ff)
    self.fc2 = nn.Linear(d_ff, d_model)
    self.act = nn.ReLU()
    
  def forward(self, x):
    out = self.fc1(x)
    out = self.act(out)
    out = self.fc1(out)
    
    return out
    
def EncoderLayer(nn.Module):
  def __init__(self, d_model, num_heads, d_ff, dropout):
    super().__init__()
    self.attn = MultiHeadAttention(d_model, num_heads)
    self.ffn = FFN(d_model, d_ff)
    self.norm1 = nn.LayerNorm(d_model)
    self.norm2 = nn.LayerNorm(d_model)
    self.dropout = nn.Dropout(dropout)
    

  def forward(self, x):
    attn_output = self.attn(x)
    x = self.norm1(x + self.dropout(attn_output))

    ffn_output = self.ffn(x)
    x = self.norm2(x + self.dropout(ffn_output))

    return x
    
    
def Transformer(nn.Module):
  def __init__(self, vocab_size, d_model, num_layers):
    super().__init__()
    self.embedding = Embedding(vocab_size, d_model)
    self.pos_encoding = PositionalEncoding(d_model)
    self.layers = nn.ModuleList([EncoderLayer(d_model, num_heads, d_ff) for _ in range(num_layers)])
    self.linear = nn.Linear(d_model, vocab_size)
    
  def forward(self, x):
      x = self.embedding(x)
      x = self.pos_encoding(x)

      for i, layer in enumerate(self.layers):
          x = layer(x)

      logits = self.linear(x)

      return logits