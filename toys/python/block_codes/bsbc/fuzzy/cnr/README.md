*Circular Normal Representations* - a VSA with von Mises-like properties.

| VSA             | Representation | Uncertainty  | Bundling          | Failure mode         |
| --------------- | -------------- | ------------ | ----------------- | -------------------- |
| BSBC            | 1-hot blocks   | implicit     | mode / random tie | rapid noise collapse |
| CGR             | modular ints   | implicit     | mode              | deterministic bias   |
| MCR             | modular ints   | implicit     | circular mean     | phase cancellation   |
| MAP             | ±1 bits        | implicit     | sum+sign          | saturation           |
| FHRR            | unit complex   | implicit     | complex sum       | magnitude loss       |
| **CNR**         | (μ, κ)         | **explicit** | von Mises fusion  | graceful degradation |

Blocks of different sizes could be bound or bundled by scaling blocks to their least common multiple, performing the operation, and then scaling back. A block's size, kappa, and mu would need to scale up/down with the same ratio.
