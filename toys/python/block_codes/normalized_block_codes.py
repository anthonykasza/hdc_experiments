'''
Factorizers for Distributed Sparse Block Codes

"Like binary SBCs [Sparse Block Codes], GSBCs
 [Generalized Sparse Block Codes] divide the
 dimensional vectors into blocks of equal
 length. However, the individual blocks are
 not restricted to be binary or sparse."

Why did the authors name they GSBC is they aren't sparse?
'''



import random

def hdv_gsbc(dimensions=10_000, number_of_blocks=1000):
  h = []
  block_size = dimensions // number_of_blocks
  for block in range(number_of_blocks):
    tmp = [random.random() for x in range(block_size)]
    tmp_sum = sum(tmp)
    norm = [round(x/tmp_sum,2) for x in tmp]
    h.append(norm)
  return h


dimensions = 12
number_of_blocks = 4
h = hdv_gsbc(dimensions, number_of_blocks)
print(h)
