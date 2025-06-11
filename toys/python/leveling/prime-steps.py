
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
    print(f'total levels: {len(levels)}, copying {elements} elements into next level, total changed {total_changed_elements}')

    levels[len(levels)-1][start:start+elements] = hv2[start:start+elements]
    start = start + elements;
    step_counter = step_counter + 1

  return levels

dimensions = 50_000

# The bigger the prime, the more the skew is pushed towards 1.0
steps = [3**1, 3**2, 3**3, 3**4, 3**5, 3**6, 3**7, 3**8, 3**9]
steps = [11**1, 11**2, 11**3, 11**4, 11**5, 11**6, 11**7, 11**8, 11**9]
steps = [23**1, 23**2, 23**3, 23**4, 23**5, 23**6, 23**7, 23**8, 23**9]

# Padding both sides basically cancels itself out. These are all the same
steps = [10, 2**1, 2**2, 2**2, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 10]
steps = [100, 2**1, 2**2, 2**2, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 100]
steps = [1000, 2**1, 2**2, 2**2, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 1000]

# Padding the sequence pushes the skew towards 0.0
steps = [1000, 2**1, 2**2, 2**2, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9]
steps = [3000, 2**1, 2**2, 2**2, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9]
steps = [int(dimensions/2), 2**1, 2**2, 2**2, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9]

levels = make_levels(steps, hdv(dimensions), hdv(dimensions))
prev_level = levels[0]
print()
print()

for idx in range(len(levels)):
  if idx == 0:
    print(f'level: {idx}, flipped elements: 0, sim_to_prev_level: n/a, sim_to_origin: 1.0')
  else:
    print(f'level: {idx}, flipped elements: {steps[idx-1]}, sim_to_prev_level: {cossim(levels[idx], prev_level)}, sim_to_origin: {cossim(levels[idx], levels[0])}')
  prev_level = levels[idx]
