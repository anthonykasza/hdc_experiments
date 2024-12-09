import copy
import numpy as np
from numpy.linalg import norm


def hdv(n=10_000):
  '''Return a new bipolar symbolic representation'''
  return np.random.choice([1, -1], size=n)


def clip(hdv, zeros=True):
  '''trims values to 1 or -1, optionally flips 0 randomly
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


def kbundles(data, k, max_iter=10, halting_sim=0.99):
  '''A kmeans-style clustering algorithm inspired by HDCluster'''

  # initialize
  #  what happens if the selected centroids belong to the same group?
  centroid_indices = np.random.choice(len(data), size=k, replace=False)
  centroids = [data[i] for i in centroid_indices]
  prev_centroids = np.zeros_like(centroids)

  # assign, update, halt check
  for i in range(max_iter):

    # assign
    labels = []
    for sample_idx in range(len(data)):
      for centroid_idx in range(len(centroids)):
        sample_centroid_sim = cossim(data[sample_idx], centroids[centroid_idx])
        max_sim = 0.0
        max_sim_idx = 0
        if sample_centroid_sim > max_sim:
          max_sim = sample_centroid_sim
          max_sim_centroid_idx = centroid_idx
        elif sample_centroid_sim == max_sim and np.random.choice([True, False]):
          max_sim = sample_centroid_sim
          max_sim_centroid_idx = centroid_idx
      if max_sim == 0.0:
        labels.append(np.random.choice(len(centroids)-1))
      else:
        labels.append(max_sim_centroid_idx)

    # update
    prev_centroids = copy.deepcopy(centroids)
    for centroid_idx in range(len(prev_centroids)):
      samples = []
      for sample_idx in range(len(data)):
        if labels[sample_idx] == centroid_idx:
          samples.append(data[sample_idx])
      if len(samples) == 0:
        print('returning because there are no samples to bundle')
        return labels, centroids, i
      centroids[centroid_idx] = bundle(*samples)


    # halt check, all centroids are halting_sim similar to their previous vectors
    centroid_sims = [cossim(c1, c2) for c1,c2 in zip(centroids, prev_centroids)]
    if all(s > halting_sim for s in centroid_sims):
      print(f'returning because sim halt, iterations {i}')
      return labels, centroids, i

  # the algo ran out of iterations
  print('returning because exhaustion')
  return labels, centroids, max_iter

