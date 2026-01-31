from math import sqrt
import numpy as np
import copy

from bsdc_cdt import *


# ============================================================
# Configuration
# ============================================================

DIMS = 1000 ** 2
HOT = int(sqrt(DIMS))
print("DIMS", DIMS)
print("HOT", HOT)

m = Model(dims=DIMS)


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
        h1 = m.new_hv(seed=100 + r)
        h2 = m.new_hv(seed=200 + r)
        hv = op([h1, h2])
        means.append(np.mean(hv))
    return np.mean(means)


# ============================================================
# 1. Base hypervectors
# ============================================================

print_header("Base hypervectors")

h1 = m.new_hv(seed=100)
h2 = m.new_hv(seed=101)

print("h1 length:", len(h1))
print("h1 sim h2:", m.similarity(h1, h2))


# ============================================================
# 2. Bundling vs Binding
# ============================================================

print_header("Bundling vs Binding")

bu = m.bundle([h1, h2])
bi = m.bind([h1, h2])

print("bundle sim h1:", m.similarity(bu, h1))
print("bundle sim h2:", m.similarity(bu, h2))
print()

print("bind sim h1:", m.similarity(bi, h1))
print("bind sim h2:", m.similarity(bi, h2))
print()

print("bind–bundle sim:", m.similarity(bi, bu))
print(
    f"bind–bundle index overlap: "
    f"{len(set(bi) & set(bu))}/{HOT}"
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

print("h1 sim h3:", m.similarity(h1, h3))
print("h2 sim h4:", m.similarity(h2, h4))
print()

print(
    "bind(h1,h2) sim bind(h3,h4):",
    m.similarity(bi, m.bind([h3, h4]))
)
print(
    "bundle(h1,h2) sim bundle(h3,h4):",
    m.similarity(bu, m.bundle([h3, h4]))
)


# ============================================================
# 4. Noise sensitivity
# ============================================================

print_header("Noise sensitivity")

noise = m.new_hv(seed=1111)

print(
    "bind(h1,h2) sim bind(h3,noise):",
    m.similarity(bi, m.bind([h3, noise]))
)
print(
    "bundle(h1,h2) sim bundle(h3,noise):",
    m.similarity(bu, m.bundle([h3, noise]))
)


# ============================================================
# 5. Dimensional bias check
# ============================================================

print_header("Mean index (bias check)")

print("bundle mean index:", mean_index_over_runs(m.bundle))
print("bind mean index:  ", mean_index_over_runs(m.bind))
