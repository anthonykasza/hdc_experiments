# If vectors are single dimensional then set are zero dimensional.
# How would a Matrix Symbolic Architecture work? Block-codes?

# TODO - are operations associative?
# TODO - how to inverse a symbol? all elements * -1?
# TODO - are there identity symbols? empty set?
# TODO - can we get better recovery rates of sub and unbind?
# TODO - what would a set-based memory look like?


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
  pick = len(s1) // 2
  s1 = copy.copy(s1)
  s2 = copy.copy(s2)
  s3 = set([])
  for j in range(pick):
    s3.add(s1.pop())
    s2.pop()
  return s3.union(s2)


def subtract(s1, id):
  '''
     Determine the max and min id and "recover" as much
     of the original symbol as possible.
  '''
  elements = [element for element in s1 if element % len(s1) != id]
  ma = max(elements)
  mi = min(elements)
  return set([each + id for each in range(mi, ma, len(s1))])

def bind(s1, s2):
  '''
     this is bundling but we modify the result's elements
     in a way that is reversible
  '''
  pick = len(s1) // 2
  s1 = copy.copy(s1)
  s2 = copy.copy(s2)
  s3 = set([])
  for j in range(pick):
    s3.add(s1.pop())
    s2.pop()
  s3 = s3.union(s2)
  # turn it to a string and reverse it
  return set( [int(str(element)[::-1]) for element in s3.union(s2)] )


def unbind(s1, id):
  '''reverse bind'''
  # TODO - use the same trick as in subtraction to
  #        "recover" more of the original symbol
  result = [int(str(element)[::-1]) for element in s1]
  elements = [element for element in result if element % len(s1) == id]
  ma = max(elements)
  mi = min(elements)
  return set([each + id for each in range(mi, ma, len(s1))])
