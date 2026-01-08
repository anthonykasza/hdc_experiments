
import numpy as np
from numpy.linalg import norm



def hdv(n=10_000, all=None):
  if all is not None:
    return np.full((1, n), all).flatten()
  return np.random.choice([-1, 1], size=n)

def sim(h1, h2):
  if norm(h1) == 0 or norm(h2) == 0:
    return 0
  return abs(np.dot(h1, h2) / (norm(h1) * norm(h2)))

def randsel_weighted_bundle(weights, *hvs):
  acc = hdv(n=len(hvs[0]), all=0)
  n = len(hvs)
  for i in range(len(acc)):
    idx = int(np.random.choice(n, p=weights))
    hv = hvs[idx]
    acc[i] = hv[i]
  return acc

def normalize_weights(w):
  return [each / sum(w) for each in w]


signals = [hdv() for _ in range(5)]
noise = hdv()

print("ignore everythin except 3")
weights = normalize_weights([0, 0, 1, 0, 0])
wb = randsel_weighted_bundle(weights, *signals)
for idx in range(len(signals)):
  print(idx, sim(wb, signals[idx]))
print("noise", sim(wb, noise))
print()

print("most like 3, then 1 and 5, then nothing like 2 or 4")
weights = normalize_weights([5, 0, 10, 0, 5])
wb = randsel_weighted_bundle(weights, *signals)
for idx in range(len(signals)):
  print(idx, sim(wb, signals[idx]))
print("noise", sim(wb, noise))
print()
