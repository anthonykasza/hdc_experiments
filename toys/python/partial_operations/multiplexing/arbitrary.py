# storing multiple bundles or bindings in disjoint subsets of a single hypervector

import numpy as np
from numpy.linalg import norm
import copy

# ----------------------------
# Hypervector creation
# ----------------------------
def new_hv(dims, low=-1, high=1, fill=None):
    """Generate a new hypervector (non-zero integers)."""
    if fill is not None:
      return np.array([fill] * dims)
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
    prodded = np.prod(hvs, axis=0)
    result = copy.copy(hvs[0])
    result[start::modulus] = prodded[start::modulus]
    return result


def index_bundle(hvs, start=0, modulus=2):
    """Bundle hypervectors on selected indices."""
    summed = np.sum(hvs, axis=0)
    result = copy.copy(hvs[0])
    result[start::modulus] = summed[start::modulus]
    return result


def index_unbind(h1, h2, start=0, modulus=2):
    """Recover one hypervector from a bound hypervector at selected indices."""
    result = copy.copy(h1.astype(float))
    ih2 = inverse(h2)
    result[start::modulus] = result[start::modulus] * ih2[start::modulus]
    return result

def inverse(hv):
    return np.array([1/x for x in hv])
def boring_bundle(hvs):
    """Boring old bundle"""
    return np.sum(hvs, axis=0)
def boring_bind(hvs):
    """Boring old bind"""
    return np.prod(hvs, axis=0)
def boring_unbind(h1, h2):
    """Boring old unbind"""
    return boring_bind([h1, inverse(h2)])

# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":

    # Example 1 ----------------------------
    print('Example 1')
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
    recovered_h1 = index_unbind(hb0, h2, start=0, modulus=4)
    print("Similarity h1 ↔ recovered_h1:", sim(h1, recovered_h1))

    # Show interference control
    hb0_mod2 = index_bind([h1, h2], start=0, modulus=2)  # covers even indices
    hb1_mod2 = index_bind([h3, h4], start=1, modulus=2)  # covers odd indices
    combined_mod2 = hb0_mod2 + hb1_mod2
    print("Similarity hb0_mod2 ↔ combined_mod2:", sim(hb0_mod2, combined_mod2))
    print("Similarity hb1_mod2 ↔ combined_mod2:", sim(hb1_mod2, combined_mod2))
    print()
    print()



    # Example 2 ----------------------------
    print('Example 2')
    dims = 20_000

    # The accumulator
    acc = new_hv(dims=dims, fill=0)

    # signals and noise
    h0, h1, h2, hall, noise = new_hv(dims), new_hv(dims), new_hv(dims), new_hv(dims), new_hv(dims)

    # 1 third of the accumulator represents h0
    acc = index_bundle([acc, h0], start=0, modulus=3)
    print(f'First index bundled in {acc[0:9]}')

    # 1 third of the accumulator represents h1
    acc = index_bundle([acc, h1], start=1, modulus=3)
    print(f'Second index bundled in {acc[0:9]}')

    # 1 third of the accumulator represents h3
    acc = index_bundle([acc, h2], start=2, modulus=3)
    print(f'Third index bundled in {acc[0:9]}')

    # 1 third of the accumulator represents h0 and hall,
    # 1 third of the accumulator represents h1 and hall,
    # 1 third of the accumulator represents h2 and hall,
    # I think this is the same as randsel bundling of 3 constituents
    #  combined with regular element-wise bundling
    acc = boring_bundle([acc, hall])
    print(f'All indices influenced by hall {acc[0:9]}')

    print()
    print(f'acc, h0 {sim(acc, h0)}')
    print(f'acc, h1 {sim(acc, h1)}')
    print(f'acc, h2 {sim(acc, h2)}')
    print(f'acc, hall {sim(acc, hall)}')
    print(f'acc, noise {sim(acc, noise)}')
    print()

    # Example 2 Results ----------------------------
    #
    # h0, h1, and h3 have some correlation with the accumulator
    #  in comparison to noise and the accumulator.
    #  However, hall is very similar to accumulator, the most so.
    # The results appear to be similar to weighted bundling.
    # How should normalization/clipping be done?
    #  What about index_clip() ?
    #  What about index_similarity() ?
    #
    # acc, h0    0.6203
    # acc, h1    0.6196
    # acc, h2    0.6128
    # acc, hall  0.8527
    # acc, noise 0.5044


    # Example 3 ----------------------------
    print('Example 3')
    dims = 20_000

    # The accumulator
    acc = new_hv(dims=dims, fill=1)

    # signals and noise
    h0, h1, h2, hall, noise = new_hv(dims), new_hv(dims), new_hv(dims), new_hv(dims), new_hv(dims)

    # 1 third of the accumulator represents h0
    acc = index_bind([acc, h0], start=0, modulus=3)
    print(f'First index binded in {acc[0:9]}')

    # 1 third of the accumulator represents h1
    acc = index_bind([acc, h1], start=1, modulus=3)
    print(f'Second index binded in {acc[0:9]}')

    # 1 third of the accumulator represents h3
    acc = index_bind([acc, h2], start=2, modulus=3)
    print(f'Third index binded in {acc[0:9]}')

    acc = boring_bind([acc, hall])
    print(f'All indices influenced by hall {acc[0:9]}')

    print()
    recovered_h0 = index_unbind(acc, h0, start=0, modulus=3)
    print(f'recovered h0 {sim(recovered_h0, h0)}')
    recovered_h1 = index_unbind(acc, h1, start=1, modulus=3)
    print(f'recovered h1 {sim(recovered_h1, h1)}')
    recovered_h2 = index_unbind(acc, h2, start=2, modulus=3)
    print(f'recovered h2 {sim(recovered_h2, h2)}')
    recovered_hall = index_unbind(index_unbind(index_unbind(acc, h0, start=0, modulus=3), h1, start=1, modulus=3), h2, start=2, modulus=3)
    print(f'recovered hall {sim(recovered_hall, hall)}')
    print(f'recovered noise {sim(boring_unbind(acc, noise), noise)}')

    # Example 3 Results ----------------------------
    #
    # The final boring_bind() makes the previous index_bind()
    #  appear as noise.
    #
    # recovered h0 0.5021
    # recovered h1 0.4994
    # recovered h2 0.50035
    # recovered hall 1.0
    # recovered noise 0.4984
