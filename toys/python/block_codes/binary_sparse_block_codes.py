# High-Dimensional Computing with Sparse Vectors
# big thanks to torchhd, also

# Bundling appears to work as expected (if not better)
# Leveling appears to work as expected (if not better)
# Permutation on compressed representations is equivalent to block-level permutation on the expanded representation. This should be the same as what's already in utils.py
# TODO: binding doesn't seem to work. How to build records using this arch?


import numpy as np
import random
from collections import Counter
import copy

import sys
sys.path.insert(0, '../')
from utils import cossim



def hdv_bsbc(dimensions=10_000, number_of_blocks=1000):
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


number_of_blocks = 6
block_size = 64
dimensions = number_of_blocks * block_size
h, on_bit_indices = hdv_bsbc(dimensions, number_of_blocks)
reconstructed = decompress(on_bit_indices, dimensions, number_of_blocks)

print("the full hypervector, block segments shown")
print(h)
print()
print("just the 'on' bits of the hypervector (compressed BSBC)")
print(on_bit_indices)
print()
print("lossless decompression")
print(reconstructed)

def flatten(hv):
  '''Flatten a block-code hypervector
  '''
  return [element for block in hv for element in block]


def bundle(*args):
  '''Combine input HV into a single HV which is similar to all inputs.

     Conceptually, this is done by randomly breaking wins of element-wise addition.
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

     output:
       [3, 3, 4, 1]

  '''
  compressed_bundle = []
  for idx in range(len(args[0])):
    counts = Counter([hv[idx] for hv in args])
    max_count = max(counts.values())
    winners = [value for value, count in counts.items() if count == max_count]
    compressed_bundle.append(random.choice(winners))
  return compressed_bundle

number_of_blocks = 128
block_size = 64
dimensions = number_of_blocks * block_size
hv1, hv1_c = hdv_bsbc(dimensions, number_of_blocks)
hv2, hv2_c = hdv_bsbc(dimensions, number_of_blocks)
hv3, hv3_c = hdv_bsbc(dimensions, number_of_blocks)
hv4, hv4_c = hdv_bsbc(dimensions, number_of_blocks)
hv5, hv5_c = hdv_bsbc(dimensions, number_of_blocks)
noise, noise_c = hdv_bsbc(dimensions, number_of_blocks)
bundle_c = bundle(hv1_c, hv2_c, hv3_c, hv4_c, hv5_c)

print()
print(f'hv1_c:    {hv1_c}')
print(f'hv2_c:    {hv2_c}')
print(f'hv3_c:    {hv3_c}')
print(f'hv4_c:    {hv4_c}')
print(f'hv5_c:    {hv5_c}')
print(f'bundle_c: {bundle_c}')

# Comparing the compressed HV isn't super useful ...
print()
print(f'hv1_c to bundle_c: {cossim(hv1_c, bundle_c)}')
print(f'hv2_c to bundle_c: {cossim(hv2_c, bundle_c)}')
print(f'hv3_c to bundle_c: {cossim(hv3_c, bundle_c)}')
print(f'hv4_c to bundle_c: {cossim(hv4_c, bundle_c)}')
print(f'hv5_c to bundle_c: {cossim(hv5_c, bundle_c)}')
print(f'noise_c to bundle_c: {cossim(noise_c, bundle_c)}')
# ... but comparing their expanded/decompressed representations is, indeed
print()
bundle = decompress(bundle_c, dimensions, number_of_blocks)
print(f'hv1 to decompressed bundle: {cossim(flatten(hv1), flatten(bundle))}')
print(f'hv2 to decompressed bundle: {cossim(flatten(hv2), flatten(bundle))}')
print(f'hv3 to decompressed bundle: {cossim(flatten(hv3), flatten(bundle))}')
print(f'hv4 to decompressed bundle: {cossim(flatten(hv4), flatten(bundle))}')
print(f'hv5 to decompressed bundle: {cossim(flatten(hv5), flatten(bundle))}')
print(f'noise to decompressed bundle: {cossim(flatten(noise), flatten(bundle))}')


def bind(*args, block_size=64):
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


