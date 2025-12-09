# Compare the similarity matrices of VSA with
#  different ranges of hypervector element vaues.


# coin_flip() is binary (hdc)
# dice_roll() is finite-group of order 6
# the larger the range of element values the closer
#  the vsa approximates FHRR's continuous unity cycle


import numpy as np
import matplotlib.pyplot as plt

def binary_similarity_matrix():
  G = np.array([+1, -1])
  S = np.outer(G, G)
  return S

def cyclic_similarity_matrix(n):
  S = np.zeros((n, n))
  for i in range(n):
    for j in range(n):
      S[i, j] = np.cos(2 * np.pi * (i - j) / n)
  return S

def plot_matrix(S, title):
  plt.imshow(S, cmap="coolwarm", vmin=-1, vmax=1)
  plt.colorbar()
  plt.title(title)
  plt.show()

# Examples
plot_matrix(binary_similarity_matrix(), "Binary HDC Similarity")
plot_matrix(cyclic_similarity_matrix(8), "Finite Group VSA (n=8)")
plot_matrix(cyclic_similarity_matrix(32), "Continuous-like FHRR Approximation (n=32)")
plot_matrix(cyclic_similarity_matrix(360), "Continuous-like FHRR Approximation (n=360)")
