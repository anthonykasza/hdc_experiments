import numpy as np

from cnr import *


# -------------------------
# idx_to_angle tests
# -------------------------

def test_idx_to_angle_basic():
    block_size = 8

    assert idx_to_angle(0, block_size) == 0.0
    assert idx_to_angle(block_size, block_size) == 2 * np.pi

    print("test_idx_to_angle_basic passed")


def test_idx_to_angle_step_size():
    block_size = 16

    step = idx_to_angle(1, block_size) - idx_to_angle(0, block_size)
    expected = 2 * np.pi / block_size

    assert np.isclose(step, expected)

    print("test_idx_to_angle_step_size passed")


# -------------------------
# angle_to_idx tests
# -------------------------

def test_angle_to_idx_basic():
    block_size = 8

    assert angle_to_idx(0.0, block_size) == 0
    assert angle_to_idx(2 * np.pi, block_size) == 0  # wraparound

    print("test_angle_to_idx_basic passed")


def test_angle_to_idx_round_trip():
    block_size = 16

    for mu in range(block_size):
        theta = idx_to_angle(mu, block_size)
        mu2 = angle_to_idx(theta, block_size)
        assert mu2 == mu, f"round-trip failed for mu={mu}"

    print("test_angle_to_idx_round_trip passed")


def test_angle_to_idx_exact_halfway():
    """
    Exactly halfway between two block centers should round up.
    """
    block_size = 8

    mu = 2
    theta_a = idx_to_angle(mu, block_size)
    theta_b = idx_to_angle(mu + 1, block_size)
    theta_half = 0.5 * (theta_a + theta_b)

    idx = angle_to_idx(theta_half, block_size)

    assert idx == mu + 1, f"expected {mu + 1}, got {idx}"

    print("test_angle_to_idx_exact_halfway passed")


def test_angle_to_idx_halfway_wraparound():
    """
    Halfway between last index and 0 should map to 0.
    """
    block_size = 8

    theta_last = idx_to_angle(block_size - 1, block_size)
    theta_zero = 2 * np.pi
    theta_half = 0.5 * (theta_last + theta_zero)

    idx = angle_to_idx(theta_half, block_size)

    assert idx == 7, f"expected 0, got {idx}"

    print("test_angle_to_idx_halfway_wraparound passed")


# -------------------------
# to_phasor tests
# -------------------------

def test_to_phasor_zero_mu():
    block_size = 8
    kappa = 2.5

    z = to_phasor(0, kappa, block_size)

    assert np.isclose(z, kappa + 0j)

    print("test_to_phasor_zero_mu passed")


def test_to_phasor_magnitude():
    block_size = 8
    kappa = 3.0

    for mu in range(block_size):
        z = to_phasor(mu, kappa, block_size)
        assert np.isclose(np.abs(z), kappa)

    print("test_to_phasor_magnitude passed")


def test_to_phasor_angle():
    block_size = 16
    kappa = 1.0
    mu = 5

    z = to_phasor(mu, kappa, block_size)
    expected = np.exp(1j * idx_to_angle(mu, block_size))

    assert np.allclose(z, expected)
    print("test_to_phasor_angle passed")


# -------------------------
# new_hv tests
# -------------------------

def test_new_hv_shape():
    mu, kappa = new_hv(4, 8)
    assert mu.shape == (4,), f"Expected mu shape (4,), got {mu.shape}"
    assert kappa.shape == (4,), f"Expected kappa shape (4,), got {kappa.shape}"
    print("test_new_hv_shape passed")

def test_new_hv_range():
    mu, _ = new_hv(4, 8, rng=42)
    assert np.all((mu >= 0) & (mu < 8)), f"mu values out of range: {mu}"
    print("test_new_hv_range passed")

def test_new_hv_kappa():
    _, kappa = new_hv(4, 8, kappa=5)
    assert np.all(kappa == 5), f"kappa values not set correctly: {kappa}"
    print("test_new_hv_kappa passed")

def test_new_hv_default_kappa():
    _, kappa = new_hv(4, 8)
    assert np.all(kappa == 1.0), f"default kappa not 1.0: {kappa}"
    print("test_new_hv_default_kappa passed")


# -------------------------
# similarity tests
# -------------------------

def test_similarity_identical_vectors():
    # identical vectors means similarity should be 1
    mu = np.array([0, 2, 5])
    kappa = np.array([1.0, 0.5, 2.0])
    hv1 = (mu, kappa)
    hv2 = (mu, kappa)
    sim = similarity(hv1, hv2, block_size=8)
    assert np.isclose(sim, 1.0), f"Expected 1.0, got {sim}"
    print("test_similarity_identical_vectors passed")


