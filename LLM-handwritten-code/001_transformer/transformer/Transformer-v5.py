class Embedding(nn.Module):
  def __init__(self, vocab_size, d_model):
    super().__init__()
    self.embedding = nn.Embedding(vocab_size, d_model)
    self.d_model = d_model
    
  def forward(self, x):
    x = self.embedding(x) * math.sqrt(self.d_model)
    # 没有返回值
    
class PositionalEncoding(nn.Module):
  def __init__(self, max_len, d_model):
    super().__init__()
    pe = torch.zeros(max_len, d_model)
    position = torch.arange(0, max_len, dtype=torch.float) # 缺少了.unsqueeze(1)
    div_item = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000) / d_model))
    pe[:, 0::2] = torch.sin(position * div_item)
    pe[:, 1::2] = torch.cos(position * div_item)
    pe = pe.unsqueeze(0)
    self.register_buffer(pe) #应该是self.register_buffer('pe', pe)
    
  def forward(self, x):
    x = x + self.pe[:, :x.size(1)]
    return x
    
class MultiHeadAttention(nn.Module):
  def __init__(self, d_model, num_head):
    super().__init__()
    self.d_model = d_model
    self.num_head = num_head
    assert d_model%num_head ==0
    self.head_dim = d_model // num_head
    
    self.w_q = nn.Linear(d_model, d_model)
    self.w_k = nn.Linear(d_model, d_model)
    self.w_v = nn.Linear(d_model, d_model)
    self.w_o = nn.Linear(d_model, d_model)
    
  def forward(self, x):
    B, T, C = x.shape
    
    q = self.w_q(x).view(B, T, self.num_head, self.head_dim).transpose(1, 2)
    k = self.w_k(x).view(B, T, self.num_head, self.head_dim).transpose(1, 2)
    v = self.w_v(x).view(B, T, self.num_head, self.head_dim).transpose(1, 2)
    
    score = q @ k.transpose(-2, -1) / math.sqrt(self.d_model) # 应该是math.sqrt(self.head_dim)
    
    casual_mask = torch.triu(
      torch.ones(T,T, dtype=torch.float),
      diagonal=1)
    casual_mask = score.mask_filled(float(-inf))
    # 应该是这样的scores = scores.masked_fill(causal_mask.unsqueeze(0).unsqueeze(0), float("-inf"))
    

    attn_out = torch.softmax(score, dim=-1)
    attn_out = attn_out @ V
    
    # output = attn_out.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
    # output = self.w_o(output)
    
    return attn_out
    
class FFN(nn.Module):
  def __init__(self, d_model, d_ff):
    super().__init__()
    self.fc1 = nn.Linear(d_model, d_ff)
    self.fc2 = nn.Linear(d_ff, d_model)
    self.act = nn.ReLU()
    
  def forward(self, x):
    x = self.fc2(self.act(self.fc1(x)))
    # 没有返回值
    
class EncoderLayer(nn.Module):
  def __init__(self, d_model, d_ff, num_head, dropout):
    super().__init__()
    self.attn = MultiHeadAttention(d_model, num_head)
    self.ffn = FFN(d_model, d_ff)
    self.norm1 = nn.LayerNorm(d_model)
    self.norm2 = nn.LayerNorm(d_model)
    self.dropout = nn.Dropout(dropout)
    
  def forward(self, x):
    x = self.norm1(self.dropout(self.attn(x))) + x
    x = self.norm2(self.dropout(self.ffn(x))) + x
    
    return x
    
class Transformer(nn.Module):
  def __init__(self, vocab_size, max_len, d_model, d_ff, num_head, dropout, layer_num):
    super().__init__()
    self.embedding = Embedding(vocab_size, d_model)
    self.pos = PositionalEncoding(max_len, d_model)
    self.layers = nn.ModuleList([EncoderLayer(d_model, d_ff, num_head, dropout) for _ in range(layer_num)])
    self.fc = nn.Linear(d_model, d_model) # nn.Linear(d_model, vocab_size)
    
  def forward(self, x):
    x = self.embedding(x)
    x = self.pos(x)
    for layer in self.layers:
      x = layer(x)
      
    x = self.fc(x)
    
    return x
    