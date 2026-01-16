from cnr import *

import random
import math

# -----------------------------
# Test configuration
# -----------------------------

BLOCK_SIZE = 128
BLOCKS = 10
SIGMA = DEFAULT_SIGMA

random.seed(0)


def avg_sigma(hv):
    return sum(s for _, s in hv) / len(hv)


# ============================================================
# 1. Random generation
# ============================================================

def test_random_generation():
    hv = random_hv(BLOCKS, BLOCK_SIZE)
    assert len(hv) == BLOCKS

    for mu, sigma in hv:
        assert 0 <= mu < BLOCK_SIZE
        assert sigma == SIGMA

    print("✓ random_hv")


# ============================================================
# 2. Circular distance
# ============================================================

def test_circular_distance():
    assert circular_distance(0, 0, 64) == 0
    assert circular_distance(0, 63, 64) == 1
    assert circular_distance(10, 20, 64) == 10
    assert circular_distance(20, 10, 64) == 10

    print("✓ circular_distance")


# ============================================================
# 3. Binding identity & inverse
# ============================================================

def test_binding_inverse():
    hv = random_hv(BLOCKS, BLOCK_SIZE)
    inv = inverse(hv, BLOCK_SIZE)

    bound = bind(hv, inv, block_size=BLOCK_SIZE)

    for mu, sigma in bound:
        assert mu == 0
        assert math.isclose(sigma, math.sqrt(2) * SIGMA)

    print("✓ bind / inverse")


# ============================================================
# 4. Binding dissimilarity
# ============================================================

def test_binding_dissimilarity():
    a = random_hv(BLOCKS, BLOCK_SIZE)
    b = random_hv(BLOCKS, BLOCK_SIZE)

    bound = bind(a, b, block_size=BLOCK_SIZE)

    sim_a = similarity(bound, a, BLOCK_SIZE)
    sim_b = similarity(bound, b, BLOCK_SIZE)

    assert sim_a < 0.5
    assert sim_b < 0.5

    print("✓ binding dissimilarity")


# ============================================================
# 5. Bundling agreement dominance
# ============================================================

def test_bundling_agreement():
    base = random_hv(BLOCKS, BLOCK_SIZE)
    b = bundle(base, base, block_size=BLOCK_SIZE)

    sim = similarity(b, base, BLOCK_SIZE)
    assert sim > 0.9
    assert avg_sigma(b) < avg_sigma(base)

    print("✓ bundling agreement dominance. bundle sigma: ", avg_sigma(b), "default sigma:", avg_sigma(base))


# ============================================================
# 6. Bundling disagreement increases sigma
# ============================================================

def test_bundling_disagreement():
    hvs = [random_hv(BLOCKS, BLOCK_SIZE) for _ in range(5)]
    b = bundle(*hvs, block_size=BLOCK_SIZE)

    assert avg_sigma(b) > SIGMA

    print("✓ bundling disagreement increases sigma", SIGMA, avg_sigma(b))


# ============================================================
# 7. Similarity identity & orthogonality
# ============================================================

def test_similarity_properties():
    hv = random_hv(BLOCKS, BLOCK_SIZE)
    hv2 = random_hv(BLOCKS, BLOCK_SIZE)

    sim_self = similarity(hv, hv, BLOCK_SIZE)
    sim_rand = similarity(hv, hv2, BLOCK_SIZE)

    assert sim_self > 0.95
    assert sim_rand < sim_self

    print("✓ similarity properties")


# ============================================================
# 8. Unbinding approximate recovery
# ============================================================

def test_unbinding():
    role = random_hv(BLOCKS, BLOCK_SIZE)
    filler = random_hv(BLOCKS, BLOCK_SIZE)

    bound = bind(role, filler, block_size=BLOCK_SIZE)
    query = bind(bound, inverse(role, BLOCK_SIZE), block_size=BLOCK_SIZE)

    sim = similarity(query, filler, BLOCK_SIZE)

    assert sim > 0.5
    assert avg_sigma(query) > avg_sigma(filler)

    print("✓ approximate unbinding")


# ============================================================
# 9. Permutation invariance
# ============================================================

def test_permutation():
    hv = random_hv(BLOCKS, BLOCK_SIZE)
    perm = permute(hv, shifts=5)

    sim = similarity(hv, perm, BLOCK_SIZE)

    assert sim < 0.2
    assert math.isclose(avg_sigma(hv), avg_sigma(perm))

    print("✓ permutation")


# ============================================================
# 10. Cleanup memory
# ============================================================

def test_cleanup():
    memory = [random_hv(BLOCKS, BLOCK_SIZE) for _ in range(10)]
    target = 3

    query = memory[target]
    idx = cleanup(query, memory, BLOCK_SIZE)

    assert idx == target

    print("✓ cleanup")


def test_symbolicity_extremes():
    base = random_hv(BLOCKS, BLOCK_SIZE)

    # create two hypervectors almost identical to base
    hv1 = [(mu, sigma) for mu, sigma in base]
    hv2 = [( (mu + 1) % BLOCK_SIZE, sigma ) for mu, sigma in base]  # slight difference

    strict = bundle(
        hv1, hv2, hv1,
        block_size=BLOCK_SIZE,
        symbolicity=1.0,
    )

    soft = bundle(
        hv1, hv2, hv1,
        block_size=BLOCK_SIZE,
        symbolicity=0.0,
    )

    assert avg_sigma(strict) > avg_sigma(soft)  # symbolicity=1 → more "symbolic" → less shrinkage

    print("✓ symbolicity extremes with slight disagreement.", avg_sigma(strict), avg_sigma(soft))



# ============================================================
# Run all tests
# ============================================================

if __name__ == "__main__":
    test_random_generation()
    test_circular_distance()
    test_binding_inverse()
    test_binding_dissimilarity()
    test_bundling_agreement()
    test_bundling_disagreement()
    test_similarity_properties()
    test_unbinding()
    test_permutation()
    test_cleanup()
    test_symbolicity_extremes()

    print("\nAll CNR tests passed.")
