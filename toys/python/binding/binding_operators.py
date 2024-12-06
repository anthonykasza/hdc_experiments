# Various methods of binding.

import numpy as np
import sys
sys.path.insert(0, "../")
from utils import hdv, bind, cossim, inverse


def sampled_bind(*args):
  '''element-wise multiplication of vectors, sometimes'''
  product = hdv(all=1)
  for idx in range(len(args[0])):
    for hv in args:
      if np.random.choice([True, False], size=1):
        product[idx] = hv[idx] * product[idx]
  return product


noise = hdv()
signal1 = hdv()
signal2 = hdv()
signal3 = hdv()
signal4 = hdv()
signal5 = hdv()

# All signals are equally recoverable from the binding
print('Regular binding')
product = hdv(all=1)
product = bind(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(bind(product, signal2, signal3, signal4, signal5), signal1)}')
print(f'signal2: {cossim(bind(product, signal1, signal3, signal4, signal5), signal2)}')
print(f'signal3: {cossim(bind(product, signal1, signal2, signal4, signal5), signal3)}')
print(f'signal4: {cossim(bind(product, signal1, signal2, signal3, signal5), signal4)}')
print(f'signal5: {cossim(bind(product, signal1, signal2, signal3, signal4), signal5)}')
print(f'noise: {cossim(product, noise)}')
print()

# Weighting doesn't make much sense when a hypervector is its own inverse
#  signal1 * signal1 = 1
# If the elements were integers, weighting each element would be useful
print('Weighted binding')
product = hdv(all=1)
product = bind(signal1, signal1, signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(bind(product, signal2, signal3, signal4, signal5), signal1)}')
print(f'signal2: {cossim(bind(product, signal1, signal3, signal4, signal5), signal2)}')
print(f'signal3: {cossim(bind(product, signal1, signal2, signal4, signal5), signal3)}')
print(f'signal4: {cossim(bind(product, signal1, signal2, signal3, signal5), signal4)}')
print(f'signal5: {cossim(bind(product, signal1, signal2, signal3, signal4), signal5)}')
print(f'noise: {cossim(product, noise)}')
print()


# Binding is commutative, so order doesn't matter (unlike bundling)
print('Iterative binding')
product = hdv(all=1)
product = bind(product, signal1)
product = bind(product, signal2)
product = bind(product, signal3)
product = bind(product, signal4)
product = bind(product, signal5)
print(f'signal1: {cossim(bind(product, signal2, signal3, signal4, signal5), signal1)}')
print(f'signal2: {cossim(bind(product, signal1, signal3, signal4, signal5), signal2)}')
print(f'signal3: {cossim(bind(product, signal1, signal2, signal4, signal5), signal3)}')
print(f'signal4: {cossim(bind(product, signal1, signal2, signal3, signal5), signal4)}')
print(f'signal5: {cossim(bind(product, signal1, signal2, signal3, signal4), signal5)}')
print(f'noise: {cossim(product, noise)}')
print()


# I'm not really sure what the implications of probabilistic binding are, but it makes recovery approximate instead of exact
#  Query results are more similar to noise but still significant
print('Sampled binding')
product = hdv(all=1)
product = sampled_bind(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(bind(product, signal2, signal3, signal4, signal5), signal1)}')
print(f'signal2: {cossim(bind(product, signal1, signal3, signal4, signal5), signal2)}')
print(f'signal3: {cossim(bind(product, signal1, signal2, signal4, signal5), signal3)}')
print(f'signal4: {cossim(bind(product, signal1, signal2, signal3, signal5), signal4)}')
print(f'signal5: {cossim(bind(product, signal1, signal2, signal3, signal4), signal5)}')
print(f'noise: {cossim(product, noise)}')
print()
