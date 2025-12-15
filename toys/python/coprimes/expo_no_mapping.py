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

def new_hv_exponential(n, coprimes, scale=None):
  coprimes = np.array(coprimes)
  if scale is None:
    scale = np.mean(coprimes)
  samples = np.random.exponential(scale=scale, size=n)
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
  "Exponential. scale=0": 0,
  "Exponential. scale=1": 1,
  "Exponential. scale=2.5": 2.5,
  "Exponential. scale=5": 5,
  "Exponential. scale=10": 10,
  "Exponential. scale=25": 25,
  "Exponential. scale=50": 50,
  "Exponential. scale=100": 100,
  "Exponential. scale=500": 500,
  "Exponential. scale=1000": 1000,
  "Exponential. scale=2500": 2500,
  "Exponential. scale=5000": 5000,
  "Exponential. scale=10000": 10000,
  "Exponential. scale=20000": 20000,
  "Exponential. scale=100000": 100000,
}

plt.figure(figsize=(18, 10))

for idx, (name, scale) in enumerate(distributions.items(), 1):
  hv = new_hv_exponential(DIMS, COPRIMES, scale)
  X, Y = prepare_points(hv, COPRIMES)
  plt.subplot(3, 5, idx)
  plt.scatter(X, Y, alpha=0.6)
  plt.title(name)
  plt.xlabel('Element modulus')
  plt.ylabel('Similarity with basis hypervector')

plt.tight_layout()
plt.savefig('./expo_no_mapping.png')
plt.show()
