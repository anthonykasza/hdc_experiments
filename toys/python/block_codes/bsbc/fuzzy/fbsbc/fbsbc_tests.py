from fbsbc import *

import random
import math

# -----------------------------
# Test configuration
# -----------------------------

BLOCKS = 1024
BLOCK_SIZE = 64
SIGMA = DEFAULT_SIGMA

random.seed(0)


def avg_sigma(hv):
    return sum(s for _, s in hv) / len(hv)


# ============================================================
# 1. Random generation
# ============================================================

def test_random_generation():
    hv = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)
    assert len(hv) == BLOCKS

    for mu, sigma in hv:
        assert 0 <= mu < BLOCK_SIZE
        assert sigma == SIGMA

    print("✓ random_fuzzy_hv")


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
    hv = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)
    inv = inverse_fuzzy(hv, BLOCK_SIZE)

    bound = bind_fuzzy(hv, inv, block_size=BLOCK_SIZE)

    for mu, sigma in bound:
        assert mu == 0
        assert math.isclose(sigma, math.sqrt(2) * SIGMA)

    print("✓ bind_fuzzy / inverse_fuzzy")


# ============================================================
# 4. Binding dissimilarity
# ============================================================

def test_binding_dissimilarity():
    a = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)
    b = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)

    bound = bind_fuzzy(a, b, block_size=BLOCK_SIZE)

    sim_a = similarity_fuzzy(bound, a, BLOCK_SIZE)
    sim_b = similarity_fuzzy(bound, b, BLOCK_SIZE)

    assert sim_a < 0.5
    assert sim_b < 0.5

    print("✓ binding dissimilarity")


# ============================================================
# 5. Bundling agreement dominance
# ============================================================

def test_bundling_agreement():
    base = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)
    bundle = bundle_fuzzy(base, base, block_size=BLOCK_SIZE)

    sim = similarity_fuzzy(bundle, base, BLOCK_SIZE)
    assert sim > 0.9
    assert avg_sigma(bundle) < avg_sigma(base)

    print("✓ bundling agreement dominance. bundle sigma: ", avg_sigma(bundle), "default sigma:", avg_sigma(base))


# ============================================================
# 6. Bundling disagreement increases sigma
# ============================================================

def test_bundling_disagreement():
    hvs = [random_fuzzy_hv(BLOCKS, BLOCK_SIZE) for _ in range(5)]
    bundle = bundle_fuzzy(*hvs, block_size=BLOCK_SIZE)

    assert avg_sigma(bundle) > SIGMA

    print("✓ bundling disagreement increases sigma", SIGMA, avg_sigma(bundle))


# ============================================================
# 7. Similarity identity & orthogonality
# ============================================================

def test_similarity_properties():
    hv = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)
    hv2 = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)

    sim_self = similarity_fuzzy(hv, hv, BLOCK_SIZE)
    sim_rand = similarity_fuzzy(hv, hv2, BLOCK_SIZE)

    assert sim_self > 0.95
    assert sim_rand < sim_self

    print("✓ similarity properties")


# ============================================================
# 8. Unbinding approximate recovery
# ============================================================

def test_unbinding():
    role = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)
    filler = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)

    bound = bind_fuzzy(role, filler, block_size=BLOCK_SIZE)
    query = bind_fuzzy(bound, inverse_fuzzy(role, BLOCK_SIZE), block_size=BLOCK_SIZE)

    sim = similarity_fuzzy(query, filler, BLOCK_SIZE)

    assert sim > 0.5
    assert avg_sigma(query) > avg_sigma(filler)

    print("✓ approximate unbinding")


# ============================================================
# 9. Permutation invariance
# ============================================================

def test_permutation():
    hv = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)
    perm = permute_fuzzy(hv, shifts=5)

    sim = similarity_fuzzy(hv, perm, BLOCK_SIZE)

    assert sim < 0.2
    assert math.isclose(avg_sigma(hv), avg_sigma(perm))

    print("✓ permutation")


# ============================================================
# 10. Cleanup memory
# ============================================================

def test_cleanup():
    memory = [random_fuzzy_hv(BLOCKS, BLOCK_SIZE) for _ in range(10)]
    target = 3

    query = memory[target]
    idx = cleanup_fuzzy(query, memory, BLOCK_SIZE)

    assert idx == target

    print("✓ cleanup_fuzzy")


def test_symbolicity_extremes():
    base = random_fuzzy_hv(BLOCKS, BLOCK_SIZE)

    # create two hypervectors almost identical to base
    hv1 = [(mu, sigma) for mu, sigma in base]
    hv2 = [( (mu + 1) % BLOCK_SIZE, sigma ) for mu, sigma in base]  # slight difference

    strict = bundle_fuzzy(
        hv1, hv2, hv1,
        block_size=BLOCK_SIZE,
        symbolicity=1.0,
    )

    soft = bundle_fuzzy(
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

    print("\nAll FUZZY tests passed.")
