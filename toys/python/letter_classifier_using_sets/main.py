import copy
from utils import new_hv, add_hv, compare_hv, sub_hv


letters = 'abcdefghijklmnopqrstuvwxyz '
symbols = {k: new_hv() for k in letters}

space = symbols[' ']

a = symbols['a']
e = symbols['e']
i = symbols['i']
o = symbols['o']
u = symbols['u']
y = symbols['y']

b = symbols['b']
c = symbols['c']
d = symbols['d']
f = symbols['f']
g = symbols['g']
h = symbols['h']
j = symbols['j']
k = symbols['k']
l = symbols['l']
m = symbols['m']
n = symbols['n']
p = symbols['p']
q = symbols['q']
r = symbols['r']
s = symbols['s']
t = symbols['t']
v = symbols['v']
w = symbols['w']
x = symbols['x']
y = symbols['y']
z = symbols['z']

vowels = add_hv(a,e,i,o,u,y)
cons = add_hv(b,c,d,f,g,h,j,k,l,m,n,p,q,r,s,t,v,w,x,y,z)

# I dont understand why this doesn't work.
# The number of zeros (uncertainty) reduces when
#  we substract the opposite class but the accuracy reduces too.
# Perhaps we need to selectively subtract certain consonants from
#  the learned vowels class ONLY if there is some confusion...?
"""
print("vowels", vowels, sum([1 for i in vowels if i == 0]))
print("cons", cons, sum([1 for i in cons if i == 0]))
vowels_copy = copy.deepcopy(vowels)
cons_copy = copy.deepcopy(cons)
vowels = sub_hv(vowels, cons_copy)
cons = sub_hv(cons, vowels)
print("vowels", vowels, sum([1 for i in vowels if i == 0]))
print("cons", cons, sum([1 for i in cons if i == 0]))
"""


print(f'Is "a" in the set of vowels?      {round(compare_hv(a, vowels), 3)}\\t Yes')
print(f'Is "a" in the set of consonants?  {round(compare_hv(a, cons), 3)}\\t No')
print()
print(f'Is "b" in the set of vowels?      {round(compare_hv(b, vowels), 3)}\\t No')
print(f'Is "b" in the set of consonants?  {round(compare_hv(b, cons), 3)}\\t Yes')
print()
print(f'Is "y" in the set of vowels?      {round(compare_hv(y, vowels), 3)}\\t Yes')
print(f'Is "y" in the set of consonants?  {round(compare_hv(y, cons), 3)}\\t Yes')
print()
print(f'Is " " in the set of vowels?      {round(compare_hv(space, vowels), 3)}\\t No')
print(f'Is " " in the set of consonants?  {round(compare_hv(space, cons), 3)}\\t No')

