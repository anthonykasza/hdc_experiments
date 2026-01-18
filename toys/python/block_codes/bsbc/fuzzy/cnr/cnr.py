# ============================================================
# CNR: Circular Normal Representation (Unified)
# ============================================================

import math
import random
from typing import List, Tuple

# -----------------------------
# Global configuration
# -----------------------------

EPSILON = 1e-12
DEFAULT_SIGMA = 1.5

# -----------------------------
# Types
# -----------------------------

CNRBlock = Tuple[int, float]   # (mu, sigma)
CNRHV = List[CNRBlock]

# ============================================================
# Circular utilities
# ============================================================

def circular_distance(a: int, b: int, modulus: int) -> int:
    """
    Shortest distance on a cyclic group Z_modulus.
    """
    d = abs(a - b) % modulus
    return min(d, modulus - d)

def circular_mean(indices: List[int], modulus: int) -> int:
    """
    Circular mean of discrete indices.
    If dispersion is maximal (vector sum ~ 0), return a random index
    from the constituents.
    """
    if not indices:
        raise ValueError("circular_mean requires at least one index")

    sum_cos = sum(math.cos(2 * math.pi * k / modulus) for k in indices)
    sum_sin = sum(math.sin(2 * math.pi * k / modulus) for k in indices)

    mag = math.hypot(sum_cos, sum_sin)
    if mag < EPSILON:
        # Uniform / maximally dispersed: return random constituent
        return random.choice(indices)

    angle = math.atan2(sum_sin, sum_cos)
    if angle < 0:
        angle += 2 * math.pi

    mu = int(math.floor(modulus * angle / (2 * math.pi) + 0.5)) % modulus
    return mu

# ============================================================
# Hypervector generation
# ============================================================

def random_hv(num_blocks: int, block_size: int, sigma_init: float = DEFAULT_SIGMA) -> CNRHV:
    return [(random.randrange(block_size), sigma_init) for _ in range(num_blocks)]

# ============================================================
# Binding / inverse
# ============================================================

def bind(*hvs: CNRHV, block_size: int) -> CNRHV:
    """
    Modular sum of μ. σ propagates as the max sigma of the constituents.
    This ensures bound hypervectors do not become artificially more certain
    than any of the inputs.
    """
    if not hvs:
        raise ValueError("bind requires at least one hypervector")

    num_blocks = len(hvs[0])
    out: CNRHV = []

    for i in range(num_blocks):
        # modular sum of mus
        mu = sum(hv[i][0] for hv in hvs) % block_size
        # propagate maximum sigma among inputs
        sigma = max(hv[i][1] for hv in hvs)
        out.append((mu, sigma))

    return out


def inverse(hv: CNRHV, block_size: int) -> CNRHV:
    return [((-mu) % block_size, sigma) for mu, sigma in hv]

# ============================================================
# Bundling
# ============================================================

def bundle(*hvs: CNRHV, block_size: int) -> CNRHV:
    """
    Belief fusion using circular statistics (von Mises inspired):
    - μ: circular mean
    - σ: shrinks when μ’s cluster, grows when μ’s disperse
    - σ now scaled relative to block_size to avoid washed-out similarity
    """
    if not hvs:
        raise ValueError("bundle requires at least one hypervector")

    num_blocks = len(hvs[0])
    out: CNRHV = []

    for i in range(num_blocks):
        mus = [hv[i][0] for hv in hvs]
        sigmas = [hv[i][1] for hv in hvs]

        # circular mean
        mu_hat = circular_mean(mus, block_size)

        # compute circular clustering r in [0,1]
        sum_cos = sum(math.cos(2*math.pi*m/block_size) for m in mus)
        sum_sin = sum(math.sin(2*math.pi*m/block_size) for m in mus)
        r = math.hypot(sum_cos, sum_sin) / len(mus)  # r ~1 clustered, ~0 dispersed

        # -----------------------------
        # Shrink sigma when mus cluster, grow when dispersed
        # -----------------------------
        avg_sigma_input = sum(sigmas) / len(sigmas)

        # shrink factor: r ~1 -> shrink, r ~0 -> no shrink
        shrink_factor = 1.0 - r  # r in [0,1], r=1 -> shrink_factor=0

        # scaled disagreement variance for dispersion
        disagreement2 = shrink_factor * (block_size**2 / 12)

        # final sigma: combine shrinked prior + disagreement
        sigma2 = (avg_sigma_input**2) * shrink_factor + disagreement2
        sigma = math.sqrt(max(sigma2, EPSILON))

        out.append((mu_hat, sigma))

    return out

# ============================================================
# Similarity
# ============================================================
def similarity(hv1: CNRHV, hv2: CNRHV, block_size: int) -> float:
    """
    Gaussian kernel over circular distance with weighted inverse variance.
    Distance and variance scaled to block_size to avoid washed-out similarity.
    """
    assert len(hv1) == len(hv2)
    score = 0.0
    weight_sum = 0.0

    for (m1, s1), (m2, s2) in zip(hv1, hv2):
        d = circular_distance(m1, m2, block_size)
        var = s1**2 + s2**2 + EPSILON

        # scale distance relative to block size
        dn = d / block_size
        v = var / (block_size**2)

        w = 1.0 / v
        score += w * math.exp(- (dn**2) / (2 * v))
        weight_sum += w

    return score / weight_sum if weight_sum > 0 else 0.0

# ============================================================
# Cleanup memory
# ============================================================

def cleanup(query: CNRHV, dictionary: List[CNRHV], block_size: int) -> int:
    sims = [similarity(query, hv, block_size) for hv in dictionary]
    return max(range(len(sims)), key=sims.__getitem__)

# ============================================================
# Permutation
# ============================================================

def permute(hv: CNRHV, shifts: int = 1) -> CNRHV:
    shifts %= len(hv)
    return hv[-shifts:] + hv[:-shifts]

# ============================================================
# Run tests
# ============================================================

if __name__ == "__main__":
    random.seed(0)

    BLOCKS = 4096
    BLOCK_SIZE = 128

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
