# This is sort of like a constrained integer variant of MAP.


import numpy as np

# ---------------------------------------------------------------------
# VSA constants
# ---------------------------------------------------------------------

POLE = 127.0
EPS = 1e-6


# ---------------------------------------------------------------------
# Symbol generation
# ---------------------------------------------------------------------

def new_hv(shape=(512, 512), rng=None):
    """
    Generate a random hypervector.

    Elements are uniformly distributed in [-127,127].
    Mean is approximately zero.
    """
    if rng is None:
        rng = np.random.default_rng()

    return rng.uniform(-POLE, POLE, size=shape).astype(np.float32)


# ---------------------------------------------------------------------
# Universal normalization
# ---------------------------------------------------------------------

def normalize(x):
    """
    Project an array back into the statistical space of a random symbol.

    Steps
    -----
    1. Remove DC bias.
    2. Normalize to unit variance.
    3. Scale so that ±3σ ≈ ±POLE.
       This means nearly all values lie inside the legal range while
       still using almost the full dynamic range.
    4. Clip remaining outliers.

    Every operation that changes statistics should end here.
    """

    x = x.astype(np.float32, copy=False)

    x = x - x.mean()

    std = x.std()
    if std > EPS:
        x = x / std

    x *= (POLE / 3.0)

    return np.clip(x, -POLE, POLE)


# ---------------------------------------------------------------------
# Identities
# ---------------------------------------------------------------------

def identity(shape=(512, 512)):
    """
    Multiplicative identity.

    bind(identity(), x) == x
    """
    return np.full(shape, POLE, dtype=np.float32)


def empty(shape=(512, 512)):
    """
    Additive identity.

    bundle(empty(), x) == x
    """
    return np.zeros(shape, dtype=np.float32)


# ---------------------------------------------------------------------
# Bundle
# ---------------------------------------------------------------------

def bundle(*vectors):
    """
    Element-wise addition with saturation.
    """

    result = np.sum(vectors, axis=0, dtype=np.float32)

    return np.clip(result, -POLE, POLE)


# ---------------------------------------------------------------------
# Bind
# ---------------------------------------------------------------------

def bind(a, b):
    """
    Element-wise multiplication.

    Multiplication changes the variance dramatically, so the result is
    normalized back into the symbol distribution.
    """

    return normalize((a * b) / POLE)


# ---------------------------------------------------------------------
# Approximate multiplicative inverse
# ---------------------------------------------------------------------

def inverse(a):
    """
    Approximate inverse for binding.

    Since bind uses multiplication, the algebraic inverse is reciprocal.

    Values near zero are clamped to avoid division by zero.
    """

    denom = np.where(np.abs(a) < EPS, EPS, a)

    return normalize(POLE / denom)


# ---------------------------------------------------------------------
# Unbind
# ---------------------------------------------------------------------

def unbind(bound, key):
    """
    Recover one constituent from a binding.
    """

    return bind(bound, inverse(key))


# ---------------------------------------------------------------------
# Similarity
# ---------------------------------------------------------------------

def cosine_similarity(a, b):

    aa = a.ravel()
    bb = b.ravel()

    return np.dot(aa, bb) / (
        np.linalg.norm(aa) *
        np.linalg.norm(bb)
    )

import numpy as np

np.random.seed(0)

print("\n==============================")
print("Generate random symbols")
print("==============================")

A = new_hv()
B = new_hv()
C = new_hv()

print("mean(A):", A.mean())
print("std(A): ", A.std())

print("A·B:", cosine_similarity(A, B))
print("A·C:", cosine_similarity(A, C))
print("B·C:", cosine_similarity(B, C))


print("\n==============================")
print("Bundle")
print("==============================")

AB = bundle(A, B)

print("bundle(A,B) -> A :", cosine_similarity(AB, A))
print("bundle(A,B) -> B :", cosine_similarity(AB, B))
print("bundle(A,B) -> C :", cosine_similarity(AB, C))


print("\n==============================")
print("Bind")
print("==============================")

BOUND = bind(A, B)

print("bind(A,B) -> A :", cosine_similarity(BOUND, A))
print("bind(A,B) -> B :", cosine_similarity(BOUND, B))
print("bind(A,B) -> C :", cosine_similarity(BOUND, C))

