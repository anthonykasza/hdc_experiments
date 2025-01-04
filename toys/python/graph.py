import copy
from utils import hdv, bind, bundle, cossim


'''
This is graph #1

      A   B       N         U--V--W--X--Y
       \ /       /         / \       \ /
        C-------I---K--L--M   |       |
       / \     /    |         |       |
      D   E   H     O--P--Q---T-------Z
           \ / \         / \
         G--F---J       R   S
'''


# Each vertex is asigned a unique label
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
vertex_to_symbol = {letter: hdv() for letter in letters}

# All of the relationships are unordered (undirected) pairs
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
edge_to_symbol = {(n1, n2): bind(vertex_to_symbol[n1], vertex_to_symbol[n2]) for (n1, n2) in edges}
edge_symbols = [edge_to_symbol[(n1, n2)] for (n1, n2) in edge_to_symbol]
graph1 = bundle(*edge_symbols)


'''
This is graph #2

      A   B       N         U--V--W--X  Y
       \ /       /         / \       \ /
        C-------I---K--L--M   |       |
         \     /    |         |       |
          E   H     O  P--Q---T-------Z
           \ / \         / \          |
         G--F---J       R   S         D
'''
edge_to_symbol2 = copy.deepcopy(edge_to_symbol)
# The C-D edge is removed in graph2
del edge_to_symbol2[("C", "D")]
# The O-P edge is removed in graph2
del edge_to_symbol2[("O", "P")]
# The X-Y edge is removed in graph2
del edge_to_symbol2[("X", "Y")]
# The Z-D edge is added in graph2
zd_edge = bind( vertex_to_symbol["Z"], vertex_to_symbol["D"] )
edge_to_symbol2[("Z", "D")] = zd_edge

edge_symbols2 = [edge_to_symbol2[(n1, n2)] for (n1, n2) in edge_to_symbol2]
graph2 = bundle(*edge_symbols2)


# the two graphs are similar are we expect
print( cossim(graph1, graph2) )


# this was a simple example where we had
#  nicely mapped vertex labels between the 2 graphs.
# how would we measure similarity between these 2 inputs?
'''
      *   *       *         *--*--*--*--*
       \ /       /         / \       \ /
        *-------*---*--*--*   |       |
       / \     /    |         |       |
      *   *   *     *--*--*---*-------*
           \ / \         / \
         *--*---*       *   *


     *     *------*---*-----*-----*
     |     |      |   |    / \
     *-----*      *   *---*   *
          / \         |    \ /
         *   *--*-----*     *
'''
# graphHD solved this by assigning vertex IDs by centrality (PageRank)
