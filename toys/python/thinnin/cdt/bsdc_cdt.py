# Based on HoloVec's bsdc.py. Instead of operating on raw binary, we
#  compress the SDR into its one-hot indices. This is done similarly to
#  compression in sparse block coding.

from math import sqrt
import numpy as np


class Model():

  def __init__(self, dims, seed=9999):
    # Dimensions of the binary representations. This is the
    #  max value of elements for integer representations.
    self.dims = dims

    # Count of 1s in binary representations. This is the
    #  dimensions of integer representations.
    self.hot_count = 1 / sqrt(self.dims)

  def new_hv(self, fill=None, seed=420):
    """Make a new hypervector"""
    # If fill is present, self.dims and seed are ignored
    if fill is not None:
      return np.array([fill] * self.dims)

    # Randomly select hot indices from 0 to self.dims-1
    rng = np.random.default_rng(seed)
    on_indices = rng.choice(self.dims, size=int(self.dims * self.hot_count), replace=False)
    return on_indices


  def bundle(self, hvs):
    """Bundle: be as similar to all inputs as possible"""
    # Stack and count frequency of indices
    stacked = np.vstack(hvs)
    unique, counts = np.unique(stacked, return_counts=True)

    # Sort by frequency (descending)
    sorted_indices = np.argsort(-counts)
    sorted_numbers = unique[sorted_indices]

    # Pick top indices to maximize overlap
    result = sorted_numbers[:int(self.dims * self.hot_count)]
    return result



  def permute(self, hv, positions=1):
    """Cyclic shift ->"""
    return np.roll(hv, shift=positions, axis=0)


  def _context_signature(self, hvs):
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


  def _score_bits(self, hv, context_sig):
    """
    Deterministic score for each bit in hv given context.
    Lower score = higher priority.
    """
    return np.array([
      hash((int(bit), context_sig)) & 0xffffffff
      for bit in hv
    ])


  def bind(self, hvs):
    """
    An implementation of Context-Dependent Thinning (CDT)
    Versions of thinning include:
      - direct conjunctive
      - permutive
      - additive
        - auto
        - self-exclusive auto
      - subtractive
        - auto
        - self-exclusive auto
    """
    if len(hvs) == 0:
      return np.array([], dtype=int)

    target_hot = int(self.dims * self.hot_count)
    per_component = max(1, target_hot // len(hvs))
    thinned_parts = []

    for i, hv in enumerate(hvs):
      # context = all other components
      context = hvs[:i] + hvs[i+1:]
      ctx_sig = self._context_signature(context)

      scores = self._score_bits(hv, ctx_sig)
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


  def similarity(self, h1, h2):
    """Overlap"""
    if len(h1) == 0 or len(h2) == 0:
      return 0.0
    return len(np.intersect1d(h1, h2)) / min(len(h1), len(h2))
