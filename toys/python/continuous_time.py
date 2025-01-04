import time
import copy
import numpy as np

from utils import hdv, cossim, substitute


memory_max_size = 10
memory = []

now = time.time()
start = now
now_symbol = hdv()
memory.append(now_symbol)

while (True):
  # events occur randomly but we ensure at least 2 steps
  #  pass between 2 consecutive events
  time.sleep(np.random.choice(range(5)) + 2)

  prev = now
  prev_symbol = memory[-1]
  now = time.time()
  now_symbol = hdv()

  for level_symbol in substitute(prev_symbol, now_symbol, int(now-prev)):
    memory.append(level_symbol)
  memory = memory[-memory_max_size:]

  print(int(now-start), [cossim(memory[-1], x) for x in memory])
