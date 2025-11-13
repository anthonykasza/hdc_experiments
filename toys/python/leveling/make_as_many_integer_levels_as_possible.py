

import copy
import numpy as np
from numpy.linalg import norm

def hdv(n=10_000, all=None, bound=100):
  '''generate a new integer hypervector'''
  if all is not None:
    return np.full((1, n), all).flatten()
  r = [x for x in range(-1*bound, bound+1) if x != 0]
  return np.random.choice(r, size=n)


def cossim(hdv1, hdv2):
  '''measure the similarity of 2 hypervector'''
  if norm(hdv1) == 0 or norm(hdv2) == 0:
    return 0
  return abs(np.dot(hdv1, hdv2) / (norm(hdv1) * norm(hdv2)))


def make_levels_incdec(hv1=hdv(), hv2=hdv(), i=1):
  '''return as many levels as possible'''
  levels = []
  levels.append(hv1)
  indices_to_alter = list(np.where(hv1 != hv2)[0])
  j = 0

  while not np.array_equal(levels[-1], hv2):
    # indices are inc/dec by round robin
    idx = indices_to_alter[j % len(indices_to_alter)]
    next_level = copy.deepcopy(levels[-1])

    # we need to increment
    if hv2[idx] > next_level[idx]:
      if hv2[idx] > next_level[idx] + i:
        next_level[idx] += i
      else:
        next_level[idx] = hv2[idx]
        indices_to_alter.remove(idx)
    # we need to decrement
    elif hv2[idx] < next_level[idx]:
      if hv2[idx] < next_level[idx] - i:
        next_level[idx] -= i
      else:
        next_level[idx] = hv2[idx]
        indices_to_alter.remove(idx)

    j += 1
    levels.append(next_level)
  return levels


# when ELEMENT_RANGE is 1 the arch is binary/ternary

'''
# these leveling parameters don't work very nicely
#  showing that more dims is better than a larger element range
DIMENSIONS = 1000
ELEMENT_RANGE = 10
INCDEC_STEP = 1
'''

'''
# these leveling parameters are more superior for crisp leveling
#  but can only support a level count of their dims
DIMENSIONS = 10000
ELEMENT_RANGE = 1
INCDEC_STEP = 1

DIMENSIONS = 20000
ELEMENT_RANGE = 1
INCDEC_STEP = 1
'''

'''
# these leveling parameters are good for generating a reliable progression
#  but can only support a level count of FEWER than their dims.
# this only happens when INCDEC_STEP is greater than ELEMENT_RANGE.
#  its because none of the level hv contain zed. none are sparse.
DIMENSIONS = 10000
ELEMENT_RANGE = 1
INCDEC_STEP = 2

DIMENSIONS = 20000
ELEMENT_RANGE = 1
INCDEC_STEP = 2
'''


# these leveling parameters don't have as reliable of a progression
#  in their levels but allow for many more levels than its dimensions
DIMENSIONS = 10000
ELEMENT_RANGE = 2
INCDEC_STEP = 1

DIMENSIONS = 10000
ELEMENT_RANGE = 3
INCDEC_STEP = 1

DIMENSIONS = 10000
ELEMENT_RANGE = 4
INCDEC_STEP = 1



hv1 = hdv(n=DIMENSIONS, bound=ELEMENT_RANGE)
hv2 = hdv(n=DIMENSIONS, bound=ELEMENT_RANGE)
print(f'hv1: {hv1}')
print(f'hv2: {hv2}')

levels = make_levels_incdec(hv1, hv2, INCDEC_STEP)
for idx in range(len(levels)):
  level = levels[idx]
  sim_hv1 = cossim(hv1, level)
  sim_hv2 = cossim(hv2, level)
  print(idx, level[:5], level[-5:], round(sim_hv1,8), round(sim_hv2,8))

  # TODO: investigate why these levels reverse direction
  if idx < len(levels)-1 and cossim(hv1, levels[idx+1]) > sim_hv1:
    print('  levels are becoming more similar to hv1 instead of less similar')
  if idx < len(levels)-1 and cossim(hv2, levels[idx+1]) < sim_hv2:
    print('  levels are becoming less similar to hv2 instead of more similar')

print(cossim(hv1, hv2))
