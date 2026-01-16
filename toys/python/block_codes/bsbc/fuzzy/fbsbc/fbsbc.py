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

FuzzyBlock = Tuple[int, float]   # (mu, sigma)
FuzzyHV = List[FuzzyBlock]


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

def random_fuzzy_hv(
    num_blocks: int,
    block_size: int,
    sigma_init: float = DEFAULT_SIGMA,
) -> FuzzyHV:
    return [
        (random.randrange(block_size), sigma_init)
        for _ in range(num_blocks)
    ]


# ============================================================
# Binding / inverse
# ============================================================

def bind_fuzzy(*hvs: FuzzyHV, block_size: int) -> FuzzyHV:
    num_blocks = len(hvs[0])
    out: FuzzyHV = []

    for i in range(num_blocks):
        mu = sum(hv[i][0] for hv in hvs) % block_size
        sigma2 = sum(hv[i][1] ** 2 for hv in hvs)
        out.append((mu, math.sqrt(sigma2)))

    return out


def inverse_fuzzy(hv: FuzzyHV, block_size: int) -> FuzzyHV:
    return [((-mu) % block_size, sigma) for mu, sigma in hv]


# ============================================================
# Bundling
# ============================================================

def bundle_fuzzy(
    *hvs: FuzzyHV,
    block_size: int,
    weights=None,
    symbolicity: float = 1.0,
) -> FuzzyHV:
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

    out: FuzzyHV = []

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

def similarity_fuzzy(
    hv1: FuzzyHV,
    hv2: FuzzyHV,
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

def cleanup_fuzzy(
    query: FuzzyHV,
    dictionary: List[FuzzyHV],
    block_size: int,
) -> int:
    sims = [
        similarity_fuzzy(query, hv, block_size)
        for hv in dictionary
    ]
    return max(range(len(sims)), key=sims.__getitem__)


# ============================================================
# Permutation
# ============================================================

def permute_fuzzy(hv: FuzzyHV, shifts: int = 1) -> FuzzyHV:
    shifts %= len(hv)
    return hv[-shifts:] + hv[:-shifts]


# ============================================================
# Example sanity check
# ============================================================

if __name__ == "__main__":
    random.seed(0)

    BLOCKS = 4096
    BLOCK_SIZE = 64

    a = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)
    b = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)

    bundle = bundle_fuzzy(a, a, a, b, block_size=BLOCK_SIZE)

    print("Similarity(a, a):", similarity_fuzzy(a, a, BLOCK_SIZE))
    print("Similarity(bundle, a):", similarity_fuzzy(bundle, a, BLOCK_SIZE))
    print("Similarity(bundle, b):", similarity_fuzzy(bundle, b, BLOCK_SIZE))
    print("Avg sigma a:", sum(s for _, s in a) / BLOCKS)
    print("Avg sigma bundle:", sum(s for _, s in bundle) / BLOCKS)
