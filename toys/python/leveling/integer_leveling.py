# After reading about Modular Composite Representations,
# it's clear that using a bounded range in hdv() is totally
# useful and what other smarter people do too. However, MCR
# requires different bundle, bind, clip implementations as what's currently
# in utils.py
# And, it needs to use manhatten distance instead of cossim or hamdis.
#
# Sampling uniformly from the range is good too so long as the range
# size is even and goes from zero to some number. The paper uses 16 as an
# example. This seems to go against the fact that bipolar HVs are great.
# Although, bipolar HV are the same as binary HVs... so, do we really need
# even-sized ranges? The paper uses quite a bit of math formulas but does
# mention, in written language, the importance of symmetry in the choice
# of range.
#
# The paper calls out specifically that
# majority vote will make a poor bundling operation in MCR VSA.
# Perhaps thingy/ should switch to bipolar or mcr?


import copy
import random
import numpy as np
from numpy.linalg import norm

def hdv(n=10_000, all=None):
  '''Make an integer hypervector'''
  if all is not None:
    return np.full((1, n), all).flatten()

  # bounded range, nincs nulla
  bound = 100
  r = [x for x in range(-1*bound, bound+1) if x != 0]
  return np.random.choice(r, size=n)


def cossim(hdv1, hdv2):
  '''measure the similarity of 2 hypervector'''
  if norm(hdv1) == 0 or norm(hdv2) == 0:
    return 0
  return abs(np.dot(hdv1, hdv2) / (norm(hdv1) * norm(hdv2)))



# Compare the different make_levels functions in this script to those
# in utils.py. In a bipolar architecture, make_levels has only 1
# choice. It must: copy elements from hv2 into new levels.
#
# In an integer-element architecture, make_levels has many choices.
#  It could:
#  1. also copy elements from hv2 into new levels
#  2. increment/decrement new levels' elements towards hv2's elements
#  3. average new levels' elements towards hv2's elements
#  4. do some combination of the above
#
# Intuitively,
#  - Direct copying of elements produces the "steepest" leveling. The levels become simiar to hv2 the quickest.
#  - Averaging is the second steepest leveling.
#  - Incrementing/decrementing is the slowest leveling if i=1.



def make_levels_copy(steps, hv1=hdv(), hv2=hdv()):
  levels = []
  levels.append(hv1)
  step_counter = 0
  start = 0

  while step_counter < len(steps):
    levels.append( copy.deepcopy(levels[len(levels)-1]) )
    elements = int(steps[step_counter] * (len(hv1) / sum(steps)))

    # copy the elements from hv2 into the level
    levels[len(levels)-1][start:start+elements] = hv2[start:start+elements]

    start = start + elements;
    step_counter = step_counter + 1

  return levels


def make_levels_incdec(steps, hv1=hdv(), hv2=hdv(), i=1):
  levels = []
  levels.append(hv1)
  step_counter = 0
  start = 0

  while step_counter < len(steps):
    levels.append( copy.deepcopy(levels[len(levels)-1]) )
    elements = int(steps[step_counter] * (len(hv1) / sum(steps)))

    # increment/decrement the elements towards hv2
    for element_idx in range(len(hv2[start:start+elements])):
      if hv2[start+element_idx] > hv1[start+element_idx]:
        levels[len(levels)-1][start+element_idx] = levels[len(levels)-1][start+element_idx] + i
      elif hv2[start+element_idx] < hv1[start+element_idx]:
        levels[len(levels)-1][start+element_idx] = levels[len(levels)-1][start+element_idx] - i

    start = start + elements;
    step_counter = step_counter + 1

  return levels


def make_levels_ave(steps, hv1=hdv(), hv2=hdv()):
  levels = []
  levels.append(hv1)
  step_counter = 0
  start = 0

  while step_counter < len(steps):
    levels.append( copy.deepcopy(levels[len(levels)-1]) )
    elements = int(steps[step_counter] * (len(hv1) / sum(steps)))

    # average the elements towards hv2
    for element_idx in range(len(hv2[start:start+elements])):
      levels[len(levels)-1][start+element_idx] = int( (levels[len(levels)-1][start+element_idx] + hv2[start+element_idx]) / 2 )

    start = start + elements;
    step_counter = step_counter + 1

  return levels




hv1 = hdv(10, all=0)
hv1 = hdv(10)
hv2 = hdv(10)
steps = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
print("hv1", hv1)
print("hv2", hv2)
print()

levels_copy = make_levels_copy(steps, hv1, hv2)
print("copies")
for idx in range(len(levels_copy)):
  if idx == 0:
    print(levels_copy[idx])
  else:
    print(levels_copy[idx], cossim(levels_copy[idx], levels_copy[idx-1]))
print(cossim(levels_copy[len(levels_copy)-1], hv2))
print()


levels_ave = make_levels_ave(steps, hv1, hv2)
print("ave")
for idx in range(len(levels_ave)):
  if idx == 0:
    print(levels_ave[idx])
  else:
    print(levels_ave[idx], cossim(levels_ave[idx], levels_ave[idx-1]))
print(cossim(levels_ave[len(levels_ave)-1], hv2))
print()

levels_incdec = make_levels_incdec(steps, hv1, hv2)
print("incdec")
for idx in range(len(levels_incdec)):
  if idx == 0:
    print(levels_incdec[idx])
  else:
    print(levels_incdec[idx], cossim(levels_incdec[idx], levels_incdec[idx-1]))
print(cossim(levels_incdec[len(levels_incdec)-1], hv2))
print()



print()
print("what happens if we over-increment on purpose?")
levels_incdec = make_levels_incdec(steps, hv1, hv2, 1000) # 1000 > bound
print("incdec")
for idx in range(len(levels_incdec)):
  if idx == 0:
    print(levels_incdec[idx])
  else:
    print(levels_incdec[idx], cossim(levels_incdec[idx], levels_incdec[idx-1]))
print(cossim(levels_incdec[len(levels_incdec)-1], hv2))


