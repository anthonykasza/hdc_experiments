import numpy as np

import sys
sys.path.insert(0, "../")
from utils import hdv, bundle, cossim


def partial_bundle(*args):
  '''element-wise addition of vectors, sometimes'''
  accumulator = hdv(all=0)
  for idx in range(len(args[0])):
    for hv in args:
      # addition fails 50% of the time
      if np.random.choice([True, False], size=1):
        accumulator[idx] += hv[idx]
  return np.sign(accumulator)


codebook = [hdv() for x in range(100)]
noise = hdv()

# Compare full and correct bundle with partial bundling
for i in range(len(codebook)):
  if i == 0:
    continue
  constituents = codebook[0:i]
  accumulator_b = bundle(*constituents)
  accumulator_pb = partial_bundle(*constituents)
  print(i)
  print(f'item0 _b\t{cossim(codebook[0], accumulator_b)}')
  print(f'noise _b\t{cossim(noise, accumulator_b)}')
  print(f'item0 _pb\t{cossim(codebook[0], accumulator_pb)}')
  print(f'noise _pb\t{cossim(noise, accumulator_pb)}')
  print()
