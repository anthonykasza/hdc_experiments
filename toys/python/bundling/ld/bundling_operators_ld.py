# Various methods of bundling on hypervectors generated using ld sobol sequences
# Compare output of bundling_operators.py to bundling_operators_ld.py

import numpy as np
import sys
sys.path.insert(0, "../../")
from utils import bundle, cossim
from utils import hdv_ld as hdv


def partial_bundle(*args):
  '''element-wise addition of vectors, sometimes'''
  accumulator = hdv(all=0)
  for idx in range(len(args[0])):
    for hv in args:
      # TODO expose the rate as a parameter to this function
      # accumulate across this index with a 50% chance
      if np.random.choice([True, False], size=1):
        accumulator[idx] += hv[idx]
  # clip to sign
  return np.sign(accumulator)

noise = hdv()
signal1 = hdv()
signal2 = hdv()
signal3 = hdv()
signal4 = hdv()
signal5 = hdv()

# All signals are equally similar to the accumulator
print('Regular bundling')
accumulator = hdv(all=0)
accumulator = bundle(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
print()

# The strongest signal is most similar to the accumulator
print('Weighted bundling')
accumulator = hdv(all=0)
accumulator = bundle(signal1, signal1, signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
print()


# The most recent signal is the most similar to the accumulator
#  This is caused by the clipping strategy
print('Iterative bundling')
accumulator = hdv(all=0)
accumulator = bundle(accumulator, signal1)
accumulator = bundle(accumulator, signal2)
accumulator = bundle(accumulator, signal3)
accumulator = bundle(accumulator, signal4)
accumulator = bundle(accumulator, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
print()


# Similar to Regular bundling but not as good.
#  If hardware implementing Regular bundling faulted
#  indeterministically, the resulting bundle could
#  still be used.
print('partial bundling')
accumulator = hdv(all=0)
accumulator = partial_bundle(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
print()
