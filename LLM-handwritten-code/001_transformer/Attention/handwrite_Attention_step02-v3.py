import torch
from torch import nn
import math

class OneHeadSelfAttention(nn.Module):
  def __init__(self, d_model):
    super().__init__()
    self.w_q = nn.Linear(d_model, d_model)
    self.w_k = nn.Linear(d_model, d_model)
    self.w_v = nn.Linear(d_model, d_model)
    self.softmax = nn.Softmax(dim=-1)
    
  def forward(self, x):
    B, T, C = x.shape
    
    q = self.w_q(x)
    k = self.w_k(x)
    v = self.w_v(x)
    
    score = q@k.transpose(-2,-1) / math.sqrt(C)
    
    casual_mask = torch.triu(
      torch.ones((T,T), device=x.device, dtype=torch.bool),
      diagonal=1
    )
    score = score.masked_fill(casual_mask, float(-10000))
    attn = self.softmax(score)
    out = attn @ v
    return out