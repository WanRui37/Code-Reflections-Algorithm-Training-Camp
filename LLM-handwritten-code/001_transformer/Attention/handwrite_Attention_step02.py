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
        B, T, C = x.shape

        q = self.w_q(x)  # [B,T,C]
        k = self.w_k(x)  # [B,T,C]
        v = self.w_v(x)  # [B,T,C]

        scores = (q @ k.transpose(-2, -1)) / math.sqrt(C)

        causal_mask = torch.triu(torch.ones(T, T, device=x.device, dtype=torch.bool), diagonal=1)
        scores = scores.masked_fill(causal_mask, float("-inf"))

        attn = self.softmax(scores)
        output = attn @ v
        return output


if __name__ == "__main__":
    x = torch.randn(2, 4, 512)  # B=2, T=4, C=512
    attn = OneHeadSelfAttention(d_model=512)
    y = attn(x)
    print(f"Output shape: {y.shape}")