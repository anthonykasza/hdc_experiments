import numpy as np

import sys
sys.path.insert(0, '../')
from utils import hdv, bundle, bind, cossim



def change_dimensions(hv: np.ndarray, matrix: np.ndarray) -> np.ndarray:
  '''project a hypervector into a different dimensionality'''
  if matrix.shape[1] != hv.shape[0]:
    raise ValueError("bad shapes")
  result = np.dot(matrix, hv)
  return result


noise_10k = hdv(10000)
signal1_10k = hdv(10000)
signal2_10k = hdv(10000)
signal3_10k = hdv(10000)
signal4_10k = hdv(10000)
signal5_10k = hdv(10000)
bundle_10k = bundle(
  signal1_10k, signal2_10k,
  signal3_10k, signal4_10k,
  signal5_10k
)

print(f'baseline bundle similarities')
print(f'  bundle_10k to signal1_10k: {cossim(bundle_10k, signal1_10k)}')
print(f'  bundle_10k to signal2_10k: {cossim(bundle_10k, signal2_10k)}')
print(f'  bundle_10k to signal3_10k: {cossim(bundle_10k, signal3_10k)}')
print(f'  bundle_10k to signal4_10k: {cossim(bundle_10k, signal4_10k)}')
print(f'  bundle_10k to signal5_10k: {cossim(bundle_10k, signal5_10k)}')
print(f'  bundle_10k to noise_10k: {cossim(bundle_10k, noise_10k)}')
print()


# fully dense
random_matrix = np.random.choice([-1, 1], size=(1000, 10000))
noise_1k = change_dimensions(noise_10k, random_matrix)
signal1_1k = change_dimensions(signal1_10k, random_matrix)
signal2_1k = change_dimensions(signal2_10k, random_matrix)
signal3_1k = change_dimensions(signal3_10k, random_matrix)
signal4_1k = change_dimensions(signal4_10k, random_matrix)
signal5_1k = change_dimensions(signal5_10k, random_matrix)
bundle_1k = bundle(
  signal1_1k, signal2_1k,
  signal3_1k, signal4_1k,
  signal5_1k
)

print(f'bundling similarities are preserved through dim contraction')
print(f'  bundle_1k to signal1_1k: {cossim(bundle_1k, signal1_1k)}')
print(f'  bundle_1k to signal2_1k: {cossim(bundle_1k, signal2_1k)}')
print(f'  bundle_1k to signal3_1k: {cossim(bundle_1k, signal3_1k)}')
print(f'  bundle_1k to signal4_1k: {cossim(bundle_1k, signal4_1k)}')
print(f'  bundle_1k to signal5_1k: {cossim(bundle_1k, signal5_1k)}')
print(f'  bundle_1k to noise_1k: {cossim(bundle_1k, noise_1k)}')
print()


bind_10k = bind(
  signal1_10k, signal2_10k,
  signal3_10k, signal4_10k,
  signal5_10k
)
bind_1k = bind(
  signal1_1k, signal2_1k,
  signal3_1k, signal4_1k,
  signal5_1k
)

first_bind_then_project = change_dimensions(bind_10k, random_matrix)
first_project_then_bind = bind_1k
print(f'binding similarities are not preversed through dim contraction')
print(f'  {cossim(first_bind_then_project, first_project_then_bind)}')
