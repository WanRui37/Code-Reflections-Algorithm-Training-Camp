import torch
import torch.nn as nn
import math
from collections import defaultdict

class SimpleBPE:
    def __init__(self, corpus, vocab_size=50):
        self.vocab = self.train_bpe(corpus, vocab_size)
        self.token_to_id = {token: idx for idx, token in enumerate(self.vocab)}
        self.id_to_token = {idx: token for idx, token in enumerate(self.vocab)}

    def train_bpe(self, corpus, target_size):
        """简化版BPE训练"""
        words = corpus.split()
        
        BOW = '\u2581'
        vocab = ['<pad>', '<unk>', BOW]
        base_chars = sorted(list(set(''.join(words))))
        vocab.extend(base_chars)

        word_splits = []
        for word in words:
            word_splits.append([BOW] + list(word))

        while len(vocab) < target_size:
            pairs = defaultdict(int)
            for word_tokens in word_splits:
                for i in range(len(word_tokens) - 1):
                    pair = (word_tokens[i], word_tokens[i+1])
                    pairs[pair] += 1

            if not pairs:
                break

            best_pair = max(pairs, key=pairs.get)

            merged_token = ''.join(best_pair)
            vocab.append(merged_token)

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

        tokens = [BOW] + list(text)

        changed = True
        while changed:
            changed = False
            i = 0
            new_tokens = []

            while i < len(tokens):
                found = False
                for length in range(min(len(tokens) - i, 10), 0, -1): 
                    candidate = ''.join(tokens[i:i+length])
                    if candidate in self.token_to_id:
                        new_tokens.append(candidate)
                        i += length
                        found = True
                        if length > 1:
                            changed = True
                        break

                if not found:
                    new_tokens.append('<unk>')
                    i += 1

            tokens = new_tokens

        return [self.token_to_id.get(t, self.token_to_id['<unk>']) for t in tokens]