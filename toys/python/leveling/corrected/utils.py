import numpy as np


def new_hv(n: int=10_000, fill_val: int | None = None) -> np.ndarray:
  """Generate a new random hypervector with elements {-1, 1}"""
  if fill_val is not None:
    return np.full(n, fill_val, dtype=np.int64)
  return np.random.choice([1, -1], size=n).astype(np.int64)


def compare_hv(hv1: np.ndarray, hv2: np.ndarray) -> float:
  """Cosine similarity of two hypervectors"""
  norm1 = np.linalg.norm(hv1)
  norm2 = np.linalg.norm(hv2)
  if norm1 == 0 or norm2 == 0:
    return 0.0
  return float(np.dot(hv1, hv2) / (norm1 * norm2))


def make_levels_hamming(
  levels: int,
  hv1: np.ndarray | None = None,
  hv2: np.ndarray | None = None
) -> dict:
  """Return a dictionary of linearly correlated hypervectors"""
  if hv1 is None:
    hv1 = new_hv()
  if hv2 is None:
    hv2 = new_hv()

  hyperspace = {}
  current = hv1.copy()
  hyperspace[0] = current.copy()

  diff_idx = np.where(hv1 != hv2)[0]
  perm = np.random.permutation(diff_idx)
  d = len(diff_idx)
  prev_replace = 0

  for level in range(1, levels):
    n_replace = round(level * d / (levels - 1))
    new_indices = perm[prev_replace:n_replace]
    current[new_indices] = hv2[new_indices]
    hyperspace[level] = current.copy()
    prev_replace = n_replace

  return hyperspace



def make_levels_manhattan(
  levels: int,
  hv1: np.ndarray | None = None,
  hv2: np.ndarray | None = None,
  step: int = 1
) -> dict:
  """Return a dictionary of linearly correlated hypervectors"""
  if hv1 is None:
    hv1 = new_hv()
  if hv2 is None:
    hv2 = new_hv()

  hyperspace = {}
  current = hv1.copy()
  hyperspace[0] = current.copy()

  total_work = np.sum(np.abs(hv2 - current))
  prev_work = 0

  for level in range(1, levels):
    target_work = round(level * total_work / (levels - 1))
    work_this_level = target_work - prev_work

    while work_this_level > 0:
      unfinished = np.where(current != hv2)[0]
      if len(unfinished) == 0:
        break

      i = np.random.choice(unfinished)
      delta = hv2[i] - current[i]
      move = min(step, abs(delta), work_this_level)

      current[i] += np.sign(delta) * move
      work_this_level -= move

    hyperspace[level] = current.copy()
    prev_work = target_work

  return hyperspace

