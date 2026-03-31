class Embedding(nn.Module):
    def __init__(self, vocab_size, d_model):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.d_model = d_model

    def forward(self, x):
        output = self.embedding(x) * math.sqrt(self.d_model)
        print("\n=== Embedding输出 ===")
        print(f"形状: {output.shape}")
        print("前3个token的嵌入均值:", output[0, :3].mean().item())
        return output



class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        output = x + self.pe[:, :x.size(1)]
        print("\n=== 位置编码输出 ===")
        print(f"形状: {output.shape}")
        print("位置编码后的第一个token:", output[0, 0, :3].detach().numpy())
        return output


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.Wq = nn.Linear(d_model, d_model)
        self.Wk = nn.Linear(d_model, d_model)
        self.Wv = nn.Linear(d_model, d_model)
        self.Wo = nn.Linear(d_model, d_model)

    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)

        # 分头处理
        Q = self.Wq(Q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.Wk(K).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.Wv(V).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        # 注意力计算
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        causal_mask = torch.triu(
            torch.ones(T, T, device=x.device, dtype=torch.bool),
            diagonal=1,
        )
        scores = scores.masked_fill(causal_mask.unsqueeze(0).unsqueeze(0), float("-inf"))
        
        attn_weights = torch.softmax(scores, dim=-1)
        output = torch.matmul(attn_weights, V)

        # 合并多头
        output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        output = self.Wo(output)

        print("\n=== 多头注意力输出 ===")
        print(f"形状: {output.shape}")
        print("注意力权重均值:", attn_weights.mean().item())
        return output


class FFN(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.activation = nn.ReLU()

    def forward(self, x):
        output = self.linear2(self.activation(self.linear1(x)))
        print("\n=== FFN输出 ===")
        print(f"形状: {output.shape}")
        print("FFN输出均值:", output.mean().item())
        return output


class EncoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.ffn = FFN(d_model, d_ff)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        print("\n=== 编码器层开始 ===")
        # 注意力子层
        attn_output = self.self_attn(x, x, x)
        x = self.norm1(x + self.dropout(attn_output))

        # FFN子层
        ffn_output = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_output))
        print("编码器层输出均值:", x.mean().item())
        return x


class Transformer(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff):
        super().__init__()
        self.embedding = Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model)
        self.layers = nn.ModuleList([EncoderLayer(d_model, num_heads, d_ff) for _ in range(num_layers)])
        self.linear = nn.Linear(d_model, vocab_size)

    def forward(self, x):
        print("=== 输入序列 ===")
        print("Token IDs:", x.tolist()[0])

        x = self.embedding(x)
        x = self.pos_encoding(x)

        for i, layer in enumerate(self.layers):
            print(f"\n=== 第{i+1}层编码 ===")
            x = layer(x)

        logits = self.linear(x)
        print("\n=== 线性层输出 ===")
        print("形状:", logits.shape)
        print("logits示例:", logits[0, -1, :3].detach().numpy())

        return logits