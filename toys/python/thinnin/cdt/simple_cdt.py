import numpy as np
import copy

DIMS = 200
MAX_VAL = DIMS**2


def new_hv(dims=DIMS, max_val=MAX_VAL):
  """Make a new symbol"""
  return np.array(np.random.choice(max_val, size=dims, replace=False))

def bundle(hvs, dims=DIMS):
  """Union"""
  union = set()
  for hv in hvs:
    union |= set(hv)
  return np.array(list(union))

def similarity(h1, h2):
  """Intersection"""
  if len(h1) == 0 or len(h2) == 0:
    return 0.0
  return len(np.intersect1d(h1, h2)) / min(len(h1), len(h2))

def make_levels(
  level_count=10,
  elements_per_level=1,
  basis_hv=new_hv(),
  max_val=MAX_VAL,
):
  """Return a list of graded levels"""
  levels = [basis_hv]
  hv = set(map(int, basis_hv))
  new_elements = set(range(max_val)) - hv
  old_elements = hv

  for _ in range(level_count):
    if len(new_elements) < elements_per_level:
      levels.append(np.array(sorted(hv)))
      continue

    to_remove = set(rng.choice(
      tuple(old_elements),
      size=elements_per_level,
      replace=False
    ))

    to_add = set(rng.choice(
      tuple(new_elements),
      size=elements_per_level,
      replace=False
    ))

    old_elements = old_elements - to_remove
    new_elements = new_elements - to_add
    hv = (hv - to_remove) | to_add
    levels.append(np.array(sorted(hv)))

  return levels



def bind(hvs, dims=DIMS, max_val=MAX_VAL):
  """Union thinned by frequency"""
  frequencies = {x: 0 for x in range(max_val)}
  for hv in hvs:
    for position in hv:
      frequencies[position] += 1

  sorted_freqs = [k for k,v in sorted(
    frequencies.items(),
    key=lambda item: item[1],
    reverse=True
  )]

  return np.array(sorted_freqs[:dims])
