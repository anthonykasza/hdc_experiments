# Various methods of bundling

import numpy as np
import sys
sys.path.insert(0, "../")
from utils import hdv, bundle, cossim


def partial_bundle_random50(*args):
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


def partial_bundle_random75(*args):
  '''element-wise addition of vectors, sometimes'''
  accumulator = hdv(all=0)
  for idx in range(len(args[0])):
    for hv in args:
      if np.random.choice([True, True, True, False], size=1):
        accumulator[idx] += hv[idx]
  # clip to sign
  return np.sign(accumulator)

def partial_bundle_random25(*args):
  '''element-wise addition of vectors, sometimes'''
  accumulator = hdv(all=0)
  for idx in range(len(args[0])):
    for hv in args:
      if np.random.choice([False, False, False, True], size=1):
        accumulator[idx] += hv[idx]
  # clip to sign
  return np.sign(accumulator)


def randsel_bundle(*args):
  '''randomly select one element from the hvs'''
  accumulator = hdv(all=0)
  for element_idx in range(len(args[0])):
    randsel_hv_idx = np.random.choice(len(args), size=1)[0]
    accumulator[element_idx] = args[randsel_hv_idx][element_idx]
  return np.sign(accumulator)


def partial_randsel_bundle50(*args):
  '''randomly select one element from the hvs, sometimes'''
  accumulator = hdv(all=0)
  for element_idx in range(len(args[0])):
    # Any bundling operation can be made "partial" or "sometimes"
    #  by flipping a coin to see if the operation happens
    #  or if the default element value of 0 is used
    if np.random.choice([True, False], size=1):
      randsel_hv_idx = np.random.choice(len(args), size=1)[0]
      accumulator[element_idx] = args[randsel_hv_idx][element_idx]
  return np.sign(accumulator)


def bundle_normal_dist(*args):
  '''create a normal distribution around each element
     sample from the distribution. add that sample to the
     accumulator. inspired by how HLB creates new hypervectors.
  '''
  accumulator = hdv(all=0)
  D = len(accumulator)
  for idx in range(len(args[0])):
    for hv in args:
      # create a normal around the hv's element's value, sample it once
      accumulator[idx] += np.random.normal(hv[idx], 1/np.sqrt(D), 1)[0]
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
print('partial bundling - random 25%')
accumulator = hdv(all=0)
accumulator = partial_bundle_random25(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
zeds = accumulator[np.where(accumulator == 0)]
print(f'count of 0s in bundle: {len(zeds)}/{len(accumulator)}')
print()

print('partial bundling - random 50%')
accumulator = hdv(all=0)
accumulator = partial_bundle_random50(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
zeds = accumulator[np.where(accumulator == 0)]
print(f'count of 0s in bundle: {len(zeds)}/{len(accumulator)}')
print()

print('partial bundling - random 75%')
accumulator = hdv(all=0)
accumulator = partial_bundle_random75(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
zeds = accumulator[np.where(accumulator == 0)]
print(f'count of 0s in bundle: {len(zeds)}/{len(accumulator)}')
print()


# Random selection bundling
print('random selection bundling - 100%')
accumulator = hdv(all=0)
accumulator = randsel_bundle(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
zeds = accumulator[np.where(accumulator == 0)]
print(f'count of 0s in bundle: {len(zeds)}/{len(accumulator)}')
print()

# Random selection bundling partially
print('random selection bundling - 50%')
accumulator = hdv(all=0)
accumulator = partial_randsel_bundle50(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
zeds = accumulator[np.where(accumulator == 0)]
print(f'count of 0s in bundle: {len(zeds)}/{len(accumulator)}')
print()


# Bundle with noisy elements fades similarly to iterative bundling
print('Bundle noisy elements (a distribution around the element)')
accumulator = hdv(all=0)
accumulator = bundle_normal_dist(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
zeds = accumulator[np.where(accumulator == 0)]
print(f'count of 0s in bundle: {len(zeds)}/{len(accumulator)}')
print()


# i'm not convinced that using ld seq to generate
# hv is useful.
# generating the hv using random uniform sampling
# to make fully dense basis hv. instead of sparsity
# in the basis hv, make the bundle operation introduce
# sparsity by binarizing an ld sequence

from scipy.stats.qmc import Sobol
def bundle_ld_sobol(*args):
  '''element-wise addition of vectors, ld'''
  accumulator = hdv(all=0)
  # thresh = 0.5
  thresh = 3/16
  sobol = Sobol(d=1, scramble=True)
  seq = sobol.random(n=2**14)
  for idx in range(len(args[0])):
    for hv in args:
      if seq[idx] < thresh:
        accumulator[idx] += hv[idx]
  # clip to sign
  return np.sign(accumulator)

print('bundling ld - sobol')
accumulator = hdv(all=0)
accumulator = bundle_ld_sobol(signal1, signal2, signal3, signal4, signal5)
print(f'signal1: {cossim(signal1, accumulator)}')
print(f'signal2: {cossim(signal2, accumulator)}')
print(f'signal3: {cossim(signal3, accumulator)}')
print(f'signal4: {cossim(signal4, accumulator)}')
print(f'signal5: {cossim(signal5, accumulator)}')
print(f'noise: {cossim(noise, accumulator)}')
zeds = accumulator[np.where(accumulator == 0)]
print(f'count of 0s in bundle: {len(zeds)}/{len(accumulator)}')
print()
