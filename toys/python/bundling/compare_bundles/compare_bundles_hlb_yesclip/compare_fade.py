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

NUM_RUNS = 20
NUM_SIGNALS = 20


results = {name: np.zeros(NUM_SIGNALS) for name in bundlers}

for _ in range(NUM_RUNS):

  signals = [hdv() for _ in range(NUM_SIGNALS)]

  for name, bundler in bundlers.items():
    b = bundler(*signals)
    for i, sig in enumerate(signals):
      results[name][i] += cossim(sig, b)

for name in results:
  results[name] /= NUM_RUNS


x = np.arange(1, NUM_SIGNALS + 1)

plt.figure(figsize=(10, 6))

for name, sims in results.items():
  plt.plot(x, sims, marker=shapes[name], linewidth=1.5, label=name, color=colors[name])

plt.xticks(x, [f"signal{i}" for i in x])
plt.ylim(0, 1)
plt.xlabel("Signal index")
plt.ylabel("Average cosine similarity")
plt.title(f"Bundle similarity vs signal index (averaged over {NUM_RUNS} runs)")
plt.grid(alpha=0.3)
plt.legend(ncol=2, fontsize=9)
plt.tight_layout()
plt.savefig('./fade.png')
plt.show()
