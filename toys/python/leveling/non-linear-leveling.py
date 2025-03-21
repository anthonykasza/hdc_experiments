# This was inspired by grid-based clustering. Adaptive meshes are neat too.
# In many domains, there will be regions of the discretized feature space
#  where it will be beneficial to have more/less granularity of leveling
# In comparing network packet lengths, the difference between 8 and 32 may
# be meaningful yet the difference between 1448 and 1480 is not as meaningful

import sys; sys.path.insert(0, "../")
import copy
from utils import hdv, cossim


def make_levels(steps, hv1=hdv(), hv2=hdv()):
  levels = []
  levels.append(hv1)
  step_counter = 0
  start = 0
  total_changed_elements = 0

  while step_counter < len(steps):
    levels.append( copy.deepcopy(levels[len(levels)-1]) )

    elements = int(steps[step_counter] * (len(hv1) / sum(steps)))
    total_changed_elements = total_changed_elements + elements
    print(f'copying {elements}. total changed {total_changed_elements}')

    levels[len(levels)-1][start:start+elements] = hv2[start:start+elements]
    start = start + elements;
    step_counter = step_counter + 1

  return levels



steps = [
  # small things are very similar
  16, 16, 16, 16,
  64, 64, 64,
  100, 100, 100,

  # medium things are medium far-away
  1000, 1000,
  2000,
  3000, 3000,
  4000,

  # the last 2k are approximately maximally distant
  500, 500, 500, 500
]

levels = make_levels(steps)
prev_level = levels[0]
print(len(steps) == len(levels))

for idx in range(len(levels)):
  if idx == 0:
    print(f'{idx} no_step no_prev_level same_level')
  else:
    print(f'{idx} {steps[idx-1]} {cossim(levels[idx], prev_level)} {cossim(levels[idx], levels[0])}')
  prev_level = levels[idx]
