from utils import cossim, hdv, sub


dims = 20
a = hdv(dims)
b = hdv(dims)

print(a)
print(b)
print()

levels = sub(a, b, dims//4)
for level in levels:
  print(cossim(level, a), cossim(level, b))
  print(level)
