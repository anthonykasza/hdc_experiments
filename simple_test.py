from utils import *

n = 100
v = hdv(n=n)
print(f'hdv length should equal {n}, {len(v) == n}')
print(f'hdv values should be approximately random, {np.sum(v) < (n * 0.25) and np.sum(v) > (n * -0.25)}')

a = [0, 1, -1]
b = [0, 2, -2]
print(all(clip(a) == [0, 1, -1]), "clip a")
print(all(clip(b) == [0, 1, -1]), "clip b")

a = hdv(10_000)
b = hdv(10_000)
c = hdv(10_000)
abc_bundle = bundle(a, b, c)
print(cossim(abc_bundle, a), "cossim abc_bundle a")
print(cossim(abc_bundle, b), "cossim abc_bundle b")
print(cossim(abc_bundle, c), "cossim abc_bundle c")

ab_bind = bind(a, b)
print(cossim(ab_bind, a), "cossim ab_bind a")
print(cossim(ab_bind, b), "cossim ab_bind b")
print(all(unbind(ab_bind, a) == b), "unbind ab_bind a == b")
print(all(unbind(ab_bind, b) == a), "unbind ab_bind b == a")

abc_bind = bind(a, b, c)
print(cossim(abc_bind, a), "cosim abc_bind a")
print(cossim(abc_bind, b), "cosim abc_bind b")
print(cossim(abc_bind, c), "cosim abc_bind c")

print(cossim(unbind(abc_bind, a), b), "cossim unbind(abc_bind, a), b")
print(cossim(unbind(abc_bind, a), c), "cossim unbind(abc_bind, a), c")
print(cossim(unbind(abc_bind, ab_bind), c), "cossim unbind(abc_bind, ab_bind), c")
