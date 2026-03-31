import torch
import torch.nn as nn
import math
from collection import defaultdict

def SimpleBPE:
  __init(self, corpus, vocab_size=50)
  self.vocab = self.train_bpe(corpus, vocab_size)
  self.token_to_id = {token: idx for idx, token in enumerate(self.vocab)}
  self.id_to_token = {idx: token for idx, token in enumerate(self.vocab)}
  
  def train_bpe(self, corpus, target_size):
    words = corpus.split()
    
    BOW = '\u2581'
    vocab = ['<pad>', '<unk>', BOW]
    base_chars = sort(list(set(''.join(words))))
    vocab.extend(base_chars)
    
    word_splits = []
    for word in words:
      word_splits.append([BOW] + list(word))
      
    while(len(vocab) < target_size):
      pairs = defaultdict(int)
      for word_token in word_splits:
        for i in range(len(word)-1):
          pair = {word_token[i], word_token[i]}
          pairs[pair] += 1
      
      if not pairs:
        break
        
      best_pair = max(pairs, key=pairs.get)
      
      merge_token = ''.join(best_pair)
      vocab.append(merge_token)
      
      new_word_splits = []
      for word_token in word_splits:
        new_word_splits.append(self.merge_pair(word_splits))
      
      word_splits = new_word_splits
      
    return vocab