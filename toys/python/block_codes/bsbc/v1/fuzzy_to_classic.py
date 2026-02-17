import math
import random
from collections import Counter
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Shared utilities
# ============================================================

def circular_distance(a: int, b: int, modulus: int) -> int:
    d = abs(a - b)
    return min(d, modulus - d)


# ============================================================
# Classic BSBC
# ============================================================

BSBCHV = List[int]


def random_bsbc_hv(num_blocks: int, block_size: int) -> BSBCHV:
    return [random.randrange(block_size) for _ in range(num_blocks)]


def bind_bsbc(*hvs: BSBCHV, block_size: int) -> BSBCHV:
    num_blocks = len(hvs[0])
    return [
        sum(hv[i] for hv in hvs) % block_size
        for i in range(num_blocks)
    ]


def bundle_bsbc_with_ties(
    *hvs: BSBCHV,
    block_size: int,
) -> Tuple[BSBCHV, float]:
    """
    Returns:
      bundled_hv
      tie_rate = fraction of blocks with multiple WTA modes
    """
    num_blocks = len(hvs[0])
    bundled = []
    tie_count = 0

    for i in range(num_blocks):
        indices = [hv[i] for hv in hvs]
        counts = Counter(indices)
        max_count = max(counts.values())
        modes = [idx for idx, c in counts.items() if c == max_count]

        if len(modes) > 1:
            tie_count += 1

        bundled.append(random.choice(modes))

    tie_rate = tie_count / num_blocks
    return bundled, tie_rate


