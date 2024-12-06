# What happens if we were to define specific
#  distributions of element values instead of
#  sampling evenly? It looks like a filter.



import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


def new_hv(n=10_000):
  return np.random.choice([1, 0], size=n)

hv = np.array([0]*300 + [1]*400 + [0]*300)

fig, ax = plt.subplots(nrows=2, figsize=(14, 12), sharex=False)

positions_1 = np.array([j for j, val in enumerate(hv) if val == 1])
positions_0 = np.array([j for j, val in enumerate(hv) if val == 0])

x = np.linspace(0, len(hv) - 1, 1000)
kde_1 = gaussian_kde(positions_1, bw_method='scott')
density_1 = kde_1(x)
centroid_1 = positions_1.mean()

ax[0].plot(x, density_1)
ax[0].scatter(positions_1, np.zeros_like(positions_1), color='red', marker='|', s=200, label='pinned items')
ax[0].axvline(centroid_1, color='green', linestyle='--', label='sag')
ax[0].set_title('Clothesline Plot')
ax[0].xaxis.set_visible(False)
ax[0].yaxis.set_visible(False)
ax[0].legend()
ax[0].invert_yaxis()

kde_0 = gaussian_kde(positions_0, bw_method='scott')
density_0 = kde_0(x)
centroid_0 = positions_0.mean()

ax[1].plot(x, density_0)
ax[1].scatter(positions_0, np.zeros_like(positions_0), color='blue', marker='|', s=200, label='unweighted region of line')
ax[1].axvline(centroid_0, color='purple', linestyle='--', label='unweighted center')
ax[1].set_title('Inverse Clothesline Plot')
ax[1].set_xlabel('element index')
ax[1].yaxis.set_visible(False)
ax[1].legend()
ax[1].invert_yaxis()

plt.tight_layout()
plt.show()
