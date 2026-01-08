import numpy as np
from numpy.linalg import norm

def hdv(D=10_000, all=None):
  '''Symbols are noisy (normal) bipolar, and dense'''
  if all is not None:
    return np.full((1, D), all).flatten()
  n1 = np.random.normal(-1, 1/np.sqrt(D), D)
  n2 = np.random.normal(1, 1/np.sqrt(D), D)
  mask = np.random.rand(D) > 0.5
  return np.where(mask, n1, n2)

def cossim(h1, h2):
  if norm(h1) == 0 or norm(h2) == 0:
    return 0
  return abs(np.dot(h1, h2) / (norm(h1) * norm(h2)))

def clip(hv):
  '''Unbounded growth'''
  return hv



def bundle(*args):
  '''Sum'''
  return clip(np.sum([hdv for hdv in args], axis=0))

def partial_bundle(p):
  '''Sum or do nothing p% of the time'''
  def fn(*args):
    acc = hdv(all=0)
    for i in range(len(acc)):
      for hv in args:
        if np.random.rand() < p:
          acc[i] += hv[i]
    return clip(acc)
  return fn

def iterative_bundle(*args):
  '''Sum and clip after each hv'''
  acc = hdv(all=0)
  for hv in args:
    acc = acc + hv
    acc = clip(acc)
  return acc

def partial_iterative(p):
  '''Sum and clip after each hv or do nothing p% of the time'''
  def fn(*args):
    acc = hdv(all=0)
    for hv in args:
      for i in range(len(acc)):
        if np.random.rand() < p:
          acc[i] += hv[i]
      acc = clip(acc)
    return acc
  return fn

def randsel_bundle(*args):
  '''Concatenate elements from random inputs'''
  acc = hdv(all=0)
  for i in range(len(acc)):
    hv = args[np.random.randint(len(args))]
    acc[i] = hv[i]
  return clip(acc)

def partial_randsel(p):
  '''Concatenate elements from random inputs or do nothing p% of the time'''
  def fn(*args):
    acc = hdv(all=0)
    for i in range(len(acc)):
      if np.random.rand() < p:
        hv = args[np.random.randint(len(args))]
        acc[i] = hv[i]
    return clip(acc)
  return fn

def normal_dist_bundle(*args):
  '''Replace each element with a sample from a normal distribution around the element's value'''
  acc = hdv(all=0)
  D = len(acc)
  for i in range(len(acc)):
    for hv in args:
      acc[i] += np.random.normal(hv[i], 1 / np.sqrt(D))
  return clip(acc)

def partial_normal_dist(p):
  '''Replace each element with a sample from a normal distribution around the element's value or do nothing p% of the time'''
  def fn(*args):
    acc = hdv(all=0)
    D = len(acc)
    for i in range(len(acc)):
      if np.random.rand() < p:
        for hv in args:
          acc[i] += np.random.normal(hv[i], 1 / np.sqrt(D))
    return clip(acc)
  return fn

