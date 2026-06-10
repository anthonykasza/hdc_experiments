
import numpy as np

from utils import new_hv, compare_hv
from utils import make_levels_hamming, make_levels_manhattan


dimensions = 5
a = new_hv(dimensions)
b = np.array([0,0,1,0,0]).astype(np.int8)
c = np.array([1,1,1,1,1]).astype(np.int8)
d = np.array([-1,-1,-1,-1,-1]).astype(np.int8)

print("A: ", a)
print("B: ", b)
print("C: ", c)
print("D: ", d)
print()

print("A compared to B: ", compare_hv(a, b))
print()

print("Leveling with replacement (hamming)")
levels = make_levels_hamming(6, d, c)
for idx,hv in levels.items():
  print(idx, hv, compare_hv(hv, d))
print()

print("Leveling with increment (manhattan)")
levels = make_levels_manhattan(11, d, c)
for idx,hv in levels.items():
  print(idx, hv, compare_hv(hv, d))
print()

print("Leveling with increment with larger element range")
levels = make_levels_manhattan(
  21,
  np.array([-2,-2,-2,-2,-2]),
  np.array([2,2,2,2,2])
)
for idx,hv in levels.items():
  print(idx, hv, compare_hv(hv, d))
print()

# If we want to ensure a smooth progression of levels
#  with uniq cossine sim, the max number of levels is
#  ((element_range * hv_dimensions) / step_size) + 1
#  step_size may be fractional but that implies elements
#   are floats

# TODO: use landmark hv to construct a varying granularity levels
# TODO: create non-monotonic cosine similarity progressions
# TODO: mix hamming and manhattan leveling?
