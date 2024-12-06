# use exponential leveling to create "primary markers",
#  then use linear leveling to discretize between "primary markers"


import random
import copy
from utils import new_hv, bind, cossim

def make_levels_linear(bins, hv1, hv2):
  bins_list = []
  bins_list.append(hv1)
  altered_indices = set([])
  flips_per_iteration = len(hv1) // bins

  for i in range(1, bins):
    next_level = copy.deepcopy(bins_list[i-1])
    indexes_to_chose_from = set(range(len(next_level))).difference(altered_indices)
    for j in random.sample(sorted(indexes_to_chose_from), flips_per_iteration):
      altered_indices.add(j)
      next_level[j] = hv2[j]
    bins_list.append(next_level)
  bins_list.append(hv2)
  return bins_list


# approximately a sinc function
def make_levels_exponential(basis_hv, exp):
  if exp == 1:
    return list(basis_hv)

  levels = [basis_hv]
  while exp > 1:
    exp -= 1
    previous_level = levels[len(levels)-1]
    levels.append(bind(previous_level, basis_hv))
  return levels


basis = new_hv(1000)
primary_markers = make_levels_exponential(basis, 5)
for idx in range(len(primary_markers)):
  print(f'{idx+1}\t{cossim(basis, primary_markers[idx])}')
  if idx == 0:
    continue
  this = primary_markers[idx]
  prev = primary_markers[idx-1]
  sublevels = make_levels_linear(10, prev, this)
  for sub_idx in range(len(sublevels)):
    print(f'  {idx+1}.{sub_idx}\t{cossim(prev, sublevels[sub_idx])}')

