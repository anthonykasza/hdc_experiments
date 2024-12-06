# If vectors are single dimensional then set are zero dimensional.
# How would a Matrix Symbolic Architecture work? Block-codes?

# TODO - operation are not associative so analogy.py would never work
# TODO - what would a set-based memory look like?
# TODO - palendrone noise


# This is neat:
#  https://commons.wikimedia.org/wiki/File:Symmetric_group_4;_Cayley_graph_4,9.svg


import random
import copy


def symbol(dims=10, id=1):
  '''Return a symbol given an id'''
  ss = set( [each for each in range(dims+id, (dims**2)+dims+id, dims)] )
  return ss


def expand(elements, id, dims, thresh=2):
  '''
     Given elements, expand to the original symbol
  '''
  if len(elements) >= thresh:
    return symbol(dims, id)
  return set([])


def sim(s1, s2):
  '''The similarity of two symbols'''
  return len(s1.intersection(s2)) / len(s1)


def bundle(*args):
  '''Thinned union'''
  pick = len(args[0]) // len(args)
  s1 = copy.copy(args[0])
  for ss in args:
    ss = copy.copy(ss)
    for j in range(pick):
      s1.pop()
      s1.add(ss.pop())
  return s1


def subtract(s1, id, dims):
  elements = [element for element in s1 if element % len(s1) != id]
  return expand(elements, id, dims)


def bind(*args):
  '''Bundle then reverse as string'''
  s1 = bundle(*args)
  # cast int to string and reverse it
  return set( [int(str(element)[::-1]) for element in s1] )


def unbind(s1, id, dims):
  '''Undo bind'''
  result = [int(str(element)[::-1]) for element in s1]
  elements = [element for element in result if element % dims == id]
  return expand(elements, id, dims)
