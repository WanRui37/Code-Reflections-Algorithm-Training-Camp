import torch
from torch import nn

class LayerNorm(nn.Module):
  def __init__(self, d_model, eps):
    super().__init__()
    
    self.gamma = nn.Parameter(torch.ones(d_model))
    self.beta = nn.Parameter(torch.zeros(d_model))
    self.eps = eps
    
  def forward(self, x):
    mean = x.mean(dim=-1, keepdim=True)
    var = x.var(dim=-1, unbias=False, keepdim=True)
    out = (x-mean) / torch.sqrt(var+self.eps)
    out = out * self.gamma + self.beta
    return out