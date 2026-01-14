We present a fuzzy generalization of Binary Sparse Block Codes (BSBCs) that incorporates explicit uncertainty at the block level. In our approach, each block stores not only an index but also a variance term σ, which is propagated through binding, unbinding, and bundling operations. This allows the hypervector to encode probabilistic information, enabling smooth degradation under superposition and interference. Our main innovation is the explicit tracking of block uncertainty (σ), which adds a probabilistic semantics not present in either traditional Binary SBCs or prior GSBC formulations, resulting in more robust memory retrieval and graceful failure behavior.


| Operation      | Binary SBC (Laiho et al.) | GSBC (Hersche et al.)       | Fuzzy BSBC (this work)                            |
| -------------- | ----------------------  | --------------------------- | ------------------------------------------------- |
| **Binding**    | Modulo‑L sum of indices | Blockwise circular convolution | Blockwise modular addition with σ accumulation   |
| **Unbinding**  | Modulo‑L difference of indices | Blockwise circular correlation | Blockwise modular negation (inverse) of indices, σ unchanged |
| **Bundling**   | Argmax / winner-take-all | Sum and normalization       | Circular mean with dispersion-based σ            |
| **Similarity** | Dot product or ℓ∞-based | Dot product                | Gaussian-kernel similarity weighted by σ         |
