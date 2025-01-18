An attempt to learn more about VSAs and HDC.


References
----------
- Language Geometry using Random Indexing
- Hyperdimensional Computing: An Introduction to Computing in Distributed Representation with High-Dimensional Random Vectors (Kanerva)
- Holographic Reduced Representations (Plate)
- HDCluster: An Accurate Clustering Using Brain-Inspired High-Dimensional Computing
- A comparison of vector symbolic architectures
- Computing with High-Dimensional Vectors (Kanerva) 
  - Stanford University Colloquium on Computer Systems EE380 Spring 2023
  - https://www.youtube.com/watch?v=zUCoxhExe0o
- Learning with Holographic Reduced Representations
- Vector Symbolic Architectures In Clojure (Carin Meier)
  - https://www.youtube.com/watch?v=j7ygjfbBJD0
- Infini-gram: Scaling Unbounded n-gram Language Models to a Trillion Tokens
- GraphHD: Efficient graph classification using hyperdimensional computing
- Understanding Hyperdimensional Computing for Parallel Single-Pass Learn
  - https://github.com/Cornell-RelaxML/Hyperdimensional-Computing
- A Survey on Hyperdimensional Computing aka Vector Symbolic Architectures, Part I: Models and Data Transformations
  - A Survey on Hyperdimensional Computing aka Vector Symbolic Architectures, Part II: Applications, Cognitive Models, and Challenges
  - over 440 papers cited in the review. its a big field
- Hyper-Dimensional Computing Challenges and Opportunities for AI Applications
- SearcHD: A Memory-Centric Hyperdimensional Computing with Stochastic Training
- Classification using Hyperdimensional Computing: A Review
  - table 1 is interesting
- Hyperdimensional Biosignal Processing: A Case Study for EMG-based Hand Gesture Recognition
- HYPERDIMENSIONAL COMPUTING: A FAST, ROBUST AND INTERPRETABLE PARADIGM FOR BIOLOGICAL DATA
  - figure 1b is awesome!
- Hyperdimensional Hashing: A Robust and Efficient Dynamic Hash Table
- HDTest: Differential Fuzz Testing of Brain-Inspired Hyperdimensional Computing
- VSAONLINE
  - https://sites.google.com/view/hdvsaonline/home
- MIDNIGHTVSA
  - https://sites.google.com/ltu.se/midnightvsa
- Vector Symbolic Architectures, Luis El Srouji 
  - https://video.ucdavis.edu/media/Vector+Symbolic+Architectures/1_9b6hn4p2
- Classification and Recall With Binary Hyperdimensional Computing: Tradeoffs in Choice of Density and Mapping Characteristics
- Robust Hyperdimensional Computing Against Cyber Atacks and Hardware Errors: A Survey
- EventHD: Robust and efficient hyperdimensional learning with neuromorphic sensor
- Get to know SAR, Interferometry
  - https://nisar.jpl.nasa.gov/mission/get-to-know-sar/interferometry/
- Generalized Holographic Reduced Representations
- Recasting Self-Attention with Holographic Reduced Representations
- Deploying Convolutional Networks on Untrusted Platforms Using 2D Holographic Reduced Representations
- Neuroscience 299: Computing with High-Dimensional Vectors - Fall 2021
  - https://redwood.berkeley.edu/courses/computing-with-high-dimensional-vectors/
- Fractional Binding in Vector Symbolic Architectures as Quasi-Probability Statements
- HDC/VSA: Binary Sparse Distributed Representation with segments
  - https://github.com/benjamin-asdf/vsa-binary-sparse-distributed-segments-clj
- Tutorial on Hyperdimensional Computing
  - https://michielstock.github.io/posts/2022/2022-10-04-HDVtutorial/


Definitions
-----------
- Vector Symbolic Architecture, computing architectures which utilize large vectors to represent symbols
  - Vector, lists
  - Symbols, representations of something else
    - e.g. emjois are symbols. what concept does 🍑 represent?
  - Architecture, the means of computation. how the computer does stuff.
    - operations, memory, data types
    - e.g. x86/x64, ARM, Power(PC), RISC-V

