# With great help from the LLMs, bind/unbind appear to function

import sys
import numpy as np

class BSBC:
  def __init__(self, num_blocks=128, block_size=64):
    self.num_blocks = num_blocks
    self.block_size = block_size
    self.dimensions = num_blocks * block_size
    # it seems num_blocks influences the precision of cossim
    # it seems (block_size / num_blocks) influences crosstalk

  def hdv(self):
    """
    Generate a random hypervector of 1-hot blocks.
    """
    hv = np.zeros(self.dimensions, dtype=int)
    one_positions = np.random.randint(0, self.block_size, size=self.num_blocks)
    hv.reshape(self.num_blocks, self.block_size)[
      np.arange(self.num_blocks), one_positions
    ] = 1
    return hv

  def compress(self, hv):
    """
    Return the hot indices of each block.
    """
    hv_blocks = hv.reshape(self.num_blocks, self.block_size)
    return np.argmax(hv_blocks, axis=1)

  def bind(self, A, B, alpha=1):
    """
    Circularly shift B's blocks by A's indices (times alpha)
    """
    B_blocks = B.reshape(self.num_blocks, self.block_size)
    a_s = self.compress(A)
    shifts = (alpha * a_s) % self.block_size
    j = np.arange(self.block_size)
    idx = (j[None, :] - shifts[:, None]) % self.block_size
    C_blocks = B_blocks[np.arange(self.num_blocks)[:, None], idx]
    return C_blocks.reshape(self.dimensions)

  def unbind(self, A, C, alpha=1):
    """
    Circularly shift C's blocks by A's indices (times alpha)
    """
    C_blocks = C.reshape(self.num_blocks, self.block_size)
    a_s = self.compress(A)
    shifts = (alpha * a_s) % self.block_size
    j = np.arange(self.block_size)
    idx = (j[None, :] + shifts[:, None]) % self.block_size
    B_blocks = C_blocks[np.arange(self.num_blocks)[:, None], idx]
    return B_blocks.reshape(self.dimensions)

  def cosine_similarity(self, A, B):
    """Compute cosine similarity between two hypervectors."""
    A = A.astype(float)
    B = B.astype(float)
    return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))

  def bundle(self, hypervectors):
    """
    Bundle multiple into a single hypervector. The bundle is
    similar to each input.
    """
    H = np.array(hypervectors)
    assert H.shape[1] == self.dimensions, "Dimension mismatch"
    sumset_blocks = np.sum(H, axis=0).reshape(self.num_blocks, self.block_size)
    max_vals = np.max(sumset_blocks, axis=1, keepdims=True)
    mask = (sumset_blocks == max_vals)
    random_matrix = np.random.rand(self.num_blocks, self.block_size)
    random_matrix[~mask] = -1
    selected_indices = np.argmax(random_matrix, axis=1)
    bundled = np.zeros_like(H[0])
    bundled_blocks = bundled.reshape(self.num_blocks, self.block_size)
    bundled_blocks[np.arange(self.num_blocks), selected_indices] = 1
    return bundled


def main():
  block_size = int(sys.argv[1])
  num_blocks = int(sys.argv[2])
  print(f'Block size: {block_size}')
  print(f'Number of blocks: {num_blocks}')
  print(f'Total hv dimensions: {block_size * num_blocks}')
  print()

  # Test generation
  bsbc = BSBC(num_blocks=num_blocks, block_size=block_size)
  A = bsbc.hdv()
  B = bsbc.hdv()
  print("Uncompressed B, the first 4 blocks")
  print(B[0:block_size * 4])
  print()

  # Test compression
  B_compressed = bsbc.compress(B)
  print(f'Compressed B has length: {len(B_compressed)}')
  print(B_compressed)
  print()

  # Test binding recoverability
  C = bsbc.bind(A, B, alpha=1)
  B_rec = bsbc.unbind(A, C, alpha=1)
  print("A to C similarity", bsbc.cosine_similarity(A, C))
  print("B to C similarity", bsbc.cosine_similarity(B, C))
  print("A to B_rec similarity", bsbc.cosine_similarity(A, B_rec))
  print("C to B_rec similarity", bsbc.cosine_similarity(C, B_rec))
  print("B to B_rec similarity", bsbc.cosine_similarity(B, B_rec))
  print()

  # Test bundle similarity
  hv_list = [bsbc.hdv() for _ in range(5)]
  bundled_hv = bsbc.bundle(hv_list)
  for i, hv in enumerate(hv_list):
    sim = bsbc.cosine_similarity(hv, bundled_hv)
    print(f"Cosine similarity between HV {i} and bundle: {sim:.4f}")
  noise = bsbc.hdv()
  sim = bsbc.cosine_similarity(noise, bundled_hv)
  print(f"Cosine similarity between NOISE and bundle: {sim:.4f}")



if __name__ == "__main__":
    main()
