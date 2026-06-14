import numpy as np


# -----------------------------
# utilities
# -----------------------------

def normalize(q):
    return q / np.linalg.norm(q, axis=-1, keepdims=True)


def to_variance(kappa, eps=1e-8):
    kappa = np.clip(kappa, eps, 1.0)
    return (1.0 / kappa) - 1.0


def to_kappa(var):
    return 1.0 / (1.0 + var)


# -----------------------------
# new hypervector
# -----------------------------

def new_hv(D, kappa=1.0):
    q = np.random.randn(D, 4)
    q = normalize(q)
    k = np.full((D,), kappa)
    return q, k


# -----------------------------
# quaternion binding
# -----------------------------

def quat_mul(q1, q2):
    w1,x1,y1,z1 = np.split(q1, 4, axis=-1)
    w2,x2,y2,z2 = np.split(q2, 4, axis=-1)

    return np.concatenate([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ], axis=-1)


def bind(h1, h2):
    q1,k1 = h1
    q2,k2 = h2

    q = normalize(quat_mul(q1, q2))

    var = to_variance(k1) + to_variance(k2)
    k = to_kappa(var)

    return q, k


def unbind(bound, query):
    q_b,k_b = bound
    q_q,k_q = query

    q_inv = q_q.copy()
    q_inv[...,1:] *= -1

    q = normalize(quat_mul(q_inv, q_b))

    var = to_variance(k_b) + to_variance(k_q)
    k = to_kappa(var)

    return q, k


# -----------------------------
# Bingham-inspired bundling
# -----------------------------

def bundle(hvs):
    qs = np.stack([h[0] for h in hvs], axis=0)
    ks = np.stack([h[1] for h in hvs], axis=0)

    # weighted resultant
    r = np.sum(qs * ks[..., None], axis=0)

    norm = np.linalg.norm(r, axis=-1, keepdims=True)
    mu = r / (norm + 1e-12)

    # Bingham-like concentration proxy
    kappa = np.squeeze(norm) / (np.sum(ks, axis=0) + 1e-12)

    return mu, kappa