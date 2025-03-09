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
  # 0-16
  16,
  # 16-32
  16,
  # 32-48
  16,
  # 48-64
  16,
  # 64-128
  64,
  # 128-192
  64,
  # 192-256
  64,
  # 256-356
  100,
  # 356-456
  100,
  # 456-556
  100,
  # 556-1100
  500,
  # 1100-1600
  500,
  # 1600-2500
  1000,
  # 2500-4000
  1500,
  # 4000-6000
  2000,
  # 6000-9000
  3000,
  # 9000-12000
  3000,
  # 12000-16385
  4500
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
