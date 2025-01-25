import random
import copy
from utils import cossim, hdv, bind, bundle


def make_levels(bins=1000, n=10_000):
  idx_list = []
  bins_list = []
  bins_list.append(hdv(n))
  altered_indices = set([])
  flips_per_iteration = n // bins

  for i in range(1, bins):
    next_level = copy.deepcopy(bins_list[i-1])
    indexes_to_chose_from = set(range(len(next_level))).difference(altered_indices)
    idx_list.append([])
    for j in random.sample(list(indexes_to_chose_from), flips_per_iteration):
      altered_indices.add(j)
      idx_list[i-1].append(j)
      next_level[j] = next_level[j] * -1
    bins_list.append(next_level)
  return idx_list, bins_list


# levels are HVs and indices are the flipped bits
#  between pairs of levels
indices, levels = make_levels(bins=5, n=10)

# there's 1 more level than set of indices
print("\t", levels[0])

for idx in range(1, len(levels)):
  altered_indices = indices[idx-1]
  level = levels[idx]
  prev_level = levels[idx-1]
  print(altered_indices)
  print("\t", level, cossim(level, prev_level))
