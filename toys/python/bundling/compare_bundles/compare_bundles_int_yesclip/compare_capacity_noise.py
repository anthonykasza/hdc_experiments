import matplotlib.pyplot as plt
import numpy as np

from utils import hdv, cossim, clip

from utils import bundle, partial_bundle
from utils import iterative_bundle, partial_iterative
from utils import randsel_bundle, partial_randsel
from utils import normal_dist_bundle, partial_normal_dist

bundlers = {
  "sum": bundle,
  "sum_p25": partial_bundle(0.25),
  "sum_p50": partial_bundle(0.50),
  "sum_p75": partial_bundle(0.75),

  "iter": iterative_bundle,
  "iter_p25": partial_iterative(0.25),
  "iter_p50": partial_iterative(0.50),
  "iter_p75": partial_iterative(0.75),

  "randsel": randsel_bundle,
  "randsel_p25": partial_randsel(0.25),
  "randsel_p50": partial_randsel(0.50),
  "randsel_p75": partial_randsel(0.75),

  "normal": normal_dist_bundle,
  "normal_p25": partial_normal_dist(0.25),
  "normal_p50": partial_normal_dist(0.50),
  "normal_p75": partial_normal_dist(0.75),
}

shapes = {
  "sum": "o",
  "sum_p25": "X",
  "sum_p50": "D",
  "sum_p75": "s",

  "iter": "o",
  "iter_p25": "X",
  "iter_p50": "D",
  "iter_p75": "s",

  "randsel": "o",
  "randsel_p25": "X",
  "randsel_p50": "D",
  "randsel_p75": "s",

  "normal": "o",
  "normal_p25": "X",
  "normal_p50": "D",
  "normal_p75": "s",
}

colors = {
  "sum": "blue",
  "sum_p25": "blue",
  "sum_p50": "blue",
  "sum_p75": "blue",

  "iter": "brown",
  "iter_p25": "brown",
  "iter_p50": "brown",
  "iter_p75": "brown",

  "randsel": "green",
  "randsel_p25": "green",
  "randsel_p50": "green",
  "randsel_p75": "green",

  "normal": "orange",
  "normal_p25": "orange",
  "normal_p50": "orange",
  "normal_p75": "orange",
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



plt.figure(figsize=(10, 6))

for name, vals in results.items():
  plt.plot(
    Ns,
    [v[0] for v in vals],
    marker=shapes[name],
    color=colors[name],
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
    color=colors[name],
    label=name
  )

plt.xlabel("Number of bundled signals")
plt.ylabel("Cosine similarity to noise")
plt.title("Noise leakage vs number of signals (average over {trials} runs)")
plt.legend()
plt.grid(True)
plt.savefig('./noise.png')
plt.show()
