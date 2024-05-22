"""
MULTI-HEADED ATTENTION
Attention mechanism are more context aware that sequence to sequence model languages
Every word has 3 vectors. 
A quary vector (q): indicates a type of search
Key vector (k): what can i offer?
Value vector (v): what i offer
To create an attention matrix, every word needs to look at another word to see its affinity level

"""
import numpy as np
import math

def softmax(x):
  return (np.exp(x).T / np.sum(np.exp(x), axis=-1)).T

def scaled_dot_product_attention(q, k, v, mask=None):
  d_k = q.shape[-1]
  scaled = np.matmul(q, k.T) / math.sqrt(d_k)
  if mask is not None:
    scaled = scaled + mask
  attention = softmax(scaled)
  out = np.matmul(attention, v)
  return out, attention