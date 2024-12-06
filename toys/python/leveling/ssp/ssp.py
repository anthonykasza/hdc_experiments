# See: "A neural representation of continuous space using fractional binding"

# This isn't really spatial semantic pointers but a cool thing
#  about HDC is that you can be close to correct and things still
#  sort of work.

from utils import bind, bundle, new_hv, cossim, inverse


# This does power encoding but not fractional power encoding
#  I believe FPE uses an additional multiplication/scaling operation
#  on the basis
def ssp_make_levels(basis_hv, exp):
  if exp == 1:
    return list(basis_hv)

  levels = [basis_hv]
  while exp > 1:
    exp -= 1
    previous_level = levels[len(levels)-1]
    levels.append(bind(previous_level, basis_hv))
  return levels


# Unexpectedly, it seems to work less well with more dimensions.
dims = 10_000
dims = 333
red = new_hv(dims)
blue = new_hv(dims)
green = new_hv(dims)

square = new_hv(dims)
circle = new_hv(dims)
triangle = new_hv(dims)

big = new_hv(dims)
small = new_hv(dims)
medium = new_hv(dims)

x = ssp_make_levels(new_hv(dims), 14)
y = ssp_make_levels(new_hv(dims), 6)


print('    ----------------')
print('5   |  1           |    1 big red square')
print('4   |              |')
print('3   |    2    3    |    2 small blue square, 3 big red triangle')
print('2   |              |')
print('1   |        4     |    4 medium green circle')
print('0   |5             |    5 big blue triangle')
print('    ----------------')
print('     01234567890123')

object1 = bind(big, red, square)
object2 = bind(small, blue, square)
object3 = bind(big, red, triangle)
object4 = bind(medium, green, circle)
object5 = bind(big, blue, triangle)

obj_loc1 = bind(object1, x[2], y[5])
obj_loc2 = bind(object2, x[4], y[3])
obj_loc3 = bind(object3, x[9], y[3])
obj_loc4 = bind(object4, x[8], y[1])
obj_loc5 = bind(object5, x[0], y[0])

scene = bundle(obj_loc1, obj_loc2, obj_loc3, obj_loc4, obj_loc5)

print(f'where is the big red triangle (object 3 at 9,3)?')
query = bind(big, red, triangle)
print(f'similarity between object3 and query: {cossim(object3, query)}')
result = bind(scene, inverse(query))

# guesses are superposed
x_guess = bind(result, inverse(bundle(*y)))
y_guess = bind(result, inverse(bundle(*x)))

# exhaustive search to find best matching level
x_max = -1
x_max_idx = -1
for idx in range(len(x)):
  sim = cossim(x[idx], x_guess)
  print('  x', idx, sim)
  if sim > x_max:
    x_max = sim
    x_max_idx = idx

y_max = -1
y_max_idx = -1
for idx in range(len(y)):
  sim = cossim(y[idx], y_guess)
  print('  y', idx, sim)
  if sim > y_max:
    y_max = sim
    y_max_idx = idx

# It is sometimes correct but seems to have difficult on the x axis
#  Run the script a few times and you may get different x_max_idx
#  and y_max_idx values
print('inferred location', x_max_idx, y_max_idx)
