import matplotlib.pyplot as plt
import numpy as np

from utils import hdv, cossim, clip

from utils import bundle, partial_bundle
from utils import iterative_bundle, partial_iterative
from utils import randsel_bundle, partial_randsel
from utils import normal_dist_bundle, partial_normal_dist

bundlers = {
  "sum": bundle,
  "sum_partial_25%": partial_bundle(0.25),
  "sum_partial_50%": partial_bundle(0.50),
  "sum_partial_75%": partial_bundle(0.75),

  "iterative": iterative_bundle,
  "iterative_partial_25%": partial_iterative(0.25),
  "iterative_partial_50%": partial_iterative(0.50),
  "iterative_partial_75%": partial_iterative(0.75),

  "randsel": randsel_bundle,
  "randsel_partial_25%": partial_randsel(0.25),
  "randsel_partial_50%": partial_randsel(0.50),
  "randsel_partial_75%": partial_randsel(0.75),

  "noisy_normal": normal_dist_bundle,
  "noisy_normal_partial_25%": partial_normal_dist(0.25),
  "noisy_normal_partial_50%": partial_normal_dist(0.50),
  "noisy_normal_partial_75%": partial_normal_dist(0.75),
}

shapes = {
  "sum": "o",
  "sum_partial_25%": "o",
  "sum_partial_50%": "o",
  "sum_partial_75%": "o",

  "iterative": "X",
  "iterative_partial_25%": "X",
  "iterative_partial_50%": "X",
  "iterative_partial_75%": "X",

  "randsel": "D",
  "randsel_partial_25%": "D",
  "randsel_partial_50%": "D",
  "randsel_partial_75%": "D",

  "noisy_normal": "s",
  "noisy_normal_partial_25%": "s",
  "noisy_normal_partial_50%": "s",
  "noisy_normal_partial_75%": "s",
}

Ns = [10, 20, 30, 40, 50]
trials = 20

results = {name: [] for name in bundlers}

for N in Ns:
  for name, fn in bundlers.items():
    print('bundle: ', name, ' constituent count:', N)
    sims = []
    noise_sims = []

    for _ in range(trials):
      signals = [hdv() for _ in range(N)]
      noise = hdv()

      acc = fn(*signals)

      sims.append(np.mean([cossim(hv, acc) for hv in signals]))
      noise_sims.append(cossim(noise, acc))

    results[name].append((
      np.mean(sims),
      np.mean(noise_sims)
    ))

# -----------------------
# Plotting
# -----------------------

plt.figure(figsize=(10, 6))

for name, vals in results.items():
  plt.plot(
    Ns,
    [v[0] for v in vals],
    marker=shapes[name],
    label=name,
    alpha=0.70
  )

plt.yscale('log')
plt.xlabel("Number of bundled signals")
plt.ylabel("Mean cosine similarity to constituents")
plt.title("Bundling strength vs number of signals")
plt.legend()
plt.grid(True)
plt.savefig('./capacity.png')
plt.show()


plt.figure(figsize=(10, 6))

for name, vals in results.items():
  plt.plot(
    Ns,
    [v[1] for v in vals],
    marker=shapes[name],
    label=name
  )

plt.xlabel("Number of bundled signals")
plt.ylabel("Cosine similarity to noise")
plt.title("Noise leakage vs number of signals (average over {trials} runs)")
plt.legend()
plt.grid(True)
plt.savefig('./noise.png')
plt.show()
