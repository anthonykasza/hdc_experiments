import numpy as np

# -----------------------------
# Utilities
# -----------------------------

def idx_to_angle(mu, block_size):
    """Block index to angle on a circle (radians)"""
    return 2 * np.pi * mu / block_size


def angle_to_idx(theta, block_size):
    """Angle on a circle rounded to a block index"""
    x = block_size * theta / (2 * np.pi)
    return np.mod(np.floor(x + 0.5), block_size).astype(int)


def idx_to_phasor(mu, kappa, block_size):
    """Block index to a complex phasor"""
    theta = idx_to_angle(mu, block_size)
    return kappa * np.exp(1j * theta)


# -----------------------------
# Hypervector creation
# -----------------------------

def new_hv(dims, block_size, kappa=1.0, rng=None):
    """Create a new random hypervector."""
    rng = np.random.default_rng(rng)
    mu = rng.integers(0, block_size, size=dims)
    kappa_arr = np.full(dims, kappa, dtype=float)
    return mu, kappa_arr


# -----------------------------
# Binding / Unbinding
# -----------------------------

def bind(hvs, block_size):
    """Modulo sum"""
    mus = np.stack([hv[0] for hv in hvs], axis=0)
    kappas = np.stack([hv[1] for hv in hvs], axis=0)
    mu = np.mod(np.sum(mus, axis=0), block_size)
    # uncertainty propagates like zero in multiplication
    kappa = np.min(kappas, axis=0)
    return mu, kappa

def unbind(hv, key, block_size):
    """Modulo substraction"""
    mu, k = hv
    mu_k, k_k = key
    # uncertainty propagates like zero in multiplication
    kappa = np.minimum(k, k_k)
    mu_out = (mu - mu_k) % block_size
    return mu_out, kappa

def inverse(hv, block_size):
    """Inverse a hypervector"""
    mu, kappa = hv
    return (-mu) % block_size, kappa

# -----------------------------
# Bundling (von Mises fusion)
# -----------------------------

def bundle(hvs, block_size, noise_thresh=None):
    """Bundle multiple hypervectors using von Mises fusion."""
    mus = np.stack([hv[0] for hv in hvs], axis=0)
    kappas = np.stack([hv[1] for hv in hvs], axis=0)
    phasors = idx_to_phasor(mus, kappas, block_size)
    z = np.sum(phasors, axis=0)
    theta = np.angle(z)
    mu = angle_to_idx(theta, block_size)
    kappa = np.abs(z) / len(kappas) # a block's max kappa is 1.0

    if noise_thresh and kappa < noise_thresh:
      mu = np.random.randint(block_size)
      kappa = 0
    return mu, kappa


# -----------------------------
# Similarity
# -----------------------------

def similarity(hv1, hv2, block_size):
    """Certainty-weighted circular similarity in [0, 1]."""
    mu1, k1 = hv1
    mu2, k2 = hv2

    theta1 = idx_to_angle(mu1, block_size)
    theta2 = idx_to_angle(mu2, block_size)

    # circular distance
    d = np.cos(theta1 - theta2)

    # certainty-weighted agreement
    w = np.minimum(k1, k2)

    if np.all(w == 0):
        return 0.0
    sim = np.sum(w * d) / np.sum(w)  # in [-1, 1]
    sim = 0.5 * (sim + 1.0)          # rescale to [0, 1]
    return sim


