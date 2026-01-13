import math
import random
import numpy as np

from fuzzy import *

# -----------------------------
# Test parameters
# -----------------------------

# The number of blocks in each hypervector
BLOCKS = 10_000

# The size of each block in a hypervector
BLOCK_SIZE = 64

# SIGMA is the size of the blur around the 1hot bit of the block.
#  SIGMA = 0 is an exact 1hot bit.
#  higher SIGMA, 2 random vectors will be more correlated
SIGMA = 0

print("NUM OF BLOCKS:", BLOCKS)
print("BLOCK SIZE:", BLOCK_SIZE)
print("SIGMA:", SIGMA)
print()
print()


def avg_sigma(hv):
  return sum(s for _, s in hv) / len(hv)


# -----------------------------
# 1. Identity / self similarity
# -----------------------------

hv = fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA)
sim = similarity_compressed(hv, hv, BLOCK_SIZE)

print("TEST 1: identity similarity")
print("similarity(hv, hv) =", sim)
print()


# -----------------------------
# 2. Random orthogonality
# -----------------------------

hv1 = fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA)
hv2 = fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA)

sim = similarity_compressed(hv1, hv2, BLOCK_SIZE)

print("TEST 2: random orthogonality")
print("similarity(random, random) =", sim)
print("(should be low, not zero)")
print()


# -----------------------------
# 3. Bundling similarity ordering
# -----------------------------

hvs = [fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA) for _ in range(5)]
bundle = bundle_compressed(*hvs, block_size=BLOCK_SIZE)

print("TEST 3: bundle similarity ordering")
for i, hv in enumerate(hvs):
  print(f"bundle vs hv{i}:", similarity_compressed(bundle, hv, BLOCK_SIZE))

noise = fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA)
print("bundle vs noise:", similarity_compressed(bundle, noise, BLOCK_SIZE))
print("bundle sigma:", avg_sigma(bundle))
print()


# -----------------------------
# 4. Partial agreement dominance
# -----------------------------

base = fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA)
agree = [base, base, base]
disagree = [fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA) for _ in range(2)]

bundle_mix = bundle_compressed(*(agree + disagree), block_size=BLOCK_SIZE)

print("TEST 4: partial agreement dominance")
print("bundle vs base:", similarity_compressed(bundle_mix, base, BLOCK_SIZE))
print("bundle sigma:", avg_sigma(bundle_mix))
print()


# -----------------------------
# 5. Binding dissimilarity
# -----------------------------

hv1 = fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA)
hv2 = fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA)
hv3 = fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA)

bound = bind_compressed(hv1, hv2, hv3, block_size=BLOCK_SIZE)

print("TEST 5: binding dissimilarity")
print("bound vs hv1:", similarity_compressed(bound, hv1, BLOCK_SIZE))
print("bound vs hv2:", similarity_compressed(bound, hv2, BLOCK_SIZE))
print("bound vs hv3:", similarity_compressed(bound, hv3, BLOCK_SIZE))
print("bound sigma:", avg_sigma(bound))
print()


# -----------------------------
# 6. Approximate unbinding
# -----------------------------

inv1 = inverse_compressed(hv1, BLOCK_SIZE)
query = bind_compressed(bound, inv1, block_size=BLOCK_SIZE)

bc = bind_compressed(hv2, hv3, block_size=BLOCK_SIZE)

print("TEST 6: approximate unbinding")
print("query vs (hv2 * hv3):",
    similarity_compressed(query, bc, BLOCK_SIZE))
print("query vs noise:",
    similarity_compressed(query, fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA), BLOCK_SIZE))
print()


# -----------------------------
# 7. Interpolation / leveling behavior
# -----------------------------

hvA = fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA)
hvB = fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA)

print("TEST 7: interpolation monotonicity")
steps = 5
for t in range(steps + 1):
  interp = []
  alpha = t / steps
  for (m1, s1), (m2, s2) in zip(hvA, hvB):
    mu = int((1 - alpha) * m1 + alpha * m2) % BLOCK_SIZE
    sigma = (1 - alpha) * s1 + alpha * s2
    interp.append((mu, sigma))
  print(
    f"step {t}: sim(A, interp) =",
    similarity_compressed(hvA, interp, BLOCK_SIZE)
  )
print()


# -----------------------------
# 8. Permutation invariance
# -----------------------------

perm = permute_compressed(hv, shifts=5)

print("TEST 8: permutation invariance")
print("hv vs perm(hv):", similarity_compressed(hv, perm, BLOCK_SIZE))
print("sigma hv:", avg_sigma(hv))
print("sigma perm:", avg_sigma(perm))
print()


# -----------------------------
# 9. Noise injection (HLB-style)
# -----------------------------

noisy = [(mu, s * 2.0) for mu, s in hv]

print("TEST 9: explicit noise injection")
print("hv vs noisy:", similarity_compressed(hv, noisy, BLOCK_SIZE))
print("sigma hv:", avg_sigma(hv))
print("sigma noisy:", avg_sigma(noisy))
print()


# -----------------------------
# 10. Capacity stress (many bundles)
# -----------------------------

many = [fuzzy_hdv_compressed(BLOCKS, BLOCK_SIZE, SIGMA) for _ in range(20)]
big_bundle = bundle_compressed(*many, block_size=BLOCK_SIZE)

print("TEST 10: capacity stress")
print("bundle vs first:", similarity_compressed(big_bundle, many[0], BLOCK_SIZE))
print("bundle sigma:", avg_sigma(big_bundle))
print()
