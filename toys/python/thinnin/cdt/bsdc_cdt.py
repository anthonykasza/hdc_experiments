# Originally based on HoloVec's bsdc.py
# Instead of operating on raw binary, we compress
#  the SDR into its one-hot indices. This is done similarly
#  to compression in sparse block coding.

from math import sqrt
import numpy as np
import copy


# Hypervectors longer than DIMS will get thinned to DIMS
#  when they are operated on.
DIMS = 200

# Squares are nice because they can be tracked as diagonals.
MAX_VAL = DIMS**2


def new_hv(dims=DIMS, max_val=MAX_VAL, fill=None, seed=420):
  """Make a new hypervector"""
  # If fill is present, MAX_VAL and seed are ignored
  if fill is not None:
    return np.array([fill] * max_val)

  # Randomly select hot indices from 0 to MAX_VAL-1
  rng = np.random.default_rng(seed)
  on_indices = rng.choice(max_val, size=dims, replace=False)
  return on_indices


def bundle(hvs, dims=DIMS):
  """Bundle: be as similar to all inputs as possible"""
  # Stack and count frequency of indices
  stacked = np.vstack(hvs)
  unique, counts = np.unique(stacked, return_counts=True)

  # Sort by frequency (descending)
  sorted_indices = np.argsort(-counts)
  sorted_numbers = unique[sorted_indices]

  # Pick top indices to maximize overlap
  result = sorted_numbers[:DIMS]
  return result



def permute(hv, positions=1):
  """Cyclic shift ->"""
  return np.roll(hv, shift=positions, axis=0)


def _context_signature(hvs):
  """
  Deterministic context hash from a set of hypervectors.
  Order-invariant.
  If we want to add attention or weighted binding then
    we would adjust this signature to value certain
    hv constituents more strongly.
  """
  if len(hvs) == 0:
    return 0
  return hash(tuple(sorted(np.unique(np.concatenate(hvs)))))


def _score_bits(hv, context_sig):
  """
  Deterministic score for each bit in hv given context.
  Lower score = higher priority.
  """
  return np.array([
    hash((int(bit), context_sig)) & 0xffffffff
    for bit in hv
  ])


def bind(hvs, dims=DIMS):
  """An implementation of Context-Dependent Thinning (CDT)"""
  if len(hvs) == 0:
    return np.array([], dtype=int)

  target_hot = dims
  per_component = max(1, target_hot // len(hvs))
  thinned_parts = []

  for i, hv in enumerate(hvs):
    # context = all other components
    context = hvs[:i] + hvs[i+1:]
    ctx_sig = _context_signature(context)
    scores = _score_bits(hv, ctx_sig)
    order = np.argsort(scores)

    # proportional sampling
    keep = hv[order[:per_component]]
    thinned_parts.append(keep)

  # merge thinned components
  merged = np.unique(np.concatenate(thinned_parts))

  # final deterministic normalization (if needed)
  if len(merged) > target_hot:
    scores = np.array([hash(int(b)) & 0xffffffff for b in merged])
    merged = merged[np.argsort(scores)[:target_hot]]

  return np.array(sorted(merged))


def similarity(h1, h2):
  """Overlap"""
  if len(h1) == 0 or len(h2) == 0:
    return 0.0
  return len(np.intersect1d(h1, h2)) / min(len(h1), len(h2))


def add_sub(hv, element_count, removable_ones, addable_zeros, rng):
  """Decimate and supplement hot indices"""
  if (len(removable_ones) < element_count or
    len(addable_zeros) < element_count):
    return hv  # no valid flip possible

  to_remove = rng.choice(
    list(removable_ones),
    size=element_count,
    replace=False
  )

  to_add = rng.choice(
    list(addable_zeros),
    size=element_count,
    replace=False
  )

  hv = set(map(int, hv))
  for idx in to_remove:
    hv.remove(idx)
    removable_ones.remove(idx)
  for idx in to_add:
    hv.add(idx)
    addable_zeros.remove(idx)
  return np.array(sorted(hv))



def make_levels(
  level_count=10,
  elements_per_level=1,
  basis_hv=None,
  seed=123
):
  """Return levels without replacement across flips"""
  if basis_hv is None:
    basis_hv = new_hv()
  rng = np.random.default_rng(seed)

  # initial state
  hv = np.array(sorted(map(int, basis_hv)))
  universe = set(range(len(hv) ** 2))
  removable_ones = set(hv)
  addable_zeros = universe - removable_ones
  levels = [hv]

  for _ in range(level_count):
    hv = add_sub(
      hv,
      elements_per_level,
      removable_ones,
      addable_zeros,
      rng
    )
    levels.append(hv)
  return levels

