import sys
sys.path.insert(0, '../')
from utils import hdv, cossim, substitute

def make_levels_periodic(n=10_000, all=0, cycles=5, cycle_size=10):
  levels = []

  hv = hdv(n=n)
  noise = hdv(n=n, all=all)
  major_markers = [hdv(n=n) for x in range(cycles)]
  for major_mark_hv in major_markers:
    noise_to_mark = substitute(noise, major_mark_hv, (cycle_size//2)-1)
    mark_to_noise = substitute(major_mark_hv, noise, (cycle_size//2)-1)
    levels.extend(noise_to_mark)
    levels.extend(mark_to_noise)

  return levels

print('all=0')
levels = make_levels_periodic(all=0)
for idx in range(len(levels)):
  if idx == 0:
    continue
  print(f'level{idx} to {idx-1}: {cossim(levels[idx], levels[idx-1])}')
print()

# all=1 and all=-1 behave the same
#  but all=0 is different because 0 stands for indecision
print('all=1')
levels = make_levels_periodic(all=1)
for idx in range(len(levels)):
  if idx == 0:
    continue
  print(f'level{idx} to {idx-1}: {cossim(levels[idx], levels[idx-1])}')
print()
print()
print()



print('all=0, cycle_size=20')
levels = make_levels_periodic(cycles=1, cycle_size=20, all=0)
for idx in range(len(levels)):
  if idx == 0:
    continue
  print(f'level{idx} to {idx-1}: {cossim(levels[idx], levels[idx-1])}')
print()

print('all=0, cycle_size=4')
levels = make_levels_periodic(cycles=1, cycle_size=4, all=0)
for idx in range(len(levels)):
  if idx == 0:
    continue
  print(f'level{idx} to {idx-1}: {cossim(levels[idx], levels[idx-1])}')
print()

print('all=0, cycle_size=100')
levels = make_levels_periodic(cycles=1, cycle_size=100, all=0)
for idx in range(len(levels)):
  if idx == 0:
    continue
  print(f'level{idx} to {idx-1}: {cossim(levels[idx], levels[idx-1])}')
print()

