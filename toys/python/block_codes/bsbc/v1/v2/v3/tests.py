import numpy as np
from utils import *


# -------------------------
# new_hv tests
# -------------------------

def test_new_hv_shape():
    mu, kappa = new_hv(4, 1)
    assert mu.shape == (4,), f"Expected mu shape (4,), got {mu.shape}"
    assert kappa.shape == (4,), f"Expected kappa shape (4,), got {kappa.shape}"
    print("test_new_hv_shape passed")

def test_new_hv_range():
    mu, _ = new_hv(dims=4, block_size=8, rng=42)
    assert np.all((mu >= 0) & (mu < 8)), f"mu values out of range: {mu}"
    print("test_new_hv_range passed")

def test_new_hv_kappa():
    _, kappa = new_hv(dims=4, block_size=8, kappa=0.123456789)
    assert np.all(np.isclose(kappa, 0.12345678)), f"kappa values not set correctly: {kappa}"
    print("test_new_hv_kappa passed")

def test_new_hv_default_kappa():
    _, kappa = new_hv(dims=4, block_size=8)
    assert np.all(kappa == 1.0), f"default kappa not 1.0: {kappa}"
    print("test_new_hv_default_kappa passed")


# -------------------------
# similarity tests
# -------------------------

def test_similarity_identical_vectors():
    # identical vectors means similarity should be 1
    hv1 = new_hv(dims=4096, block_size=128)
    sim = similarity(hv1, hv1, block_size=128)
    assert np.isclose(sim, 1.0), f"Expected 1.0, got {sim}"
    print("test_similarity_identical_vectors passed")


def test_similarity_opposite_vectors():
    # diametrically opposite vectors means similarity should be zero
    block_size = 128
    hv1 = new_hv(dims=4096, kappa=1.0, block_size=block_size)
    mu1, kappa1 = hv1
    mu2 = (mu1 + (block_size/2)) % block_size  # opposite on circle with block_size 128
    hv1 = (mu1, kappa1)
    hv2 = (mu2, kappa1)
    sim = similarity(hv1, hv2, block_size=block_size)
    assert np.all(sim == 0), f"Expected 0.0 similarity, got {sim}"
    print("test_similarity_opposite_vectors passed")


def test_similarity_zero_weight():
    # all kappa=0 means similarity should be 0
    mu1 = np.array([1, 2, 3])
    mu2 = np.array([4, 5, 6])
    kappa = np.array([0.0, 0.0, 0.0])
    hv1 = (mu1, kappa)
    hv2 = (mu2, kappa)
    sim = similarity(hv1, hv2, block_size=8)
    assert sim == 0.5, f"Expected 0.5 for zero weights, got {sim}"
    print("test_similarity_zero_weight passed")


def test_similarity_weighted_average():
    # test that certainty weighting matters
    mu1 = np.array([0, 1])
    mu2 = np.array([0, 3])
    k1 = np.array([1.0, 0.1])  # first dimension more certain
    k2 = np.array([1.0, 0.1])
    hv1 = (mu1, k1)
    hv2 = (mu2, k2)
    sim = similarity(hv1, hv2, block_size=8)
    # first dimension dominates so similarity should be close to 1
    assert sim > 0.7, f"Weighted similarity too low: {sim}"
    print("test_similarity_weighted_average passed")

# -------------------------
# bind tests
# -------------------------
def test_bind_unbind_behavior():
    dims = 4096
    block_size = 128

    a = new_hv(dims, block_size)
    b = new_hv(dims, block_size)
    noise = new_hv(dims, block_size)
    c = bind([a, b], block_size)

    sim_c_a = similarity(c, a, block_size)
    sim_c_b = similarity(c, b, block_size)
    sim_c_noise = similarity(c, noise, block_size)

    assert sim_c_a < 0.6, f"c too similar to a: {sim_c_a}"
    assert sim_c_b < 0.6, f"c too similar to b: {sim_c_b}"
    assert sim_c_noise < 0.6, f"c too similar to noise: {sim_c_noise}"

    recovered_b = unbind(c, a, block_size)
    sim_recovered_b = similarity(recovered_b, b, block_size)
    assert sim_recovered_b > 0.9, f"unbind(c, a) not similar to b: {sim_recovered_b}"

    # unbind c with b should recover a approximately
    recovered_a = unbind(c, b, block_size)
    sim_recovered_a = similarity(recovered_a, a, block_size)
    assert sim_recovered_a > 0.9, f"unbind(c, b) not similar to a: {sim_recovered_a}"

    # unbind c with noise should not be similar to a or b
    recovered_noise = unbind(c, noise, block_size)
    sim_noise_a = similarity(recovered_noise, a, block_size)
    sim_noise_b = similarity(recovered_noise, b, block_size)
    assert sim_noise_a < 0.6, f"unbind(c, noise) too similar to a: {sim_noise_a}"
    assert sim_noise_b < 0.6, f"unbind(c, noise) too similar to b: {sim_noise_b}"

    print("test_bind_unbind_behavior passed")