def similarity_bsbc(hv1: BSBCHV, hv2: BSBCHV, block_size: int) -> float:
    total_error = sum(
        circular_distance(a, b, block_size)
        for a, b in zip(hv1, hv2)
    )
    max_error = len(hv1) * (block_size // 2)
    return 1.0 - (total_error / max_error)


def inverse_bsbc(hv: BSBCHV, block_size: int) -> BSBCHV:
    return [(-x) % block_size for x in hv]


# ============================================================
# Fuzzy BSBC
# ============================================================

FuzzyBlock = Tuple[int, float]
FuzzyHV = List[FuzzyBlock]


def random_fuzzy_hv(
    num_blocks: int,
    block_size: int,
    sigma_init: float = 1.5,
) -> FuzzyHV:
    return [(random.randrange(block_size), sigma_init)
            for _ in range(num_blocks)]


def bind_fuzzy(*hvs: FuzzyHV, block_size: int) -> FuzzyHV:
    num_blocks = len(hvs[0])
    out = []
    for i in range(num_blocks):
        mu = sum(hv[i][0] for hv in hvs) % block_size
        sigma = math.sqrt(sum(hv[i][1] ** 2 for hv in hvs))
        out.append((mu, sigma))
    return out


def bundle_fuzzy(*hvs: FuzzyHV, block_size: int) -> Tuple[FuzzyHV, float]:
    """
    Returns:
      bundled_hv
      mean_sigma
    """
    num_blocks = len(hvs[0])
    bundled = []
    sigmas_out = []

    for i in range(num_blocks):
        mus = np.array([hv[i][0] for hv in hvs], dtype=float)
        sigmas = np.array([hv[i][1] for hv in hvs], dtype=float)

        angles = mus * 2 * math.pi / block_size
        mean_angle = math.atan2(
            np.mean(np.sin(angles)),
            np.mean(np.cos(angles)),
        )
        mu = int((mean_angle * block_size / (2 * math.pi)) % block_size)

        dispersion = np.mean([
            circular_distance(mu, int(m), block_size) ** 2
            for m in mus
        ])
        sigma = math.sqrt(np.mean(sigmas ** 2) + dispersion)

        bundled.append((mu, sigma))
        sigmas_out.append(sigma)

    return bundled, float(np.mean(sigmas_out))


def similarity_fuzzy(
    hv1: FuzzyHV,
    hv2: FuzzyHV,
    block_size: int,
    eps: float = 1e-6,
) -> float:
    sims = []
    for (m1, s1), (m2, s2) in zip(hv1, hv2):
        d = circular_distance(m1, m2, block_size)
        scale = s1 + s2 + eps
        sims.append(math.exp(-(d ** 2) / (2 * scale ** 2)))
    return float(sum(sims) / len(sims))


def inverse_fuzzy(hv: FuzzyHV, block_size: int) -> FuzzyHV:
    return [((-mu) % block_size, sigma) for mu, sigma in hv]


# ============================================================
# Cleanup memories
# ============================================================

def cleanup_bsbc(
    query: BSBCHV,
    dictionary: List[BSBCHV],
    block_size: int,
) -> int:
    sims = [
        similarity_bsbc(query, hv, block_size)
        for hv in dictionary
    ]
    return max(range(len(sims)), key=sims.__getitem__)


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
# Superposition benchmark
# ============================================================

def run_superposition_benchmark(
    max_K: int,
    trials_per_K: int,
    num_blocks: int,
    block_size: int,
):
    Ks = []
    acc_bsbc = []
    acc_fuzzy = []
    tie_rates = []
    mean_sigmas = []

    for K in range(1, max_K + 1):
        bsbc_hits = 0
        fuzzy_hits = 0
        tie_acc = []
        sigma_acc = []

        for _ in range(trials_per_K):
            symbols_bsbc = [
                random_bsbc_hv(num_blocks, block_size)
                for _ in range(K + 20)
            ]
            symbols_fuzzy = [
                random_fuzzy_hv(num_blocks, block_size)
                for _ in range(K + 20)
            ]

            mem_bsbc, tie_rate = bundle_bsbc_with_ties(
                *symbols_bsbc[:K], block_size=block_size
            )
            mem_fuzzy, mean_sigma = bundle_fuzzy(
                *symbols_fuzzy[:K], block_size=block_size
            )

            target = random.randrange(K)

            sims_bsbc = [
                similarity_bsbc(mem_bsbc, hv, block_size)
                for hv in symbols_bsbc
            ]
            sims_fuzzy = [
                similarity_fuzzy(mem_fuzzy, hv, block_size)
                for hv in symbols_fuzzy
            ]

            bsbc_hits += int(
                max(range(len(sims_bsbc)), key=sims_bsbc.__getitem__) == target
            )
            fuzzy_hits += int(
                max(range(len(sims_fuzzy)), key=sims_fuzzy.__getitem__) == target
            )

            tie_acc.append(tie_rate)
            sigma_acc.append(mean_sigma)

        Ks.append(K)
        acc_bsbc.append(bsbc_hits / trials_per_K)
        acc_fuzzy.append(fuzzy_hits / trials_per_K)
        tie_rates.append(float(np.mean(tie_acc)))
        mean_sigmas.append(float(np.mean(sigma_acc)))

    return Ks, acc_bsbc, acc_fuzzy, tie_rates, mean_sigmas


# ============================================================
# Binding / unbinding benchmark
# ============================================================

def binding_trial(
    K: int,
    num_blocks: int,
    block_size: int,
):
    roles_bsbc = [random_bsbc_hv(num_blocks, block_size) for _ in range(K)]
    fillers_bsbc = [random_bsbc_hv(num_blocks, block_size) for _ in range(K)]

    roles_fuzzy = [random_fuzzy_hv(num_blocks, block_size) for _ in range(K)]
    fillers_fuzzy = [random_fuzzy_hv(num_blocks, block_size) for _ in range(K)]

    bound_bsbc = [
        bind_bsbc(roles_bsbc[i], fillers_bsbc[i], block_size=block_size)
        for i in range(K)
    ]
    bound_fuzzy = [
        bind_fuzzy(roles_fuzzy[i], fillers_fuzzy[i], block_size=block_size)
        for i in range(K)
    ]

    mem_bsbc, _ = bundle_bsbc_with_ties(*bound_bsbc, block_size=block_size)
    mem_fuzzy, _ = bundle_fuzzy(*bound_fuzzy, block_size=block_size)

    j = random.randrange(K)

    q_bsbc = bind_bsbc(
        mem_bsbc,
        inverse_bsbc(roles_bsbc[j], block_size),
        block_size=block_size,
    )
    q_fuzzy = bind_fuzzy(
        mem_fuzzy,
        inverse_fuzzy(roles_fuzzy[j], block_size),
        block_size=block_size,
    )

    mean_sigma_unbind = float(np.mean([s for _, s in q_fuzzy]))

    raw_bsbc = cleanup_bsbc(q_bsbc, fillers_bsbc, block_size) == j
    raw_fuzzy = cleanup_fuzzy(q_fuzzy, fillers_fuzzy, block_size) == j

    return raw_bsbc, raw_fuzzy, mean_sigma_unbind


def binding_benchmark(
    steps: List[int],
    trials_per_K: int,
    num_blocks: int,
    block_size: int,
):
    Ks = []
    acc_bsbc = []
    acc_fuzzy = []
    sigmas = []

    for K in steps:
        hits_bsbc = 0
        hits_fuzzy = 0
        sigma_acc = []

        for _ in range(trials_per_K):
            b_ok, f_ok, sigma = binding_trial(
                K,
                num_blocks,
                block_size,
            )
            hits_bsbc += int(b_ok)
            hits_fuzzy += int(f_ok)
            sigma_acc.append(sigma)

        Ks.append(K)
        acc_bsbc.append(hits_bsbc / trials_per_K)
        acc_fuzzy.append(hits_fuzzy / trials_per_K)
        sigmas.append(float(np.mean(sigma_acc)))

    return Ks, acc_bsbc, acc_fuzzy, sigmas


# ============================================================
# Plotting
# ============================================================

def plot_superposition_results(Ks, acc_bsbc, acc_fuzzy, tie_rates, mean_sigmas):
    fig, axes = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

    axes[0].plot(Ks, acc_bsbc, label="Classic BSBC", marker="o")
    axes[0].plot(Ks, acc_fuzzy, label="Fuzzy BSBC", marker="o")
    axes[0].set_ylabel("Retrieval accuracy")
    axes[0].set_title("Superposition capacity")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(Ks, tie_rates, color="red")
    axes[1].set_ylabel("Tie rate per block")
    axes[1].set_title("Implicit uncertainty (Classic BSBC)")
    axes[1].grid(True)

    axes[2].plot(Ks, mean_sigmas, color="green")
    axes[2].set_ylabel("Mean σ")
    axes[2].set_xlabel("Number of bundled items (K)")
    axes[2].set_title("Explicit uncertainty (Fuzzy BSBC)")
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig("./plot_superposition.png")
    plt.show()


def plot_binding_results(Ks, acc_bsbc, acc_fuzzy, sigmas):
    fig, axes = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

    axes[0].plot(Ks, acc_bsbc, label="Classic BSBC", marker="o")
    axes[0].plot(Ks, acc_fuzzy, label="Fuzzy BSBC", marker="o")
    axes[0].set_ylabel("Unbinding accuracy")
    axes[0].set_title("Binding / Unbinding Capacity")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(Ks, sigmas, color="green")
    axes[1].set_ylabel("Mean σ after unbinding")
    axes[1].set_xlabel("Number of bound pairs (K)")
    axes[1].set_title("Explicit uncertainty during factorization")
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig("./plot_binding.png")
    plt.show()


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    random.seed(0)
    np.random.seed(0)

    Ks_s, acc_bsbc_s, acc_fuzzy_s, tie_rates, mean_sigmas = run_superposition_benchmark(
        max_K=50,
        trials_per_K=50,
        num_blocks=4096,
        block_size=64,
    )

    plot_superposition_results(
        Ks_s, acc_bsbc_s, acc_fuzzy_s, tie_rates, mean_sigmas
    )

    Ks_b, acc_bsbc_b, acc_fuzzy_b, sigmas = binding_benchmark(
        steps=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 200, 300, 500],
        trials_per_K=20,
        num_blocks=4096,
        block_size=64,
    )

    plot_binding_results(Ks_b, acc_bsbc_b, acc_fuzzy_b, sigmas)
