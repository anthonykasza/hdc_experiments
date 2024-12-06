# This doesn't work as I had hoped :(
#  However, it demonstrates some interesting things:
#  1. bundling capacity can be used for fading. bundles can
#     be boosted to reinforce a sample or centroid. a bundle's
#     capacity can be distributed to some set of constituents
#     according to some set of weights
#  2. an HV can be shifted using substitute()
#     to shift a symbol, towards randomness, away from the concept
#     which it represents:
#       sub(concept_hv, hdv(), 99)[ round(concept_weight*100, 2) ]
#     to shift one concept half way, 50%, towards another concept:
#       sub(concept1_hv, concept2_hv, 99)[50]
#       sub(concept1_hv, concept2_hv, 2)[1]
#       sub(concept1_hv, concept2_hv, 9)[5]
#
# NOTE - there is no binding in this script, all bundling and leveling
# NOTE - bundling can accumulate noise, substitute (aka shift aka smear)
#        does not accumulate noise because it's based on a gradation/leveling/scale

import random
import sys; sys.path.insert(0, "../")
from utils import cossim, bundle, hdv, sub



# The stream of data samples
stream = []

# Total count of samples observed from the stream
timestep = 0

# Regions of density
centroids = []

# if a new sample is similar to an existing centroid by this
#  amount, it shift the centroid. a single new sample may
#  influence multiple centroids.
eps_radius = 0.2

# centroids are ensured to be this distance from each other
centroids_max_similarity = 0.8

# the minimum similarity to the time window required for a
#  centroid to not be expired
temporal_fade = 0.04

# the time window
time_window = hdv(all=0)

'''
# TODO - how to temporal fade centroid weights as new samples arrive?
#        we need to allow centroids to drift and forget the influence
#        of older samples

# each centroid has a corresponding density which fades with time
centroid_weights = []

# the minimum weight a centroid must have to be a cluster candidate
#  DBSCAN calls this minPts
min_cluster_weight = 3
'''


# The data stream
signal1 = hdv() # cluster1
signal2 = hdv() # cluster2
signal3 = hdv() # cluster3
signal4 = hdv() # not dense enough to form a cluster
signal5 = hdv() # too infrequent to form a cluster

stream.append(sub(signal5, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(sub(signal1, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal1, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(sub(signal2, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal1, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal1, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(sub(signal2, hdv(), 99)[random.choice(range(25))])

stream.append(hdv())
stream.append(sub(signal3, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal1, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal2, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal2, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(sub(signal1, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal3, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(sub(signal2, hdv(), 99)[random.choice(range(25))])

stream.append(hdv())
stream.append(hdv())
stream.append(sub(signal3, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(sub(signal1, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal3, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(hdv())
stream.append(sub(signal2, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal5, hdv(), 99)[random.choice(range(25))])

stream.append(sub(signal3, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(hdv())
stream.append(sub(signal2, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal1, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal3, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(sub(signal1, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(hdv())

stream.append(hdv())
stream.append(sub(signal1, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal3, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(sub(signal4, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal2, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal4, hdv(), 99)[random.choice(range(25))])
stream.append(sub(signal5, hdv(), 99)[random.choice(range(25))])
stream.append(hdv())
stream.append(hdv())


def ground_truth(hv):
  '''Find the ground truth for a sample or centroid'''
  if cossim(hv, signal1) >= eps_radius:
    return "signal1"
  elif cossim(hv, signal2) >= eps_radius:
    return "signal2"
  elif cossim(hv, signal3) >= eps_radius:
    return "signal3"
  elif cossim(hv, signal4) >= eps_radius:
    return "weak"
  elif cossim(hv, signal5) >= eps_radius:
    return "infrequent"
  else:
    return "noise"


def get_time(time_window, centroids):
  '''Show the distances of each centroid to the current time window'''
  return dict(zip([cossim(x, time_window) for x in centroids], [ground_truth(x) for x in centroids]))


def redistribute_time(time_window, centroids):
  '''Redistribute the time window to the current centroids'''
  weights = []
  for centroid in centroids:
    weights.append(cossim(centroid, time_window))
  maxi = max(weights)
  mini = min(weights)
  rang = maxi-mini
  normalized_weights = [100 * round((w - mini) / rang, 2) for w in weights]

  weighted_centroids = []
  for idx in range(len(normalized_weights)):
    weighted_centroid = sub(time_window, centroids[idx], 99)[ int(weights[idx]) ]
    weighted_centroids.append(weighted_centroid)
  return bundle(*weighted_centroids)


def expire(centroids, time_window):
  '''expire old centroids'''
  oldness = []
  # 1. find the old things
  for idx in range(len(centroids)):
    if cossim(centroids[idx], time_window) < temporal_fade:
      oldness.append(idx)
  # 2. delete the old things
  for idx in reversed(oldness):
    print(f'expiring centroid: {ground_truth(centroids[idx])}')
    del centroids[idx]
  # redistribute time window
  if len(oldness) > 0:
    time_window = redistribute_time(time_window, centroids)
  return centroids, time_window


def add_sample(new_sample):
  global centroids
  global eps_radius
  global centroids_max_similarity
  global temporal_fade
  global time_window
  global timestep

  centroids, time_window = expire(centroids, time_window)
  timestep += 1
  print(timestep, f'new sample: {ground_truth(new_sample)}')

  similar_centroids = []
  # find all centroids new_sample is similar to
  for idx in range(len(centroids)):
    centroid = centroids[idx]
    sim = cossim(new_sample, centroid)
    if sim >= eps_radius:
      similar_centroids.append(centroids[idx])

  # shift all similar centroids, or don't
  for idx in range(len(similar_centroids)):
    centroid = similar_centroids[idx]
    print(f'  belongs to existing: {ground_truth(centroid)}, {sim}')

    # attempt to move the centroid some percent closer to the new sample...
    new_centroid = sub(centroid, new_sample, 99)[75] # shift the centroid towards the new sample
    do_it = True

    # ... but don't shift the centroid if doing so causes it to become too close to another centroid
    for j_centroid in centroids:
      if cossim(new_centroid, j_centroid) > centroids_max_similarity:
        do_it = False
    if do_it:
      print(f'    moving centroid. old centroid: {ground_truth(centroid)}, new centroid: {ground_truth(new_centroid)}')
      centroids[idx] = new_centroid

      # learn the new centroid
      #  TODO - how do we unlearn the old centroid?
      time_window = bundle(time_window, new_centroid)

    else:
      print(f'    not moving centroid.')
      # don't move the centroid, but reinforce the sample
      time_window = bundle(time_window, centroid, sub(time_window, new_sample, 99)[25])

  # sample makes a new centroid
  if len(similar_centroids) == 0:
    centroids.append(new_sample)
    time_window = bundle(time_window, new_sample)
    print(f'  new centroid: {ground_truth(new_sample)}')

  time_window = redistribute_time(time_window, centroids)


# some things fade too fast and other fade too slow :(
for sample in stream:
  add_sample(sample)
  print(get_time(time_window, centroids))
  print()
