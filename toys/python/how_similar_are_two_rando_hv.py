
from utils import hdv, cossim

a = hdv()
i = 0

while (True):
  b = hdv()
  sim = cossim(a, b)
  if sim > 0.04:
    print(i, sim)
  i += 1
