import sys
sys.path.insert(0, '../')
from utils import hdv, bundle, bind, cossim
from utils import substitute as make_levels

# two linear progressions with the same start and stop
#  two different walks of the hyperspace
start = hdv(10_000)
stop = hdv(10_000)
levels1 = make_levels(start, stop, bins=100)
levels2 = make_levels(start, stop, bins=100)

# Compare the different walks, instead of going from
#  0 to 1, it goes from 1 to 0.5 then back up to 1
print(f'0: {cossim(levels1[0], levels2[0])}')
print(f'24: {cossim(levels1[24], levels2[24])}')
print(f'49: {cossim(levels1[49], levels2[49])}')
print(f'74: {cossim(levels1[74], levels2[74])}')
print(f'99: {cossim(levels1[99], levels2[99])}')
print()

# Bundle the two levelings together and see what happens
#  The trough is not as pronounced
levels_bundled = []
for idx in range(len(levels1)):
  levels_bundled.append( bundle(levels1[idx], levels2[idx]) )

print(f'0: {cossim(levels1[0], levels_bundled[0])}')
print(f'24: {cossim(levels1[24], levels_bundled[24])}')
print(f'49: {cossim(levels1[49], levels_bundled[49])}')
print(f'74: {cossim(levels1[74], levels_bundled[74])}')
print(f'99: {cossim(levels1[99], levels_bundled[99])}')

