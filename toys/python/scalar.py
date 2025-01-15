# How can we get bind and bundle to behave like
#  multiply and add for integers?


from utils import hdv, bundle, bind, make_bins, cossim

# a vector of hypervectors, a space, which
#  preserves localilty
hyperspace = make_bins(n=10_000, bins=100)
one = hyperspace[1]
two = hyperspace[2]
three = hyperspace[3]
four = hyperspace[4]
five = hyperspace[5]
six = hyperspace[6]

print(cossim( bundle(two, two), four ))   # 2 + 2 = 4, true
print(cossim( bundle(two, three), five )) # 2 + 3 = 5, true
print(cossim( bind(two, three), six ))    # 2 * 3 = 6, false
