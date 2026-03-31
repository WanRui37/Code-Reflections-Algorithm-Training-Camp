import torch
from torch import nn
import math


class OneHeadSelfAttention():
  def __init__(self, d_model):
    super().__init__()
    self.d_model = d_model
    self.w_q = nn.Linear(d_model, d_model)
    self.w_k = nn.Linear(d_model, d_model)
    self.w_v = nn.Linear(d_model, d_model)
    self.softmax = nn.softmax(-1)  ## 错了
    
  def forwarf(self, x):
    q = self.w_q(x)
    k = self.w_k(x)
    v = self.w_v(x)
    
    score = torch.mulmat(q, k.transport(-2, -1)) / math.sqrt(self.d_model) ## 错了
    attn = self.softmax(score)
    output = attn @ v
    ## 错了
    
if __name__ == "__main__":