import numpy as np
import matplotlib.pyplot as plt

from cnr import new_hv, bundle, similarity


# -------------------------
# Experiment parameters
# -------------------------
configs = [
    (3, 1024),
    (3, 512),
    (3, 128),
    (1024, 64),
    (1024, 128),
    (1024, 256),
    (4096, 64),
    (4096, 128),
    (4096, 256),
    (4096, 512),
]

ks = [2, 4, 8, 16, 32, 64, 128, 256, 512]
n_trials = 20
base_rng = 42


# -------------------------
# Visual encodings
# -------------------------
dims_colors = {
    3: "tab:orange",
    1024: "tab:blue",
    4096: "tab:green",
}

block_markers = {
    64: "o",
    128: "s",
    256: "^",
    512: "D",
    1024: "X",
}


# -------------------------
# Run experiment
# -------------------------
results = {}

for dims, block_size in configs:
    cap_means = []
    cap_stds = []

    for k in ks:
        caps = []

        for trial in range(n_trials):
            hvs = [
                new_hv(
                    dims,
                    block_size,
                    rng=base_rng + trial * 100000 + i
                )
                for i in range(k)
            ]

            bundled = bundle(hvs, block_size)

            # signal
            signal_sims = [
                similarity(bundled, hv, block_size)
                for hv in hvs
            ]

            # noise
            noise_hv = new_hv(
                dims, block_size,
                rng=base_rng + 999999 + trial
            )
            noise_sim = similarity(bundled, noise_hv, block_size)

            caps.append(np.mean(signal_sims) - noise_sim)

        cap_means.append(np.mean(caps))
        cap_stds.append(np.std(caps))

    results[(dims, block_size)] = (
        np.array(cap_means),
        np.array(cap_stds),
    )


# -------------------------
# Plot with variance bands
# -------------------------
plt.figure(figsize=(10, 6))

for (dims, block_size), (means, stds) in results.items():
    color = dims_colors[dims]
    marker = block_markers[block_size]

    plt.plot(
        ks,
        means,
        color=color,
        marker=marker,
        linewidth=2,
        markersize=6,
        alpha=0.7,
        label=f"dims={dims}, block={block_size}",
    )

    plt.fill_between(
        ks,
        means - stds,
        means + stds,
        color=color,
        alpha=0.15,
    )

plt.xscale("log", base=2)
plt.xlabel("Number of bundled hypervectors (k)")
plt.ylabel("Signal − Noise similarity")
plt.title("Bundling Capacity with Variance Bands (CNR)")

plt.axhline(0.0, color="black", linestyle="--", linewidth=1)
plt.grid(True, which="both", linestyle="--", alpha=0.5)

plt.legend(fontsize=9, ncol=2)
plt.tight_layout()
plt.show()
