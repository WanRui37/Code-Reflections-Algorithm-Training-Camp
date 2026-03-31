import torch
from torch import nn
import math

class MultiHeadSelfAttention(nn.Module):
  def __init__(self, d_model, head):
    super().__init__()
    assert d_model % head == 0
    self.head = head
    self.head_dim = d_model // head
    self.w_q = nn.Linear(d_model, d_model)
    self.w_k = nn.Linear(d_model, d_model)
    self.w_v = nn.Linear(d_model, d_model)
    self.w_o = nn.Linear(d_model, d_model)
    self.softmax = nn.Softmax(dim=-1)
    
  def forward(self, x):
    B, T, C = x.shape
    
    q = self.w_q(x).view(B, T, self.head, self.head_dim).transpose(1, 2)
    k = self.w_k(x).view(B, T, self.head, self.head_dim).transpose(1, 2)
    v = self.w_v(x).view(B, T, self.head, self.head_dim).transpose(1, 2)
    
    score = q @ k.transpose(-2, -1) / math.sqrt(self.head_dim)
    
    casual_mask = torch.triu(
      torch.ones((T,T), device=x.device, dtype=torch.bool),
      diagonal=1
    )
    score = score.masked_fill(casual_mask.unsqueeze(0).unsqueeze(0), float(-10000))
    
    attn = self.softmax(score)
    attn = attn @ v
    attn = attn.transpose(1, 2).contiguous().view(B, T, C)
    out = self.w_o(attn)
    
    return out