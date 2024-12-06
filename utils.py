import copy
import numpy as np
from numpy.linalg import norm


def hdv(n=10_000):
  '''Return a new bipolar symbolic representation'''
  return np.random.choice([1, -1], size=n)


def clip(hdv, zeros=True):
  '''trims values to 1 or -1, optionally flips 0 randomly
     clip is essentially a relu
  '''
  if zeros:
    return np.array([1 if x > 0 else -1 if x < 0 else 0 for x in hdv])
  else:
    return np.array([1 if x > 0 else -1 if x < 0 else np.random.choice([1, -1]) for x in hdv])


def bundle(*args):
  '''element-wise addition of vectors'''
  return clip(np.sum([hdv for hdv in args], axis=0))


def unbundle(hdv1, hdv2):
  '''element-wise unbundling should be subtraction but ...'''
  pass


def bind(*args):
  '''element-wise multiplication of vectors'''
  return np.prod([hdv for hdv in args], axis=0)


def unbind(*args):
  '''bind is the inverse of itself'''
  return bind(*args)


def permute(hdv, positions=[0,1], segments=1):
  '''permute the values of a vector towards the tail
     gracias: https://stackoverflow.com/questions/30639656/numpy-roll-in-several-dimensions/30655508#30655508
  '''
  hdv = hdv.reshape(segments, len(hdv)//segments)
  hdv = np.roll(hdv, positions, axis=(0, 1))
  return np.ravel(hdv)


def unpermute(hdv, positions=[0,-1], segments=1):
  '''permute the values of a vector towards the head'''
  return permute(hdv, positions, segments)


def cossim(hdv1, hdv2):
  '''find how similar 2 vectors are'''
  if norm(hdv1) == 0 or norm(hdv2) == 0:
    return 0
  return np.dot(hdv1, hdv2) / (norm(hdv1) * norm(hdv2))


def hamdis(hdv1, hdv2):
  '''find how dissimilar 2 vectors are'''
  return np.sum(hdv1 != hdv2) / len(hdv1)


def make_bins(bins=1000, n=10_000):
  '''Return a list of HDVs representing linearly discretized histogram buckets'''
  bins_list = []
  bins_list.append(hdv(n))
  flips_per_iteration = n // bins
  for i in range(1, bins):
    next_level = copy.deepcopy(bins_list[i-1])
    for j in range(flips_per_iteration):
      next_level[(i * flips_per_iteration) + j] = next_level[(i * flips_per_iteration) + j] * -1
    bins_list.append(next_level)
  return bins_list


def discretize(min_val, max_val, bins):
  '''Given a max and min value, split a range into bins'''
  ranges = []
  step = (max_val - min_val) / bins
  for i in range(bins):
    # keep everything to 2 decimal places
    start = round(min_val + (i * step), 2)
    stop = round(min_val + ((i + 1) * step), 2)
    ranges.append((start, stop))
  return ranges



def assign_labels(data, centroids):
  # assign each sample to a centroid based on cossim
  tags = []

  for j in range(len(data)):
    max_sim = 0.0
    max_sim_idx = -1

    for c in range(len(centroids)):
      sim_score = cossim(data[j], centroids[c])
      # keep the largest similarity score
      if sim_score > max_sim:
        max_sim = sim_score
        max_sim_idx = c
      # flip a coin if similarity scores are equal
      elif sim_score == max_sim and np.random.choice([True, False]):
        max_sim = sim_score
        max_sim_idx = c
    if max_sim_idx == -1 or max_sim == 0.0:
      tags.append(np.random.choice(len(centroids)-1))
    else:
      tags.append(max_sim_idx)
  return tags


def kmeans(data, k=3, max_iter=10, halting_sim=0.9999):
  '''A kmeans-style clustering algorithm inspired by HDCluster'''
  centroid_indices = np.random.choice(len(data), size=k, replace=False)
  centroids = [data[i] for i in centroid_indices]
  prev_centroids = np.zeros_like(centroids)

  for i in range(max_iter):
    labels = assign_labels(data, centroids)

    # halt when old centroids are very similar to new centroids
    centroid_sims = [cossim(centroids[idx], prev_centroids[idx]) for idx in range(len(centroids))]
    if all(s > halting_sim for s in centroid_sims):
      print(f'halting at iteration: {i}')
      break

    # compute new centroids based on labels
    new_centroids = []
    for k in range(len(centroids)):
      centroid = centroids[k]
      samples = []
      for i in range(len(data)):
        if np.array_equal(centroids[labels[i]], centroid):
          samples.append(data[i])
      samples = np.array(samples)
      new_centroids.append(np.mean(samples, axis=0))
    prev_centroids = copy.deepcopy(centroids)
    centroids = new_centroids

  return np.array(labels), centroids
