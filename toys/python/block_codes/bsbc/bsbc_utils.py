# High-Dimensional Computing with Sparse Vectors
# big thanks to torchhd, also

import random
from collections import Counter
import copy
import numpy as np

import sys
sys.path.insert(0, '../../')
from utils import cossim as wrapped_cossim


def flatten(hv):
  '''Flatten a block-code hypervector
  '''
  return [element for block in hv for element in block]


def cossim(hv1, hv2):
  '''Same cosine similarity but on flattened hv
  '''
  return wrapped_cossim(flatten(hv1), flatten(hv2))


def hdv(dimensions=10_000, number_of_blocks=1000):
  '''Return a binary sparse block-code hypervector
     and a map of it's 'on' bits
  '''
  h = []
  block_size = dimensions // number_of_blocks
  on_bit_indices = []
  for block in range(number_of_blocks):
    on_bit = random.randint(0, block_size-1)
    on_bit_indices.append(on_bit)
    # all element in the block are zero ...
    tmp = [0] * block_size
    # ... except a a randomly chosen index is set to 1
    tmp[on_bit] = 1
    h.append(tmp)
  return h, on_bit_indices


def decompress(onbits, dimensions, number_of_blocks):
  '''Given a list of the indices of the 'on' bits
     and the original dims, exoand the BSBC hypervector
  '''
  h = []
  block_size = dimensions // number_of_blocks
  for block in range(number_of_blocks):
    on_bit = onbits[block]
    tmp = [0] * block_size
    tmp[on_bit] = 1
    h.append(tmp)
  return h



def bundle(*args):
  '''Combine input HV into a single HV which is similar to all inputs.

     Conceptually, this is done by randomly breaking wins of element-wise addition.
     This ensures only a single on-bit per block and is similar to clipping in MAP. The paper calls it thinning.

     input:
       [ [0,0,1,0], [0,0,1,0], [1,0,0,0], [1,0,0,0] ]
       [ [0,0,1,0], [0,1,0,0], [0,1,0,0], [1,0,0,0] ]
       [ [0,0,1,0], [0,0,1,0], [0,0,1,0], [0,1,0,0] ]
       [ [0,0,1,0], [0,0,1,0], [0,0,0,1], [0,1,0,0] ]

     element-wise addition:
       [ [0,0,4,0], [0,1,3,0], [1,1,1,1], [2,2,0,0] ]

     possible output:
       [ [0,0,1,0], [0,0,1,0], [0,0,0,1], [1,0,0,0] ]

     In the first block, the winner is clearly the 3rd element.
     In the second block, the winner is again the 3rd element.
     In the third block, the winner is selected randomly from all elements.
     In the fourth block, the winner is selected randomly from the first and second element.

     Practically, we don't operate on the expanded version of the HV but
     just the compressed version. So, instead of element-wise addition
     we count the 'on' bit indices and randomly chose from the most
     frequent indices per block.
     input:
       [3, 3, 1, 1]
       [3, 2, 2, 1]
       [3, 3, 3, 2]
       [3, 3, 4, 2]

     possible output:
       [3, 3, 4, 1]

  '''
  compressed_bundle = []
  for idx in range(len(args[0])):
    counts = Counter([hv[idx] for hv in args])
    max_count = max(counts.values())
    winners = [value for value, count in counts.items() if count == max_count]
    # The paper also mentions using a deterministic approach instead of selecting randomly.
    compressed_bundle.append(random.choice(winners))
  return compressed_bundle


from scipy.stats import circmean
def bundle_cyclic(*args, block_size=64):
  '''
  Circular mean of elements treated as angles.
  If the circular mean is undefined (angles evenly distributed),
  randomly pick one of the elements.
  '''
  n = len(args[0])
  bundle = []

  for idx in range(n):
    elements = [hv[idx] for hv in args]

    # Convert elements to radians
    elements_rad = np.array(elements) * 2 * np.pi / block_size
    # Compute mean resultant length
    R = np.sqrt(np.mean(np.cos(elements_rad))**2 + np.mean(np.sin(elements_rad))**2)

    threshold = 1e-6
    if R < threshold:
      mean = random.choice(elements)
    else:
      mean = int(circmean(elements, high=block_size, low=0))

    bundle.append(mean)
  return bundle


def bind(*args, block_size):
  '''Combine input HV into a single HV which is unlike
     any of the inputs. Bound constituents should be
     recoverable.

     BSBC does not use multiplication like MAP. Instead, it uses
     block-level permutation which turns out to be element-wise addition
     modulus the block size on the compressed HV.

     "With maximally sparse vectors this is equivalent to modulo
      sum of the indices of the two operands as in frequency domain
      HRR"
  '''
  compressed_binding = []
  for idx in range(len(args[0])):
    s = sum([hv[idx] for hv in args])
    compressed_binding.append(s % block_size)
  return compressed_binding


def inverse(hv, block_size):
  '''Return the inverse of a compressed HV
  '''
  return [block_size - element for element in hv]


def make_levels(hv1_c, hv2_c, block_size):
  '''Make as many incremental levels as possible between two HV
  '''
  levels = []
  levels.append(hv1_c)

  for idx in range(len(hv1_c)):

    while levels[-1][idx] !=  hv2_c[idx]:
      next_level = copy.deepcopy(levels[-1])
      middle_of_the_block = block_size // 2

      if hv2_c[idx] > hv1_c[idx]:
        if hv2_c[idx] - hv1_c[idx] <= middle_of_the_block:
          next_level[idx] = (next_level[idx] + 1) % block_size
        else:
          next_level[idx] = (next_level[idx] - 1) % block_size
      else:
        if hv1_c[idx] - hv2_c[idx] <= middle_of_the_block:
          next_level[idx] = (next_level[idx] - 1) % block_size
        else:
          next_level[idx] = (next_level[idx] + 1) % block_size
      levels.append(next_level)
  return levels

def permute(hdv, positions=1):
  '''Permute the hypervector block-wise'''
  positions %= len(hdv)
  return hdv[-positions:] + hdv[:-positions]


def sim_cyclic(hv1, hv2, hv1_block_size, hv2_block_size):
  '''Compare two compressed BSBC hypervectors
     regardless of their block sizes, so long as their
     block count is equal.
  '''

  # scale one hv to another. DONT SCALE DOWN
  if hv1_block_size == hv2_block_size:
    hv1_rescaled = hv1
    hv2_rescaled = hv2
    target_block_size = hv1_block_size

  elif hv1_block_size > hv2_block_size:
    scale = hv1_block_size / hv2_block_size
    hv1_rescaled = hv1
    hv2_rescaled = [int(p * scale) for p in hv2]
    target_block_size = hv1_block_size

  else:
    scale = hv2_block_size / hv1_block_size
    hv1_rescaled = [int(p * scale) for p in hv1]
    hv2_rescaled = hv2
    target_block_size = hv2_block_size

  # Compute the cyclic similarity
  total_dist = 0
  for p1, p2 in zip(hv1_rescaled, hv2_rescaled):
    raw = abs(p1 - p2)
    total_dist += min(raw, target_block_size - raw)
  avg_dist = total_dist / len(hv1)
  similarity = max(0, 1 - avg_dist / np.pi)
  return similarity
