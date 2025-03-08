# HDC can be used for efficiently searching file directory trees,
#  process trees, API call sequences and more


import random
from utils import bundle, bind, cossim, hdv, permute
from symbols import function_symbols, function_names
from collections import deque


def new_ngram(hvs):
  ngram = hdv(100000, all=1)
  for idx in range(len(hvs)):
    ngram = bind(ngram, permute(hvs[idx], [0,idx]))
  return ngram


def make_sequence(iterations, n, store=False):
  global store_a_ngram_name
  global store_a_ngram_hv

  gram_deque = deque([])
  name_deque = deque([])
  process_call_sequence = []
  process_call_sequence_ngram_bundle = hdv(all=0)
  ngrams = []

  for i in range(iterations):

    func_idx = random.choice(range(len(function_symbols)))
    f_name = function_names[func_idx]
    f_hv = function_symbols[func_idx]
    gram_deque.appendleft(f_hv)
    name_deque.appendleft(f_name)

    if len(gram_deque) >= n:
      ngram = new_ngram(gram_deque)
      ngrams.append(ngram)
      if store:
        store_a_ngram_hv = ngram
        store_a_ngram_name = '/'.join(name_deque)
      gram_deque.pop()
      name_deque.pop()

    process_call_sequence.append(f_name)
    process_call_sequence_ngram_bundle = bundle(*ngrams)

  return process_call_sequence, process_call_sequence_ngram_bundle


store_a_ngram_hv = ''
store_a_ngram_name = ''
n = 4
i = 100 # consider the capacity of your bundle!
learned_pcs, learned_pcsnb = make_sequence(i, n, store=True)
sample_pcs, sample_pcsnb = make_sequence(n, n)

print()
print(f'is the randomly selected subseq {"/".join(sample_pcs)} in the call seq?')
print(f'{cossim(sample_pcsnb, learned_pcsnb)}')
print()
print(f'is the last added subseq {store_a_ngram_name} in the call sequence?')
print(f'{cossim(store_a_ngram_hv, learned_pcsnb)}')
