
from utils import hdv, cossim

# the more dimensions, the more accuracy, the more capacity
dims = 100000
a = hdv(dims)
i = 0

while (True):
  b = hdv(dims)
  sim = cossim(a, b)
  if sim > 0.01:
    print(i, sim)
  i += 1
