import torch
from torch import nn
import math

class OneHeadSelfAttention(nn.Module):
  def __init__(self, d_model):
    super().__init__()
    self.d_model = d_model
    self.w_q = nn.Linear(d_model, d_model)
    self.w_k = nn.Linear(d_model, d_model)
    self.w_v = nn.Linear(d_model, d_model)
    self.softmax = nn.Softmax(dim=-1)
    
  def forward(self, x):
    q = self.w_q(x)
    k = self.w_k(x)
    v = self.w_v(x)
    
    score = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_model)
    attn = self.softmax(score)
    out = torch.matmul(attn, v)
    return out
    
    
if __name__ == "__main__":
  x = torch.randn(16,24,512)
  d_model = 512
  attn = OneHeadSelfAttention(d_model)
  out = attn(x)
  print(f"out's shape: {out.shape}")