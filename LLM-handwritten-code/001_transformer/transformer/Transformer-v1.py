class Embedding(nn.Module):
  def __init__(self, vocab_size, d_model):
    super().__init__()
    self.embedding = nn.Embedding(vocab_size, d_model)
    
  def forward(self, x):
    out = self.embedding(x) * math.sqrt(self.d_model)
    
    return out
    
class PositionalEncoding(nn.Module):
  def __init__(self, max_len, d_model):
    super().__init__()
    
    pe = torch.zeros(max_len, d_model)
    position = torch.arrange(0, max_len).unsqueeze(1)
    div_item = torch.exp(torch.arrange(0,d_model,2) * (-math.log(10000)) / d_model)
    pe[:, 0::2] = torch.sin(position * div_item)
    pe[:, 1::2] = torch.cos(position * div_item)
    pe = pe.unsqueeze(0)
    self.register_buffer('pe', pe)
    
  def forward(self, x):
    out = x + self.pe[:, :x.size(1)]
    return out
    
