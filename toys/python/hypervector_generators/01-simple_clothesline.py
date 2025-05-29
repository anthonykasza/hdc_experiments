# To think about densities and probabilies one can imagine
#  a clothesline. Where the items are pinned, the line will
#  be pulled down by gravity. The denser a region of the
#  line is, the more it will sag.
# The value of hv was hand-crafted to show a clothesline with
#  items bunching towards the middle of the line.
# The inverse of a clothesline exists but it is also just
#  a clotheline.


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# toy hypervector
hv = [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]

positions_1 = np.array([i for i, val in enumerate(hv) if val == 1])
positions_0 = np.array([i for i, val in enumerate(hv) if val == 0])

# ones
kde_1 = gaussian_kde(positions_1, bw_method='scott')
x_1 = np.linspace(0, len(hv) - 1, 1000)
density_1 = kde_1(x_1)
centroid_1 = positions_1.mean()

# zeros
kde_0 = gaussian_kde(positions_0, bw_method='scott')
x_0 = np.linspace(0, len(hv) - 1, 1000)
density_0 = kde_0(x_0)
centroid_0 = positions_0.mean()

fig, axes = plt.subplots(nrows=2, figsize=(10, 6), sharex=True)

# ones
axes[0].plot(x_1, density_1)
axes[0].scatter(positions_1, np.zeros_like(positions_1), color='red', marker='|', s=200, label='pinned items')
axes[0].axvline(centroid_1, color='green', linestyle='--', label='sag')
axes[0].xaxis.set_label_position('top')
axes[0].xaxis.tick_top()
axes[0].set_ylabel('')
axes[0].yaxis.set_visible(False)
axes[0].set_title('Clothesline Plot')
axes[0].set_xlabel('element index')
axes[0].legend()
axes[0].invert_yaxis()

# zeros
axes[1].plot(x_0, density_0)
axes[1].scatter(positions_0, np.zeros_like(positions_0), color='blue', marker='|', s=200, label='unweighted region of line')
axes[1].axvline(centroid_0, color='purple', linestyle='--', label='unweighted center')
axes[1].xaxis.set_label_position('top')
axes[1].xaxis.tick_top()
axes[1].set_ylabel('')
axes[1].yaxis.set_visible(False)
axes[1].set_title('Inverse Clothesline Plot')
axes[1].legend()
axes[1].invert_yaxis()
axes[1].set_xlabel('')

plt.tight_layout()
plt.show()
