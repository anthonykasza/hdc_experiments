import sys; sys.path.insert(0, "../")
from utils import hdv, cossim, sub, inverse

dims = 10


############################################

a = hdv(dims, all=0)
b = hdv(dims, all=1)

print(f'a {a}')
print(f'b {b}')
print(f'cossim(a, b) {cossim(a, b)}')
print('randomly move all 0s to be more like all 1s')
levels = sub(a, b, dims)
for level in levels:
  print(f'  {level}')
print()

############################################

a = hdv(dims)
b = hdv(dims)

print(f'a {a}')
print(f'b {b}')
print(f'cossim(a, b) {cossim(a, b)}')
print('randomly move a to be more like b')
levels = sub(a, b, dims)
for level in levels:
  print(f'  {level}')
print()


print(f'inverse(b) {inverse(b)}')
print(f'cossim(a, inverse(b)) {cossim(a, inverse(b))}')
print(f'cossim(b, inverse(b)) {cossim(b, inverse(b))}')
print('randomly move a to be less like b')
levels = sub(a, inverse(b), dims)
for level in levels:
  print(f'  {level}')
print()


# Why is cossim(b, inverse(b)) so close to 1? Recall, we're using a
#  bipolar architecture

# What would happen if `dims` was larger?
