# HLB makes MAP fuzzy.
# This is an attempt to make 1hot BSBC fuzzy.
#
# This may be related to Generic Spare Block Codes as
#  described in Factorizers for Distributed Sparse Block


import random
import math
import numpy as np

# -----------------------------
# Hypervector creation
# -----------------------------

def fuzzy_hdv_compressed(
  number_of_blocks=1000,
  block_size=64,
  sigma_init=1.5,
):
  """
  Create a compressed fuzzy BSBC hypervector.

  BSBC:
    - stores only index

  Fuzzy BSBC (this):
    - stores (index, variance)

  FHRR analogy:
    - index ~ phase
    - variance ~ phase noise
  """
  hv = []
  for _ in range(number_of_blocks):
    mu = random.randint(0, block_size - 1)
    sigma = sigma_init
    hv.append((mu, sigma))
  return hv


# -----------------------------
# Circular distance
# -----------------------------

def circ_dist(a, b, block_size):
  d = abs(a - b)
  return min(d, block_size - d)


# -----------------------------
# Binding
# -----------------------------

def bind_compressed(*hvs, block_size):
  """
  Bind compressed fuzzy BSBC hypervectors.

  BSBC:
    - index addition mod block_size

  FHRR:
    - phase addition

  Variance:
    - adds (independent noise assumption)
  """
  num_blocks = len(hvs[0])
  bound = []

  for i in range(num_blocks):
    mu = sum(hv[i][0] for hv in hvs) % block_size
    sigma = math.sqrt(sum(hv[i][1] ** 2 for hv in hvs))
    bound.append((mu, sigma))

  return bound


# -----------------------------
# Inverse
# -----------------------------

def inverse_compressed(hv, block_size):
  """
  Invert a compressed fuzzy BSBC hypervector.

  BSBC:
    - index -> (block_size - index)

  FHRR:
    - complex conjugate

  Variance is unchanged.
  """
  inv = []
  for mu, sigma in hv:
    inv.append(((block_size - mu) % block_size, sigma))
  return inv


# -----------------------------
# Bundling
# -----------------------------

def bundle_compressed(*hvs, block_size):
  """
  Bundle compressed fuzzy BSBC hypervectors.

  BSBC:
    - winner-take-all thinning

  FHRR / HLB:
    - averaging increases noise

  Here:
    - circular mean of indices
    - variance decreases with agreement, increases with disagreement
  """
  num_blocks = len(hvs[0])
  bundle = []

  for i in range(num_blocks):
    mus = np.array([hv[i][0] for hv in hvs])
    sigmas = np.array([hv[i][1] for hv in hvs])

    # circular mean
    angles = mus * 2 * math.pi / block_size
    mean_angle = math.atan2(
      np.mean(np.sin(angles)),
      np.mean(np.cos(angles)),
    )
    mu = int((mean_angle * block_size / (2 * math.pi)) % block_size)

    # variance grows with disagreement
    dispersion = np.mean([
      circ_dist(mu, m, block_size) ** 2 for m in mus
    ])
    sigma = math.sqrt(np.mean(sigmas ** 2) + dispersion)

    bundle.append((mu, sigma))

  return bundle


# -----------------------------
# Similarity
# -----------------------------

def similarity_compressed(hv1, hv2, block_size):
  """
  Similarity between two compressed fuzzy BSBC hypervectors.

  Combines:
    - circular distance of centers
    - uncertainty (variance)

  Analogous to cosine similarity in FHRR / HLB.
  """
  sims = []
  for (m1, s1), (m2, s2) in zip(hv1, hv2):
    d = circ_dist(m1, m2, block_size)
    scale = s1 + s2 + 1e-6
    sims.append(math.exp(-(d ** 2) / (2 * scale ** 2)))
  return sum(sims) / len(sims)


# -----------------------------
# Permutation
# -----------------------------

def permute_compressed(hv, shifts=1):
  """
  Block permutation.

  Same role as:
    - BSBC block rotation
    - permutation matrices in FHRR / HLB
  """
  shifts %= len(hv)
  return hv[-shifts:] + hv[:-shifts]

