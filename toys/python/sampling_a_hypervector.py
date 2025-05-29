# it doesn't matter which elements are compared to the original HV
# all that matters is the number of elements. this demonstrates that:
#  - all elements represent that same amount of information
#  - sampling/compression of an HVs can be done by
#    - reducing the elements of an HV
#    - introducing sparsity (zeros) into the HV



import random
import numpy as np
from utils import hdv, cossim, bundle


def pad(v, length, padding_val=0, start_padding=0):
  v = list(v)
  start_pad = [padding_val] * start_padding
  end_pad = [padding_val] * (length - len(v) - start_padding)
  return np.array(start_pad + v + end_pad)


# First I tried comparing subsequences to the full HV...
hv = hdv()
for idx in range(len(hv)):
  start_idx = random.randint(0, len(hv)-1)

  if idx + start_idx < len(hv) - 1:
    stop_idx = start_idx + idx
    partial_hv = pad(hv[start_idx:stop_idx], len(hv), padding_val=0, start_padding=start_idx)
  else:
    stop_idx = (start_idx + idx) % len(hv)
    partial_hv = bundle(hv, hdv(all=0))
    for zero_this_idx in range(stop_idx, start_idx):
      partial_hv[zero_this_idx] = 0

  # idx is the number of elements in common between the hv and partial hv
  # start_idx is where the common subsequence of elements begins
  # stop_idx is where the " " " " ends
  # cossim is the similarity between the full HV and a randomly selected subsequence of its elements
  print(f'elements in common {idx}, sim {cossim(hv, partial_hv)}')


# ... Then I tried flipping random elements from all zero towards hv, 1 element at a time
hv = hdv()

for idx in range(len(hv)):
  partial = hdv(all=0)
  j = idx
  while (j > 0):
    element = random.randint(0, len(hv)-1)
    if partial[element] == 0:
      partial[element] = hv[element]
      j -= 1
  print(f'elements in common {idx}, sim {cossim(hv, partial)}')
