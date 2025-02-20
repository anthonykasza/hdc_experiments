import time
import copy
import numpy as np

from utils import hdv, cossim, substitute, permute


memory = []
dims = 15
now_symbol = hdv(dims)
memory.append(now_symbol)
step_count = 0
perm_count = 0

while (True):

  if step_count >= dims:
    step_count = step_count - dims
    now_symbol = permute(now_symbol, 1)
    perm_count += 1

    if perm_count >= dims:
      print("ran out of bits")
      break

  now_symbol[step_count] = now_symbol[step_count] * -1
  memory.append(copy.deepcopy(now_symbol))
  step_count += 1

for each in memory:
  print(each)

print("number of timesteps", len(memory))
print("first to last", cossim(memory[0], memory[-1]) )
print("first to perm(last)", cossim(memory[0], permute(memory[-1])) )
