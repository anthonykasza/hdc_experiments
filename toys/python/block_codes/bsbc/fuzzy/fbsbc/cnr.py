import math
import random
from typing import List, Tuple

# ============================================================
# Global configuration
# ============================================================

EPSILON = 1e-9
DEFAULT_SIGMA = 1.5


# ============================================================
# Types
# ============================================================

CNRBlock = Tuple[int, float]   # (mu, sigma)
CNRHV = List[CNRBlock]


# ============================================================
# Circular utilities
# ============================================================

def circular_distance(a: int, b: int, modulus: int) -> int:
    d = abs(a - b)
    return min(d, modulus - d)


def circular_weighted_mean(indices, weights, modulus):
    angles = [2 * math.pi * x / modulus for x in indices]
    s = sum(w * math.sin(a) for w, a in zip(weights, angles))
    c = sum(w * math.cos(a) for w, a in zip(weights, angles))
    angle = math.atan2(s, c)
    mu = round((angle * modulus) / (2 * math.pi))
    return mu % modulus


# ============================================================
# Hypervector generation
# ============================================================

def random_hv(
    num_blocks: int,
    block_size: int,
    sigma_init: float = DEFAULT_SIGMA,
) -> CNRHV:
    return [
        (random.randrange(block_size), sigma_init)
        for _ in range(num_blocks)
    ]


# ============================================================
# Binding / inverse
# ============================================================

def bind(*hvs: CNRHV, block_size: int) -> CNRHV:
    num_blocks = len(hvs[0])
    out: CNRHV = []

    for i in range(num_blocks):
        mu = sum(hv[i][0] for hv in hvs) % block_size
        sigma2 = sum(hv[i][1] ** 2 for hv in hvs)
        out.append((mu, math.sqrt(sigma2)))

    return out


def inverse(hv: CNRHV, block_size: int) -> CNRHV:
    return [((-mu) % block_size, sigma) for mu, sigma in hv]


# ============================================================
# Bundling
# ============================================================

def bundle(
    *hvs: CNRHV,
    block_size: int,
    weights=None,
    symbolicity: float = 1.0,
) -> CNRHV:
    """
    Belief fusion with semantic confidence.

    μ  : circular weighted mean (integer, rounded)
    σ  : semantic uncertainty
         - shrinks with agreement (self-bundling)
         - grows with disagreement
         - controlled by symbolicity ∈ [0,1]
         - clipped to [0, block_size/2]

    weights:
        deterministic randsel-style participation weights
        default: equal weighting
    """
    num_blocks = len(hvs[0])
    n = len(hvs)

    # -----------------------------
    # Weights
    # -----------------------------
    if weights is None:
        weights = [1.0] * n
    else:
        assert len(weights) == n

    # normalize to sum=1
    wsum = sum(weights)
    weights = [w / wsum for w in weights]

    out: CNRHV = []

    for i in range(num_blocks):
        mus = [hv[i][0] for hv in hvs]
        sigmas = [hv[i][1] for hv in hvs]

        # -----------------------------
        # μ : circular weighted mean
        # -----------------------------
        mu_hat = circular_weighted_mean(mus, weights, block_size)

        # -----------------------------
        # mean variance (self-bundling shrinkage)
        # -----------------------------
        mean_var = sum((w ** 2) * (s ** 2) for w, s in zip(weights, sigmas))

        # -----------------------------
        # disagreement (correlation term)
        # -----------------------------
        disagreement = sum(
            w * circular_distance(m, mu_hat, block_size) ** 2
            for w, m in zip(weights, mus)
        )

        # -----------------------------
        # σ² interpolation
        # -----------------------------
        sigma2 = (1.0 - symbolicity) * mean_var + symbolicity * (mean_var + disagreement)
        sigma = math.sqrt(max(sigma2, 0.0))

        # -----------------------------
        # Hard clip in block units
        # -----------------------------
        sigma = min(max(sigma, 0.0), block_size / 2)

        out.append((mu_hat, sigma))

    return out




# ============================================================
# Similarity
# ============================================================

def similarity(
    hv1: CNRHV,
    hv2: CNRHV,
    block_size: int,
) -> float:
    num = 0.0
    den = 0.0

    for (m1, s1), (m2, s2) in zip(hv1, hv2):
        d = circular_distance(m1, m2, block_size)
        var = s1 * s1 + s2 * s2 + EPSILON
        w = 1 / var
        num += w * math.exp(-(d * d) / (2 * var))
        den += w

    return num / den if den > 0 else 0.0


# ============================================================
# Cleanup memory
# ============================================================

def cleanup(
    query: CNRHV,
    dictionary: List[CNRHV],
    block_size: int,
) -> int:
    sims = [
        similarity(query, hv, block_size)
        for hv in dictionary
    ]
    return max(range(len(sims)), key=sims.__getitem__)


# ============================================================
# Permutation
# ============================================================

def permute(hv: CNRHV, shifts: int = 1) -> CNRHV:
    shifts %= len(hv)
    return hv[-shifts:] + hv[:-shifts]


# ============================================================
# Example sanity check
# ============================================================

if __name__ == "__main__":
    random.seed(0)

    BLOCK_SIZE = 128
    BLOCKS = 10

    for BLOCKS in list(range(1, 21)) + [1024, 2048, 10_000]:
      for BLOCK_SIZE in [8, 16, 32, 64, 128, 1000]:
        a = random_hv(BLOCKS, BLOCK_SIZE)
        b = random_hv(BLOCKS, BLOCK_SIZE)
        noise = random_hv(BLOCKS, BLOCK_SIZE)

        b_b = bundle(a, a, a, b, block_size=BLOCK_SIZE)

        print("Blocks count:", BLOCKS)
        print("Block size:", BLOCK_SIZE)
        print("Similarity(a, a):", similarity(a, a, BLOCK_SIZE))
        print("Similarity(bundle, a):", similarity(b_b, a, BLOCK_SIZE))
        print("Similarity(bundle, b):", similarity(b_b, b, BLOCK_SIZE))
        print("Similarity(bundle, noise):", similarity(b_b, noise, BLOCK_SIZE))
        print("Avg sigma a:", sum(s for _, s in a) / BLOCKS)
        print("Avg sigma bundle:", sum(s for _, s in b_b) / BLOCKS)
        print()