- What makes a VSA?
  - random initialization of elements
    - however, the distributions can vary between VSA
  - fixed dimension vector operatations
    - consider the following: in C, types are symbols
      - how are `int` types represented in memory in C?
        - 32 bits (4 bytes)
          - min value: `00000000 00000000 00000000 00000000`
          - max value: `11111111 11111111 11111111 11111111`
        - `int x = 3;`
          - 3 value: `00000000 00000000 00000000 00000011`
            - most/least significant bit
            - values are positional encoded
        - why 4 bytes? why not 4 MB?
          - those concerned with memory efficiency (C programmers) would say that's a waste of bits (waste of memory)
            - unnecessary dimensionality appears wasteful
      - how are types represented in memory in VSA/HDC?
        - everything is a list of elements
          - all elements hold the same amount of information
          - there is no most/least significant bit, all bits are equally significant

    - large dimensionality is both a blessing and curse
      - redundancy, useful for error correction and noisy calculations
      - dimensionality stays fixed through any operation
      - concentration of measure ensures randomly intialized HVs are dissimilar
      - each dimension (element) increases the vector space exponentially
      - projecting something onto a bigger surface is often useful
        - think about a screen projector, it makes small images easier to see
    - aligns well with the theory of "distributed representation" of the brain
      - the brain doesn't have a single neuron representing the word "desk"
      - the brain probably has a set of neurons representing the concept of "desk"
      - the set of neurons (symbol) for "desk" is likely similar (cossim) to the set of neurons (symbol) for "table"


- VSA goes by many names
  - distributed representations, because information contained in the symbol is distributed amoung all of its elements
  - high-dimensional computing and hyper-dimensional computing, because it uses high dimensional vectors as atomic/basis types (HDC)
  - random indexing
  - reduced representations
  - spatter code and block codes
  - projections
  - embeddings

  Tensor Product Representation
  - combination of role vectors (representing structure of data) and filler vectors (representing values of data)
  - resulting vector is longer than either input HV
  - TPR is arguably not HDC because HDC requires fixed length vectors
  - TPR did, however, inspire HDC

  Multiply-Add-Permute (MAP)

  Holographic Reduced Representations
  - "reduced", all HVs are fixed length
  - "holographic", all elements represent information equally
    - a subset of bits from an HV represents the same object, just with less precision
      - 10 randomly selected bits from the HV represents the same symbol as all 10_000 bits
      - this is akin to cutting a hologram into pieces
    - what is a hologram?
      - jó napot, Gabor úr
      - holograms involve lasers and lightwave interference patterns
        - scanning objects with interference patterns is called interferometry
          - interferometry has a ton of applications, e.g. JPL used it to measure surface topography changes after the 2014 Napa earthquake
  - Fourier HHR
    - FHRR/HRRF is measurably better than other VSAs in some cases
    - each element of a HV is a random phase angle (phasor) between -pi and pi
    - magnitude only is used
      - this appears related to spiking networks architectures

  Sparse Block Codes
  - HV is partitioned into blocks (segments) of equal size 
    - the HV’s dimensionality is a multiple of the block size
  - block-wise (segment-wise) operations
    - ensure a specified sparsity
    - permute the block
    - combine blocks with other blocks or scalars
      - bind, bundle, substitue, maybe further subdivide the block?
        - block of block codes, hyperdimensional blocks

  Bloom filters, a special case of VSA
  - a set is represented by a binary vector
    - an empty set is all zeros
    - a single vector is more memory efficient than storing all samples
  - when adding an element to a bf, the item is hashed with several functions
    - the functions result in an index which is flipped from 0 to 1
  - when checking inness, an element is hashed (using the same set of functions)
    - the resulting indices of the bit vector are then checked for 1 values
    - if indices are 0, the item is definitely not in the set
    - hash collisions may cause FPs
  - no FNs, possible FPs
    - is this thing in your cache? the bf can answer with 'definitely no' or 'maybe yeah'
  - what happens if we were to introduce noise and flip a few random bits in a vector?
    - what happens to a bloom filter?
      - FPs introduced for 0 bits changed to 1 bits
      - FNs introduced for 1 bits changed to 0 bits
    - what happens to the similarity between two HVs?
      - not much



Architectures
-------------
- Denis Kleyko provides a great 'Overview of different HD Computing/VSA models'
  - https://redwood.berkeley.edu/wp-content/uploads/2021/08/Module2_VSA_models_slides.pdf
- A comparison of Vector Symbolic Architectures provides a comprehensive taxonomy of architectures
  - https://arxiv.org/abs/2001.11797





Operations 
----------
not all operations are applicable to all architectures.
in my opinion, the most imporant operatation is binding followed by similarity.

operations can be conceptualize with 3 abstraction levels:
- elements operations which result in blocks or vectors
- blocks operations which result in blocks or vectors
- vectors operations which result in vectors or vector spaces

implementations of operations need to consider:
- atomic elements
  - types: bool, int, float
  - algebraic qualities: identity, symmetry, inverse
  - bounds checking
    - clipping, ensure element values are within a range
    - normalization, ensure element values are normalized to a range
- dimensionality and segmentation of vectors
- sparsity of vectors or segments
  - adding sparse vectors decreases sparsity
  - multiplying sparse vectors increase sparsity
- precision of results
  - cleanup step


operations include:
- addition, summing two vectors into a single vector preserves information from both consituents
  - aka: bundle, summation, superposition, learning, accumulation, majority vote

