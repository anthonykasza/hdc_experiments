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

def sample_nearest(coprimes, samples):
  coprimes = np.array(coprimes)
  nearest = np.array([coprimes[np.argmin(np.abs(coprimes - x))] for x in samples])
  return nearest

def new_hv_poisson(n, coprimes, lam=None):
  coprimes = np.array(coprimes)
  if lam is None:
    lam = np.mean(coprimes)
  samples = np.random.poisson(lam=lam, size=n)
  return sample_nearest(coprimes, samples)

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
  "Poisson. lam=0": 0,
  "Poisson. lam=1": 1,
  "Poisson. lam=2.5": 2.5,
  "Poisson. lam=5": 5,
  "Poisson. lam=10": 10,
  "Poisson. lam=25": 25,
  "Poisson. lam=50": 50,
  "Poisson. lam=100": 100,
  "Poisson. lam=500": 500,
  "Poisson. lam=1000": 1000,
  "Poisson. lam=2500": 2500,
  "Poisson. lam=5000": 5000,
  "Poisson. lam=10000": 10000,
  "Poisson. lam=15000": 15000,
  "Poisson. lam=20000": 20000,
}

plt.figure(figsize=(18, 10))

for idx, (name, lam) in enumerate(distributions.items(), 1):
  hv = new_hv_poisson(DIMS, COPRIMES, lam)
  X, Y = prepare_points(hv, COPRIMES)
  plt.subplot(3, 5, idx)
  plt.scatter(X, Y, alpha=0.6)
  plt.title(name)
  plt.xlabel('Element modulus')
  plt.ylabel('Similarity with basis hypervector')

plt.tight_layout()
plt.savefig('./poisson_map_to_coprimes.png')
plt.show()
