import torch
from torch import nn
import math

class OneHeadSelfAttention(nn.Module):
    def __init__(self, d_model: int):
        super().__init__()
        self.d_model = d_model
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [batch, seq_len, d_model]
        q = self.w_q(x)
        k = self.w_k(x)
        v = self.w_v(x)

        score = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_model)  # [B, S, S]
        attn_weights = self.softmax(score)
        output = torch.matmul(attn_weights, v)  # [B, S, D]
        return output

if __name__ == "__main__":
    x = torch.randn(16, 64, 512)
    attn = OneHeadSelfAttention(d_model=512)
    y = attn(x)
    print(y.shape)  # torch.Size([16, 64, 512])