# If vectors are single dimensional then set are zero dimensional.
# How would a Matrix Symbolic Architecture work? Block-codes?

# TODO - are operations associative?
# TODO - how to inverse a symbol? all elements * -1?
# TODO - are there identity symbols? empty set?


import random
import copy


def new(dims=10, id=1):
  '''Return a new symbol'''
  ss = set([])
  while len(ss) < dims:
    ss.add( (random.randint(0, (dims-1)) * dims) + id )
  return ss

def sim(s1, s2):
  '''
     The similarity of two symbols.
     Symbols do not need to be of the same size.
  '''
  return len(s1.intersection(s2)) / len(s1)

def bundle(s1, s2):
  '''Thinned union'''
  return set([element for element in s2.union(s1) if element <= (len(s1)**2)//2])

def subtract(s1, id):
  return set([element for element in s1 if element % len(s1) != id])

def bind(s1, s2):
  '''
     this is bundling but we modify the result's elements
     in a way that is reversible
  '''
  return set([int(str(element)[::-1]) for element in s2.union(s1) if element <= (len(s1)**2)//2])

def unbind(s1, id):
  '''reverse bind'''
  result = [int(str(element)[::-1]) for element in s1]
  return set([element for element in result if element % len(s1) == id])
