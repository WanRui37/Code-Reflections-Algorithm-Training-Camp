
# ====================== 安装依赖包 ======================

# 基础深度学习框架
get_ipython().system('pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu')

# 如果有GPU，使用以下命令替代上面的（根据你的CUDA版本选择）
# CUDA 11.8
# !pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# CUDA 12.1
# !pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 数据处理和科学计算
get_ipython().system('pip install numpy')
get_ipython().system('pip install pandas')
get_ipython().system('pip install matplotlib')


import torch
import torch.nn as nn
import math
from collections import defaultdict

# ====================== 1. BPE分词器实现 ======================
class SimpleBPE:
    def __init__(self, corpus, vocab_size=50):
        self.vocab = self.train_bpe(corpus, vocab_size)
        self.token_to_id = {token: idx for idx, token in enumerate(self.vocab)}
        self.id_to_token = {idx: token for idx, token in enumerate(self.vocab)}

    def train_bpe(self, corpus, target_size):
        """简化版BPE训练"""
        words = corpus.split()
        
        # 初始化词汇表，添加特殊标记
        BOW = '\u2581'
        vocab = ['<pad>', '<unk>', BOW]  # 添加必要的特殊标记
        base_chars = sorted(list(set(''.join(words))))
        vocab.extend(base_chars)

        # 初始化词表示
        word_splits = []
        for word in words:
            word_splits.append([BOW] + list(word))

        while len(vocab) < target_size:
            # 统计所有相邻token对的频率
            pairs = defaultdict(int)
            for word_tokens in word_splits:
                for i in range(len(word_tokens) - 1):
                    pair = (word_tokens[i], word_tokens[i+1])
                    pairs[pair] += 1

            if not pairs:
                break

            # 找出频率最高的token对
            best_pair = max(pairs, key=pairs.get)

            # 合并最高频对
            merged_token = ''.join(best_pair)
            vocab.append(merged_token)

            # 更新所有词的token表示
            new_word_splits = []
            for word_tokens in word_splits:
                new_word_splits.append(self.merge_pair(word_tokens, best_pair))
            word_splits = new_word_splits

        return vocab

    def merge_pair(self, tokens, pair):
        """合并token序列中的指定token对"""
        merged = []
        i = 0
        while i < len(tokens):
            # 检查是否匹配要合并的pair
            if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i+1] == pair[1]:
                merged.append(''.join(pair))
                i += 2
            else:
                merged.append(tokens[i])
                i += 1
        return merged

    def encode(self, text):
        """将文本编码为token ID序列"""
        if not text:
            return []

        # 初始化tokens
        tokens = [BOW] + list(text)

        # 迭代合并，直到无法合并为止
        changed = True
        while changed:
            changed = False
            i = 0
            new_tokens = []

            while i < len(tokens):
                # 尝试找到最长的匹配
                found = False
                for length in range(min(len(tokens) - i, 10), 0, -1):  # 限制最大长度
                    candidate = ''.join(tokens[i:i+length])
                    if candidate in self.token_to_id:
                        new_tokens.append(candidate)
                        i += length
                        found = True
                        if length > 1:
                            changed = True
                        break

                if not found:
                    # 如果没有找到匹配，使用<unk>
                    new_tokens.append('<unk>')
                    i += 1

            tokens = new_tokens

        # 转换为ID
        return [self.token_to_id.get(t, self.token_to_id['<unk>']) for t in tokens]


# ====================== 测试代码 ======================
if __name__ == "__main__":
    # 测试语料
    corpus = "hello world hello there world of code code hello"

    # 训练BPE
    bpe = SimpleBPE(corpus, vocab_size=50)

    print("词汇表大小:", len(bpe.vocab))
    print("词汇表:", bpe.vocab[:20])  # 显示前20个token

    # 测试编码
    test_text = "hello world"
    encoded = bpe.encode(test_text)
    print(f"\n原文: {test_text}")
    print(f"编码: {encoded}")
    print(f"编码tokens: {[bpe.id_to_token[id_] for id_ in encoded]}")



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


# In[22]:


# ====================== 3. 运行示例 ======================
if __name__ == "__main__":
    # 初始化BPE分词器
    corpus = "我 爱 学习 大 语言 模型"  # 训练数据
    bpe = SimpleBPE(corpus, vocab_size=20)

    # 编码输入文本
    input_text = "我爱学习大语言模型"
    input_ids = torch.tensor([bpe.encode(input_text)])

    print("=== BPE分词结果 ===")
    print("Tokenized IDs:", input_ids.tolist()[0])
    print("对应Tokens:", [bpe.id_to_token[i] for i in input_ids[0].tolist()])

    # 模型参数
    vocab_size = len(bpe.vocab)
    d_model = 64
    num_heads = 4
    num_layers = 2
    d_ff = 128

    # 初始化模型
    model = Transformer(vocab_size, d_model, num_heads, num_layers, d_ff)

    # 前向传播
    logits = model(input_ids)

    # 最终输出
    probs = torch.softmax(logits, dim=-1)
    print("\n=== 最终概率输出 ===")
    print("概率形状:", probs.shape)
    print("最后一个token的top3概率:", torch.topk(probs[0, -1], 3).values.tolist())

