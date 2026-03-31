import torch
from torch import nn
import math


class OneHeadSelfAttention(nn.Module):
  def __init__(self, d_model=None):
    super().__init__()
    self.d_model = d_model
    self.w_q = nn.Linear(d_model, d_model)
    self.w_k = nn.Linear(d_model, d_model)
    self.w_v = nn.Linear(d_model, d_model)
    self.softmax = nn.Softmax(dim=-1)
    
  def forward(self, x):
    B, T, C = x.shape
    
    q = self.w_q(x)
    k = self.w_k(x)
    v = self.w_v(x)
    
    score = q @ k.transpose(-2, -1) / math.sqrt(C)
    
    casual_mask = torch.tril((T,T), diagnoal=1)
    score = score.mask_fill(casual_mask, -inf)
    
    attn = self.softmax(score)
    out = attn @ v