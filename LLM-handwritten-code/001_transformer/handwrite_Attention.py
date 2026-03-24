import torch
from torch import nn 
import math

X = torch.randn(16,64,512)
print(X.shape)

d_model = 512
n_head = 8

class one_head_attention(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)

    def forward(self, x):
        # x: (B, T, D)
        Q = self.w_q(x)   # (B, T, D)
        K = self.w_k(x)   # (B, T, D)
        V = self.w_v(x)   # (B, T, D)

        score = Q @ K.transpose(-2, -1) / math.sqrt(Q.size(-1))  # (B, T, T)
        attn = torch.softmax(score, dim=-1)                      # (B, T, T)
        out = attn @ V                                           # (B, T, D)
        return out
    
class multi_head_attention(nn.Module):
    def __init__(self, d_model, n_head):
        # 调用父类构造函数
        super(multi_head_attention, self).__init__()
        
        # 保存注意力头的数量和模型的维度
        self.n_head = n_head
        self.d_model = d_model
        
        # 定义查询（Q）、键（K）、值（V）的线性变换层
        self.w_q = nn.Linear(d_model, d_model)  # 输入d_model维度，输出d_model维度
        self.w_k = nn.Linear(d_model, d_model)  # 输入d_model维度，输出d_model维度
        self.w_v = nn.Linear(d_model, d_model)  # 输入d_model维度，输出d_model维度
        self.w_o = nn.Linear(d_model, d_model)  # 输出线性变换层
        
        # 定义softmax函数，用于计算注意力得分的归一化
        self.softmax = nn.Softmax(dim=-1)  # softmax会在最后一维（dim=-1）上操作
        
    def forward(self, q, k, v):
        # 获取输入查询（q），键（k），值（v）的形状
        B, T, D = q.shape  # B: batch size, T: sequence length, D: feature dimension (d_model)
        
        # 每个注意力头的维度
        n_d = self.d_model // self.n_head  # 每个头的维度（d_model / n_head）
        
        # 将输入的q、k、v通过各自的线性变换层映射到新的空间
        q, k, v = self.w_q(q), self.w_k(k), self.w_v(v)
        
        # 将q, k, v按头数进行拆分（reshape），并转置使得各头的计算可以并行
        # q, k, v的形状变为 (B, T, n_head, n_d)，然后转置变为 (B, n_head, T, n_d)
        q = q.view(B, T, self.n_head, n_d).transpose(1, 2)  # (B, n_head, T, n_d)
        k = k.view(B, T, self.n_head, n_d).transpose(1, 2)  # (B, n_head, T, n_d)
        v = v.view(B, T, self.n_head, n_d).transpose(1, 2)  # (B, n_head, T, n_d)

        # 计算缩放点积注意力（scaled dot-product attention）
        score = q @ k.transpose(2, 3) / math.sqrt(n_d)  # (B, n_head, T, T)
        # score是查询q与键k之间的相似度矩阵，进行缩放以防止数值过大
        
        # 生成一个下三角矩阵，用于实现自注意力中的"masking"，屏蔽未来的信息
        mask = torch.tril(torch.ones(T, T, dtype=bool))  # 生成一个下三角的布尔矩阵
        
        # 使用mask进行屏蔽，mask为0的位置会被填充为一个非常大的负值（-10000）
        score = score.masked_fill(mask == 0, -10000)  # 把mask == 0的位置置为-10000
        
        # 对score进行softmax归一化处理，得到注意力权重
        score = self.softmax(score)  # (B, n_head, T, T)

        # 将注意力权重与值（v）相乘，得到加权后的值
        score = score @ v  # (B, n_head, T, n_d)

        # 将多个头的结果合并（concatenate），并通过线性层进行映射
        # 首先将score的维度变为 (B, T, n_head * n_d)，然后通过w_o进行线性变换
        x_concate = score.transpose(1, 2).contiguous().view(B, T, self.d_model)  # (B, T, d_model)
        x_output = self.w_o(x_concate)  # (B, T, d_model)

        # 返回最终的输出
        return x_output

        
attn = multi_head_attention(d_model, n_head)
Y = attn(X,X,X)
print(Y.shape)

# layer norm
class layer_norm(nn.Module):
    def __init__(self, d_model, eps = 1e-12):
        super(layer_norm, self).__init__()
        
        self.gamma = nn.Parameter(torch.ones(d_model))
        self.beta = nn.Parameter(torch.zeros(d_model))
        self.eps = eps
        
    def forward(self, x):
        mean = x.mean(-1, keepdim = True)
        var = x.var(-1, unbiased=False, keepdim = True)
        out = (x - mean) / torch.sqrt(var + self.eps)
        out = self.gamma * out + self.beta
        return out
    
d_model = 512
X = torch.randn(2,5,512) # 2句话, 5个token，词向量512
ln = layer_norm(d_model)
print("d_model: ", d_model)
print(f"ln gamma: {ln.gamma.shape}")
print(f"ln beta: {ln.beta.shape}")
Y_ln = ln(X)
print(Y_ln.shape)