print("mean(bound):", BOUND.mean())
print("std(bound): ", BOUND.std())


print("\n==============================")
print("Recovery")
print("==============================")

recover_A = unbind(BOUND, B)
recover_B = unbind(BOUND, A)

print("recover A -> A :", cosine_similarity(recover_A, A))
print("recover A -> B :", cosine_similarity(recover_A, B))
print("recover A -> C :", cosine_similarity(recover_A, C))

print()

print("recover B -> B :", cosine_similarity(recover_B, B))
print("recover B -> A :", cosine_similarity(recover_B, A))
print("recover B -> C :", cosine_similarity(recover_B, C))


print("\n==============================")
print("Identity tests")
print("==============================")

I = identity()
Z = empty()

print("bind(I,A) :", cosine_similarity(bind(I, A), A))
print("bundle(Z,A):", cosine_similarity(bundle(Z, A), A))


print("\n==============================")
print("Repeated binding stability")
print("==============================")

X = new_hv()

for i in range(10):
    X = bind(X, new_hv())

print("mean:", X.mean())
print("std :", X.std())
print("range:", X.min(), X.max())



import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------

def to_image(hv):
    """
    Convert a hypervector in [-POLE, POLE] into an 8-bit grayscale image.
    """

    return np.clip(
        (hv + POLE) * (255.0 / (2.0 * POLE)),
        0,
        255,
    ).astype(np.uint8)


def show(hv, title="", ax=None):
    """
    Display a hypervector as an image.
    """

    if ax is None:
        _, ax = plt.subplots(figsize=(5, 5))

    ax.imshow(to_image(hv), cmap="gray", vmin=0, vmax=255)
    ax.set_title(title)
    ax.axis("off")

    return ax


def show_hist(hv, title="", ax=None):
    """
    Plot the value distribution of a hypervector.
    """

    if ax is None:
        _, ax = plt.subplots(figsize=(5, 3))

    ax.hist(
        hv.ravel(),
        bins=100,
        range=(-POLE, POLE),
        color="steelblue",
        edgecolor="black",
        linewidth=0.3,
    )

    ax.set_title(title)
    ax.grid(alpha=.3)

    return ax


def show_statistics(*named_vectors):
    """
    Print summary statistics for one or more hypervectors.

    Example
    -------
    show_statistics(
        ("A",A),
        ("B",B),
        ("Bind",BOUND)
    )
    """

    print()

    print(
        f"{'Name':<10}"
        f"{'Mean':>10}"
        f"{'Std':>10}"
        f"{'Min':>10}"
        f"{'Max':>10}"
    )

    print("-"*50)

    for name, hv in named_vectors:

        print(
            f"{name:<10}"
            f"{hv.mean():>10.2f}"
            f"{hv.std():>10.2f}"
            f"{hv.min():>10.1f}"
            f"{hv.max():>10.1f}"
        )
fig, ax = plt.subplots(2,3, figsize=(12,8))

show(A,"A",ax[0,0])
show(B,"B",ax[0,1])
show(C,"C",ax[0,2])

show_hist(A,"A",ax[1,0])
show_hist(B,"B",ax[1,1])
show_hist(C,"C",ax[1,2])

plt.tight_layout()
fig, ax = plt.subplots(2,3, figsize=(12,8))

show(A,"A",ax[0,0])
show(B,"B",ax[0,1])
show(AB,"Bundle(A,B)",ax[0,2])

show_hist(A,"A",ax[1,0])
show_hist(B,"B",ax[1,1])
show_hist(AB,"Bundle",ax[1,2])

plt.tight_layout()
fig, ax = plt.subplots(2,3, figsize=(12,8))

show(A,"A",ax[0,0])
show(B,"B",ax[0,1])
show(BOUND,"Bind(A,B)",ax[0,2])

show_hist(A,"A",ax[1,0])
show_hist(B,"B",ax[1,1])
show_hist(BOUND,"Bound",ax[1,2])

show_statistics(
    ("A",A),
    ("B",B),
    ("C",C),
    ("Bundle",AB),
    ("Bound",BOUND),
    ("Recover",recover_A),
)

plt.show()
