class Embedding(nn.Module):
  def __init__(self, vocab_size, d_model):
    super().__init__()
    self.embedding = nn.Embedding(vocab_size, d_model)
    
  def forward(self, x):
    out = self.embedding() * math.sqrt(d_model)
    return out
    
    
class PositionalEncoding(nn.Module):
  def __init__(self, max_len, d_model):
    super().__init__()
    pe = torch.zeros(max_len, d_model)
    position = torch.arrange(0, max_len, dtype=float).unsqueeze(1)
    div = torch.exp(torch.arrange(0, d_model, 2) * (-math.log(10000.0) / d_model))
    
    pe[:, 0::2] = torch.sin(position * div)
    pe[:, 1::2] = torch.cos(position * div)
    pe = pe.unsqueeze(0)
    self.register_buffer('pe', pe)
    
    
  def forward(self, x):
    out = x + pe[:, x.size(1)]
    
    return out
    