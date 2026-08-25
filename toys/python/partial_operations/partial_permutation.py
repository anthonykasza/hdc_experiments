# Demonstration of partial permutation

from matplotlib import pyplot as plt
import numpy as np
from numpy.linalg import norm


def hdv(n=10_000, all=None):
  return np.random.choice([1, -1], size=n)

def sim(hdv1, hdv2):
  if norm(hdv1) == 0 or norm(hdv2) == 0:
    return 0
  return np.dot(hdv1, hdv2) / (norm(hdv1) * norm(hdv2))

def permute(hdv, positions=[0,1], segments=1):
  '''typical ol' perm'''
  hdv = hdv.reshape(segments, len(hdv)//segments)
  hdv = np.roll(hdv, positions, axis=(0, 1))
  return np.ravel(hdv)

def permute_partial(hv, percent=1.0):
  '''permute a subset of the elements'''
  hv = np.asarray(hv).copy()
  n = len(hv)
  k = int(round(percent * n))
  if k <= 1:
    return hv
  indices = np.random.choice(n, size=k, replace=False)
  hv[indices] = hv[np.random.permutation(indices)]
  return hv


print('Typical permutation, small dimensions')
h1 = np.array([1,2,3,4,5,6,7,8])
h2 = permute(h1)
print(f'{len(h1)}, h1: {h1}')
print(f'{len(h2)}, h2: {h2}')
print(f'sim(h1, h2): {sim(h1, h2)}')
print()

print('Typical permutation, large dimensions')
h1 = hdv()
h2 = permute(h1)
print(f'{len(h1)}, h1: {h1}')
print(f'{len(h2)}, h2: {h2}')
print(f'sim(h1, h2): {sim(h1, h2)}')
print()

print('Partial permutation, small dimensions')
h1 = np.array([1,2,3,4,5,6,7,8])
h2 = permute_partial(h1, 0.5)
print(f'{len(h1)}, h1: {h1}')
print(f'{len(h2)}, h2: {h2}')
print(f'sim(h1, h2): {sim(h1, h2)}')
print()



print('Linear correlated codebook based on partial permutations')

def make_levels_perm(hv, levels=10):
  # segment the hypervector equally into blocks
  block_size = len(hv) // levels
  blocks = [
    hv[i * block_size:(i + 1) * block_size]
    for i in range(levels)
  ]
  # permute each block
  permuted = [
    np.random.permutation(block)
    for block in blocks
  ]
  # create a trajectory from hv to the fully permuted hv
  return [
    np.concatenate(permuted[:level] + blocks[level:])
    for level in range(levels + 1)
  ]


h1 = hdv()
levels = make_levels_perm(h1, 10)
data = []
for o_idx in range(len(levels)):
  data.append([])
  for i_idx in range(len(levels)):
    data[o_idx].append( sim(levels[o_idx], levels[i_idx]) )

plt.imshow(data, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Similarity')
plt.title('Level Similarity')
plt.show()
