import torch
from torch import nn
import math

class OneHeadSelfAttention(nn.module): ## 错了
  def __init__(self, d_model):
    super().__init__()
    self.d_model = d_model
    self.w_q = nn.Linear(d_model, d_model)
    self.w_k = nn.Linear(d_model, d_model)
    self.w_v = nn.Linear(d_model, d_model)
    self.softmax = nn.softmax(dim=-1) ## 错了
    
  def forward(self, x):
    q = w_q(x)
    k = w_k(x)
    v = w_v(x)
    
    score = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_model)
    attn = self.softmax(score)
    output = torch.matmul(attn, v)
    return output
    
if __name__ == "main":
  x = torch.randn(16,24,512)
  d_model = 512
  attn = OneHeadSelfAttention(d_model)
  out = attn(x)
  ## 错了