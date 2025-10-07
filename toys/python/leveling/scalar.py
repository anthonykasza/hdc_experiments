# How can we get bind and bundle to behave like
#  multiply and add for integers?

# NOTE: all combinations of HV in this sscript are from
#  the same hyperspace. Combining levels from different
#  hyperspaces behaves differently than these examples.

import sys
sys.path.insert(0, '../')
from utils import hdv, bundle, bind, make_levels, cossim

hyperspace = make_levels(n=10_000, bins=100)
zed = hyperspace[0] # should the first level be 0 or 1?
one = hyperspace[1]
two = hyperspace[2]
three = hyperspace[3]
four = hyperspace[4]
five = hyperspace[5]
six = hyperspace[6]
ten = hyperspace[10]
fifty = hyperspace[50]
ninetythree = hyperspace[93]
ninetynine = hyperspace[99]

def find_most_similar_level(hv, levels):
  max_sim = -1
  max_sim_idx = -1
  for idx in range(len(hyperspace)):
    level = hyperspace[idx]
    if cossim(level, result) > max_sim:
      max_sim = cossim(level, result)
      max_sim_idx = idx
  return max_sim, max_sim_idx

print('adding levels which are near to each other')
print("2 + 2 = 4", cossim( bundle(two, two), four ))
print("2 + 3 = 5", cossim( bundle(two, three), five ))
print("0 + 0 = 0", cossim( bundle(zed, zed), zed ))
print()

print('adding levels which are far from each other')
result = bundle(six, ninetythree)
max_sim, max_sim_idx = find_most_similar_level(result, hyperspace)
print("6 + 93 = 99", cossim(result, ninetynine))
print(f'  the level most similar to 6 + 93 is: {max_sim_idx}, with sim: {max_sim}')
print()
print()

print('multiplying levels')
result = bind(two, three)
max_sim, max_sim_idx = find_most_similar_level(result, hyperspace)
print("2 * 3 = 6", cossim(result, six))
print(f'  the level most similar to 2 * 3 is: {max_sim_idx}, with sim: {max_sim}')
print()

result = bind(five, ten)
max_sim, max_sim_idx = find_most_similar_level(result, hyperspace)
print("5 * 10 = 50", cossim(result, fifty))
print(f'  the level most similar to 5 * 10 is: {max_sim_idx}, with sim: {max_sim}')
print()

result = bind(zed, zed)
max_sim, max_sim_idx = find_most_similar_level(result, hyperspace)
print("0 * 0 = 0", cossim(result, zed))
print(f'  the level most similar to 0 * 0 is: {max_sim_idx}, with sim: {max_sim}')
print()

print('why is the same idx sometimes the best match for more than 1 example?')