number_of_blocks = 128
block_size = 64
dimensions = block_size * number_of_blocks
hv1, hv1_c = hdv_bsbc(dimensions, number_of_blocks)
hv2, hv2_c = hdv_bsbc(dimensions, number_of_blocks)
hv3, hv3_c = hdv_bsbc(dimensions, number_of_blocks)
hv4, hv4_c = hdv_bsbc(dimensions, number_of_blocks)
hv5, hv5_c = hdv_bsbc(dimensions, number_of_blocks)
noise, noise_c = hdv_bsbc(dimensions, number_of_blocks)
binding_c = bind(hv1_c, hv2_c, hv3_c, hv4_c, hv5_c, block_size=block_size)

print()
print(f'hv1_c:     {hv1_c}')
print(f'hv2_c:     {hv2_c}')
print(f'hv3_c:     {hv3_c}')
print(f'hv4_c:     {hv4_c}')
print(f'hv5_c:     {hv5_c}')
print(f'binding_c: {binding_c}')

binding = decompress(binding_c, dimensions, number_of_blocks)

print()
print(f'these are supposed to all be small!')
print(f'hv1 to decompressed binding: {cossim(flatten(hv1), flatten(binding))}')
print(f'hv2 to decompressed binding: {cossim(flatten(hv2), flatten(binding))}')
print(f'hv3 to decompressed binding: {cossim(flatten(hv3), flatten(binding))}')
print(f'hv4 to decompressed binding: {cossim(flatten(hv4), flatten(binding))}')
print(f'hv5 to decompressed binding: {cossim(flatten(hv5), flatten(binding))}')
print(f'noise to decompressed binding: {cossim(flatten(noise), flatten(binding))}')

def inverse(hv, block_size=64):
  '''Return the inverse of a compressed HV
  '''
  return [block_size - element for element in hv]


# Invert hv1_c, bind it with binding_c, expand the result, and compare with hv1
print()
print(f'hv1_c:             {hv1_c}')
print(f'hv1_c inverse:     {inverse(hv1_c, block_size=block_size)}')
hv1_c_inverse = inverse(hv1_c, block_size=block_size)
query_c = bind(binding_c, hv1_c_inverse)
query_d = decompress(query_c, dimensions, number_of_blocks)
print()
print(f'query to hv1: {cossim(flatten(hv1), flatten(query_d))}')
print(f'query to hv2: {cossim(flatten(hv2), flatten(query_d))}')
print(f'query to hv3: {cossim(flatten(hv3), flatten(query_d))}')
print(f'query to hv4: {cossim(flatten(hv4), flatten(query_d))}')
print(f'query to hv5: {cossim(flatten(hv5), flatten(query_d))}')
print(f'query to noise: {cossim(flatten(noise), flatten(query_d))}')




def make_levels(hv1_c, hv2_c, block_size=64):
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


print()
print('====leveling')

number_of_blocks = 10
block_size = 64
dimensions = number_of_blocks * block_size
hv1, hv1_c = hdv_bsbc(dimensions, number_of_blocks)
hv2, hv2_c = hdv_bsbc(dimensions, number_of_blocks)
levels_c = make_levels(hv1_c, hv2_c, block_size=block_size)
print()
print(f'hv1_c:  {hv1_c}')
print(f'hv2_c:  {hv2_c}')
print()

for idx in range(len(levels_c)):
  level_c = levels_c[idx]
  level_d = decompress(level_c, dimensions, number_of_blocks)
  if idx == 0:
    print(idx, level_c)
    continue
  level_prev_c = levels_c[idx-1]
  level_prev_d = decompress(level_prev_c, dimensions, number_of_blocks)
  print(idx, level_c, cossim(flatten(level_d), flatten(level_prev_d)))


level_first_c = levels_c[0]
level_mid_c = levels_c[len(levels_c)//2]
level_last_c = levels_c[-1]
level_first_d = decompress(level_first_c, dimensions, number_of_blocks)
level_mid_d = decompress(level_mid_c, dimensions, number_of_blocks)
level_last_d = decompress(level_last_c, dimensions, number_of_blocks)
flat_l_f_d = flatten(level_first_d)
flat_l_m_d = flatten(level_mid_d)
flat_l_l_d = flatten(level_last_d)
print(f'level0 to last level{len(levels_c)} sim: {cossim(flat_l_f_d, flat_l_l_d)}')
print(f'level0 to middle level{len(levels_c)//2} sim: {cossim(flat_l_f_d, flat_l_m_d)}')
print(f'middle level{len(levels_c)//2} to last level{len(levels_c)} sim: {cossim(flat_l_f_d, flat_l_m_d)}')
