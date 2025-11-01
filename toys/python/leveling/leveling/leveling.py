# An Extension to Basis-Hypervectors for Learning from Circular Data in Hyperdimensional Computing
#  figure 3 and 6
# An Encoding Framework for Binarized Images using HyperDimensional Computing
#  figure 5

import copy
import random

import sys
sys.path.insert(0, '../../')
from utils import hdv, bundle, cossim, permute


def nonlinear_global_leveling(steps, hv1=hdv(), hv2=hdv()):
  '''A generalization of linear_local_leveling.
     Any number of steps and any sized step
  '''
  hyperspace = []
  major_levels = orthogonal_global_leveling(len(steps) + 1)

  for idx in range(len(major_levels)):
    if idx == len(major_levels) - 1:
      return hyperspace

    start = major_levels[idx]
    stop = major_levels[idx+1]
    lm = linear_global_leveling(steps[idx], start, stop)
    hyperspace.extend(lm)


def linear_local_leveling(hyperspace_length=1000, dims=10_000, splits=100):
  '''Numeric data. Nearby levels are similar.
     Values further outside of a localization window are maximally dissimilar.

     Similarity is based on the ratio of 2 numbers not their absolute difference
     See "The construction of large number representations in adults" and
       https://youtu.be/W2PY6z1Wddg?t=690
  '''
  hyperspace = []
  major_levels = orthogonal_global_leveling((hyperspace_length // splits) + 1)

  for idx in range(len(major_levels)):
    if idx == len(major_levels) - 1:
      return hyperspace

    start = major_levels[idx]
    stop = major_levels[idx+1]
    lm = linear_global_leveling(splits, start, stop)
    hyperspace.extend(lm)



def linear_global_leveling(hyperspace_length=1000, start=hdv(), stop=hdv()):
  '''Ordinal values. All levels have some amount of correlation.
  '''
  hyperspace = []
  hyperspace.append(start)
  dims = len(start)
  visited_elements = set([])
  elements_per_iteration = (dims // (hyperspace_length - 1))

  for i in range(1, hyperspace_length-1):
    next_level = copy.deepcopy(hyperspace[i-1])
    unvisited_elements = set(range(len(next_level))).difference(visited_elements)

    for j in random.sample(sorted(unvisited_elements), elements_per_iteration):
      visited_elements.add(j)
      next_level[j] = stop[j]

    hyperspace.append(next_level)
  hyperspace.append(stop)
  return hyperspace


# TODO - incorporate an 'r-value' so locality can be controlled.
#        currently this function is global only
def halfcircular_global_leveling(hyperspace_length=1000, start=hdv()):
  '''Angular values like color wheels, clocks, or gestures.
     Levels are correlated, then not, then yes again.
     The start hv is hv1, the stop hv is inverse(hv1).
  '''
  hyperspace = []
  hyperspace.append(start)
  dims = len(start)
  visited_elements = set([])
  elements_per_iteration = dims // hyperspace_length

  for i in range(1, hyperspace_length):
    next_level = copy.deepcopy(hyperspace[i-1])
    unvisited_elements = set(range(len(next_level))).difference(visited_elements)

    for j in random.sample(sorted(unvisited_elements), elements_per_iteration):
      visited_elements.add(j)
      next_level[j] = next_level[j] * -1

    hyperspace.append(next_level)
  return hyperspace



def orthogonal_global_leveling(hyperspace_length=1000, dims=10_000):
  '''Categorial variables. Levels are uncorrelated
  '''
  return[hdv(dims) for i in range(hyperspace_length)]



# These should have the same shape
#   ll = linear_local_mapping(200, 10_000, 50)
#   nl = nonlinear_global_mapping([50]*4)
