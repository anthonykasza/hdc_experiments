import sys; sys.path.insert(0, '../')
import random
import copy
from utils import hdv, bind, bundle, cossim, permute


def random_walk(suffix, min_len=2):
  '''make a random walk'''
  walk = []
  nodes = list(suffix.keys())
  walk.append(random.choice(nodes))
  while (True):
    walk.append(random.choice(nodes))
    # if there's a loop, remove the prev node and return the walk
    if len(walk) > min_len and len(walk) > len(set(walk)):
      walk.pop()
      return tuple(walk)

'''
      A   B       N         U--V--W--X--Y
       \ /       /         / \       \ /
        C-------I---K--L--M   |       |
       / \     /    |         |       |
      D   E   H     O--P--Q---T-------Z
           \ / \         / \
         G--F---J       R   S
'''

# a vertex's centrality is it's edge count
suffix = {
  'A': ('C'),
  'B': ('C'),
  'C': ('A', 'B', 'D', 'E'),
  'D': ('C'),
  'E': ('C', 'F'),
  'F': ('G', 'E', 'H', 'J'),
  'G': ('F'),
  'H': ('I', 'J', 'F'),
  'I': ('H', 'N', 'C', 'K'),
  'J': ('H', 'F'),
  'K': ('I', 'L', 'O'),
  'L': ('K', 'M'),
  'M': ('L', 'U'),
  'O': ('K', 'P'),
  'P': ('O', 'Q'),
  'Q': ('P', 'R', 'S', 'T'),
  'R': ('Q'),
  'S': ('Q'),
  'N': ('I'),
  'T': ('Q', 'U', 'Z'),
  'U': ('M', 'V', 'T'),
  'V': ('U', 'W'),
  'W': ('V', 'X'),
  'X': ('Y', 'W', 'Z'),
  'Y': ('X', 'Z'),
  'Z': ('X', 'Y', 'T')
}

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
vertex_symbols = {letter: hdv() for letter in letters}

# Make a bundle which represents many random walks of the graph
walk_count = 1_000
paths = []
paths_hv = hdv(all=0) #bundle identity

for idx in range(walk_count):
  path = random_walk(suffix)
  if path not in paths:
    paths.append(path)
    path_hv = hdv(all=1) #bind identity
    for vertex_idx in range(len(path)):
      vertex = path[vertex_idx]
      vertex_hv = permute(vertex_symbols[vertex], positions=[0,vertex_idx])
      path_hv = bind(path_hv, vertex_hv)
    paths_hv = bundle(paths_hv, path_hv)

print(f'we iterated over the graph {walk_count} times')
print(f'we found {len(paths)} unique random paths')
print('we bundled those paths into a single HV', paths_hv[0:3], paths_hv[-3:])


# Make a bundle which represents the graph
edges = [
  ("A", "C"),
  ("B", "C"),
  ("C", "D"), ("C", "E"),
  ("F", "G"), ("F", "J"), ("F", "H"),
  ("H", "J"), ("H", "I"),
  ("I", "N"), ("I", "K"),
  ("K", "L"), ("K", "O"),
  ("O", "P"),
  ("P", "Q"),
  ("Q", "R"), ("Q", "S"), ("Q", "T"),
  ("T", "U"), ("T", "Z"),
  ("L", "M"),
  ("M", "U"),
  ("U", "V"),
  ("V", "W"),
  ("W", "X"),
  ("X", "Y"), ("X", "Z"),
  ("Y", "Z"),
]
edge_to_symbol = {(n1, n2): bind(vertex_symbols[n1], vertex_symbols[n2]) for (n1, n2) in edges}
edge_symbols = [edge_to_symbol[(n1, n2)] for (n1, n2) in edge_to_symbol]
graph = bundle(*edge_symbols)


# the bundle representing all the random walks (bound ordered lists of nodes)
#   is not similar to the bundle of bound unordered node pairs
# i believe this is because the bound ordered node lists (walks)
#   contains directional informatin and may contain redundant info
#   as there is no filtering of subwalks
#    e.g. a random path A-B-C and B-C are considered different
#    and both are bundled into the paths_hv

print("we encoded the same graph in different ways and the results are not similar")
print( cossim(graph, paths_hv) )

