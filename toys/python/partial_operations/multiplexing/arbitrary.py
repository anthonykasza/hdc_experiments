# storing multiple bundles or bindings in disjoint subsets of a single hypervector

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
    """Cosine similarity between two hypervectors."""
    hv1_norm = norm(hv1)
    hv2_norm = norm(hv2)
    if hv1_norm == 0 or hv2_norm == 0:
        return 0.0
    cosine = np.dot(hv1, hv2) / (hv1_norm * hv2_norm)
    return (1 + cosine) / 2

# ----------------------------
# Generalized index-aware bind, bundle, unbind
# ----------------------------
def index_bind(hvs, start=0, modulus=2):
    """Bind hypervectors on selected indices."""
    prod = np.prod(hvs, axis=0)
    result = np.zeros_like(prod)
    idx = np.arange(start, prod.size, modulus)
    result[idx] = prod[idx]
    return result

def index_bundle(hvs, start=0, modulus=2):
    """Bundle hypervectors on selected indices."""
    summed = np.sum(hvs, axis=0)
    result = np.zeros_like(summed)
    idx = np.arange(start, summed.size, modulus)
    result[idx] = summed[idx]
    return result

def index_unbind(bound_hv, hvs, start=0, modulus=2):
    """Recover one hypervector from a bound hypervector at selected indices."""
    result = bound_hv.astype(float)
    idx = np.arange(start, bound_hv.size, modulus)
    for hv in hvs:
        result[idx] /= hv[idx]
    return result

# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    dims = 20_000

    # Create 4 hypervectors
    h1, h2, h3, h4 = new_hv(dims), new_hv(dims), new_hv(dims), new_hv(dims)

    # Pack 2 bundles in a single hypervector using modulus=4
    b0 = index_bundle([h1, h2], start=0, modulus=4)  # stored in indices 0,4,8,...
    b1 = index_bundle([h3, h4], start=1, modulus=4)  # stored in indices 1,5,9,...
    combined_bundle = b0 + b1  # single HV containing 2 bundles

    # Compare similarities
    print("Similarity h1 ↔ combined_bundle:", sim(h1, combined_bundle))
    print("Similarity h3 ↔ combined_bundle:", sim(h3, combined_bundle))

    # Bind example
    hb0 = index_bind([h1, h2], start=0, modulus=4)
    hb1 = index_bind([h3, h4], start=1, modulus=4)
    combined_bind = hb0 + hb1

    print("Similarity h1 ↔ combined_bind:", sim(h1, combined_bind))
    print("Similarity h3 ↔ combined_bind:", sim(h3, combined_bind))

    # Recover h1 from combined_bind
    recovered_h1 = index_unbind(hb0, [h2], start=0, modulus=4)
    print("Similarity h1 ↔ recovered_h1:", sim(h1, recovered_h1))

    # Show interference control
    hb0_mod2 = index_bind([h1, h2], start=0, modulus=2)  # covers even indices
    hb1_mod2 = index_bind([h3, h4], start=1, modulus=2)  # covers odd indices
    combined_mod2 = hb0_mod2 + hb1_mod2
    print("Similarity hb0_mod2 ↔ combined_mod2:", sim(hb0_mod2, combined_mod2))
    print("Similarity hb1_mod2 ↔ combined_mod2:", sim(hb1_mod2, combined_mod2))
