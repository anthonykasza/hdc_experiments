# Thanks to TorchHD and HoloVec

import numpy as np


def wrap_angle(theta):
  # this is better than modular wrapping for some reason
  return np.arctan2(np.sin(theta), np.cos(theta))

def to_complex(theta):
  return np.exp(1j * theta)

def to_angle(z):
  return np.angle(z)


def hdv(dims):
  return np.random.uniform(-np.pi, np.pi, size=dims)

def bind(*hvs):
  # cleanup?
  return wrap_angle(np.sum(hvs, axis=0))

def unbind(h1, h2):
  return wrap_angle(h1 - h2)

def bundle(*hvs, eps=1e-9):
  # only use complex numbers when we bundle
  z = np.sum([to_complex(hv) for hv in hvs], axis=0)
  mag = np.abs(z)
  z = z / np.maximum(mag, eps)
  return np.angle(z)

def inverse(hv):
  return wrap_angle(-hv)

def permute(hv, k=1):
  return np.roll(hv, k)

def sim(h1, h2):
  return (np.mean(np.cos(h1 - h2)) + 1) / 2

def fractional_power(basis_hv, x, bandwidth=1.0):
  return wrap_angle(basis_hv * (bandwidth * x))


def main():
  DIMS = 10000

  print("Sequences")
  # create symbols
  A = hdv(DIMS)
  B = hdv(DIMS)
  C = hdv(DIMS)

  # encode sequence A,B,C
  seq = bundle(
      bind(permute(A, 0)),
      bind(permute(B, 1)),
      bind(permute(C, 2)),
  )

  # retrieve middle element (B)
  B_hat = unbind(seq, permute(A, 0))
  B_hat = unbind(B_hat, permute(C, 2))

  print("Similarity B' to B:", sim(B_hat, B))
  print("Similarity B' to A:", sim(B_hat, A))
  print("Similarity B' to C:", sim(B_hat, C))
  print("Similarity B' to ABC bundle:", sim(B_hat, seq))
  print()

  print('Records')
  # keys and values
  key1, val1 = hdv(DIMS), hdv(DIMS)
  key2, val2 = hdv(DIMS), hdv(DIMS)

  # store associations
  memory = bundle(
    bind(key1, val1),
    bind(key2, val2),
  )

  # query with key1
  val1_hat = unbind(memory, key1)
  print("Similarity val1' to val1:", sim(val1_hat, val1))
  print("Similarity val1' to val2:", sim(val1_hat, val2))
  print("Similarity val1' to record bundle:", sim(val1_hat, memory))
  print()



  # Multi-variate feature embedding using Fractional Power Encoding
  import matplotlib.pyplot as plt

  np.random.seed(0)
  DIMS = 8000
  NUM_FEATURES = 25
  BANDWIDTHS = [0.05, 0.08, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]

  # create base hypervectors for each feature vector dimension
  bases = [hdv(DIMS) for _ in range(NUM_FEATURES)]

  # generate 25 feature vectors in 0-10 where all elements are the same value
  feature_vectors = np.linspace(1, 10, NUM_FEATURES).reshape(NUM_FEATURES, 1) * np.ones((1, NUM_FEATURES))

  # Create subplots
  fig, axes = plt.subplots(2, 5, figsize=(22, 14))
  axes = axes.flatten()

  for i, bw in enumerate(BANDWIDTHS):
    # encode all feature vectors using FPE with varying B
    encoded_vectors = []
    for fv in feature_vectors:
      hv = bundle(*[fractional_power(b, val, bw) for b, val in zip(bases, fv)])
      encoded_vectors.append(hv)
    encoded_vectors = np.array(encoded_vectors)

    # compute pairwise similarity
    sims = np.zeros((NUM_FEATURES, NUM_FEATURES))
    for j in range(NUM_FEATURES):
      for k in range(NUM_FEATURES):
        sims[j, k] = sim(encoded_vectors[j], encoded_vectors[k])

    # plot FPE similarity
    im = axes[i].imshow(sims, cmap='viridis', vmin=0, vmax=1)
    axes[i].set_title(f'Bandwidth = {bw}')
    axes[i].set_xlabel('Feature index')
    axes[i].set_ylabel('Feature index')

  # Adjust layout to make space for colorbar on the right
  fig.subplots_adjust(right=0.92, hspace=0.4, wspace=0.4)

  # Add a single colorbar for all subplots
  cbar_ax = fig.add_axes([0.94, 0.15, 0.02, 0.7])
  fig.colorbar(im, cax=cbar_ax, label='FPE similarity')

  plt.show()


if __name__ == '__main__':
  main()