# -------------------------
# bundle tests
# -------------------------
def test_bundle_two_inputs_even_block():
    block_size = 8

    # Both hv blocks have the same mu
    mu = np.array([3])
    hv1 = (mu, np.array([0.0]))  # Total uncertainty
    hv2 = (mu, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2], block_size=block_size)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 1.0), f"Expected kappa=1.0, got {kappa_out[0]}"
    print("same mus kappa of 0 and 1 passed")


    # Both hv blocks have the same mu
    mu = np.array([3])
    hv1 = (mu, np.array([0.5]))  # Partial certainty
    hv2 = (mu, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2], block_size=block_size)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 1.0), f"Expected kappa=1.0, got {kappa_out[0]}"
    print("same mus kappa of 0.5 and 1 passed")


    # Both hv blocks have the same kappa but exactly opposed angles
    # [0, 1, 2, 3, 4, 5, 6, 7]
    #     *           *
    mu1 = np.array([5])
    mu2 = np.array([1])
    hv1 = (mu1, np.array([1.0])) # Total certainty
    hv2 = (mu2, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2], block_size=block_size)
    # When angles are exactly opposed all values of mu as equally likely, bundle averages them to 3 but since kappa is 0 mu is a uniform distribtuion around the circle
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 0.0), f"Expected kappa=0, got {kappa_out[0]}"
    print("opposed mus with kappa=1.0 passed")


    # Both hv blocks have the same kappa but slightly disagreeing mu
    # [0, 1, 2, 3, 4, 5, 6, 7]
    #        *     *
    mu1 = np.array([2])
    mu2 = np.array([4])
    hv1 = (mu1, np.array([1.0])) # Total certainty
    hv2 = (mu2, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2], block_size=block_size)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert kappa_out[0] > 0.5 and kappa_out[0] < 1.0, f"Expected kappa=0.75, got {kappa_out[0]}"
    print("slightly disagreeing mus with kappa=1.0 passed")


def test_bundle_three_inputs_even_block():
    # All hv blocks have the same mu
    mu = np.array([3])
    hv1 = (mu, np.array([0.0]))  # Total uncertainty
    hv2 = (mu, np.array([1.0]))  # Total certainty
    hv3 = (mu, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2, hv3], block_size=8)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 1.0), f"Expected kappa=1.0, got {kappa_out[0]}"
    print("same mus kappa of 0,1,1 passed")


    # Both hv blocks have the same mu
    mu = np.array([3])
    hv1 = (mu, np.array([0.0]))  # Total uncertainty
    hv2 = (mu, np.array([0.0]))  # Total uncertainty
    hv3 = (mu, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2, hv3], block_size=8)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 1.0), f"Expected kappa=1.0, got {kappa_out[0]}"
    print("same mus kappa of 0,0,1 passed")


    # Both hv blocks have the same kappa but approximately opposed angles
    # [0, 1, 2, 3, 4, 5, 6, 7]
    #  *        *     *
    mu1 = np.array([0])
    mu2 = np.array([3])
    mu3 = np.array([5])
    hv1 = (mu1, np.array([1.0])) # Total certainty
    hv2 = (mu2, np.array([1.0]))  # Total certainty
    hv3 = (mu3, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2, hv3], block_size=8)
    # When angles are exactly opposed all values of mu as equally likely, bundle averages them to 3 but since kappa is 0 mu is a uniform distribtuion around the circle
    assert mu_out[0] == 4, f"Expected mu=4, got {mu_out[0]}"
    assert kappa_out[0] < 0.15, f"Expected kappa=0, got {kappa_out[0]}"
    print("opposed mus with kappa=1.0 passed")


    # Both hv blocks have the same kappa but agreeing mus
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    #              *     *        *
    hv1 = (np.array([4]), np.array([1.0]))  # Total certainty
    hv2 = (np.array([6]), np.array([1.0]))  # Total certainty
    hv3 = (np.array([9]), np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2, hv3], block_size=16)
    assert mu_out[0] == 6, f"Expected mu=6 or 7, got {mu_out[0]}"
    assert kappa_out[0] > 2/3 and kappa_out[0] < 1.0, f"Expected kappa=0.75, got {kappa_out[0]}"
    print("slightly disagreeing mus with kappa=1.0 passed")


    # Both hv blocks have the same kappa but agreeing mus
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    #              *     *        *
    hv1 = (np.array([4]), np.array([0.5]))  # Partial certainty
    hv2 = (np.array([6]), np.array([0.5]))  # Partial certainty
    hv3 = (np.array([9]), np.array([0.5]))  # Partial certainty
    mu_out, kappa_out = bundle([hv1, hv2, hv3], block_size=16)
    assert mu_out[0] == 6, f"Expected mu=6, got {mu_out[0]}"
    assert kappa_out[0] > 1/2 and kappa_out[0] < 1.0, f"Expected kappa=0.75, got {kappa_out[0]}"
    print("slightly disagreeing mus with kappa=1.0 passed")


