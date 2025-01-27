# How can we get bind and bundle to behave like
#  multiply and add for integers?


from utils import hdv, bundle, bind, make_levels, cossim

# a vector of hypervectors, a space, which
#  preserves localilty
hyperspace = make_levels(n=10_000, bins=100)
one = hyperspace[1]
two = hyperspace[2]
three = hyperspace[3]
four = hyperspace[4]
five = hyperspace[5]
six = hyperspace[6]

# the following two seem to behave as scalar math but it's only
#  because 2 is similar to 3 is simialr to 4
print("2 + 2 = 4", cossim( bundle(two, two), four ))
print("2 + 3 = 5", cossim( bundle(two, three), five ))

# if we increase distance between symbols within the space
#  then addition stops working
print("2 + 97 = 99", cossim( bundle(hyperspace[2], hyperspace[97]), hyperspace[99]))

# multiplying HVs does not behave as real numbers would neither
print("2 * 3 = 6", cossim( bind(two, three), six ))