def test_similarity_opposite_vectors():
    # diametrically opposite vectors means similarity should be negative
    mu1 = np.array([0, 2, 4])
    mu2 = (mu1 + 4) % 8  # opposite on circle with block_size 8
    kappa = np.array([1.0, 1.0, 1.0])
    hv1 = (mu1, kappa)
    hv2 = (mu2, kappa)
    sim = similarity(hv1, hv2, block_size=8)
    assert np.all(sim <= 0), f"Expected non-positive similarity, got {sim}"
    print("test_similarity_opposite_vectors passed")


def test_similarity_zero_weight():
    # all kappa=0 means similarity should be 0
    mu1 = np.array([1, 2, 3])
    mu2 = np.array([4, 5, 6])
    kappa = np.array([0.0, 0.0, 0.0])
    hv1 = (mu1, kappa)
    hv2 = (mu2, kappa)
    sim = similarity(hv1, hv2, block_size=8)
    assert sim == 0.0, f"Expected 0.0 for zero weights, got {sim}"
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
    # first dimension dominates means similarity close to 1
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
    c = bind(a, b, block_size)

    sim_c_a = similarity(c, a, block_size)
    sim_c_b = similarity(c, b, block_size)
    sim_c_noise = similarity(c, noise, block_size)

    assert sim_c_a < 0.6, f"c too similar to a: {sim_c_a}"
    assert sim_c_b < 0.6, f"c too similar to b: {sim_c_b}"
    assert sim_c_noise < 0.6, f"c too similar to noise: {sim_c_noise}"

    recovered_b = unbind(c, a, block_size)
    sim_recovered_b = similarity(recovered_b, b, block_size)
    assert sim_recovered_b > 0.9, f"unbind(c, a) not similar to b: {sim_recovered_b}"

    # unbind c with b → should recover a approximately
    recovered_a = unbind(c, b, block_size)
    sim_recovered_a = similarity(recovered_a, a, block_size)
    assert sim_recovered_a > 0.9, f"unbind(c, b) not similar to a: {sim_recovered_a}"

    # unbind c with noise → should not be similar to a or b
    recovered_noise = unbind(c, noise, block_size)
    sim_noise_a = similarity(recovered_noise, a, block_size)
    sim_noise_b = similarity(recovered_noise, b, block_size)
    assert sim_noise_a < 0.6, f"unbind(c, noise) too similar to a: {sim_noise_a}"
    assert sim_noise_b < 0.6, f"unbind(c, noise) too similar to b: {sim_noise_b}"

    print("test_bind_unbind_behavior passed")

# -------------------------
# bundle tests
# -------------------------
def test_bundle():
    block_size = 8

    # Both hv blocks have the same mu
    mu = np.array([3])
    hv1 = (mu, np.array([0.0]))  # Total uncertainty
    hv2 = (mu, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2], block_size=block_size)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 0.5), f"Expected kappa=0.5, got {kappa_out[0]}"
    print("same mus kappa of 0 and 1 passed")


    # Both hv blocks have the same mu
    mu = np.array([3])
    hv1 = (mu, np.array([0.5]))  # Partial certainty
    hv2 = (mu, np.array([1.0]))  # Total certainty
    mu_out, kappa_out = bundle([hv1, hv2], block_size=block_size)
    assert mu_out[0] == 3, f"Expected mu=3, got {mu_out[0]}"
    assert np.isclose(kappa_out[0], 0.75), f"Expected kappa=0.75, got {kappa_out[0]}"
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


# -------------------------
# Run all tests
# -------------------------

if __name__ == "__main__":
    test_idx_to_angle_basic()
    test_idx_to_angle_step_size()

    test_angle_to_idx_basic()
    test_angle_to_idx_round_trip()
    test_angle_to_idx_exact_halfway()
    test_angle_to_idx_halfway_wraparound()

    test_to_phasor_zero_mu()
    test_to_phasor_magnitude()
    test_to_phasor_angle()

    test_new_hv_shape()
    test_new_hv_range()
    test_new_hv_kappa()
    test_new_hv_default_kappa()

    test_similarity_identical_vectors()
    test_similarity_opposite_vectors()
    test_similarity_zero_weight()
    test_similarity_weighted_average()

    test_bind_unbind_behavior()

    test_bundle()

    print("All tests passed ✅")