def test_bundle_two_inputs_odd_block():
    block_size = 13

    # Both hv blocks have the same mu
    mu = np.array([3])
    hv1 = (mu, np.array([0.0]))  # Total uncertainty
    hv2 = (mu, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2], block_size=block_size)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 1.0), f"Expected kappa=1.0, got {kappa_out[0]}"
    print("same mus kappa of 0 and 1 passed")


    # Both hv blocks have the same mu
    mu = np.array([3])
    hv1 = (mu, np.array([0.5]))  # Partial certainty
    hv2 = (mu, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2], block_size=block_size)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 1.0), f"Expected kappa=1.0, got {kappa_out[0]}"
    print("same mus kappa of 0.5 and 1 passed")


    # Both hv blocks have the same kappa but exactly opposed angles
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    #     *                 *
    hv1 = (np.array([7]), np.array([1.0])) # Total certainty
    hv2 = (np.array([1]), np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2], block_size=block_size)
    # When angles are exactly opposed all values of mu as equally likely, bundle averages them to 3 but since kappa is 0 mu is a uniform distribtuion around the circle
    assert mu_out[0] == 4, f"Expected mu=4, got {mu_out[0]}"
    assert kappa_out[0] < 0.15, f"Expected kappa=0, got {kappa_out[0]}"
    print("opposed mus with kappa=1.0 passed")


    # Both hv blocks have the same kappa but slightly disagreeing mu
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    #        *     *
    mu1 = np.array([2])
    mu2 = np.array([4])
    hv1 = (mu1, np.array([1.0])) # Total certainty
    hv2 = (mu2, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2], block_size=block_size)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert kappa_out[0] > 0.5 and kappa_out[0] < 1.0, f"Expected kappa=0.75, got {kappa_out[0]}"
    print("slightly disagreeing mus with kappa=1.0 passed")


def test_bundle_three_inputs_odd_block():
    # All hv blocks have the same mu
    mu = np.array([3])
    hv1 = (mu, np.array([0.0]))  # Total uncertainty
    hv2 = (mu, np.array([1.0]))  # Total certainty
    hv3 = (mu, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2, hv3], block_size=13)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 1.0), f"Expected kappa=1.0, got {kappa_out[0]}"
    print("same mus kappa of 0,1,1 passed")


    # Both hv blocks have the same mu
    mu = np.array([3])
    hv1 = (mu, np.array([0.0]))  # Total uncertainty
    hv2 = (mu, np.array([0.0]))  # Total uncertainty
    hv3 = (mu, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2, hv3], block_size=13)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 1.0), f"Expected kappa=1.0, got {kappa_out[0]}"
    print("same mus kappa of 0,0,1 passed")


    # Both hv blocks have the same kappa but approximately opposed angles
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    #  *           *           *
    mu1 = np.array([0])
    mu2 = np.array([4])
    mu3 = np.array([8])
    hv1 = (mu1, np.array([1.0])) # Total certainty
    hv2 = (mu2, np.array([1.0]))  # Total certainty
    hv3 = (mu3, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2, hv3], block_size=13)
    # When angles are exactly opposed all values of mu as equally likely, bundle averages them to 3 but since kappa is 0 mu is a uniform distribtuion around the circle
    assert mu_out[0] == 4, f"Expected mu=4, got {mu_out[0]}"
    assert kappa_out[0] < 0.1, f"Expected kappa=0, got {kappa_out[0]}"
    print("opposed mus with kappa=1.0 passed")


    # Both hv blocks have the same kappa but agreeing mus
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    #              *     *        *
    hv1 = (np.array([4]), np.array([1.0]))  # Total certainty
    hv2 = (np.array([6]), np.array([1.0]))  # Total certainty
    hv3 = (np.array([9]), np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2, hv3], block_size=17)
    assert mu_out[0] == 6, f"Expected mu=6 or 7, got {mu_out[0]}"
    assert kappa_out[0] > 2/3 and kappa_out[0] < 1.0, f"Expected kappa=0.75, got {kappa_out[0]}"
    print("slightly disagreeing mus with kappa=1.0 passed")


    # Both hv blocks have the same kappa and partially agreeing mus
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    #              *     *        *
    hv1 = (np.array([4]), np.array([0.5]))  # Partial certainty
    hv2 = (np.array([6]), np.array([0.5]))  # Partial certainty
    hv3 = (np.array([9]), np.array([0.5]))  # Partial certainty
    mu_out, kappa_out = bundle([hv1, hv2, hv3], block_size=17)
    assert mu_out[0] == 6, f"Expected mu=6 or 7, got {mu_out[0]}"
    assert kappa_out[0] > 1/2 and kappa_out[0] < 1.0, f"Expected kappa=0.75, got {kappa_out[0]}"
    print("slightly disagreeing mus with kappa=1.0 passed")


# -------------------------
# Run all tests
# -------------------------

if __name__ == "__main__":
    test_new_hv_shape()
    test_new_hv_range()
    test_new_hv_kappa()
    test_new_hv_default_kappa()

    test_similarity_identical_vectors()
    test_similarity_opposite_vectors()
    test_similarity_zero_weight()
    test_similarity_weighted_average()

    test_bind_unbind_behavior()

    test_bundle_two_inputs_even_block()
    test_bundle_three_inputs_even_block()
    test_bundle_two_inputs_odd_block()
    test_bundle_three_inputs_odd_block()

    print("All tests passed ✅")
