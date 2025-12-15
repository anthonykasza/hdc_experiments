# Hypervector elements are coprimes up to dims*dims, inspired by
#  Computing With Residue Numbers in High-Dimensional Representation

# I was looking for a means of representing numbers without self-binding
#  and fractional power encoding, so I was playing with modulo

# What happens when we sample from the (co)primes in different ways
#  as in Computing on Functions Using Randomized Vector Representations?
#  We get different shapes.


import matplotlib.pyplot as plt
import random
import math
import numpy as np
from numpy.linalg import norm


def first_n_coprime(n, k):
  result = []
  x = 1
  while len(result) < n:
    if math.gcd(x, k) == 1:
      result.append(x)
    x += 1
  return result


def new_hv_uniform(n, coprimes):
  samples = np.random.choice(coprimes, size=n)
  return samples

def new_hv_normal(n, coprimes, mean=None, std=None):
  coprimes = np.array(coprimes)
  if mean is None:
    mean = np.mean(coprimes)
  if std is None:
    std = np.std(coprimes)
  samples = np.random.normal(loc=mean, scale=std, size=n)
  return samples

def new_hv_triangular(n, coprimes, left=None, mode=None, right=None):
  coprimes = np.array(coprimes)
  if left is None:
    left = np.min(coprimes)
  if right is None:
    right = np.max(coprimes)
  if mode is None:
    mode = np.mean(coprimes)
  samples = np.random.triangular(left, mode, right, size=n)
  return samples

def new_hv_poisson(n, coprimes, lam=None):
  coprimes = np.array(coprimes)
  if lam is None:
    lam = np.mean(coprimes)
  samples = np.random.poisson(lam=lam, size=n)
  return samples

def new_hv_exponential(n, coprimes, scale=None):
  coprimes = np.array(coprimes)
  if scale is None:
    scale = np.mean(coprimes)
  samples = np.random.exponential(scale=scale, size=n)
  return samples

def new_hv_beta(n, coprimes, a=2, b=5):
  coprimes = np.array(coprimes)
  samples = np.random.beta(a, b, size=n)
  # scale beta [0,1] to coprimes range
  samples = samples * (np.max(coprimes) - np.min(coprimes)) + np.min(coprimes)
  return samples

def sim(h1, h2):
  if norm(h1) == 0 or norm(h2) == 0:
    return 0
  return abs(np.dot(h1, h2) / (norm(h1) * norm(h2)))

def mod(h1, i):
  return [x % i for x in h1]

def prepare_points(hv, coprimes):
  points = []
  for i in coprimes[0:1000]:
    points.append( (i, sim(hv, mod(hv, i))) )
    points.append( (-i, sim(hv, mod(hv, -i))) )
  X = [x for (x,_) in points]
  Y = [y for (_,y) in points]
  return X, Y

DIMS = 10000
COPRIMES = first_n_coprime(DIMS, DIMS*DIMS)
print(COPRIMES[0:1000])

distributions = {
  "Uniform": new_hv_uniform,
  "Normal": new_hv_normal,
  "Triangular": new_hv_triangular,
  "Poisson": new_hv_poisson,
  "Exponential": new_hv_exponential,
  "Beta": new_hv_beta
}

plt.figure(figsize=(18, 10))

for idx, (name, func) in enumerate(distributions.items(), 1):
  hv = func(DIMS, COPRIMES)
  X, Y = prepare_points(hv, COPRIMES)
  plt.subplot(2, 3, idx)
  plt.scatter(X, Y, alpha=0.6)
  plt.title(name)
  plt.xlabel('Element modulus')
  plt.ylabel('Similarity with basis hypervector')

plt.tight_layout()
plt.savefig('./no_mapping.png')
plt.show()