- multiplication, multiplying two vectors into a single vector moves the relationship between the inputs to a new region of the hyperspace 
  - aka: bind, compose, XOR, FFT, circular convolution
    - binding approximates TPR by because HDC requires fixed-dimensionality
    - see The Binding Problem
  - exponentiation
    - fractional power encoding (FPE)
      - aka: trajectory association
      - bind vector x times with itself, then the vector represents x
        - raise each element to the exponent x
        - this only works if the bind op is NOT the inverse of itself
      - multiplying is the same as adding exponents if the base vectors are the same
        - accomplishes scalar-like behavior 
      - variants on FPE
        - FPE with hadamard binding (phasor)
        - FPE with circular convolution binding (real valued)
        - block local circular convolution (sparse)
        - VFA, vector function architecture
          - FPE VSA plus a kernel function
            - your task will dictate your kernel but it opens the door to using VSA for learning with kernel functions
              - multidimensional kernels
              - window/modulus/circular kernels
              - periodic multidimensional kernels
                - grid cells, hex pattern in mice neurons
                - crystallography
                - lattice-based crypto
          - "the distribution from which components of the base vector are sampled [how sparsity is sprinkled into the HVs] determines the shape of the FPE kernel, which in turn induces a VFA for computing with band-limited functions"
          - any FPE with uniformly sampled base vectors have a universal kernel
            - whittaker-shannon interpolation formula
              - sinc function
                - normalized vs not
                - well defined envelop
                - crosses zero at the integers
          - binding a scalar to a vector (function) shifts the vector
          - binding 2 vectors (functions) together is a convolution of functions
             - functions are compositional
          - calculate similarities between functions

- division, undo multiplication
  - aka: unbind, factorization, decomposition
  - in some VSA unbinding is imperfect and requires a second cleanup operation

- cleanup, replace an operation's result with something else based on the result
  - its nearest neighbor in memory
    - resonator networks
    - replace the noisy HV from unbinding with the most similar HV in memory
  - a filtered version of itself
    - thinning
      - ensure the density/sparsity of a vector/segment

- permutation, preserves the order of elements or segments 
  - aka: shift, rotate, braid, protect
  - the operation needs to be invertible
    - does not need to be perfectly invertible if a cleanup is used
  - permute is similar to multiple
  - reverse is one type of permutation operation which:
    - takes 0 parameters
    - is lossess
    - is the inverse of itself
  - shift is one type of permuation operation which:
    - takes 1 parameter
    - is lossess
    - can be inverted by flipping the sign of the parameter

- similarity, a measure applied to vectors (segments) pairwise
  - e.g. cos similarity, hamming distance
  - similarity is robust to noise

- substitution, mutating an HV to become more similar to another HV
  - this is useful for leveling a vector space
  - HV1 becomes more similar to HV2, HV2 remains unchanged
  - a sequence of 'levels' (bins/buckets) is produces which leads from HV1 to HV2

- segmentation, create structure or depth
  - segment a vector into positional blocks
    - aka: blocking, grouping, chunking, windowing
    - locality preserving encoding (LPE)
      - thermometer code
        - linearly discretized levels
          - the first vector is hdv(all=0)
          - the last vector is hdv(all=1)
          - the HV grows its count of 1 values by flipping 0s to 1s by incrementing index
        - bundle(HVs[2],HVs[2]) != bundle(HVs[1],HVs[3])
          - if using integers: 2 + 2 != 1 + 3
          - consider the linearly discritized vector of hypervectors: HVs
          - bundling/binding indices of the hyperspace do not behave as adding/multiplying integers would
      - float code / sliding code
        - simmilar to 1-hot but more like window-hot, where the window is centered around the element
        - uses a fixed width window, slide across the all zeros vector, ensure bits in the window are 1s
        - the window is slid across the all-zeros HV
        - the start of the window is the HV's index in hypserspace
        - more sparse compared to thermometer codes
          - different similarity kernel
      - scatter code
        - no strict limitation on number of levels in a hyperspace
        - hspace[0] = some random dense vector
        - each level is created by randomly flipping a few elements in the previous unit

  - segment the 'space' between vectors into levels
    - aka: leveling, sampling, binning, discretization, quantization, bucketing
    - enearby levels are somewhat similar, distant levels are dissimilar
    - leveling strategies
      - linear, for representing a continuous range as an evenly spaced buckets
        - exact linear, dimensions / bins = elementsPerBin
        - approximate linear mapping - cheaper than exact linear mapping 
          - "Approximate linear mapping [58] does not guarantee ideal linear characteristic of the mapping, but the overall decay of similarity between feature levels will be approximately linear"
          - only store the start and stop HVs instead of the entire hyperspace
          - construct levels on the fly
      - circular, useful for modulus/cyclical calculations such as:
        - seasons of the year, hours of the day, months of the year, color spaces, round-robin hashing (rendezvous/hrw)
      - logarithmic/exponential, shrink of shrink/growth of growth
      - fibonacci (retracement)
      - combine different leveling strategies to create a vector space with varying granularity
        - e.g. log then linear
        - elliptic, like a circle but longer on two of the sides


