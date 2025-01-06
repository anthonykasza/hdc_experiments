import sys; sys.path.insert(0, '../')
from utils import hdv, bind, bundle, cossim, unbind, permute

'''
      A   B       N         U--V--W--X--Y
       \ /       /         / \       \ /
        C-------I---K--L--M   |       |
       / \     /    |         |       |
      D   E   H     O--P--Q---T-------Z
           \ / \         / \
         G--F---J       R   S
'''

# this is a directed graph
suffix_directional = {
  'A': ('C'),
  'B': ('C'),
  'D': ('C'),
  'E': ('C', 'F'),
  'G': ('F'),
  'H': ('I', 'J'),
  'I': ('N', 'C'),
  'K': ('I', 'L'),
  'L': ('M'),
  'O': ('K', 'P'),
  'P': ('Q'),
  'R': ('Q'),
  'S': ('Q'),
  'T': ('Q', 'U', 'Z'),
  'U': ('M', 'V'),
  'V': ('W'),
  'W': ('X'),
  'X': ('Y', 'Z'),
  'Y': ('Z'),
}


letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
node_symbols = {letter: hdv() for letter in letters}
nodes = []
for src, destinations in suffix_directional.items():
  for dst in destinations:
    nodes.append(node_symbols[src])
    nodes.append(permute(node_symbols[dst]))
nodes = bundle(*nodes)

srcs = {}
dsts = {}
for letter in letters:
  hv = node_symbols[letter]
  is_this_node_a_src = cossim(nodes, hv)
  is_this_node_a_dst = cossim(nodes, permute(hv))
  if is_this_node_a_src > 0.1:
    srcs[is_this_node_a_src] = letter
  if is_this_node_a_dst > 0.1:
    dsts[is_this_node_a_dst] = letter

print("nodes with most outgoing edges")
for sim in sorted(srcs.keys(), reverse=True):
  letter = srcs[sim]
  print(letter, sim)

print("nodes with most incoming edges")
for sim in sorted(dsts.keys(), reverse=True):
  letter = dsts[sim]
  print(letter, sim)
