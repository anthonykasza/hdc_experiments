
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

def new_hv_normal(n, coprimes, mean=None, std=None):
  coprimes = np.array(coprimes)
  if mean is None:
    mean = np.mean(coprimes)
  if std is None:
    std = np.std(coprimes)
  samples = np.random.normal(loc=mean, scale=std, size=n)
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
  "Normal. mean=-100, std=1": {'mean': -100, 'std': 1},
  "Normal. mean=-100, std=2": {'mean': -100, 'std': 2},
  "Normal. mean=-100, std=5": {'mean': -100, 'std': 5},
  "Normal. mean=-100, std=10": {'mean': -100, 'std': 10},
  "Normal. mean=-100, std=100": {'mean': -100, 'std': 100},
  "Normal. mean=0, std=1": {'mean': 0, 'std': 1},
  "Normal. mean=0, std=2": {'mean': 0, 'std': 2},
  "Normal. mean=0, std=5": {'mean': 0, 'std': 5},
  "Normal. mean=0, std=10": {'mean': 0, 'std': 10},
  "Normal. mean=0, std=100": {'mean': 0, 'std': 100},
  "Normal. mean=100, std=1": {'mean': 100, 'std': 1},
  "Normal. mean=100, std=2": {'mean': 100, 'std': 2},
  "Normal. mean=100, std=5": {'mean': 100, 'std': 5},
  "Normal. mean=100, std=10": {'mean': 100, 'std': 10},
  "Normal. mean=100, std=100": {'mean': 100, 'std': 100},
}

plt.figure(figsize=(18, 10))

for idx, (name, args) in enumerate(distributions.items(), 1):
  hv = new_hv_normal(DIMS, COPRIMES, args['mean'], args['std'])
  X, Y = prepare_points(hv, COPRIMES)
  plt.subplot(3, 5, idx)
  plt.scatter(X, Y, alpha=0.6)
  plt.title(name)
  plt.xlabel('Element modulus')
  plt.ylabel('Similarity with basis hypervector')

plt.tight_layout()
plt.savefig('./normal_no_mapping.png')
plt.show()