Searching Memory
----------------
Consider the following: unbinding a "scene" of objects each with some set of properties
- decompose the scene into its composed constituents
  - objects in the scene have properties
    - color
    - shape
    - location
      - x
      - y
  - e.g. scene = bind(HV1, HV2, HV3)
    - HV1 = bind(color_HV, shape_HV, bind(x, y))
    - HV2 = bind(color_HV, shape_HV, bind(x, y))
    - HV3 = bind(color_HV, shape_HV, bind(x, y))
  - to understand the scene, you need to search the codebook for combinations of all atomic symbols for all properties
    - this can be expensive, which is why selecting an efficient encoding method is important
  - assume there are 100 unique items in each HV's codebook (lookup memory)
    - 100 possible items for HV1
    - 100 possible items for HV2
    - 100 possible items for HV3
    - worst case: 10 * 100 * 100 = 1_000_000 item combinations to check cossim with
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
- Hyperdimensional Quantum Factorization
  - in archetectures where unbinding is noisy (bind is not the exact inverse of unbind) a cleanup step is used
  - this paper utilizes Grover's algo to speed up the memory search done in the cleanup step
    - this approach is better than resonator networks
  - hardware does not currently exist to implement. womp womp.


Composing Structure with Vectors
--------------------------------
- sets (bundle)
- maps (bind)
- sequences (permute)
  - graphs (bind nodes, bundle paths)
    - paths and words are both ngrams
      - bind(HV1, perm(HV2, 2), perm(HV3, 3)
    - trees
    - finite state automata
- stacks

Misc
----
- torchhd
- HDC accuracy can be improved by increasing vector lengths (dimensions) or making elements types more complex
  - increasing complexity of each element is "better" at conveying information than making the vectors longer
  - more complex element types make for more complex hardware needs
- hrrformer
- datasets mentioned in literature
  - isolet
  - ucihar
  - mnist
  - UCI Machine Learning Repository
  - UCR Time Series Archive
  - Numenta Anomaly Benchmark (NAB)
- VSA has relationships with compressed sensing, which makes sense given how bundling of vectors is how VSA "learns"
- when creating vectors, the distribution of element values does not need to be random (50% 1's and 50% 0's)
  - it may be useful to create sparse vectors where the distribution of 1's is 1% of the elements
  - sparse vectors are more easily compressed, making them more memory efficient 
- how to encode a vector into a vector symbol? multiply it by a constant random matrix (a projection/hat matrix)
- one of the big issues with HDC/VSA is that there is no standard method of encoding the application-specific data into vectors
  - should i bind with multiplication or permuation? that depends on your use-case.
  - "the HV representations must be designed to capture the information that is important for solving the problem and presenting it in a form that can be exploited by the HDC/VSA"
  - 2d images need special encoding steps to ensure nearby pixels are "related" to each other
    - turning a 2d image into a 1d vector simply by concatination is naive
    - there is a need to incorporate both x and y axis data as well as pixel color value
    - partial permutation can address this by creating a radius where similar colors will have similar HVs
    - fractional power encoding can also be used
      - generate role-filler HVs for x and y
      - then raise the x vector to the exponent indicating the column of the pixel
      - do the same for the y
      - bind the pixel value HV with the exponentialized x and y HVs
- HDC can be incorporated into NN to make both better
  - NN frontend to generate HVs
  - HDC frontend to generate vectors for NN
- what happens when a HDC model is trained on "levels" but then tested with samples that are outside of the HDV's range's max/min?
- fix sized ternary vectors remind me of
  - nPrint
    - concatenate all maximum length PDUs together to make a long sparse block vector
  - Ramanujan's sum, namaste sir
    - infinite sum of natural numbers equals -1/12
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
- Random High-Dimensional Binary Vectors, Kernel Methods, and Hyperdimensional Computing
  - https://cse.umn.edu/ima/events/random-high-dimensional-binary-vectors-kernel-methods-and-hyperdimensional-computing
  - i do not understand all the math discussed
  - if you're working with spacial data and you don't encode spacial features in your VSA pipeline then the results will not be great
- a block can be thought of and operated on like a 'sampled' (or 'reduced') version of its source vector
  - all HV symbols are conceptually sampled versions of larger, and more precise, vector
    - the tensor product is the Platonic Form
  - blocks are a special case of vector which carry with them a:
    - source vector
    - contextual mapping into their source vector
