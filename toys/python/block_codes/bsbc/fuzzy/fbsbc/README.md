*Circular Normal Representations* - a VSA with von Mises-like properties.

| VSA             | Representation | Uncertainty  | Bundling          | Failure mode         |
| --------------- | -------------- | ------------ | ----------------- | -------------------- |
| BSBC            | 1-hot blocks   | implicit     | mode / random tie | rapid noise collapse |
| CGR             | modular ints   | implicit     | mode              | deterministic bias   |
| MCR             | modular ints   | implicit     | circular mean     | phase cancellation   |
| MAP             | ±1 bits        | implicit     | sum+sign          | saturation           |
| FHRR            | unit complex   | implicit     | complex sum       | magnitude loss       |
| **CNR**         | (μ, σ)         | **explicit** | Bayesian fusion   | graceful degradation |
