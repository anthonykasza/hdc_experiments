We present a fuzzy generalization of Binary Sparse Block Codes (BSBCs) that incorporates explicit uncertainty at the block level. In our approach, each block stores not only an index but also a variance term σ, which is propagated through binding, unbinding, and bundling operations. This allows the hypervector to encode probabilistic information, enabling smooth degradation under superposition and interference. Our main innovation is the explicit tracking of block uncertainty (σ), which adds a probabilistic semantics not present in either traditional Binary SBCs or prior GSBC formulations, resulting in more robust memory retrieval and graceful failure behavior.


| Operation      | Binary SBC (Laiho et al.) | GSBC (Hersche et al.)       | Fuzzy BSBC (this work)                            |
| -------------- | ----------------------  | --------------------------- | ------------------------------------------------- |
| **Binding**    | Modulo‑L sum of indices | Blockwise circular convolution | Blockwise modular addition with σ accumulation   |
| **Unbinding**  | Modulo‑L difference of indices | Blockwise circular correlation | Blockwise modular negation (inverse) of indices, σ unchanged |
| **Bundling**   | Argmax / winner-take-all | Sum and normalization       | Circular mean with dispersion-based σ            |
| **Similarity** | Dot product or ℓ∞-based | Dot product                | Gaussian-kernel similarity weighted by σ         |



### Intuition for σ (fuzzy BSBC blocks)

Each block stores **where the symbol is (μ)** and **how sure we are (σ)**.
σ turns a sharp 1-hot index into a *blur of confidence* around that index.

As σ grows, **confidence spreads outward from the hot bit**.
Bundling increases σ when inputs disagree, binding preserves σ, and similarity degrades smoothly as σ becomes large relative to block size.

---

Legend:
- █ = hot bit (highest confidence)
- ▓ = very likely
- ░ = somewhat likely
- ▁ = very unlikely

Block size: 16

---

#### σ = 0 (exact, classic BSBC)
```
  |▁▁▁▁▁▁▁▁█▁▁▁▁▁▁▁|
   0123456789012345
```

*It is exactly at 8.*

---

#### σ = small (slight uncertainty)
```
  |▁▁▁▁▁▁░▓█▓░▁▁▁▁▁|
   0123456789012345
```

*"Probably at 8, maybe one slot off.*

---

#### σ = medium (bundling with partial agreement)
```
  |▁▁▁░▓▓████▓▓░▁▁▁|
   0123456789012345
```

*Several inputs mostly agree that 8 is hot.*

---

#### σ = large (heavy interference)
```
  |▁░▓▓████████▓▓░▁|
   0123456789012345
```

*Some index near the 'middle' of the block is hot but the exact position is unclear.*

---

#### σ ≈ block_size / 2 (information collapse)
```
  |▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓|
   0123456789012345
```

*Every position is equally plausible.*
This can occur when bundling maximally different blocks.

  Inputs:
```
  |▁▁▁▁▁▁▁▁█▁▁▁▁▁▁▁|   (8)

  |█▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁|   (0)
   0123456789012345
```
  Result:
```
  |▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓|   (?)
   0123456789012345
```

---


What happens if the blocks support more than 1 fuzzy hot bit?
What happens if we use modular integer averaging instead of angle averaging for bundling?
