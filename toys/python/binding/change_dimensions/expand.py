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


noise_1k = hdv(1000)
signal1_1k = hdv(1000)
signal2_1k = hdv(1000)
signal3_1k = hdv(1000)
signal4_1k = hdv(1000)
signal5_1k = hdv(1000)
bundle_1k = bundle(
  signal1_1k, signal2_1k,
  signal3_1k, signal4_1k,
  signal5_1k
)

print(f'baseline bundle similarities')
print(f'  bundle_1k to signal1_1k: {cossim(bundle_1k, signal1_1k)}')
print(f'  bundle_1k to signal2_1k: {cossim(bundle_1k, signal2_1k)}')
print(f'  bundle_1k to signal3_1k: {cossim(bundle_1k, signal3_1k)}')
print(f'  bundle_1k to signal4_1k: {cossim(bundle_1k, signal4_1k)}')
print(f'  bundle_1k to signal5_1k: {cossim(bundle_1k, signal5_1k)}')
print(f'  bundle_1k to noise_1k: {cossim(bundle_1k, noise_1k)}')
print()


# fully dense
random_matrix = np.random.choice([-1, 1], size=(10000, 1000))
noise_10k = change_dimensions(noise_1k, random_matrix)
signal1_10k = change_dimensions(signal1_1k, random_matrix)
signal2_10k = change_dimensions(signal2_1k, random_matrix)
signal3_10k = change_dimensions(signal3_1k, random_matrix)
signal4_10k = change_dimensions(signal4_1k, random_matrix)
signal5_10k = change_dimensions(signal5_1k, random_matrix)
bundle_10k = bundle(
  signal1_10k, signal2_10k,
  signal3_10k, signal4_10k,
  signal5_10k
)

print(f'bundling similarities are preserved through dim expansion')
print(f'  bundle_10k to signal1_10k: {cossim(bundle_10k, signal1_10k)}')
print(f'  bundle_10k to signal2_10k: {cossim(bundle_10k, signal2_10k)}')
print(f'  bundle_10k to signal3_10k: {cossim(bundle_10k, signal3_10k)}')
print(f'  bundle_10k to signal4_10k: {cossim(bundle_10k, signal4_10k)}')
print(f'  bundle_10k to signal5_10k: {cossim(bundle_10k, signal5_10k)}')
print(f'  bundle_10k to noise_10k:   {cossim(bundle_10k, noise_10k)}')
print()


bind_1k = bind(
  signal1_1k, signal2_1k,
  signal3_1k, signal4_1k,
  signal5_1k
)
bind_10k = bind(
  signal1_10k, signal2_10k,
  signal3_10k, signal4_10k,
  signal5_10k
)
first_bind_then_project = change_dimensions(bind_1k, random_matrix)
first_project_then_bind = bind_10k
print(f'binding similarities are not preversed through dim expansion')
print(f'  {cossim(first_bind_then_project, first_project_then_bind)}')




