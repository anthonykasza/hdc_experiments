from math import sqrt
import numpy as np
import copy

from bsdc_cdt import *


# ============================================================
# Configuration
# ============================================================

print("DIMS", DIMS)
print("MAX_VAL", MAX_VAL)


# ============================================================
# Utility helpers
# ============================================================

def print_header(title):
  print("\n" + "=" * 60)
  print(title)
  print("=" * 60)


def mean_index_over_runs(op, runs=100):
  means = []
  for r in range(runs):
    h1 = new_hv(seed=100 + r)
    h2 = new_hv(seed=200 + r)
    hv = op([h1, h2])
    means.append(np.mean(hv))
  return np.mean(means)


# ============================================================
# 1. Base hypervectors
# ============================================================

print_header("Base hypervectors")

h1 = new_hv(seed=100)
h2 = new_hv(seed=101)

print("h1 length:", len(h1))
print("h1 sim h2:", similarity(h1, h2))


# ============================================================
# 2. Bundling vs Binding
# ============================================================

print_header("Bundling vs Binding")

bu = bundle([h1, h2])
bi = bind([h1, h2])

print("bundle sim h1:", similarity(bu, h1))
print("bundle sim h2:", similarity(bu, h2))
print()

print("bind sim h1:", similarity(bi, h1))
print("bind sim h2:", similarity(bi, h2))
print()

print("bind–bundle sim:", similarity(bi, bu))
print(
  f"bind–bundle index overlap: "
  f"{len(set(bi) & set(bu))}/{DIMS}"
)


# ============================================================
# 3. Structured similarity (controlled perturbation)
# ============================================================

print_header("Structured similarity")

h3 = copy.copy(h1)
h4 = copy.copy(h2)

# Controlled perturbation: shift every other bit
for i in range(len(h3)):
  if i % 2 == 0:
    h3[i] = (h3[i] + 1) % DIMS
    h4[i] = (h4[i] + 1) % DIMS

print("h1 sim h3:", similarity(h1, h3))
print("h2 sim h4:", similarity(h2, h4))
print()

print(
  "bind(h1,h2) sim bind(h3,h4):",
  similarity(bi, bind([h3, h4]))
)
print(
  "bundle(h1,h2) sim bundle(h3,h4):",
  similarity(bu, bundle([h3, h4]))
)


# ============================================================
# 4. Noise sensitivity
# ============================================================

print_header("Noise sensitivity")

noise = new_hv(seed=1111)

print(
  "bind(h1,h2) sim bind(h3,noise):",
  similarity(bi, bind([h3, noise]))
)
print(
  "bundle(h1,h2) sim bundle(h3,noise):",
  similarity(bu, bundle([h3, noise]))
)


# ============================================================
# 5. Dimensional bias check
# ============================================================

print_header("Mean index (bias check)")

print("bundle mean index:", mean_index_over_runs(bundle))
print("bind mean index:  ", mean_index_over_runs(bind))
print()


# ============================================================
# 6. Leveling
# ============================================================
print_header("Self leveling")

h1 = np.array([0, 1, 2, 3, 4])
rng = np.random.default_rng(123)

# universe definition remains unchanged
universe = set(range(len(h1) ** 2))

# persistent state
removable_ones = set(h1)
addable_zeros = universe - removable_ones

h2 = add_sub(
  h1,
  element_count=2,
  removable_ones=removable_ones,
  addable_zeros=addable_zeros,
  rng=rng
)

print('original\t', h1)
print('2 flips \t', h2)
print()

print("Small HV: Five levels with a single flip per level")
levels = make_levels(
  level_count=5,
  elements_per_level=1,
  basis_hv=h1,
  seed=123
)
for idx, level in enumerate(levels):
  print(idx, level)
print()


h1 = new_hv()
flips_per_level = int(len(h1) / 5)
print(f'Large HV: Five levels with {flips_per_level} flip per level')
levels = make_levels(
  level_count=5,
  elements_per_level=flips_per_level,
  basis_hv=h1,
  seed=123
)
for idx, level in enumerate(levels):
  print(f'{idx} {level[0:3]}..{level[-3:]} {similarity(h1, level)}')
print()
