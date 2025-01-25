from utils import cossim, hdv, substitute


dims = 20
a = hdv(dims)
b = hdv(dims)

print(a)
print(b)
print()

levels = substitute(a, b, dims//4)
for level in levels:
  print(cossim(level, a), cossim(level, b))
  print(level)
