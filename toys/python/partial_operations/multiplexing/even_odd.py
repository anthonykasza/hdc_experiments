import numpy as np
from numpy.linalg import norm

# ----------------------------
# Hypervector creation
# ----------------------------
def new_hv(dims, low=-1, high=1):
    """Generate a new hypervector (non-zero integers)."""
    choices = np.arange(low, high + 1)
    choices = choices[choices != 0]
    return np.random.choice(choices, size=dims)

# ----------------------------
# Similarity
# ----------------------------
def sim(hv1, hv2):
    hv1_norm = norm(hv1)
    hv2_norm = norm(hv2)
    if hv1_norm == 0 or hv2_norm == 0:
        return 0.0
    cosine = np.dot(hv1, hv2) / (hv1_norm * hv2_norm)
    return (1 + cosine) / 2

# ----------------------------
# Bind and Unbind
# ----------------------------
def bind(*hvs, mode="all"):
    """
    Element-wise multiplication with optional index awareness.
    mode:
        - "all"  : multiply all indices (regular MAP)
        - "odd"  : multiply only odd indices (bind-sensitive)
        - "even" : multiply only even indices
    """
    prod = np.prod(hvs, axis=0)
    result = np.zeros_like(prod)
    if mode == "all":
        result[:] = prod
    elif mode == "odd":
        result[1::2] = prod[1::2]
    elif mode == "even":
        result[::2] = prod[::2]
    return result

def unbind(bound_hv, *hvs, mode="all"):
    """Recover one hypervector from bound hypervector using others."""
    result = bound_hv.astype(float)
    if mode == "all":
        for hv in hvs:
            result /= hv
    elif mode == "odd":
        for hv in hvs:
            result[1::2] /= hv[1::2]
    elif mode == "even":
        for hv in hvs:
            result[::2] /= hv[::2]
    return result

# ----------------------------
# Bundle
# ----------------------------
def bundle(*hvs, mode="all"):
    """
    Element-wise addition with optional index awareness.
    mode:
        - "all"  : sum all indices (regular MAP)
        - "odd"  : sum only odd indices
        - "even" : sum only even indices (bundle-sensitive)
    """
    summed = np.sum(hvs, axis=0)
    result = np.zeros_like(summed)
    if mode == "all":
        result[:] = summed
    elif mode == "odd":
        result[1::2] = summed[1::2]
    elif mode == "even":
        result[::2] = summed[::2]
    return result

# ----------------------------
# Example: Index-aware interference
# ----------------------------
if __name__ == "__main__":
    dims = 20_000

    h1, h2, h3, h4 = new_hv(dims), new_hv(dims), new_hv(dims), new_hv(dims)
    noise = new_hv(dims)

    print('binding on even')
    b1 = bind(h1, h2, mode="even")
    b2 = bind(h3, h4, mode="even")

    odd_bundle = bundle(b1, b2, mode="odd")
    even_bundle = bundle(b1, b2, mode="even")
    all_bundle = bundle(b1, b2, mode="all")

    print('sim(odd_bundle, h1)', sim(odd_bundle, h1))
    print('sim(odd_bundle, b1)', sim(odd_bundle, b1))
    print('sim(odd_bundle, noise)', sim(odd_bundle, noise))
    print()

    print('sim(even_bundle, h1)', sim(even_bundle, h1))
    print('sim(even_bundle, b1)', sim(even_bundle, b1))
    print('sim(even_bundle, noise)', sim(even_bundle, noise))
    print()

    print('sim(all_bundle, h1)', sim(all_bundle, h1))
    print('sim(all_bundle, b1)', sim(all_bundle, b1))
    print('sim(all_bundle, noise)', sim(all_bundle, noise))
    print()

    print('sim(odd_bundle, all_bundle)', sim(odd_bundle, all_bundle))
    print('sim(even_bundle, all_bundle)', sim(even_bundle, all_bundle))
    print('sim(odd_bundle, even_bundle)', sim(odd_bundle, even_bundle))
    print()

    e_b = bundle(h1, h2, mode="even")
    o_b = bundle(h1, h2, mode="odd")
    print(sim(e_b, o_b))
