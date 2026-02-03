An attempt to learn more about VSAs and HDC.


References
----------
- Language Geometry using Random Indexing
- Hyperdimensional Computing: An Introduction to Computing in Distributed Representation with High-Dimensional Random Vectors (Kanerva)
- Holographic Reduced Representations (Plate)
- HDCluster: An Accurate Clustering Using Brain-Inspired High-Dimensional Computing
- A comparison of vector symbolic architectures
- [Computing with High-Dimensional Vectors](https://www.youtube.com/watch?v=zUCoxhExe0o) (Kanerva) 
  - Stanford University Colloquium on Computer Systems EE380 Spring 2023
- Learning with Holographic Reduced Representations
- [Vector Symbolic Architectures In Clojure](https://www.youtube.com/watch?v=j7ygjfbBJD0) (Carin Meier)
- Infini-gram: Scaling Unbounded n-gram Language Models to a Trillion Tokens
- GraphHD: Efficient graph classification using hyperdimensional computing
- GrapHD: Graph-Based Hyperdimensional Memorization for Brain-Like Cognitive Learning
- [Understanding Hyperdimensional Computing for Parallel Single-Pass Learning](https://github.com/Cornell-RelaxML/Hyperdimensional-Computing)
  - binary HDC is finite group (order=2) approximation of FHRR (unit cycle)
    - 2 phases: 0 and 180. the smallest possible finite group
    - FHRR didn't really make sense to me until I thought about it in terms of approximating it via a modular permuation as in BSBC
  - finite groups of larger orders could better approximate the unity cycle
    - "This cyclic group VSA is in some sense a “subset” of the unit cycle VSA, and as n goes to infinity, it approximates the the unit cycle VSA arbitrarily well [Plate, 1994], serving as an interpolation between the binary HDC and the unit cycle VSA"
      - the unity cycle VSA (HRR) may have infinite phases, but once its implemented in a computer inifinity will need to be approximated anyways.
      - there are infinity phases on a clock, too. most of them just don't matter.
    - a group of size 60 is like a 60-sides die representing a marble. not quite round but close. 
      - a 1hot block of 60 bits could also represent seconds/minute hand on a clock
  - 6.2 Cycle Group VSA
    - "addition modulo n as binding operation"
    - sim is measured by the cosine of the phase differences
    - bundling for learning a centroid/prototype is replaced with stochastic gradient decent
    - "We leave exploration of non-Abelian VSAs to future work"
- A Survey on Hyperdimensional Computing aka Vector Symbolic Architectures, Part I: Models and Data Transformations, A Survey on Hyperdimensional Computing aka Vector Symbolic Architectures, Part II: Applications, Cognitive Models, and Challenges
- Hyper-Dimensional Computing Challenges and Opportunities for AI Applications
- SearcHD: A Memory-Centric Hyperdimensional Computing with Stochastic Training
- Classification using Hyperdimensional Computing: A Review
  - table 1 is interesting
- Hyperdimensional Biosignal Processing: A Case Study for EMG-based Hand Gesture Recognition
- HYPERDIMENSIONAL COMPUTING: A FAST, ROBUST AND INTERPRETABLE PARADIGM FOR BIOLOGICAL DATA
  - figure 1b is awesome! and is similar to Figure 1 of Modular Composite Representation
- Computing on Functions Using Randomized Vector Representations (in brief)
  - "The kernel shape depends on the random structure of the FPE base vector. Uniformly sampled base vectors produce VFAs with a universal kernel shape, the sinc function, independent of the underlying binding operation. Thus, vectors in the resulting VFA can represent the band-limited functions"
    - the distribution from which the vector elements are draw influences the shape of the similarity kernel which develops between FPE levels
    - if the distribution from which hv elements are sampled influences the induced kernel, can we compose/combine hv of differing sampling distributions (e.g. bind a normal_hv and an exponential_hv) to create mixture models or arbitrary PDFs? i think that the paper is saying yes indeed.
  - 2d kernels can be constructed by sampling hypervectors elements from different distributions
    - 2d combinations of distributions make lattices, such as hex-shaped, like gridcells
- Computing on Functions Using Randomized Vector Representations
  - this is a very strong and thorough paper and i cannot claim to understand it all
  - generalize VSA to VFA (vector function architectures)
  - continous valued data is mapped to the vector space so the inner product of vectors is a sim kernel
    - inner product is the sum of pairwise multiplication. the sum provides a similarity score between the embedded functions
    - cosine sim uses normalized inner product
  - data points as well as functions are both hypervectors
  - fractional power encoding (HRR)
  - "the distribution from which elements of the base vector are sampled determines the shape of the FPE kernel, which in turn induces a VFA for computing with band-limited functions".

| VSA  | Vector Element Distribution          | Element Values        |
|------|--------------------------------------|-----------------------|
| HRR  | Real values [-1,1)                   | Continuous            |
| FHRR | Phases [0, 2pi)                      | Continuous            |
| HLB  | Normal +/-1, scaled by 1/sqrt(d)     | Continuous            |
| BSC  | {0, 1}                               | Discrete              |
| MAP-B| {-1, 0, 1}                           | Discrete              |
| MAP-I| Integer values                       | Both, sort of         |
| MAP-C| Real values                          | Continuous            |

    - although with enough discrete measurements you become continuous. floating point digits (continuous) are represented as binary (discrete)
    - I wonder if HLB supports FPE. HLB elements are real and hv are NOT self-inverses... so maybe?
  - VFA (com)binds Reproducing Kernel Hilbert Spaces with VSA. or 
    - radial basis kernel functions used by SVMs
    - polynomial regression tasks
  - BSBC are related to MCR
  - "Combining KLPE and VSA produces a computing framework we refer to as Vector Function Architectures (VFA), in which not only symbols but real-valued data and functions can be represented and manipulated in a transparent fashion"
    - kernel locality-preserving encoding + vsa = vfa
  - "An optimal separation can be achieved by an encoding scheme with exactly orthogonal representation vectors...This encoding scheme ... is ... a quite ineﬃcient use of an n-dimensional representation space"
    - this reminds me of how cyclic permutation restricts the resulting group size to n while the vector space is n^2
  - VFA represents functions just like DNN. continuous holistic distributed
  - VFA manipulates function just like VSA. structured symbolic distributed 
  - VSA using FPE are KLPEs compatible with binding
  - VFA requires FPE which requires continuous representations 
    - i wonder if another method of representing scalars, other than FPE, could be used to build a VFA
    - FPE is "self binding" and it can be used by various VSA and thus binding ops
      - hadamard (element-wise) multiply
      - circular convolve
      - block-local circular convolve
  - figure 2 reminds me of Generic Sparse Block Codes from Factorizers for Distributed Sparse Block Codes
  - figure 3 is neat. changing the distribution from which FPE's basis hv elements are sampled changes the similarity kernel
    - "By drawing the base vector of an FPE from distributions other than the uniform band-limited distribution, one can design kernels with shapes that diﬀer from the sinc function"
    - use different distributions to make different/common kernel shapes then use them like wavelets
    - the relationship between the distribution the hv are generated from and the resulting induced kernel shape
    - HLB uses not a single Gaussian (left panels second row of fig3) but a mixture of 2 Gaussians (not shown in fig 3). One of which is centered around 1 and the other aroubd -1. Both with a variance of 1/d
      - fuzzy hamming distance
  - figure 4: MCR produces a periodic kernel
  - section 7. i like that they provide applications, not just theory/math
    - MCR makes a torus and that can be used to make a scene's borders wrap
    - nonlinear regression
  - they call "leveling" "locality-preserving encoding" LPE
    - float codes, concatenation, thermom codes "can also induce RKHS function spaces. However, none of these other LPEs induce a VFA because they do not include a binding operation compatible with the encoding scheme" 
  - "a VFA vector can be seen as a compact probabilistic data structure or sketch of a function" which can go beyond sketching like bloom filters and count-mins
  - "phasor vectors ... can be naturally represented by spikes". then MCR/BSBC should integrate well with SNN?
  - "Probably closest to the VFA concept are population codes (Pouget et al., 2000; Barber et al., 2003), such as Bayesian population codes (Ma et al., 2006). In these models each neuron typically has a Gaussian-shaped receptive field on the encoding manifold. This leads to an inner product kernel that decays with distance and is translation invariant. Thus Bayesian population codes induce a kernel function space. However, they lack the binding operation (at least we are not aware of one) to perform the algebraic function manipulations possible with VFA"
- Computing reaching dynamics in motor cortex with Cartesian spatial coordinates
  - moving an arm with a feed-forward only
  - i mostly just looked at the pictures
  - fig 1
    - this model uses spatial coordinates (B), not joint-based (A)
    - (C) looks like it could be represented symbolically
  - figure 6 is neat
    - imagine each arrow is a phase and each phase is a real valued element of a hypervector, a population vector
    - "Because the muscle tensions required to make a reaching movement can be accurately approximated by a linearly weighted sum of motoneuron activities, the muscle tensions could be computed directly from the cross products represented by neurons in the motor cortex with our simplified muscle model. This could explain how the neurons in primate motor cortex that project directly to lower motoneurons in the spinal cord can effectively control muscle tension activities."
- The structures and functions of correlations in neural population codes
  - if neurons have independent noise (or correlations orthogonal to some signal) adding more neurons averages out the noise and the signal/inforamtion grows with population size
  - "information-limiting correlations" cannot be averaged away by adding more neurons
    - these correlations are noise which mimics a change in stimulus
    - to me this sound like "ambiguity"
    - the signal and noise grow at the same rate
    - gain fluctuations aka feedback loops
- Compositional Factorization of Visual Scenes with Convolutional Sparse Coding and Resonator Networks
  - "Visual perception requires making sense of previously unencountered combinations of objects and their poses in a visual scene"
  - "Learning new objects from limited examples is possible when one exploits the idea of compositionality"
  - use a CNN to make sparse representations, use FHRR resonator network to factor the scene
    - Vector Function Architecture (VFA)
    - generate 3 hv and bind/bundle your way to an image embedding
      - x, represents horizontal using FPE 
      - y, represents vertical using FPE 
      - j, randomly generated 'basis'
    - objects are represented as hv
  - a codebook is a matrix. rows may be uncorrelated as with random basis or correlated as in leveling
  - factorizers, like RNs, work better with smaller codebooks
    - bundling a codebook is a great way to compute in superposition but too large of a bundle and things go awry
    - keeping a logical boundary/separation between codebooks allows a model to "focus" on one set of object attributes at a time. first, think about its shape, then its color, then its size, etc.
  - what's novel in the paper is the pipeline. CNN -> sparse representations -> FHRR vectors -> scene factoring
    - no pixel values used directly within the HDC/VSA part pipeline
- Properties of Sparse Distributed Representations and their Application to Hierarchical Temporal Memory
  - neocortex processes a contast high-definition stream of the outside world. it does so in realtime using sparse representations.
  - "The SDRs in later sensory areas encode more abstract and categorical information" 
    - this ties to category theory and sets
  - "Robustness to noise is high enough such that reliable classification can be performed with as much as 50% noise"
  - Sparse Distributed Representations types:
    - binary SDR example (uncompressed) *from paper*
      - dims = 40
      - hot_count = 4
      - x = vector([0100000000000000000100000000000110000000])
      - y = vector([1000000000000000000100000000000110000000])
      - overlap = 3, sim = 3/4
      - 40 * 1 bit = 40 bits per symbol
    - integer set example (compressed binary SDR) *not in paper*
      - dims = 4
      - max_val = 40
      - x = set([1, 19, 31, 32])
      - y = set([0, 19, 31, 32])
      - intersect = 3, sim = 3/4
      - 4 * 8 bits = 32 bits per symbol
    - tuple set example (compressed binary SDR with magnitudes) *not in paper*
      - dims = 4
      - max_val = 40
      - not only do x and y have hot positions, but those hot positions have a value
        - x = vector([0400000000000000000700000000000920000000])
        - y = vector([7000000000000000000700000000000920000000])
          - should this be called real-valued SDR?
          - sparsity is preserved just as with binary SDR
      - x = set([(1, 4/40), (19, 7/40), (31, 9/40), (32, 2/40)])
      - y = set([(0, 7/40), (19, 7/40), (31, 9/40), (32, 2/40)])
        - tuple(position, value)
          - [0], index/position of the hot bit
          - [1], magntiude/value of the position normalized to `(0-1]`. the magnitude cannot be zero but it could be negative
          - symbols are lists of tuples `(int, float)` just like Circular Normal Representations's use of (mu, kappa) except here they are sets and in CNR they are vectors
            - here, the [0] in tuples are guaranteed unique so order of tuples/elements is insignificant
            - in CNR, the [0] in tuples are not unique but the order of tuple/elements is significant
      - intersect = 3, sim = 3/4
        - similarity could utilize the difference or ratio of overlapping indices
  - the paper explores math behind various combinations of dims and hot_count for FPs and noise
    - the appendix includes actuarial tables
  - OR is the bundling operation. it increase density of binary vectors. it increases the size of integer sets
    - prior to thinning, you can compare a symbol to a superposition to see if its in the set the superposition represents
    - the more constituents to bundle, the more possible an FP is. same as other HDC/VSA.
  - SDRs can be subsampled
  - "In the absence of learning, the SP process examines the overlap between a set of randomly initialized columns and individual binary input vectors. The top 𝑘 columns, determined by calculating the overlap, win and form the ON bits in the resulting SDR." this is thinning
  - Temporal Memory, a sequence prediction model using SDR
    - prodcues a union of possible temporal states for the next timestep
- Quantum Computation via Sparse Distributed Representation
  - SDRs enable "quantum speed-up[s]" on classical hardware
    - published as "Opinion and Perspectives". the author believes "that SDR constitutes a classical instantiation of quantum superposition and that switching from localist representations to SDR, which entails no new, esoteric technology, is the key to achieving quantum computation in a single-processor, classical (Von Neumann) computer."
  - Figure 1. "SDR provides a classical realization of quantum superposition in which probability amplitudes are represented directly and implicitly by sizes of intersections"
  - thinning is great. add recurrent connections and you can steer the bundle over timesteps while still permitting collapse at each timestep.
- Encoding Data for HTM Systems
  - methods for encoding various types of data using binary SDRs
    - goals for an encoder:
      - semantically similar data should result in similar SDRs
      - deterministic outputs for all inputs
      - outputs have fixed dimensionality
      - outputs have fixed hotness
    - numbers, logs, deltas (no mention of decimate/supplement encoder from Sparse Binary Distributed Encoding of Scalars)
    - categories
    - orders and cycles
    - geospatial (2d such as images)
      - incorporate speed to find anomalous moving objects
    - natural language
    - multi-modal
- The Use of Hierarchical Temporal Memory and Temporal Sequence Encoder for Online Anomaly Detection in Industrial Cyber-Physical Systems
  - SDRs for realtime detections in OT environments
  - novel temporal sequnce encoder (TSSE)
    - designed for "processing data streams of slowly varying physical measurement"
  - deep learning models need a ton of data and often need retrained :(
  - their encoder uses 2 encoders described in Encoding Data for HTM Systems
  - they use CDT on SDRs. where does the 2% sparsity come from?
  - i think "substructive" is supposed to read "subtractive"
  - HTM does need a training period with supervised feedback on anomalies
- A Distributed Anomaly Detection System for In-Vehicle Network Using HTM
- Representation and Processing of Structures with Binary Sparse Distributed Codes
  - when generating new symbols, ensure the ratio of 1 to 0 is 1/sqrt(D)
    - altering the distribution of elements influences the resulting kernel
  - CDT for binding operator
    - CDT is iterative conjunction with permuted self
- Binding and Normalization of Binary Sparse Distributed Representations by Context-Dependent Thinning
  - CDT makes SDRs
  - CDT is a special type of superposition
    - CDT can also be considered as a hashing procedure: the subspace to where hashing is performed is defined by 1s of z, and some 1s of z are mapped to that subspace"
  - section 3 really spells out what makes a CDT procedure
  - section 4: direct, permutative, additive, subtractive
  - "Performing the CDT procedure can be viewed as an analog of introducing brackets into symbolic descriptions"
    - if cdt does not have a true binding operator then the family of models it can produce must be set-like not group-like.
      - set symbolic architecture. you can bundle, you can thin, but you cannot bind. 
      - the symbols are sets. integer SDR/hv act as sets. thinning ensures DIMS which is actually set size. OR/conjunction is union.
- Sparse Binary Distributed Encoding of Scalars
  - "The number of unity (1s) elements M in sparse codevectors should be significant for maintenance statistical stability of the number of unities and reducing its deviation about the mean value"
  - historically these are used ...
    - thermometric
      - start with all 0s
      - for each level flip the next 0 bit to 1
    - partially distributed float
      - start with all 0s but first 3 (or 4 or 5) elements are 1s
      - shift the consecutive 1s, as a group, cyclically
    - partially distributed multifloat
      - serval float encoding hvs represent a single number
      - the hvs are concatentated
      - ?
  - ... but the authors suggested these distributed stochastic encodings
    - subtractive-additive: exponential
      - geenrate a random reference/basis hv, 10000 elements, 100 hot, k is some percent of hot
      - randomly flip k 0s to 1s of the basis hv. randomly flip k 1s to 0s of the basis hv. that's the next level.
        - this can be done by conjuncting the basis hv with another random hv.
      - repeat the adding and removing of hot bits for more levels
      - k determines the steepness of the leveling
      - steps from paper
        - generate the basis hv
        - generate decimator hv
        - conjunct basis with decimator
       - generate complementor hv
        - disjunct basis with complementor
    - concatenation of parts: linear
      - generate a start hv and a stop hv, then interpolate between them to make levels
      - or generate multiple landmark hv, then interpolate between the landmarks
    - cyclic quantities
      - with reproduction
        - ? disjunction of preceding hv ?
      - with reference
        - generate multiple hv, representing the equal division of a circle's angles: 0, 90, 180, 270
        - level between them  using concatenation of parts or subtractive-additive
- Efficient Context-Preserving Encoding and Decoding of Compositional Structures Using Sparse Binary Representations
  - "the key to overcoming those limitations in artificial neural networks is efficiently combining continuity with compositionality principles"
  - context-dependent thinning (CDT) is one algorithm that ensures sparsity as the brain does but also supports encoding compositional structure
  - CDT
    - bound hv are similar to their constituents
    - similarity does not require unbinding
      - which is good because unbinding isn't possible because thinning isn't undoable
        - thin_weave.py
    - is slow
    - is commutative (which means the VSA will require explicit encoding of positional info for binding)
  - Context-preserving SDR encoding/decoding (CPSE/CPSD)
    - cpse allows for order of binding input to be preserved
    - cpsd allows for decoding using triadic memory
      - what is triadic memory? it seems to be a columnary co-ocurrence table
  - section 2 has a nice history review
    - Holographic Reduced Representations (HRRs)
    - Fourier Holographic Reduced Representations (FHRRs)
    - Binary Splatter Codes (BSCs)
    - Sparse Block Code (SBC)
    - Vector-Derived Transformation Binding (VTB)
    - Binary Sparse Distributed Code (BDSC)
      - makes use of context-dependent thinning (CDT)
    - Sparse binary representations (SDRs)
  - "Despite their unprecedented success, artificial neural networks suffer extreme opacity and weakness in learning general knowledge from limited experience"
- Variable Binding for Sparse Distributed Representations: Theory and Applications
  - "Sparse block-codes can be regarded as an extreme version of competitive coding principles observed in the brain"
- High-Dimensional Computing with Sparse Vectors
  - segements aka blocks are 1hot
  - bundle: context-dependent thinning durin bundling (they call is sumset)
    - competitive because blocks ties are thinned
  - bind: modulo sum of indices, segment-wise permutation
  - sparsity of blocks
    - when the blocks are maximally sparse, "each block is ... a phase angle" or a 1hot bit
    - "When the block is not maximally sparse, it functions more like a superposition of phase angles"
    - increasing sparsity decreases the distributed nature of the information
      - Blocks are concentrated represenations. All information is in the hot bit. Blocks are _not_ robust to noise. A single flipped element is very impactful.
      - with enough blocks (dims) in an hv, the representation becomes distributed. The hypervectors become robust to noise. A single incorrect/missing block and the system continues relatively unffected (given ~10k blocks).
  - the elements of blocks do not need to be contiguous, they can be randomly indexed within a hv. contiguous blocks are nice for for-loops tho.
    - some method of mapping vector indices to blocks is necessary
    - each hv can have its own unique element-to-block map
  - conceptualizing the block as a circle is useful
    - convert the 1hot value into degrees/radians
    - compare the degrees of different blocks for a distance metric
    - it is possible to compare hv of differnet block sizes so long as the 2 hv have the same number of blocks. always scale up so as to not lose information
      - hv1 has a block size of 4 with value of 3: 270 degrees
      - hv2 has a block size of 12 with value of 9: 270 degrees
      - hv3 has a block size of 64 with value 48: 270 degrees
    - the distance between 2 blocks is the cyclic distance (0 degrees == 360 degrees)
      - the distance between 2 hv is the sum of their block distances divided by their number of blocks
      - the maximum distance between 2 hv is 180 degrees times the number of blocks in the hv
  - params
    - block_count
    - block_size
    - k = "hotness"
      - vector sparsity = k / block_count 
      - during bundle op, the result is thinned so there are k number of 1s per block. the rest 0.
  - bundle examples when k>1
    - block_size=8, k=2, mode_count=2, mode=3
    - no thinning necessary
      ```
      0 0 0 0  0 1 0 0
      0 0 1 0  0 0 0 0
      0 0 1 0  0 1 0 0
      0 1 0 0  0 0 0 0
      0 1 1 0  0 1 0 0
      0 0 0 0  0 0 1 1
      ----------------
      0 0 1 0  0 1 0 0
      ```

    - block_size=8, k=3, mode_count=3, mode=3
    - no thinning necessary
      ```
      0 0 0 0  0 1 0 0
      0 0 1 0  0 0 0 0
      0 0 1 0  0 1 0 0
      0 1 0 0  0 0 0 0
      0 1 1 0  0 1 0 0
      0 1 0 0  0 0 1 1
      ----------------
      0 1 1 0  0 1 0 0
      ```

    - block_size=8, k=2, mode_count=3, mode=3
    - thinning achieved by random selection of mode indices
      ```
      0 0 0 0  0 1 0 0
      0 0 1 0  0 0 0 0
      0 0 1 0  0 1 0 0
      0 1 0 0  0 0 0 0
      0 1 1 0  0 1 0 0
      0 1 0 0  0 0 1 1
      ----------------
      0 0 1 0  0 1 0 0
      or
      0 1 0 0  0 1 0 0
      ```

    - block_size=8, k=2, mode_count=1, mode=2
    - mode_count less than k. 1hot when 2hot is expected
      - randomly pick one of the "second place" modes or...
      - ...leave the 2hot block as 1hot
      ```
      0 0 0 0  0 1 0 0
      0 1 0 0  0 0 0 0
      0 0 1 0  0 0 0 0
      0 0 0 0  0 0 0 0
      0 0 0 0  0 1 0 0
      0 0 0 0  0 0 0 1
      ----------------
      0 1 0 0  0 1 0 0
      or
      0 0 1 0  0 1 0 0
      or
      0 0 0 0  0 1 0 1
      or 
      0 0 0 0  0 1 0 0
      ```

    - block_size=8, k=2, mode_count=3, mode=3
    - if blocks are permitted to have less than k hotness then we can use weighted voting.
      - the index vote is divided by the hotness/certainty of the block
      - ties are randomly broken
      ```
      0 0 0 0  0 1 0 0
      0 0 1 0  0 0 0 0
      0 0 1 0  0 1 0 0
      0 1 0 0  0 0 0 0
      0 0 1 0  0 1 0 0
      0 1 0 0  0 0 1 0
      0 1 0 0  0 0 0 0
      0 0 0 1  0 0 1 0
      ----------------
      0 1 1 0  0 0 0 0
      or 
      0 1 0 0  1 0 0 0
    
      0: 0
      1: 1 + 1/2 + 1    * 1st
      2: 1 + 1/2 + 1/2  * 2nd
      3: 1/2              4th
      4: 0
      5: 1 + 1/2 + 1/2  * 2nd
      6: 1/2 + 1/2        3rd
      7: 0
      ```
  - when k>1
    - blocks are superpositions of phases instead of just a single phase
    - binary hypervector compresses to `vector of vector of ints` instead of `vector of int`
      - the length of the nested vectors is equal to the hotness of the binary block
        - what happens if hotness exceeds 1/2 * block_size? 0110 is the same as 1001.
    - binding must change.
      - examples:
        - 1hot by 1hot, k=1, block_size=8
        - vector of int
          - cyclic shift A by the 1hot index of B
        - (4 + 2) % 8 = 6
        ```
        A:  0 0 0 0  1 0 0 0....4 idx
        B:  0 0 1 0  0 0 0 0....2 idx
        ----------------‐-------------
        C:  0 0 0 0  0 0 1 0....6 idx
        ```

        - 2hot by 1hot, k=2, block_size=8
        - vector of [int, int]
          - cyclic shift A by the 1hot index of B. B's single index influences all of A's bits.
          - (1+2) % 8 = 3, (4+2) % 8 = 6
          ```
          A:  0 1 0 0  1 0 0 0....1,4 idx
          B:  0 0 1 0  0 0 0 0....2   idx
          -------------------------------------
          C:  0 0 0 1  0 0 1 0....3,6 idx
          ```

        - 2hot by 2hot, k=2, block_size=8
        - vector of [int, int]
          - cyclic shift the index of the 1st bit of A by the index of the 1st bit of B
          - cyclic shift the index of the 2nd bit of A by the index of the 2nd bit of B
          - (1+1) % 8 = 2, (4+7) % 8 = 3
          ```
          A:  0 1 0 0  1 0 0 0....1,4 idx
          B:  0 1 0 0  0 0 0 1....1,7 idx
          ------------------------------------
          C:  0 0 1 1  0 0 0 0....2,3 idx
          ```
          - if you permute different bits different amounts, you can create collisions which makes unbinding imperfect
            - A is 2hot, B is 2hot, C is 1hot
              - what happens if we permit less than k hotness?
              - what happens if we randomly select another bit and turn it on to ensure k?
          ```
          A:  0 1 0 0  1 0 0 0....1,4 idx
          B:  0 0 1 0  0 0 0 1....2,7 idx
          ------------------------------------
          C:  0 0 0 1  0 0 0 0....3 idx
          ```

        - 2hot by 3hot, k=3, block_size=8
          - how do?
          - i'm not sure if it's a good idea to allow "under hot" blocks 
            - would a binding of 3hot by 3hot work?
          ```
          A:  0 1 0 0  1 0 0 0....1,4 idx
          B:  0 1 0 0  0 0 1 1....1,6,7 idx
          ---------------------------------
          C:  ? ? ? ?  ? ? ? ? 
          ```
- Geometric Analogue of Holographic Reduced Representation
  - "Replacing convolutions by geometric products one arrives at reduced representations analogous to HRR but interpretable in terms of geometry"
  - intro
    - quantum computation is "tensor products of two-dimensional complex vectors called qubits"
    - replace tensor product with geometric ones from geometric algebra (GA)
    - "Systems where HRR are applicable might therefore, at least in principle, perform quantum algorithms"
  - the beef
    - BSC is mapped to HRR thru an exponential map
    - "the 'algebra' formalizes a procedure that resembles an IQ test". if groups/algebras define IQ tests then of course we should be using them to build AI
    - wow, math.
  - conclusion
    - something about the geometric product?
- Computing with Hypervectors for Efficient Speaker Identification
- Integer Factorization with Compositional Distributed Representations
  - "Thus, setting the value of 𝛽 allows traversing between two extremes: when 𝛽 is very small, FPEs of scalars that are far away from each other are still very similar (subsymbolic behavior) while when 𝛽 is very large, FPEs of scalars that are near each other are dissimilar (symbolic behavior)."
    - this sound similar to local vs global similarity param in leveling
- Hyperdimensional Quantum Factorization
  - in archetectures where unbinding is noisy (bind is not the exact inverse of unbind) a cleanup step is used
  - this paper utilizes Grover's algo to speed up the memory search done in the cleanup step
    - this approach is better than resonator networks
  - hardware does not currently exist to implement. womp womp.
- Learning and generalization of compositional descriptions of visual scenes
- Computing with Residue Numbers in High-Dimensional Representation
- Modular Composite Representation (MCR)
  - Thank you to the University of Memphis for making the research paper EASY to locate on the interwebs and FREE, as ,in beer, to download
    - hurray! open science!
  - figure 4 reminds me of Gilbert Strang's [The Big Picture of Linear Algebra](https://youtu.be/rwLOfdfc4dw?t=284)
    - orthogonality around a circle
  - "each model utilizes a different distance (or similarity) measurement, which explains the variations in performance between the two models"
  - same as Cyclic Group Representation "but uses a bundling based on element-wise mode instead of addition of complex numbers"
    - if each element is an approximate angle of a circle, why not bundle with the cyclic mean?
- Efficient Hyperdimensional Computing with Modular Composite Representations
  - hardware! hyperdimensional coprocessing unit on risc-v. neat.
  - after having implemented BSBC, MCR seems like the same thing
    - the modulo N is the block size is the order of the finite-group
    - in BSBC each hv can be permuted cyclically and each block can be permuted cyclically - a toroid shape.
      - each hv is a candy necklace
        - the necklace is not perfectly round because the hv has a finite number of blocks
      - each hv element (in MCR) or block (in BSBC) is a bead of the necklace. its value represents a dot on the bead.
        - the bead is not perfectly round because the block has a finite size
      - [see this](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Torus_cycles_(labeled).png/341px-Torus_cycles_(labeled).png). "b" is the circular hv. "a" is the cyclical block. the value of the block sits as a single point on "a".
    - MCR works on the compressed representations of BSBC hv
    - BSBC hv are vectors of 1-hot cyclic segments
      - blocks are thinned within eeach op
      - cyclic/modulus structure is built by permutation of
        - elements within blocks
        - blocks within vectors
        - one can imagine all bits of a block forming a circle. within each block only 1 (element) location on the circle is active at at time. hv are just lists of approximated circles.
          - why not compute on lists of approximated spheres?
      - can block sizes change in BSBC/MCR? perhaps block size changes depending on the operation?
        - TO TRY: add/drop an element adjacent to the hot bit
          - whatever is done to 1 block must be done to all blocks
        - the vector remains a multiple of the number of blocks it contains
      - can the number of blocks within a vector change?
        - yeah, bind hv with a random matrix
  - ops
    - bundle is majority vote, ties broken randomly or with the lowest mode
    - bind is modulo addition
    - unbind is modulo subtraction. perfect unbind, no noise.
    - sim is a "a modular variant of the Manhattan distance". my intuition tells me that their operation is more efficient than my current implementation of...
      - expand the hvs to their decompressed binary form, flatten them, then take the cossim of them
      - replace cossine sim with circular sim/dist metric
  - "Surprisingly, MCR even performs significantly better than the unconstrained MAP model with 32 bits per component, with an average accuracy gain of 7.63%. Although this may appear counterintuitive, the difference in performance comes from the different properties of superposition adopted by the two models. While MAP relies on a simple integer sum (in effect, only a real part), MCR interprets integers as discretized phasors on the unit circle, and then performs vector addition in [the complex space]. The greater expressivity in the complex plane preserves more information during superposition and explains why MCR achieves higher capacity."
    - superposition is majority voting, not addition.
    - what is the optimal number of discrete/sampled phasors?
      - can we have too many?
  - FHRR, MCR, BSDC-SEG, and BSC are similar
    - FHRR is the most robust, but using complex numbers makes it expensive to implement.
    - MCR works like FHRR by operating on phases, but those phases are discretized, so it approximates FHRR using integers instead of real numbers.
    - BSDC-SEG is similar to MCR, but represents those discrete values using binary segments, making it efficient to implement in hardware.

- Toroidal topology of population activity in grid cells
  - "using simultaneous recordings from many hundreds of grid cells and subsequent topological data analysis, we show that the joint activity of grid cells from an individual module resides on a toroidal manifold, as expected in a two-dimensional CAN. Positions on the torus correspond to positions of the moving animal in the environment"
  - thank you, rats.
  - "What kind of network architecture keeps the activity on a toroidal manifold ... remains to be determined"
  - why a torus? why not a [lumpy torus](https://www.youtube.com/watch?v=sEnugXJblFU)?
- Hyperdimensional Hashing: A Robust and Efficient Dynamic Hash Table
- HDTest: Differential Fuzz Testing of Brain-Inspired Hyperdimensional Computing
- [VSAONLINE](https://sites.google.com/view/hdvsaonline/home) and its [GGroup](https://groups.google.com/g/vsacommunity/about)
- [MIDNIGHTVSA](https://sites.google.com/ltu.se/midnightvsa)
- [Vector Symbolic Architectures](https://video.ucdavis.edu/media/Vector+Symbolic+Architectures/1_9b6hn4p2) (Luis El Srouji)
- Classification and Recall With Binary Hyperdimensional Computing: Tradeoffs in Choice of Density and Mapping Characteristics
- Robust Hyperdimensional Computing Against Cyber Atacks and Hardware Errors: A Survey
- EventHD: Robust and efficient hyperdimensional learning with neuromorphic sensor
- [Get to know SAR, Interferometry](https://nisar.jpl.nasa.gov/mission/get-to-know-sar/interferometry/)
- [An Introduction to Hyperdimensional Computing](https://www.esa.int/gsp/ACT/coffee/2024-03-22%20-%20Mike%20Heddes/)
- Generalized Holographic Reduced Representations
  - "HDC's simplicity poses challenges for encoding complex compositional structures"
  - GHRR is FHRR with a different binding operation
    - GHRR "maintain[s] the kernel properties of FHRR"
    - GHRR uses a binding operation that is not commutative, meaning order is significant. unlike multiplication.
      - cyclic permute is not needed to build sequences which means the breadth/depth of conceivable data structures is not limited to the dimensions of the hv
      - the binding is similar to both FHRR and the TPR
  - hv elements are unitary matrices, binding is a composition of 2 transformations
    - unitary matrices have inverse
  - hypervectors with elements of matrices are more expressive than hv with elements of scalars
- Recasting Self-Attention with Holographic Reduced Representations
- Deploying Convolutional Networks on Untrusted Platforms Using 2D Holographic Reduced Representations
- Fractional Binding in Vector Symbolic Architectures as Quasi-Probability Statements
- [Category Theory Illustrated](https://github.com/abuseofnotation/category-theory-illustrated/tree/master)
  - MellSans is disagreeable
  - picture books are a great way to teach. this is cool.
- Developing a Foundation of Vector Symbolic Architectures Using Category Theory
  - if CDT SDRs are sets then category theory aligns well
  - MBAT and VTB can do leveling via self-binding because their binds are not commutative. Non diagonal matrices are used to control the commutative of multiplication in GHRR.
  - "VSA require two binary operations. One must be reversible, and the other must distribute over the first."
  - "many of the alterations to element-wise multiplication/division (i.e. normalisation, thresholding, etc.) are imposed to model certain behavioural effects, such as neuronal saturation, rather than endowing computational advantages"
    - so, the choice to clip hvs elements is not inherent in the VSA's division ring, but rather it is a modeling choice "strapped onto" the algebra by engineers to achieve desired modeling results.
  - similarity
    - FHRR uses the inner product
      - cosine similarity is normalized inner product
        - hamming distance is cosine sim for binary
    - what about other distance/edit metrics? 4.4 is a slim section
    - what about uncertainty propagation through operations?
- [Learning sensorimotor control with neuromorphic sensors: Toward hyperdimensional active perception](https://ece.umd.edu/release/helping-robots-remember-hyperdimensional-computing-theory-could-change-the-way-ai-works)
  - DVS are super neat
  - CNN-level performance without a CNN
  - [Pt I: Hyperdimensional Computing (HDC) with Peter Sutor (Interview)](https://www.youtube.com/watch?v=1T2WdXcnefc)
    - instead of clipping bundle after each operation, periodically clip when the bundle elements get too big/small
  - [Pt II: Hyperdimensional Computing (HDC) with Peter Sutor (Interview)](https://www.youtube.com/watch?v=VjQBpJR3wsg)
    - if you iterate the training data, it's possible to boost while learning
      - this is similar to what was done in A Brain-Inspired Hyperdimensional Computing Approach for Classifying Massive DNA Methylation Data of Cancer
    - [pyhdc](https://github.com/ncos/pyhdc)
    - shout outs to San Jose and Cardiff U
  - [April 2024 AICamp Boston meetup - Peter Sutor - Hyperdimensional Computing](https://www.youtube.com/watch?v=Nob2j5aY0yw)
- Holographic Global Convolutional Networks for Long-Range Prediction Tasks in Malware Detection
  - [code](https://github.com/FutureComputing4AI/HGConv)
- What Can N-Grams Learn for Malware Detection?
  - compared ngrams of: raw bytes vs assembly opcodes
    - "it seems that byte n-grams are robust in their ability to learn, but weak in what types of information they are able to learn"
    - "assembly-grams, at least when obtained from static analysis, are uniformly less effective then byte n-grams"
  - more than 1 way to disassemble a cat
- KiloGrams: Very Large N-Grams for Malware Classification
  - kilogramming: top-k most frequent ngram
  - hdc can embed an entire ngram histogram, not just top-k ngrams
- A Walsh Hadamard Derived Linear Vector Symbolic Architecture
  - [HLB code](https://github.com/FutureComputing4AI/Hadamard-derived-Linear-Binding)
    - based on torchhd
  - MAP but hv elements aren't -1 or +1. instead, +1/-1 are "relaxed"
    - ternary (binary) elements are real (floats)
      - better performing binding op :)
      - higher processing requirements :(
    - values are +1/-1 with a variance of `1 / sqrt(dimensions)`
    - pick a value near +1, pick a value near -1, flip a coin to determine which value is used as an hv element, repeat until desired length is reached
      ```
      dims = 10
      var = 0.3
      hv1 = hlb_new(dims)
      print(hv1)
      [1.30005046, -0.73675245, 0.88357413, 1.11876397, -0.96991859, -0.78981784, 0.85872794, -1.01049667, -1.2368788, -1.246146]
      ```
    - going slightly beyond the range of +1/-1 allows for differentiation/backpropegation and plugs nicely into the realm of DNN
    - noise in the hv grows as dimensionality grows
      - some noise is necessary for robustness of hv
      - too much noise makes operations less efficient
      - 1/sqrt(d) is a nice finding. what if we use values larger or smaller?
        - in discrete HDC/VSA, like binary or ternary architectures, the noise in an hv is localized. you can point to the element's index that has ben corrupted. in binary, elements flip. in ternary, elements equal 0. in H-DLB the noise is distributed randomly/evenly throughout the elements of an hv through the variance from +/-1
- Automatic Yara Rule Generation Using Biclustering
  - [code](https://github.com/FutureComputing4AI/AutoYara)
  - generate yara rules automagically
  - use long ngrams
  - practically, SOCs still need analysts to review metrics about generated signatures
  - packers
- Configurable Hardware Acceleration for Hyperdimensional Computing Extension on RISC-V
  - hyperdimensional coprocessor unit - push HDC tasks into hardware
- Orthogonal Matrices for MBAT Vector Symbolic Architectures, and a “Soft” VSA Representation for JSON
  - represent JSON objects as hypervectors for ML on JSON. very cool.
    - i wonder if nosql databases do something like this
  - bindings can be typed by introducing a common signal (a random matrix) in grouped symbols, this is how nested structures can be created
  - "VSAs in general, can be viewed as similarity-preserving hash codes for complex structures, where resulting hashes are amenable to machine learning and to searching for nearest neighbors"
- Efficient Host Intrusion Detection using Hyperdimensional Computing
  - they can find attack in Sysflow data by embedding provence graphs and ATT&CK TTPs into hypervectors and then mathing on them
  - "We adopted the method to work with an arbitrary length of paths within the graph, enhancing the capability of our framework to efficiently identify attack patterns of any length within provenance graphs"
- Audio Fingerprinting with Holographic Reduced Representations
- HyperCam: Low-Power Onboard Computer Vision for IoT Cameras
  - HDC vision using COTS hardware. bravo!
    - DVS are neat but they aren't cheap
  - naive encoding method
    - pixel position codebook uses randomized leveling
      - there will be no correlation between levels?
    - pixel value codebook uses linear leveling
      - the paper randomizes which bits they flip but all the bits hold the same amount of information so it doesn't matter
    - pixels are encoded as bind(Row, Col, Val)
    - images are encoded as bundle(pixel_binding0, pixel_binding1, ...)
  - rewrite 1
    - utilize permutation operation instead of position codebook to save memory
      - still no correlation between row1,col1 and row2,col1?
  - rewrite 2
    - another codebook reduction to save memory
    - pixels are treated as 1d?
  - rewrite 3
    - introduced weighted bundling operation to ensure pixel values that occur more often are considered more important
      - this sort of reminds me of adjusting the contrast on a b/w image
        - up the black and white values so the mid-tones become less important
  - rewrite 4
    - the sparse bundling operation:
      - randomly select some percent of the elements and bundle those only
      - use a CountSketch or BloomFilter backend
    - they merged the binding operation and generation of value HVs into a single pass for more better performance
  - remaining thoughts
    - i don't understand how BF and CS are used
    - i really like the idea of a partial bundling operation
      - it seems related to leveling strategies (replace, average, inc/dev)
      - how would other other operation modifications be useful? partial permutation?
      - partial bundling sounds similar to what Gayler calls "random selection" bundling or randsel bundling. however, randsel bundling is just random weighted (50-50 in the case of 2 constituents) concatenation. a leveling strategy.
        - parital bundling is element-wise failure or success some percent of the time. when it partial bundle fails it could use randsel as a result instead.
    - they are very concerned with performance. why not reduce HV dimensions? this would have made all operations more efficient (and less accurate)
    - they don't address the fact that neighboring pixels are often very near in value
- VSA Next Generation Reservoir Computing
  - 5 Feature fading, discusses bundle fading
- Detecting COVID-19 Related Pneumonia on CT Scans using Hyperdimensional Computing
  - this is awesome because it's theoretical AND tangible
    - wow, expert radiologists are only 70% accurate!
  - the use of opencv to adjust contrast prior to encoding reminds me of HyperCam's weighting added in rewrite 3
    - they use b/w images and pixel values of 0-255
  - "For creating the hypervectors, we use orthogonal or uncorrelated encoding [13]–[15] to represent the position of each pixel and linear or correlated encoding [17] to represent the pixel intensity."
    - similar to HyperCam, this paper uses uncorrelated positional encoding of pixels
    - using orthogonal encoding for pixels reminds me of using categorical encoding for integer values
    - dataset 3 having different image sizes than datasets 1 and 2 complicates things
      - i dunno if this will work but... use a single codebook of size 512 (the largest feature range) for all features
        - for 200x300 pixel images, flip some percent of the HV's elements to 0
          - `x_hv = zero_flip(levels[pixel_x], 312/512)`
          - `y_hv = zero_flip(levels[pixel_y], 212/512)`
          - `value_hv = zero_flip(levels[pixel_val], 256/512)`
        - for 512x512 pixel images, don't flip anything for positional variables
          - `x_hv = levels[pixel_x]`
          - `y_hv = levels[pixel_y]`
          - `value_hv = zero_flip(levels[pixel_val], 256/512)`
        - then `pixel_binding0 = bind(x_hv, y_hv, value_hv)`
        - then `image_bundle = bundle(pixel_binding0, pixel_binding1 ... pixel_bindingN)`
  - "Future research needs to be done to discover an encoding that is not dependent upon pixel position and that could be implemented to three-dimensional images"
- [A Brain-Inspired Hyperdimensional Computing Approach for Classifying Massive DNA Methylation Data of Cancer](https://github.com/cumbof/chopin2)
  - they, too, use uncorrelated levels to encode a range of numberical values. why?
    - i tried MNIST classification with leveled codebooks and it didn't work as well as randomized codebooks. i don't understand why
  - this is very cool: during training, if the wrong class is predicted, they subtract the sample_hv from all incorrect class prototypes
    - this is done in MoleHD as well and is mentioned in "Tutorial on Hyperdimensional Computing"
    - then they continually bundle the sample_hv into the correct class prototype HV until the accuracy reaches some threshold 
  - they also demonstrate that more dimensions and more levels doesn't mean better accuracy. table 4 shows that there's a sweet-spot for the datasets they use
- HDC-MiniROCKET: Explicit Time Encoding in Time Series Classification with Hyperdimensional Computing
  - i don't understand most of this paper but...
  - they bind in the timestep of the observation when encoding, which validates what thingy/ does
    - they use fractional binding (power encoding) to level the timesteps
      - they also mention DFT so i assume they're using FHRR
    - "To be able of adjust the temporal similarity of feature vectors, we introduce a parameter s, which influences the graded similarity between consecutive timestamps"
    - "s weigths the importance of temporal position – the higher its value, the more dissimilar become timestamps"
    - "the similarity of two feature vectors, each bound to the encoding of their timestamp, gradually decreases with increasing difference of the timestamps."
    - "It is very important to keep in mind that not all tasks and datasets benefit from explicit temporal encoding (e.g.. we can similarly construct datasets where temporal encoding is harmful."
    - "In practice, selecting s should incorporate knowledge about the particular task."
- [MIT 9.13 The Human Brain, Spring 2019](https://www.youtube.com/watch?v=ba-HMvDn_vU&list=PLUl4u3cNGP60IKRN_pFptIBxeiMc0MCJP)
  - this course is radical
  - grid cells, whoa
- Intrusion Detection in IoT Networks Using Hyperdimensional Computing: A Case Study on the NSL-KDD Dataset
  - i like the application of HDC to network detection <3
  - i don't like using public intrusion datasets
  - i don't like assuming DoS or scan detection has any relevance to other types of attacks
  - "Another avenue for future research could involve extending the model to handle sophisticated attacks, such as zero-day and advanced persistent threats, and incorporating real-time detection and response for better performance in dynamic, resource-constrained IoT environments."
    - let's say you bought 100 zero-days to further evaluate this experiment
      - at $100,000 each, that'll only run about $10,000,000
      - once you buy an ohday it is an ohday no longer
- Network Anomaly Detection for IoT Using Hyperdimensional Computing on NSL-KDD
  - this is very similar to "Intrusion Detection in IoT Networks Using Hyperdimensional Computing: A Case Study on the NSL-KDD Dataset" but with 1/4 different authors and way more math equations
- An Extension to Basis-Hypervectors for Learning from Circular Data in Hyperdimensional Computing
  - basis-hypervectors, a representation of an atomic symbol
  - level-hypervectors, derived from, and correlated with, a basis-hv
  - class-hypervectors, a centroid or "prototype"
  - query-hypervectors, an unlabeled HV which is queried against all class-hvs
  - classification model, a group of class-hvs is the model. compare a query-hv against each of the class-hvs to determine its label
  - regression model, a set of linearly leveled level-hvs is the model. 
    - starts at a place and goes to another place
    - requires a lookup function to conver the real-number to an HV
    - bundle the levels to make a levels_bundle, then bind(query, levels_bundle)
      - i'm pretty sure this is what factorization.py does
  - on uncorrelated codebooks "While this seems suitable for encoding letters, which to some extent represent unrelated information, clearly it is not as adequate for other kinds of unitary information, such as real numbers"
  - "the level-hypervectors created with the existing method, as described above, have a fixed distance between each pair of hypervectors."
  - circular-hypervectors, similar to leveling but each "level" hv represents a single point "of a set of equidistant points on a circle"
    - both even and odd number of levels can be used
    - hvs which are represent opposite side of the circle have minimum similarity (they are as similar are any 2 random hv)
    - see figure 6
      - r parameter controls window of simialrity. r value determines global circular vs local circular similarity of circular levels, similar to global linear vs local linear
  - their results
    - surgery robots, so cool
    - it's nice to see that leveling didn't perform as well as random symbols for them too on a classification task. maybe that's why it doesn't work well on MNIST digit classification
  - is it possible to create exponential/log correlate levels?
    - it seems to be possible, albeit my code is a overcomplicated... see `toys/zeek/thingy/testing/Baseline/tests.codebook_btest/output`

  - why haven't any of the paper's on image classification use 2d ngrams?
    - random (non) levels
    - linear levels
    - circular levels
    - permutation
    - no one has tried using column and row ngrams. sorta like a kernel/mask/convolution
      - after using photoshop filters for last 20 years i finally understand how they work
- [Fractional Binding in Vector Symbolic Architectures as Quasi-Probability Statements](https://www.youtube.com/watch?v=aYbJ_beUja8)
  - VSAs enable probabilist programming
    - binding encodes data, similarity computes probability, bundling updates beliefs (learns), unbinding is sort of like conditional probabilities
    - lots o' math
      - "Fractional binding is mathematically equivalent to the inverse Fourier transform of data encoded with RFFs"
    - let's make some mental leaps: VSAs are probabilities, quantum things are probabilities, VSAs are quantum things, VSAs are neuromorphically inspired, our brains are quantum computers
  - why do the waterloo papers use a different format for their References sections compared to other papers?
- [Efficient navigation using a scalable, biologically inspired spatial representation](https://www.youtube.com/watch?v=QrvUVECQDkk)
  - [code](https://github.com/ctn-waterloo/cogsci2020-ssp-nav). thank you.
- A neural representation of continuous space using fractional binding
- MoleHD: Ultra-Low-Cost Drug Discovery using Hyperdimensional Computing
  - [SMILES](https://en.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_System) are already strings, so just embed them into hv then learn
  - retrain/fine-tune during training by subtract example from incorrect class prototypes and add to correct ones
- [Structure and Interpretation of Computer Programs](https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/)
- Hyperdimensional Computing for ADHD Classification using EEG Signals
  - "when trained on just 8.86% of the dataset, the model reached an accuracy of 72.8%, surpassing the 72.2% achieved by the LSTM-ADHD model trained on the full dataset"
- Hypervector Design for Efficient Hyperdimensional Computing on Edge Devices
  - [tinyML Research Symposium 2021](https://www.youtube.com/watch?v=CSJ9Qr-SkeQ)
- Autonomous Learning with High-Dimensional Computing Architecture Similar to von Neumann’s
  - "the circuits in the cerebellum are laid out beautifully in 3D for a massive long-term memory for high-dimensional vectors"
  - "The vectors can be binary or integer or real or complex—the computing power comes more from high dimensionality (e.g., H = 10,000) than from the nature of vector components."
  - "New representations are made from existing ones with explicit calculation, which is fundamentally different from the generation of representations in an autoencoder or in the layers of a deep neural net as it is trained."
  - "they [HDC/VSA] compute with high precision if the dimensionality is high enough—and even if some of the simple circuits malfunction! In contrast, traditional circuits for computing with numbers are complicated and are expected to work flawlessly"
  - catastrophic forgetting in neural nets is akin to a phase transition in physics, the network changes all at once
  - storing information beyond short-term capacity is called "chunking"
    - chunking is related to ngrams
  - short-term memory can work on about 10 vectors (1 chunk) at a time, these are summarized into a single vector called "focus"
    - sensors, actuators, and memory are all integrated into the "focus" or the current state of self
      - this reminds me of the Ship of Theseus
  - "the cochlea of the inner ear analyses sound into frequencies—it Fourier-transforms the sound before passing it on to the rest of the brain"
  - "the optic nerve brings in information along about 1.4 million fibers and the primary visual cortex distributes it among 280 million neurons—a 200-fold increase"
    - that's a huge fan out. hey brain. here's some raw vision data. now, do the analytics.
  - "Detecting. Recognizing previously encountered states makes it possible to detect irregularities and anomalies that can serve as an alarm, for example."
  - he keeps using this term "regularities" to refer to patterns/structure in data. regularities are anything that isn't random.
  - everytime i read something by this Pentti guy, i wish there was more 
- Computing with Hypervectors for Efficient Speaker Identification
  - "The proposed speech encoder aims to capture the pronunciation variations between speakers"
  - algo
    - formants in a time window are embedded into a hypervector
    - ngrams are created from ordered time-slice hypervectors
      - component HV are weighted by when creating the ngram HV
        - weights are the "total energy of a spectrum slice" at each component time
      - weights for ngram components are normalized
    - ngram hypervectors are summed up to create a profile/prototype of the speaker
  - what are "similarly located formants"?
  - "training and testing on 40 speakers’ data take roughly 5 minutes on an Apple M1 processor"
  - "The results obtained so far are solely based on making use of one acoustic feature (formants) and their course over a short time. There are many more acoustic features yet to be considered, such as the pitch and cepstral coefficients. HD computing is especially suited for encoding a combination of features and producing a fixed-dimensional representation for them [27]. Therefore, its identification accuracy is expected to keep improving when combined with other acoustic features, with a modest increase in computing time and memory use."
- [Random High-Dimensional Binary Vectors, Kernel Methods, and Hyperdimensional Computing](https://cse.umn.edu/ima/events/random-high-dimensional-binary-vectors-kernel-methods-and-hyperdimensional-computing)
  - i do not understand all the math discussed
  - if you're working with spacial data and you don't encode spacial features in your VSA pipeline then the results will not be great
- Neuro-Symbolic Architecture Meets Large Language Models: A Memory-Centric Perspective
  - "While VSA excels at manipulating and reasoning with symbolic information, it typically assumes that the input data is intrinsically structured and symbolic in nature."
  - in Fig 3b, what happens to the index of hypervector which have the same number of 1 elements but a different permutation of 1s? how are the 2 different HV indexed?
    - nearest neighbor becomes a simple subtraction of indices, but how can you support that NN operation and permutation of HV?
  - "In essence, quantization in NeSy [HDC/VSA] systems can be understood as a function whose performance is influenced by parameters in the symbolic space, such as the length and number of vector-symbolic representations."
- [QLS/CAMBAM Seminar - Chris Eliasmith - February 25 2025](https://youtu.be/DvRWP4Xxhro?t=782)
  - i like the penguin+cat explaination of bundling
  - it reminds me of [My Wife and My Mother-in-Law](https://en.wikipedia.org/wiki/My_Wife_and_My_Mother-in-Law)
- A Neurodiversity-Inspired Solver for the Abstraction & Reasoning Corpus (ARC) Using Visual Imagery and Program Synthesis
  - wow.
- Vector Symbolic Algebras for the Abstraction and Reasoning Corpus
  - [ARC Prize 2025](https://www.kaggle.com/competitions/arc-prize-2025)
  - [code](https://github.com/ijoffe/ARC-VSA-2025)
    - [vsa.py](https://github.com/ijoffe/ARC-VSA-2025/blob/main/src/vsa.py#L75) shows how to make "number tags" from a basis hypervector
    - uses [sspspace](https://github.com/ctn-waterloo/sspspace) also by UoW
      - i wish the demo notebook had words describing what was going on in each cell
  - reminds me of "A Neurodiversity-Inspired Solver for the Abstraction & Reasoni..."
  - 2.1.1 Holographic Reduced Representations
    - complex number hv elements
    - similarity, cosine sim
      - 2 input vectors, 1 scalar result
      - the cost of "cleaning up" noisy vectors depends on the size of your library/codebook
    - bundle, addition
      - combines 2 input vectors resulting in a single vector which is similar to both inputs
    - bind, circular convolution (DFT then multiplication)
      - combines 2 input vectors resulting in a single vector which is unlike either input. if you know some of the inputs to a result, the other inputs may be recovered through another bind op
      - used to build records
        - the paper uses the term "slot-filler". others have other used the term role/filler
      - used to build sequential structures
        - "repeated binding" in HRR is possible unlike in a ternary/binary VSA
          - this sounds computationally expensive
    - inversion, used for unbinding
      - 1 input vector, resulting in 1 output vector. when the input and result are bound their result is the binding identity vector (all=1)
      - unbinding is used for querying
  - 2.1.2 Spatial Semantic Pointers
    - SSP is HRR for continuous spaces
    - can be used for
      - modeling grid cells
      - spatial reasoning
        - does not use language which means LLMs aren't useful. in human brains language and spatial tasks are handled by different brainial regions
    - "SSP space"
      - instead of calculating all the levels upfront, the math let's you efficiently calculate the level
        - it may have sounded expensive at first until you see the FT reduces
      - instead of having a discretized leveling vectors precomputed in memory, you just compute levels as needed
      - data feature vectors can thus be represented as bindings (records) of continuous numeric values
        - range bounds on the features values the space can represent?
          - "the zero vector in the feature space (i.e., the origin) is represented as the identity vector in the SSP space"
        - "Binding is addition in the feature space"
        - "Inversion is negation in the feature space"
  - dual process theory
    - thinking fast and slow
      - deep learning is system 1
      - old symbolic models are system 2
      - vsa are both systems and "VSAs are biologically and cognitively plausible and can be implemented in spiking NN"
        - snn == loihi
    - in my opinion, this link is tenuous as dp theory could arguably frame any 2-step process. i am not no scientist tho.
  - ARC
    - it's tough for computers and relatively simple for humans
      - spatial tasks. no language required to:
        1. close your eyes
        2. imagine a 3d object
        3. rotate the object with your mind's eye
      - language is not the gateway to all intelligence, thus LLMs alone will never reach agi
    - "objectness, goal-directedness, numbers, and geometry"
  - recognize objects, synthesize transformation hypotheses (programs), select best guess
    - objects: "a group of pixels transformed cohesively", "task-dependent"
      - "representing position in Cartesian coordinates makes performing translations simple but rotations complicated, and vice versa for polar coordinates"
      - colour. caegorical. only supports single-coloured objects
      - centre. is midpoint of object's border as SSP
      - shape. normalized bundle all of object's pixels as SSPs relative to centre
        - does not consider symmetry (mirroring), pixel counts, or other "higher-level object properties". the authors admit their work is a start and can be improved upon
    - programs: think fast and slow and use a DSL
      - humans are constrained by their own transformation DSLs which are a mixture of transformations they've seen previously
      - e.g. RECOLOUR, RECENTRE, RESHAPE, GENERATE
      - rules (if-then conditions) which map input objects to output objects
    - synthesis: do what humans do
      - first, determine the solution grid size. this restricts possible objects/transformations
      - demonstration, abduction, rule induction, and answer deduction
      - use a nn
  - other ARCish datasets: Sort-of-ARC, 1D-ARC, KidsARC, ConceptARC, MiniARC
  - "we do not address the fundamental problem of how these conceptualizations came to be; instead, we assume they have already been acquired"
    - from playing with:
      - malcolmn gladwell's [grid puzzle](https://puzzling.stackexchange.com/questions/25738/malcolm-gladwells-outliers-progressive-matrices-puzzle)
      - minecraft and legos
  - instead of synthesizing programs, how could transformation sythensis occur?
  - 5.2 limitations. "our solver can conceptualize neither many-to-one nor many-to-many object mappings" :(
- Probabilistic Abduction for Visual Abstract Reasoning via Learning Rules in Vector-symbolic Architectures
  - Raven progressive matrices are similar to ARC
- Loihi: A Neuromorphic Manycore Processor with On-Chip Learning
  - "low-EE-hee"
  - SNNs incorporate time as an explicit dependency in their computations
  - spike trains, "a sum of ... delta functions ... where tk is the time of the k-th [transmission]"
    - i wonder if times are measured from transmission by the orig synapse or from receipt by the resp synapse? perhaps somewhere in between? like a tap.
    - how fast does an action potential travel from one neuron to another?
      - i wonder if wiring lengths are considered. some axons can reach multiple feet in length
  - i could not understand most of this paper
- Hyperdimensional Computing with Spiking-Phasor Neurons
  - "Throughout this paper, we will tend to use phase angles when we refer to spike times, but with the understanding that they are isomorphic to each other."
    - spike times are phase angles
    - spikes -> fhrr -> self-binding -> fractional self binding (fpe) -> ssp ?
- Multivariate Time Series Analysis for Driving Style Classification using Neural Networks and Hyperdimensional Computing
- An Introduction to Hyperdimensional Computing for Robotics
  - "The fact that in hyperdimensional computing most things work only approximately, requires a diferent engineer’s mindset."
- Hyperdimensional computing as a framework for systematic aggregation of image descriptors
  - place recognition datasets: Nordland1k, StLucia, CMU Visual Localization, GardensPointWalking3, OxfordRobotCar, and SFUMountain
  - uses "local" linear leveling. Concatenation (c) as described in figure 5 of An Encoding Framework for Binarized Images using HyperDimensional computing
- [Navigation Using a Biologically Inspired Spatial Representation](https://www.youtube.com/watch?v=QrvUVECQDkk)
  - "SSPs utilize the concept of fractional binding to extend vector symbolic architectures to include continous value signals in addition to discrete symbols"
- The Recommendation Functional Architecture as the Basis for a Neurophysiological Understanding of Cognition
  - L. Andrew Coward
  - REM reinforcement
  - perceive, cluster (find patterns), then select (compete)
  - incremental without overwritting previous patterns
- Efficient Exploration in Edge-Friendly Hyperdimensional Reinforcement Learning
  - QHD: A brain-inspired hyperdimensional reinforcement learning algorithm
    - a prior paper but it doesn't read as clearly
    - very greedy, perhaps too greedy
  - more better faster than a deep q approach
  - fig 2
    - each possible action is modeled using an hv
    - action1_q_value = sim(action1_hv, current_state_hv)
  - "experience replay buffer" memory
    - current_state, prev_state, and action use to estimate q value for state-action pair
    - update the hv modeling the action using weighted bundling or subtraction
  - to encourage exploration, incorporate a confidence/confusion metric
- [Word Embeddings with HD Computing/VSA](https://drive.google.com/file/d/1vXO4wtBI2swI6uQUew3Y3NARM6GHXV8f/view)
  - context embeddings are a fun trick for languages where word order (subject-verb-object) conveys information 
  - do context embeddings work well on non-english languages?
- Vector Symbolic Architectures as a Computing Framework for Emerging Hardware
  - Section 5
- Exploring Storing Capacity of Hyperdimensional Binary Vectors
  - "HD computing also "includes ideas from probability theory, statistics and abstract algebra""
  - "Based on the obtained results ... we can state that a binary vector of size N = 2,500 is enough"
  - see Table 2
    - it actually got worse with too many dimensions!
- [An Introduction to Vector Symbolic Architectures and Hyperdimensional Computing, VSA Tutorial](https://www.tu-chemnitz.de/etit/proaut/vsa_ecai20)
- Representing Objects, Relations, and Sequences
  - a bind operator that is it's own inverse has some issues.
    1. the girl, `bind(THE_hv, GIRL_hv)`
    2. the smart girl, `bind(THE_hv, SMART_hv, GIRL_hv)`
    3. the very smart girl, `bind(THE_hv, VERY_hv, SMART_hv, GIRL_hv)`
    4. the very very smart girl, `bind(THE_hv, VERY_hv, VERY_hv, SMART_hv, GIRL_hv)`
      - VERY_hv bound to VERY_hv will equal the identity HV (all=1)
      - the result of number 2 and number 4 will be indistinguishable
- Learning from Hypervectors: A Survey on Hypervector Encoding
  - TLDR: all you need is coding
  - "resistive RAM-based processing" aka memristors
    - Mem-fractive Properties of Mushrooms
      - grey oyster fungi
    - Sustainable memristors from shiitake mycelium for high-frequency bioelectronics
      - mycelia memristors
      - edible space computers
        - shiitake and button
      - [code](https://github.com/javeharron/abhothData)
      - "dehydration  can preserve the observed properties in a previously “programmed” sample"
      - "Unlike expensive conventional memristors, culturing fungal memristors does not require large facilities or rare minerals. The process can be scaled to grow large systems, which can be programmed and pre-served for long-term use at low cost."
  - szection III. hypervector mapping
    - orthogonal hv for symbolic/categorical data
      - orthogonality can be improved by generating atomic hv from sogol sequence
        - A Linear-Time, Optimization-Free, and Edge Device-Compatible Hypervector Encoding 
        - No-multiplication deterministic hyperdimensional encoding for resource-constrained devices
      - low discrepency sobol sequences ensure roughly the same mean in each generated HV but ensures better orthogonality.
        - better orthogonality means less random noise introduced when bundling or leveling
        - i wonder how sampling in this way influences binding compared to bundling
    - correlated hv for numeric data
      - uniform steps
      - non-uniform steps
    - (fractional) power encoding works well on 2d input
      - W = A<sup>u</sup> ⊕ B<sup>v</sup>
      - with encoding pixel x,y position using uniform leveling W doesn't have the desired properties
    - sparsity
      - "Choosing the proper sparsity factor can significantly reduce the number of arithmetic operations"
      - it may be wise to consider the operations used by the encoding process while choosing a sparsity factor. for example, multiplying 2 sparse vectors results in a sparser vector
        - Low-Power Sparse Hyperdimensional Encoder for Language Recognition
          - "the n-gram and text hypervectors can benefit far less from such initial sparsity"
          - they discuss how XOR must be interpreted when using sparse hv
    - sampling elements from a non-normal distribution induces that kernel
    - different hv element types will hold information in different ways
      - binary is nearest to the metal
      - bipolar is easiest to reason about and is fundamentally the same as binary
      - integers allow for variations on leveling and clipping. binding/bundling operations are still relatively intuitive
      - f32 can hold more info than a single bit but they are treated more like vectors of blocks instead of vectors of bits which makes their binding/bundling operations less intuitive
- An Encoding Framework for Binarized Images using HyperDimensional Computing
  - local linear leveling
  - Figure 5
  - minor leveling between major levels
  - a window around a point where anything outside of the window is maximally orthogonal
- Hyperdimensional computing as a framework for systematic aggregation of image descriptors
  - 3.1.5 uses concatenation of bits from random basis "major level" hv. compare with local linear leveling
    - if a subrange is divided into thirds, and the desired location is between hv1 and hv2 then 1/3 of the elements from h1 and 2/3 of the elements from hv2 are concatenated to form the position hv
    - this introduces unwanted artefacts as the paper admits. see local linear mapping for an improved method
      - "this approach is able to evaluate similarities across the grid borders"
      - local linear mapping evaluates similarities within grid borders
- Classification using hyperdimensional computing: a review with comparative analysis
  - fig5 and fig6 are both excellent
  - 2.3.1 encoding univariate data, correlated hypervectors for dicrete levels
    - they only discuss leveling from a basis hv to its inverse but leveling can also utilize a walk as done in "local linear mapping"
  - section 3 has pseudocode for various modeling types. fig 13 is a taxonomy of the types:
    - prototypes
      - centroid
      - adaptive
      - regenerative
      - compressed
      - semi-spervised
      - multiprototype
    - optimization
      - linear discriminant analysis
      - svm
      - backprop
      - ridge regression
- HDnn-PIM: Efficient in Memory Design of Hyperdimensional Computing with Feature Extraction
  - pretrained CNN frontend plumbed to an HDC backend. neato.
  - 2 HDnn algorithmic flow
    - use the first few convolutions and first pooling layer of popular pretrained DNNs, such as ResNet, to learn convolutional features of each set of training images
    - multiply the extracted image features by a random matrix to project the features onto fixed length hypervectors
      - this reminds me of MBAT
    - use HD operations, like add and clip, to learn class prototypes. use cossim operation for inference.
    - i dont understand (3) FE tuning
- Designing Vector-Symbolic Architectures for Biomedical Applications: Ten Tips and Common Pitfalls
  - molto bene. grazie mille. i love tip #10. science needs more tutorial style papers that include code. this paper is great even for those who study VSAs but are outside of the the biomedical domain.
  - [use-cases](https://github.com/cumbof/Biomed-VSAs) that are licensed permissively. very cool.
    - the paper reads a bit promotional for the author's hdlib project but since it's open source i can forgive all marketing aspects of the paper.
  - "How to avoid the pitfall: add 3D information to the codebook"
    - it would be nice to see some discussion of "correlation-aware codes" and how to select the best type of correlation-aware code. for example, should the design use circular codes since it represents angular data? or should it use linear codes? if linear, local or global linear codes?
  - since many of the concept codebooks use uncorrelated atomic hypervectors i wonder how the results of each use case would be influenced by using sobol sequences to maximize orthogonality of atomic symbols.
  - "As long as all your vectors share the same dimensionality, they can be mathematically combined, regardless of their origin"
    - some VSA support resizing of a hypervector, via matrix multiplication, to enable computing on varying sized hv
  - "Instead of taking just the single best match, take the top 2-3 matches, bundle them together, and then search the codebook again with this new, denoised vector" this is clever, but i agree that "A better long-term solution is to design your encoding scheme hierarchically"
  - types of input data examined in the paper
    - categorical data (symbol)
      - bioinfo data seems to have lots of records which are easily expressed as bundles of bound key-value pairs
      - diagnosis, medication, lab_test, etc
    - numeric data (number)
      - a brief mention of FPE for numeric ranges
      - bond angles and molecule handedness
    - compositional data (containers)
      - sequential data
        - long and categorical: acgt
        - numeric: ecg, emg, eeg
      - relational data
        - patient knowledge graphs
        - molecules (again)
      - multi-modal data
    - opaque data
      - images
      - use the early layers of a CNN as a front-end then VSA as a backend
  - i couldn't find the source code for uhd :(
- Linear Codes for Hyperdimensional Computing
  - random linear codes makes unbinding, "recovery", simpler and better than resonator networks
    - linear algebra instead of combinatorial/exhaustive search
  - the paper supports generating hypervectors on the fly
    - so you don't have to ask for _G_ orthogonal symbols upfront
  - the "un" operations (undo)
    - bundle-recovery vs bind-recovery
    - exact vs approximate
  - "decoding random linear codes under noise is NP-hard"
    - what does this do to robustness of HDC?
  - instead of `coin_toss()` or `dice_roll()` being used to generate an element of a hypervector, hypervector are generated as linear combinations of some generator matrix's rows - predictable
- All You Need is Unary: End-to-End Bit-Stream Processing in Hyperdimensional Computing
  - "demonstrating that there is no need for randomness in HDC systems" ... "In this work, we advocate unary HVs, free from randomness"
    - randomness is used to decrease orthog between basis hv but orthog can be ensured in other ways
    - how does removing randomness for the HV generation process affect security or cloud-based HDC computing paradigms?
    - random HVs (10k random bits) look much like encrypted data. i suspect using ld sequences tarnishes this resemblance
  - ld sequence, van der corput
  - unary bit-stream processing
  - figure 1, the bumpy blue field is caused by noise in the hv
    - another way to decrease the height of these lumps is to increase hv dimensionality but that comes with a computational tax on _every_ operation
  - leveling
    - instead of flipping bits at random, flip some proportion of bits to 1s which represents 1 equal-sized level in the range
    - the example from the paper uses vectors with dim = 1024 and b/w pixel intensity range of 256, so each level is represented by 4 elements of the hvs
    - there's no step in the level procedure that says, "randomly pick 10 bits to flip"
      - if you want level 37, `[1] * (37 * (1024//256)) + [0] * (1024 - 37*(1024//256))`
      - if you want level 250, `[1] * (250 * (1024//256)) + [0] * (1024 - 250*(1024//256))`
- uHD: Unary Processing for Lightweight and Dynamic Hyperdimensional Computing
  - image embedding without binding in x,y coordinates sounds efficient
  - more ld seqeunce stuff
  - i don't full understand this paper
- Predicting the toxicity of chemical compounds via Hyperdimensional Computing
  - binary string classifier similar to spam sms model
    - 2 centroid/prototype hv
    - subtraction is used during training misclassification
  - data are SMILES ASCII strings (127 basis hv)
    - molecule -> 3d graph -> SMILES -> hypervector
      - an encoding of an encoding of an ...
    - SMILES has different tokenization strategies, they compare different ones: atom-wise, k-mer, or fragment-based
  - discovered optimal subsequence length
  - source code!
- A novel Vector-Symbolic Architecture for graph encoding and its application to viral pangenome-based species classification
  - viruses evolve quickly. good for classifying unseen variants/strains
    - any overlap with how malware variants are developed?
  - graph encoding of viral species
    - pangenome kmers -> graphs -> hypervector
      - "These pangenome graphs are powerful representations that can capture large-scale structural variations, such as insertions, deletion, and rearrangements, which are often missed by linear sequence alignment"
    - a node is a kmer
    - edge represents kmer adjacency
      - edge weight is the label/class
  - kmer_length=9, stride=1, grapHD encoding scheme
    - 2.3.2 contains pseudo-code implementation of the embedding procedure
  - retraining only made use of additive reinforcements, no subtraction used. why?
- HDC-X: A Hyperdimensional Computing Framework for Efficient Classification on Low-Power Devices
  - [code](https://github.com/jianglanwei/HDC-X)
  - leveling strategy for representing numbers is global linear using a single hv
- Practical Lessons on Vector-Symbolic Architectures in Deep Learning-Inspired Environments
  - MAP is great
    - "Even faster, with a linear runtime, multiple add permute (MAP (11)) and Hadamard linear binding (HLB (4)) appear as the best candidates for DNN integration."
    - "HLB can be seen as a real continuation of MAP-I"
  - overall guidance
    1. "Prefer linear VSAs or GPU-optimized implementations of HRR"
    2. "Replace cosine similarity with a linear readout"
    3. "Use linear VSAs or HRR equivalently under noise-free or noisy conditions"
    4. "Use weighted multi-level compositions to create hierarchical data structures"
- MissionHD: Hyperdimensional Refinement of Distribution-Deficient Reasoning Graphs for Video Anomaly Detection
  - nsf
    - 2127780  $299,999.00  4yrs  cyber
    - 2319198  $360,000.00  3yrs  cyber
    - 2321840  $796,800.00  3yrs  bioinformatics
    - 2312517  $499,793.00  3yrs  cyber
    - 2235472  $450,000.00  3yrs  cyber
    - 2431561  $499,999.00  3yrs  cyber
  - semiconductor research corporation
  - mil
    - office naval research
    - army research office
    - air force office of scientific research
  - industry
    - xilinx
    - cisco
- A Neural Hypervector Model of Memory-Driven Spatial Navigation
  - "modeling navigation-oriented memory"
  - i like that they used real humans
- Brain Inspired Probabilistic Occupancy Grid Mapping with Vector Symbolic Architectures
  -  multi-agent mapping is neat. hive mind.
  - [code](https://github.com/Parsa-Research-Laboratory/VSA-OGM)
- Structured temporal representation in time series classification with ROCKETs and hyperdimensional computing
- Implementing Holographic Reduced Representations for Spiking Neural Networks
  - [code](https://github.com/vidurayashan/SNN_VSA)
    - python, lava
  - "VSA ... implementation [can] be computed using binary, bipolar, continuous real, or continuous complex vectors"
  - FHRR is best as shown in "A Comparison of Vector Symbolic Architectures"
    - FHRR is the only VSA to enable scalar encoding via FPE
    - FHRR fits well with spiking neural networks architectures
      - SNNs are great for event-driven stuff like DVS and LiDAR
        - FHRR is good at binding input from multiple sensors
  - SNNs
   - input streams are encoded as spike trains
   - spike trains are operated upon
   - output is decoded from spike trains
  - neural responses based on time between spikes
  - "Since spikes are evaluated at discrete time steps, the original continuous values are discretised during this conversion, introducing error into the computations"
    - "Intel Loihi approximate ... continuous-time dynamics using a fixed-size discrete time-step model"
    - "timesteps have to be infinitely small, resulting in infinitely small LIF voltage increments. Practically, when simulating the spikes on digital hardware, a finite timestep is inevitable, and this introduces an encoding error"
  - I didn't understand the majority of this paper
- Recursive Binding for Similarity-Preserving Hypervector Representations of Sequences
  - FHRR for sequence encoding
    - their method should work on any VSA that supports self-binding
    - they use "recursive binding" which can be thought of as "integer power encoding". no fractional exponents needed as position in a sequence is discrete. no mention of bandwidth as in FPE
  - this paper reminds me of "LANGUAGE RECOGNITION USING RANDOM INDEXING" aka "Language Geometry using Random Indexing" by Joshi, Halseth, and Kanerva
    - language recognition via a bag of ngrams. similarity shows shared n-grams
  - this paper embeds a sequence as an hv such that small changes, like transposition, result in small similarity differences
    - Спасибо, мистер Левенште́йн
    - position similarity is continuous unlike in Joshi's paper where position is binary (the same or not)
      - turns edit distance into a continuous similarity kernel
        - why would we want this? in case the typo is 2 characters away?
        - perhaps the continuous nature would be useful when considering diphthongs or minimal pair words with similar sounds, such as replacing g/k, ㄱ/ㅋ
      - requires a similarity radius
        - R=1 behaves like exact match, hamming distance
        - R=2 1 position shift of symbol is a small penalty in similarity of hv
        - R=3 0-2 position shift results in small similarity penality
          - this R matches human perception: thsee lteter suqeeencs are stlil radbeale
        - R>5 differing sequences may result in hv which are too similar
    - position location 3 is near position 2 but is far from position 33
    - transposition reduces similarity less than replacement
    - this provides equivariance to sequence shifts
  - see also "Shift-Equivariant Similarity-Preserving Hypervector Representations of Sequences"

Summary
-------
What is Hyperdimensional computing?
- See [this video](https://www.youtube.com/watch?v=8Lonl-jSqUw).
- See a [Tutorial on Hyperdimensional Computing](https://michielstock.github.io/posts/2022/2022-10-04-HDVtutorial/).
- See [Neuroscience 299: Computing with High-Dimensional Vectors - Fall 2021](https://redwood.berkeley.edu/courses/computing-with-high-dimensional-vectors/)


What makes a Vector Symbolic Architecture?
- concepts are high, but fixed, dimension random vectors. structure is built up from randomness
- holographic elements / distributed information
- operatorations: multiply, add, permute, similarity, ...

What are the differences between VSAs?
- Denis Kleyko provides a great [Overview of different HD Computing/VSA models](https://redwood.berkeley.edu/wp-content/uploads/2021/08/Module2_VSA_models_slides.pdf)
- [A comparison of Vector Symbolic Architectures](https://arxiv.org/abs/2001.11797) provides a comprehensive taxonomy of architectures

Why use HDC?
- HDC is inspired by the Tensor Product Representation
- supports probabilistic calculations
- supports online/streaming learning
- it aligns well with the theory of "distributed representation" aka "assemblies of neurons" theory of the brain
  - the cerebellum is a random access memory for high dimensional vectors. it supports a lifetime of learning.
- learned results are not a blackbox but are instead interpretable
- by pushing most of the heavy computations into embedding, the compelxities of learning are reduced
- binary models fail when the world is continuous. continuous models fail when the world is symbolic. HDC blends the two.


Notable VSAs
------------
- *Tensor Product Representations*
  - lossless :)
  - dimensionality grows :(

- *Holographic Reduced Representations*
  - *HRR*
    - the progenitor of VSA/HDC
    - bind: converts real elements to complex then back to real
      - noisy, requires cleanup
      - mixes amplitutes and phases of waves
  - *Fourier HRR*
    - bind: operates on complex elements directly
     - exact invertibility
     - rotates phases. everything has magnitude of 1
     - forms a group
    - same as HRR as "you can losslessly transform between them"
  - *Geometric Analogue of HRR*
  - *Generalized HRR*
    - elements are square matrices
    - bind: non-commutative, order matters
      - no need for permute operation
  - *Vector-Derived Transformation Binding*
    - bind: block-diagonal matrix-vector multiplication on real elements
      - hv length must be an integer squared
      - noisy, requires cleanup
  - *Square Matrix Representations*
    - square matrices

- *Binary Spatter Codes*
  - a special case of HRR where values are bound to binary: 0 or 180 degrees

- *Multiply Add Permute*
  - MAP-C (real)
  - MAP-B (bipolar)
    - the same thing as BSC but I think it's the easiest VSA to think about
  - MAP-I (integer)
    - instead of clipping addition/multiplication, permit uint32 overflows and then both operations are cyclical. no?
  - *Hadamard-derived Linear Binding (HLB)*
    - elements are sampled from bipolar Gaussian MM with means at +/-1 and variances of 1/d

- *Sparse Binary Distributed Representations*
  - aka *Binary Sparse Distributed Codes*
  - Conjunction-Disjunction
  - Context-Dependent Thinning (CDT)
  - only VSA where bind(A,B) is similar to bind(A,C). see Figure 1 of A Comparison of Vector Symbolic Architectures

- *(Binary) Sparse Block Codes*
  - aka *Binary Sparse Distributed Codes - segments* (BSDC-SEG)
  - similarities to SBDR, BSC, CGR
  - compressed (integers) and expanded (binary) hypervectors
  - bundle is thinned voting (CDT)
  - bind: block-wise permutation (binary) or modulus add (integers)

- *Modular Composite Representation*
  - bind: component-wise modular addition just like BSBC, BSC, FHRR, CGR
    - behaves the same as BSBC compressed (integers) 
  - *Cyclic Group Representation*
    - uses a different bundle and similarity op than MCR

- *Matrix Binding of Additive Terms*
  - binding is a matrix multiplication
  - permutation is a matrix multiplication
  - resizing is a matrix multiplication
  - bundling is just addition
  - "soft" support for JSON

- *Bloom filter*
  - a special case of VSA
  - standard, counting, scalable, etc.
  - the representation of an item is distributes across elements
  - all elements hold equal amounts of information


HDC Operations
--------------

| Operation            | Input                                              | Output                                                                 |
|----------------------|----------------------------------------------------|------------------------------------------------------------------------|
| *similarity*         | Two hypervectors                                   | A similarity metric |
| *bind*               | Two or more hypervectors                           | A bound (composite) hypervector approximately orthogonal to its constituents, from which constituents may be queried via inverse binding |
| *bundle*             | Two or more hypervectors                           | A superposed hypervector that preserves similarity to all constituent hypervectors |
| *permute*            | One hypervector and one permutation map               | A hypervector transformed by an invertible permutation, preserving similarity structure |
| *new symbol*         | None                                               | A randomly generated, approximately orthogonal hypervector symbol     |
| *level*              | Zero, one, or two hypervectors                     | A set or sequence of hypervectors encoding ordered or continuous values via structured similarity in hyperspace |
| *normalize / clip*   | One hypervector                                    | A constrained or normalized hypervector, typically applied after bundling or binding to maintain representational capacity |
| *unbind*             | One bound hypervector and one or more constituents | An approximate inverse binding operation yielding the remaining bound components |
| *unbundle*           | One superposed hypervector and one or more constituents | A partial removal of superposed components from a bundled hypervector |
| *cleanup*            | One noisy hypervector                              | The closest matching stored hypervector retrieved via associative (cleanup) memory |


- Similarity
  - Quantifies how near two symbols are in the hyperspace
  - Common measures: Hamming, Cosine, Dot product, Correlation, Manhattan or Cyclic Manhattan

- Binding
  - Captures structured associations, similar to Tensor Product Representations
  - Maintains fixed dimensionality unlike TPR
  - Pefectly invertible binding operations form groups over a set of hypervectors in a fixed-dimensional hyperspace
    - In binary HDC with XOR binding, the group has order `2^n`
    - Some operations include: circular convolution, permutation, element-wise multiplication, element-wise xor, matrix-vector multiplication

- Bundle
  - Also called superposition, learning, accumulation, or voting
  - Combines multiple hypervectors into a single symbol that represents all of them simultaneously, or [holographically](https://en.wikipedia.org/wiki/Dennis_Gabor). Jó napot, Gabor úr.

- Permutation operations
  - Transforms hypervector indices. Can be any bijective map. Cyclic shift is simple to think about
  - The full set of index permutations has order `n!`
  - Cyclic permutations form a smaller subgroup with order `n`
  - Block permutations form can form groups of discretized phases
  - Permutations are also bindings

- Normalization constraints
  - Keeps hypervectors within valid ranges
  - Methods: element-wise clipping or global normalization
  - Preserves similarity structure and prevents unbounded growth 

- Cleanup
  - Corrects noisy vectors from approximate operations
  - Uses a codebook or associative memory to restore/retrieve the closest matching hypervector

- Leveling
  - Creating a walk of the hyperspace based on similarity
  - How far similarity propagates from a single symbol: locality vs. globality
  - Common strategies include: Linear, Circular, Exponential, "Steps", Combinations of previously listed

- Generating new symbols
  - From a normal (Gaussian) distribution
  - From a weighted distribution
  - From a low-discrepancy sequence (e.g. Sobol)
  - From a Walsh–Hadamard sequence
  - From an external process like sensor data or a CNN
  - From the result of another operation in the hypervector space

- Implementing operations
  - Element type: boolean, integer, floating-point, or block-based components
  - Algebraic properties: presence of an identity element, symmetry, and inverses
  - Dimensionality: number of components in each hypervector
  - Segmentation: whether vectors are partitioned into blocks for structured operations
  - Sparsity: proportion of nonzero or active elements
  - Precision: effects of approximate calculations and normalization/clipping/pooling
  - Reliability: partial/faulty operations. Are operations permitted to fail occasionally? If pair-wise multiply fails on 10% of the elements of bound/bundled/permuted vector, what is the affect on the system?


Misc
----
- code
  - Various [data structures](https://github.com/denkle/HDC-VSA_cookbook_tutorial/blob/main/HDVecSym/DS.py) built up from a custom ternary MAP implementation
  - [Binary Sparse Distributed Representation with segments BSBC-SEG](https://github.com/benjamin-asdf/vsa-binary-sparse-distributed-segments-clj) in clojure
  - [HoloVec](https://github.com/Twistient/HoloVec)
    - lovely examples, numpy only, modern looking docs, cool name, uses emojis ✅
    - encoders by data type
    - examples even include recommendations as to when to use different types of encoders and architectures. use cases, suggested next tutorial. wow.
      - they compare: FPE, Thermom, Leveling :)
      - they dont make any mention of the "similarity spread" or locality of leveling strategies :( they also assume evenly spaced steps/levels
    - [gesture recognition](https://github.com/Twistient/gesture-demo/blob/main/src/lib/hdc.ts) using HDC in TypeScript. no license :(
  - [torchhd](https://github.com/hyperdimensional-computing/torchhd)
    - excellent coverage of different HDC/VSA including references to literature
    - well engineered codebase, readable
  - [openhd](https://github.com/UCSD-SEELab/openhd)
  - [hdtorch](https://pypi.org/project/hdtorch/)
  - [hdlib](https://github.com/cumbof/hdlib)
  - [hypervector](https://github.com/rishikanthc/hypervector)
    - encoder.rs utilizes MBAT to encode JSON into HV. very cool.
  - [hdc](https://github.com/Zeldax64/hdc), HDC examples in C++ including BSC Vector classes and item memories
    - no license :(
  - [HDCpy](https://github.com/jdcasanasr/hdcpy)
    - hobby project so nothing groundbreaking, BUT its dead simple to understand
    - applying BSC and MAP to common datasets
      - leveling element "flips"
  - [HLB](https://github.com/FutureComputing4AI/Hadamard-derived-Linear-Binding/blob/main/Classical%20VSA%20Tasks/vsa_models.py#L13)
  - [hrrformer](https://github.com/FutureComputing4AI/Hrrformer)
  - [hrr](https://github.com/MahmudulAlam/Holographic-Reduced-Representations)
- what's the difference between HoloVec and TorchHD?
  - bsc was dense parent of
    - bsdr-cdt, sparsity across the entire hypervector, constrains the lengths of integer hv to the square root of the binary hv dimensionality, leads to square matrices which leads to ghrr which generalizes fhrr into a vector function architecture. in ghrr commutivity is controllable by diagonality through the size, m, of unitary matrices which act as hv elements.
    - bsdr-seg, sparsity in blocks leads to hardware friendly approximation of fhrr. with a block size of 2 this behaves like bsc. as the block size goes to inifity it becomes fhrr-like.
    - both, binary representations can be compressed to integers. 
  - holovec provides best VSA/HDC for expressivity - deeply nested structures like trees and graphs
  - torchhd provides best VSA/HDC for hardware-friendliness - RISCV, FPGA, ASIC friendly
- datasets mentioned in literature
  - Secure Water Treatment (SWaT) from [iTrust](https://itrust.sutd.edu.sg/itrust-labs_datasets/dataset_info/) or [Kaggle](https://www.kaggle.com/datasets/vishala28/swat-dataset-secure-water-treatment-system)
    - [Anomaly Detection for Industrial Control Systems](https://www.kaggle.com/code/scarss/anomaly-detection-for-industrial-control-systems)
  - voxceleb and voxceleb2
    - [VoxCeleb1](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox1.html)
  - isolet
  - ucihar
  - mnist
  - UCI Machine Learning Repository
  - UCR Time Series Archive
  - Numenta Anomaly Benchmark (NAB)
  - Long-Range Arena (LRA)
  - malware
    - Microsoft Malware Classification Challenge (Kaggle)
    - The Drebin Dataset
    - EMBER (Elastic Malware Benchmark for Empowering Researchers)
  - eTraM : Event-based Traffic Monitoring Dataset
    - FREE event data from a DVS camera
    - https://github.com/eventbasedvision/eTraM
    - https://eventbasedvision.github.io/eTraM/
  - [CICIDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)
  - [Car-Hacking](https://ocslab.hksecurity.net/Datasets/car-hacking-dataset)
  - NWPU-RESISC45 - REmote Sensing Image Scene Classification
  - FMA: A Dataset For Music Analysis
  - ARCish datasets: Sort-of-ARC, 1D-ARC, KidsARC, ConceptARC, MiniARC
  - A Dataset of EEG Signals from Adults with ADHD and Healthy Controls: Resting State, Cognitive function, and Sound Listening Paradigm
- pangenomics
  - studying all the genes of all strains of a species
  - [a simple pangenomic graph](https://pangenome.github.io/images/genomic-vs-pangenomic-analysis.png)
  - [a tube map visualization](https://pmc.ncbi.nlm.nih.gov/articles/PMC10638906/figure/F1/) of a pangeonmic graph from  "Pangenome graph construction from genome alignments with Minigraph-Cactus" 
    - [a tube map view of the loop](https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Chicago_L_diagram_sb.svg/1827px-Chicago_L_diagram_sb.svg.png)
- HDC accuracy can be improved by increasing vector lengths (dimensions) or making elements types more complex
  - increasing complexity of each element is "better" at conveying information than making the vectors longer
  - more complex element types make for more complex hardware needs
- VSA has relationships with compressed sensing, which makes sense given how bundling of vectors is how VSA "learns"
- when creating vectors, the distribution of element values does not need to be random (50% 1's and 50% 0's)
  - it may be useful to create sparse vectors where the distribution of 1's is 1% of the elements
  - sparse vectors are more easily compressed, making them more memory efficient 
  - the distribution from which elements are sampled influence the shape of the induced kernel as shown in VFA
- how to encode a vector of scalars into a hypervector symbol?
  - multiply it by a constant random matrix (a projection/hat matrix)
  - use FPE to encode each scalar element then compose/combine the FPE hypervectors together
- one of the big issues with HDC/VSA is that there is no standard method of encoding the application-specific data into vectors
  - should i bind with multiplication or permuation? that depends on your use-case.
  - "the HV representations must be designed to capture the information that is important for solving the problem and presenting it in a form that can be exploited by the HDC/VSA"
  - 2d images need special encoding steps to ensure nearby pixels are "related" to each other
    - turning a 2d image into a 1d vector simply by concatination is naive
    - there is a need to incorporate both x and y axis data as well as pixel color value
      - how to encode colors?
        - rgb?
          - ["There are colors you can't get in this system"](https://youtu.be/TEjDYtkLRdQ?t=686)
        - what about the [Munsell system](https://cdn.britannica.com/34/2834-050-8758A9D8/tree-Munsell-system-colours-representation-scales-chroma.jpg)? or [OKLAB](https://upload.wikimedia.org/wikipedia/commons/1/16/Linear%2C_sRGB%2C_OKLAB.gif)?
    - partial permutation can address this by creating a radius where similar colors will have similar HVs
    - fractional power encoding can also be used
      - generate role-filler HVs for x and y
      - then raise the x vector to the exponent indicating the column of the pixel
      - do the same for the y
      - bind the pixel value HV with the exponentialized x and y HVs
- Fractional Power Encoding (FPE)
  - discussed in Plate's original HR paper
  - self-binding can be a method for encoding integers in VSAs where vectors are NOT their own inverse. so this wont work for ternary or binary VSA
    1. pick a random basis vector. this represents 1.
    2. bind it with itselg. this represents 2.
    3. repeat n times to reach the integer n.
  - consider a simple example where we only examine a single element of a vector, 6
    - vector represents integer 1, vector element value: 6 (6)
    - vector represents integer 2, vector element value: 36 (6 * 6)
    - vector represents integer 3, vector element value: 216 (6 * 6 * 6)
  - FPE takes this self-binding scheme one step further by introducing fractional self-binding. this permits the representation of real numbers, not just integers
    - vector represents real 1.5, vector element value: 18 (6 * 6 * 1/2)
    - vector represents real 1.33, vectot element value: 12 (6 * 6 * 1/3)
  - self-binding/FPE works for binding operators besides element-wise multiplication
- Resonator Networks
  - aka Hopfield Network
  - similar to the result of gradient descent
  - an iterative algorithm that searches the combinatoric space of the codebooks without searching by exhaustion
  - given an HV from a binding operation, the codebooks for the input of the binding operation, determine the inputs of binding operation
    - create 'estimate' vectors, these represent your initial guesses
      - xhat, yhat, zhat = hdv(), hdv(), hdv()
    - do something with the estimates
    - update the estimates based on results of comparison to portions of the codebooks
    - utilizes superimposed 'guesses' or 'estimates' to find best guesses for one parameter at a time
    - iterates to find best
      - z, with estimates of y and x
      - y, with estimates of x and z
      - z, with estimates of y and z
- low discrepency sequences
  - i'm not sure about using these...
  - sobol and others
  - much literature points to these instead of random hv generation
  - ld seqs fill a space more evenly. randomly filling a space will produce clumps
  - similar to ordered dithering and halftones 
  - may be useful for images as in uhd
- HDC can be incorporated into NN to make both better
  - NN frontend to generate HVs
  - HDC frontend to generate vectors for NN
- what happens when a HDC model is trained on "levels" but then tested with samples that are outside of the levels' range's max/min?
- fix sized binary/ternary vectors, as in MAP, remind me of
  - nPrint: A Standard Data Representation for Network Traffic Analysis
    - concatenate all maximum length PDUs together to make a long sparse block vector
  - Ramanujan's sum, namaste sir
    - infinite sum of natural numbers equals `-1/12`
    - one of the steps to solve the formula is to calculate 1/2 as the sum of the infinite series: 1 - 1 + 1 - 1 + 1 - ...
- multiple time-based signals can be quantized, then the signal at each timestep can be bundled together
  - combining multiple signals into a single vector
  - this was done for seizure detection as well as gesture identification
- "In general, DL’s [Deep Learning] strength is in learning a mapping from one space to another, given that these spaces are densely populated with examples. HDC, however, shines when there is a specific, known structure that one wishes to encode."
- HDC models can be improved with adversarial mutated samples, just like other models
  - mutate/alter the training data with some strategy (random noise, column/row permuation, etc)
  - train/test on the mutated data
  - inspired by fuzzing techniques
- HDC has capacity limits in the number of symbols...
  - you can have in working memory given the need for a cleanup step in retrieval
  - you can bundle together before the resulting HV converge to random noise
    - this causes results of bundling to "forget"
- a block can be thought of and operated on like a 'sampled' (or 'reduced') version of its source vector
  - all HV symbols are conceptually sampled versions of larger, and more precise, vector
    - the tensor product is the Platonic Form
  - blocks are a special case of vector which carry with them a:
    - source vector
    - contextual mapping into their source vector
- there is no least significant bit in a hyper vector. all the elements hold th same amount of information
- concentration of measure ensures randomly intialized HVs are dissimilar
- each dimension (element) of an HV increases the vector space exponentially
  - projecting something onto a bigger surface is often useful
    - think about a screen projector, it makes small images easier to see
  - projecting higher dimensional data into lower dimensions is often useful too
    - think about the 2d shadow cast by a 3d object
- hypercomplex hypervectors, quaternions and octonions
- [zotero HDC/VSA group library](https://www.zotero.org/groups/5100301/hdvsa_literature/library)
- if we can substitute from one HV to another, making hv1 more similar to hv2...
  - can we make hv1 more unlike hv2?
  - instead of copying bits from hv2 into new levels, copy flipped bits from hv2 into hv1
- special purpose block coding or hv which support holographic operations
  - 30000 dim hvs
    - block_size: 3
    - block_count: 10000
  - index % 3 determines if an operation applies to the element
    - 0, used for bundling
    - 1, used for permuting
    - 2, used for binding
  - each operation would essentially be done partially at 33% but would have a deterministic pattern to which elements it 'fails' on
- binding
  - binding all the hypervectors in a VSA together converges to the binding identity
  - binding is a symmetric operation. bind with itself to invert.
    - A rotated/reflected around the hypercube according to B results in C
  - binding is a group operation
    - element * element = element
    - the space is the set of all possible hypervectors
      - consider integer MAP... clipping influences the group
    - permutation is a binding operation. it too forms a group.
      - multi-binding with multiplcation is commutative
      - multi-binding with permutation is not unless constrained to cyclic shifting
  - binding is how we "combine" concepts into new concepts in our mind
- i wonder if our brains bundle when we sleep
- "science cannot move forward without heaps"
  - [thank you to the heaps](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Memorial_to_the_lab_animals_%2814604111622%29.jpg/1024px-Memorial_to_the_lab_animals_%2814604111622%29.jpg)
