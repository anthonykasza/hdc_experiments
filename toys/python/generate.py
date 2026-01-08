import numpy as np
import matplotlib.pyplot as plt

def _snap(samples, r):
    r = np.asarray(r)
    return r[np.argmin(np.abs(samples[:, None] - r[None, :]), axis=1)]

def hdv_uniform(n=10_000, r=[1, -1]):
    return np.random.choice(r, size=n)

def hdv_normal(n=10_000, r=[1, -1]):
    mu = np.mean(r)
    sigma = np.std(r)
    samples = np.random.normal(loc=mu, scale=sigma, size=n)
    return _snap(samples, r)

def hdv_power(n=10_000, r=[1, -1], a=1.0):
    samples = np.random.power(a, size=n)
    return _snap(samples, r)

def hdv_exponential(n=10_000, r=[1, -1], scale=1.0):
    samples = np.random.exponential(scale=scale, size=n)
    return _snap(samples, r)

def hdv_poisson(n=10_000, r=[1, -1], lam=1.0):
    samples = np.random.poisson(lam=lam, size=n)
    return _snap(samples, r)

def count_values(hvs, r):
    counts = {v: 0 for v in r}
    for hv in hvs:
        vals, freqs = np.unique(hv, return_counts=True)
        for v, f in zip(vals, freqs):
            counts[v] += f
    return counts

# symetric, no 0
# symetric, yes 0
# non-symetric, no 0
# non-symetric, yes 0
element_ranges = [
    [-1, 1],
    [-1, 0, 1],
    [-2, 1],
    [-2, 0, 1],

    [-2, -1, 1, 2],
    [-2, -1, 0, 1, 2],
    [-2, -1, 1],
    [-2, -1, 0, 1],

    [x for x in range(-10, 0)] + [x for x in range(1, 11)],
    [x for x in range(-10, 0)] + [0] + [x for x in range(1, 11)],
    [x for x in range(-10, 0)] + [1],
    [x for x in range(-10, 0)] + [0, 1]
]

trials = 100
dims = 10_000
hv_count = 10

hdv_fns = {
    "uniform": hdv_uniform,
    "normal": hdv_normal,
    "power": hdv_power,
    "exponential": hdv_exponential,
    "poisson": hdv_poisson,
}

# Calculate total number of subplots
n_rows = len(element_ranges)
n_cols = len(hdv_fns)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 4 * n_rows), sharey=True)
fig.suptitle("Value frequencies for all element ranges and distributions", fontsize=16)

for row_idx, r in enumerate(element_ranges):
    avg_counts = {name: {v: 0 for v in r} for name in hdv_fns}

    for _ in range(trials):
        for name, fn in hdv_fns.items():
            hvs = [fn(n=dims, r=r) for _ in range(hv_count)]
            counts = count_values(hvs, r)
            for v in r:
                avg_counts[name][v] += counts[v]

    total = trials * hv_count * dims

    for col_idx, (name, counts) in enumerate(avg_counts.items()):
        ax = axes[row_idx, col_idx] if n_rows > 1 else axes[col_idx]
        freqs = [counts[v] / total for v in r]
        ax.bar([str(v) for v in r], freqs)
        ax.set_title(name)
        ax.set_ylim(0, 1)
        if col_idx == 0:
            ax.set_ylabel(f"r = {r}\nFrequency")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('./generate.png')
plt.show()
