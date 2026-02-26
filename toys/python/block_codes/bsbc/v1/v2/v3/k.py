import numpy as np
from utils import *


def kuramoto_bind(hvs, block_size, steps=10, dt=0.1, coupling=1.0, phase_offset=np.pi/2):
    """
    Kuramoto-based binding for CNR.

    Complexity: O(ND)

    hvs: list of (mu, kappa)
    """

    mus = np.stack([hv[0] for hv in hvs])
    kappas = np.stack([hv[1] for hv in hvs])

    # convert to radians
    theta = 2 * np.pi * mus / block_size

    for _ in range(steps):

        # κ-weighted phasor mean
        phasors = kappas * np.exp(1j * theta)

        mean_phasor = np.sum(phasors, axis=0)

        psi = np.angle(mean_phasor)
        r = np.abs(mean_phasor) / (np.sum(kappas, axis=0) + 1e-12)

        # broadcast update
        theta += dt * coupling * r * np.sin(
            psi - theta + phase_offset
        )

    # extract resulting phase
    phasors = np.exp(1j * theta)
    mean = np.mean(phasors, axis=0)

    mean_angle = np.angle(mean)

    mu = np.mod(
        np.floor(mean_angle * block_size / (2*np.pi) + 0.5),
        block_size
    ).astype(int)

    # synchronization strength
    kappa = np.abs(mean)

    return mu, kappa


def rotate(hv, shift, block):
    mu, kappa = hv
    return (mu + shift) % block, kappa




dims = 1024
block = 64

A = new_hv(dims, block)
B = new_hv(dims, block)
C = new_hv(dims, block)

seq = bundle([
    kuramoto_bind([A, rotate(B, 1, block)], block),
    kuramoto_bind([B, rotate(C, 1, block)], block)
], block)

query = kuramoto_bind([inverse(A, block), seq], block)

prediction = rotate(query, -1, block)
print(similarity(prediction, B, block))
print(similarity(prediction, C, block))
