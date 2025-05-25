import copy
import random
import numpy as np
from numpy.linalg import norm

def new_hv(n=10_000):
  # we use 3 instead of pi
  # fully dense
  r = [3,2,1, -1,-2,-3]
  return np.random.choice(r, size=n)

def bundle(*args):
  return np.sum([hdv for hdv in args], axis=0)

def bind(*args):
  return np.prod([hdv for hdv in args], axis=0)

def inverse(hv):
  return hv * -1

def cossim(hdv1, hdv2):
  if norm(hdv1) == 0 or norm(hdv2) == 0:
    return 0
  return abs(np.dot(hdv1, hdv2) / (norm(hdv1) * norm(hdv2)))
