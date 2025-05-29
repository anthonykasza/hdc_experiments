# Removed the inverse plots, the dotted sag line,
#  and the x-ticks
# Comparing a bundle to its constituents


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

def new_hv(n=10_000):
    return np.random.choice([1, -1], size=n)

signal1 = new_hv()
signal2 = new_hv()
signal3 = new_hv()

# This is clipped bundling.
# The resulting bundle signal will be most similar to signal1
#  since it is included in the bundle multiple times
bundle = np.sign(signal1 + signal1 + signal1 + signal2 + signal3)

b_positions_1 = np.array([i for i, val in enumerate(bundle) if val == 1])
b_x = np.linspace(0, len(bundle) - 1, 1000)
b_kde_1 = gaussian_kde(b_positions_1, bw_method='scott')
b_density_1 = b_kde_1(b_x)
b_centroid_1 = b_positions_1.mean()

s1_positions_1 = np.array([i for i, val in enumerate(signal1) if val == 1])
s1_x = np.linspace(0, len(signal1) - 1, 1000)
s1_kde_1 = gaussian_kde(s1_positions_1, bw_method='scott')
s1_density_1 = s1_kde_1(s1_x)
s1_centroid_1 = s1_positions_1.mean()

s2_positions_1 = np.array([i for i, val in enumerate(signal2) if val == 1])
s2_x = np.linspace(0, len(signal2) - 1, 1000)
s2_kde_1 = gaussian_kde(s2_positions_1, bw_method='scott')
s2_density_1 = s2_kde_1(s2_x)
s2_centroid_1 = s2_positions_1.mean()

s3_positions_1 = np.array([i for i, val in enumerate(signal3) if val == 1])
s3_x = np.linspace(0, len(signal3) - 1, 1000)
s3_kde_1 = gaussian_kde(s3_positions_1, bw_method='scott')
s3_density_1 = s3_kde_1(s3_x)
s3_centroid_1 = s3_positions_1.mean()

fig, axes = plt.subplots(nrows=3, figsize=(14, 4), sharex=False)

axes[0].plot(b_x, b_density_1, color='blue', alpha=0.7, label='Bundle (bundle)')
axes[0].plot(s1_x, s1_density_1, color='red', alpha=0.7, label='Signal 1')
axes[0].set_title('Clothesline Plot - Bundle, Signal1')
axes[0].set_xlabel('element index')
axes[0].yaxis.set_visible(False)
axes[0].xaxis.set_visible(False)
axes[0].invert_yaxis()
axes[0].legend()

axes[1].plot(b_x, b_density_1, color='blue', alpha=0.7, label='Bundle (bundle)')
axes[1].plot(s2_x, s2_density_1, color='red', alpha=0.7, label='Signal 2')
axes[1].set_title('Clothesline Plot - Bundle, Signal2')
axes[1].set_xlabel('element index')
axes[1].yaxis.set_visible(False)
axes[1].xaxis.set_visible(False)
axes[1].invert_yaxis()
axes[1].legend()

axes[2].plot(b_x, b_density_1, color='blue', alpha=0.7, label='Bundle (bundle)')
axes[2].plot(s3_x, s3_density_1, color='red', alpha=0.7, label='Signal 3')
axes[2].set_title('Clothesline Plot - Bundle, Signal3')
axes[2].set_xlabel('element index')
axes[2].yaxis.set_visible(False)
axes[2].xaxis.set_visible(False)
axes[2].invert_yaxis()
axes[2].legend()

plt.tight_layout()
plt.show()
