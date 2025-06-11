# The more elements we pin onto a clotheline
#  the more it begins to look like a horizontal line
#  being stretched downward near its ends.
# Notice how there is a clear sag in the clothelines
#  until we have 10_000 items pinned to it.
# Notice that the pinned items on the x-ticks at the top
#  of the plots begin to resemble bar codes until
#  we have 10_000 ticks, where they appear as solid
#  blocks of color.


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


def new_hv(n=10_000):
  return np.random.choice([1, 0], size=n)

hv_sizes = [10, 100, 1000, 10_000]

fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14, 12), sharex=False)

for i, size in enumerate(hv_sizes):
  hv = new_hv(size)

  positions_1 = np.array([j for j, val in enumerate(hv) if val == 1])
  positions_0 = np.array([j for j, val in enumerate(hv) if val == 0])

  x = np.linspace(0, len(hv) - 1, 1000)

  kde_1 = gaussian_kde(positions_1, bw_method='scott')
  density_1 = kde_1(x)
  centroid_1 = positions_1.mean()

  ax1 = axes[i, 0]
  ax1.plot(x, density_1)
  ax1.scatter(positions_1, np.zeros_like(positions_1), color='red', marker='|', s=200, label='pinned items')
  ax1.axvline(centroid_1, color='green', linestyle='--', label='sag')
  ax1.set_ylabel(f'hv size = {size}')
  ax1.set_title('Clothesline Plot')
  ax1.xaxis.set_visible(False)
  ax1.yaxis.set_visible(False)
  ax1.legend()
  ax1.invert_yaxis()

  kde_0 = gaussian_kde(positions_0, bw_method='scott')
  density_0 = kde_0(x)
  centroid_0 = positions_0.mean()

  ax0 = axes[i, 1]
  ax0.plot(x, density_0)
  ax0.scatter(positions_0, np.zeros_like(positions_0), color='blue', marker='|', s=200, label='unweighted region of line')
  ax0.axvline(centroid_0, color='purple', linestyle='--', label='unweighted center')
  ax0.set_title('Inverse Clothesline Plot')
  ax0.set_xlabel('element index')
  ax0.yaxis.set_visible(False)
  ax0.legend()
  ax0.invert_yaxis()

plt.tight_layout()
plt.show()
