import sys; sys.path.insert(0, "../")
from utils import cossim, bundle, hdv, sub

red = hdv()
blue = hdv()
purples = sub(red, blue, 99)

# combining red and blue in different amounts makes different shades or purple
i = 0
for shade in purples:
  print(f'{i}    red: {cossim(shade, red)}, blue: {cossim(shade, blue)}')
  i += 1
print()

# "true" purple is about 50% red and 50% blue
purple = purples[49]
print(f'red: {cossim(purple, red)}, blue: {cossim(purple, blue)}')

