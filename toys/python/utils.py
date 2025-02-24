import copy
import random
import numpy as np
from numpy.linalg import norm


def hdv(n=10_000, all=None):
  '''return a new bipolar symbolic representation using a normal distribution'''
  if all is not None:
    return np.full((1, n), all).flatten()
  return np.random.choice([1, -1], size=n)


def clip(hdv, zeros=True):
  '''trims values to 1 or -1, optionally flips 0 randomly'''
  if zeros:
    tmp = np.sign(hdv)
    return np.where(tmp==0, np.random.choice([1, -1], size=1), tmp)
  else:
    return np.sign(hdv)


def bundle(*args):
  '''element-wise addition of vectors'''
  return clip(np.sum([hdv for hdv in args], axis=0))


def bind(*args):
  '''element-wise multiplication of vectors'''
  return np.prod([hdv for hdv in args], axis=0)


def unbind(*args):
  '''in a bipolar architecture, bind is the inverse of itself'''
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
  return abs(np.dot(hdv1, hdv2) / (norm(hdv1) * norm(hdv2)))


def hamdis(hdv1, hdv2):
  '''find how dissimilar 2 vectors are'''
  return np.sum(hdv1 != hdv2) / len(hdv1)


def make_levels(bins=1000, n=10_000):
  '''Return a list of HDVs representing linearly discretized histogram buckets'''
  bins_list = []
  bins_list.append(hdv(n))
  altered_indices = set([])
  flips_per_iteration = n // bins

  for i in range(1, bins):
    next_level = copy.deepcopy(bins_list[i-1])
    # all the possible indices, except those in altered_indices
    indexes_to_chose_from = set(range(len(next_level))).difference(altered_indices)
    for j in random.sample(indexes_to_chose_from, flips_per_iteration):
      altered_indices.add(j)
      next_level[j] = next_level[j] * -1
    bins_list.append(next_level)
  return bins_list


def discretize(min_val, max_val, bins):
  '''Given a max and min value, split a range into bins'''
  ranges = []
  step = (max_val - min_val) / bins
  for i in range(bins):
    start = min_val + (i * step)
    stop = min_val + ((i + 1) * step)
    ranges.append((start, stop))
  return ranges


def kbundles(data, k, max_iter=10, halting_sim=0.999):
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
      sample = data[sample_idx]
      highest_similarity = 0.0
      best_centroid_idx = -1
      for centroid_idx in range(len(centroids)):
        centroid = centroids[centroid_idx]
        # do not score the sample against itself on the first iteration
        if i == 0 and np.array_equal(centroid, sample):
          continue
        similarity = cossim(sample, centroid)
        # store the centroid with the highest similarity to the sample
        if similarity > highest_similarity:
          highest_similarity = similarity
          best_centroid_idx = centroid_idx
        # if the sample is equally similar to 2 centroids, randomly pick one
        elif similarity == highest_similarity and np.random.choice([True, False]):
          highest_similarity = similarity
          best_centroid_idx = centroid_idx
      # if we've compared the sample to all centroids and didn't set
      #  highest_similarity or best_centroid_idx, randomly pick a centroid
      if highest_similarity == 0.0 or best_centroid_idx == -1:
        best_centroid_idx = np.random.choice(len(centroids)-1)
      labels.append(best_centroid_idx)


    # update
    prev_centroids = copy.deepcopy(centroids)
    for centroid_idx in range(len(prev_centroids)):
      samples = []
      for sample_idx in range(len(data)):
        if labels[sample_idx] == centroid_idx:
          samples.append(data[sample_idx])
      if len(samples) == 0:
        return labels, centroids, i
      centroids[centroid_idx] = bundle(*samples)


    # halt check, all centroids are halting_sim similar to their previous vectors
    centroid_sims = [cossim(c1, c2) for c1,c2 in zip(centroids, prev_centroids)]
    if all(s > halting_sim for s in centroid_sims):
      return labels, centroids, i

  # the algo ran out of iterations
  return labels, centroids, max_iter



def substitute(hv1, hv2, bins):
  '''
  this is conceptually similar to make_levels() except
  substitution defines the start and stop HVs
  while make_levels() randomizes both

  make_levels() returns a list that is 1 shroter than substitute
  '''
  bins_list = []
  bins_list.append(hv1)
  altered_indices = set([])
  flips_per_iteration = len(hv1) // bins

  for i in range(1, bins):
    next_level = copy.deepcopy(bins_list[i-1])
    # all the possible indices, except those in altered_indices
    indexes_to_chose_from = set(range(len(next_level))).difference(altered_indices)
    for j in random.sample(indexes_to_chose_from, flips_per_iteration):
      altered_indices.add(j)
      next_level[j] = hv2[j]
    bins_list.append(next_level)
  bins_list.append(hv2)
  return bins_list

def sub(hv1, hv2, bins):
  '''shorter alias for bad typists'''
  return substitute(hv1, hv2, bins)
