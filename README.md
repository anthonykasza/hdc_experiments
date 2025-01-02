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
- Vector Symbolic Architectures, Luis El Srouji 
  - https://video.ucdavis.edu/media/Vector+Symbolic+Architectures/1_9b6hn4p2
- Classification and Recall With Binary Hyperdimensional Computing: Tradeoffs in Choice of Density and Mapping Characteristics
- Robust Hyperdimensional Computing Against Cyber Atacks and Hardware Errors: A Survey
- EventHD: Robust and efficient hyperdimensional learning with neuromorphic sensor



Definitions
-----------
- Vector Symbolic Architecture - computing architectures which utilize large vectors to represent symbols
  - Vector - indexed lists
    - element types
      - binary
      - bipolar/ternary
      - integers
      - floats
      - imaginary
      - "finite groups"
        - binary is a special type of group VSA, with group of size 2
  - Symbols - representations of something else
    - e.g. emojis are symbols
      - what concept does 🍑 represent?
    - e.g. types in system languages are symbols
      - how are `int` types represented in memory in C?
        - 32 bits (4 bytes)
          - min: 00000000 00000000 00000000 00000000
          - max: 11111111 11111111 11111111 11111111
        - `int x = 3;`
          - 00000000 00000000 00000000 00000011
        - why 4 bytes? why not 4 MB?
          - C programmers would say that's a waste of bits (waste of memory)
            - VSA programmers would disagree - discussed more below
  - Architecture - the means of computation. how the computer does stuff.
    - operations, memory, data types
    - e.g. x86/x64, ARM, Power(PC), RISC-V
  - VSA go by many names
    - distributed representations
      - because information contained in the symbol is distributed amoung all of its elements
    - high/hyper-dimensional computing
      - because it uses high (hyper) dimensional vectors as atomic/basis types
    - random indexing
    - projection
    - embeddings



Revisiting Dimensionality
-------------------------
- a return to the question "why 4 bytes? why not 4 MB?"
  - this approach may seem wasteful in comparison to the memory efficiency of languages like C
  - dimensionality is both a blessing and curse
    - redundancy in VSA vectors, more bits than needed to represent the data
    - dimensionality stays fixed under addition, multiplication, and permutation
  - each additional element (bit) of the vector increases the "space" exponentially
  - ensures randomly sampled vectors will be quasi-orthogonal
    - -100 is blue, 0 is green(yellow), 100 is red: what color is the number 2?
      - is the number 2 green? no.
      - is the number 2 pretty-much-basically-sort-kinda green? yeah, with a dash of red
      - which color is the number 50? half-green and half-red.
      - which color is the number 51 or 49? 
    - pick a number 1 through 10
      - someone guesses 1, 4, 8, and someone guesses 2.9
      - we just assume that person meant 3 because 2.9 is nearest to 3
        - perhaps there was some noise in their guess?
  - projecting something onto a bigger surface is often useful
    - think about a screen projector, it makes small images easier to see
  - aligns well with the theory of "distributed representation" of the brain
    - the brain doesn't have a single neuron representing the word "desk"
    - the brain probably has a set of neurons representing the concept of a desk
    - the set of neurons (symbol) for "desk" is likely similar (cossim) to the set of neurons (symbol) for "table"



Proposed Architectures
----------------------
- Multiply-Add-Permute (MAP)
  - C, real (e.g. floats from -1 to 1)
  - B, binary (e.g. 0/1 or -1/1)
  - I, integers (e.g. range of values grows unless "clipped")
  - MAP operations on hyperdimensional vectors resembles quantum superpositions
    - operations on superposed vectors can occur
      - in parallel
      - originals HDV are recoverable post-operation
    - results can be extracted with inverse operations
- Binary Spatter Codes
- Binary Sparse Distributed Representation
  - CDT
  - S
  - SEG
- Holographic Reduced Representations
  - "reduced" in that all HVs are fixed length
  - "holographic" in that all elements represent information
  - Frequency
    - HRRF is measurably better than the rest in some cases
    - each component is a random complex number, a phase angle (phasor) between 0 and 2pi or between -pi and pi (centered around zed)
    - magnitude only is used
      - this appears related to spiking networks architectures
    - binding is Hadamard product
- Vector Derived Binding
- Matrix Binding of Additive Terms
- Tensor Product Representation
  - results in higher dimensional vectors
  - TPR is arguably not HDC because HDC uses fixed length vectors
  - TPR did, however, inspire HDC/VSA
- sparse block codes
  - HV is partitioned into blocks of equal size (so that the HV’s dimensionality is a multiple of the block size). In each block, there is only one nonzero component, i.e., the activity in each block is maximally sparse


Operations 
----------
- addition - summing two vectors into a single vector preserves information from both consituents
  - in some architectures, addition in replaced with a majority vote
  - cos(A) !~ cos(B)
  - cos(A) ~ cos(A+B)
  - cos(B) ~ cos(A+B)
  - cos(A+B) == cos(B+A)
- multiplication - multiplying two vectors into a single sector ensures all three has low similarity
  - distributes over add
  - no binding problem in HDC, to bind is to multiply
  - multiplication "binds" multiple vectors into a single vector
    - things can be "unbound" from the resulting vector by multiplying it with a constituent's inverse
      - which is itself in binary/bipolar representations
      - depending on the element complexity, unbinding is not always the reverse of binding
        - if this is the case, a "cleanup" step is required after unbinding which searches memory for the nearest HV and replaces the unbound HV with its the most similar in memory
  - cos(A) !~ cos(B)
  - cos(B) !~ cos(A)
  - cos(A) !~ cos(A*B)
  - cos(B) !~ cos(A*B)
  - cos(A*B) == cos(B*A)
  - (A*B) * A == B
  - (A*B) * B == A
- permutation - permutation "protects" the order of inputs to add/multiply
   - distributes over add and multiply
   - cos(A*B*C) == cos(B*C*A)
   - cos(A) !~ cos(permute(A))
- similarity - a measure applied to vector pairs
  - how similar are two vectors? 
    - which cluster does this unlabeled sample belong to? compare it to all centroid vectors
  - cossim for reals
  - hamdis for bipolar
  - what happens if we were to introduce noise and flip a few random bits in a vector?
    - what happens to a bloom filter?
      - FPs introduced for 0 bits changed to 1 bits
      - FNs introduced for 1 bits changed to 0 bits
    - what happens to the similarity between 2 hyperdimensional vectors?
      - not much
- substitution
  - continous real-time windowing
  - HVs A and B are dissimilar
  - elements of A are changed to match elements of B
  - B remains unchanged, A becomes more similar to B

Composing Data Structures
-------------------------
- sets (bundle)
- maps (bind)
  - aka "role-filler" binding
  - dict/tuple/record/row/struct types are formed using maps
- sequences (permute)
- bins/ranges/levels (permute then bundle)
  - some leveling strategies
    - incorporate a final step to ensure density is maintained after doing the random bit flips
      - this is typically beneficial for HVs of low dimensionality
    - ensure nearby levels are somewhat similar but levels which are a certain distance apart are considered MAXIMALLY dissimilar
      - this reminds me of an image convolution kernel
    - combine different strategies
      - e.g. log then linear
  - strategies, what sort of line would you like to draw?
    - linear, for representing a continuous range as an evenly spaced buckets
      - exact linear - hdDimensions / nBins = elementsPerBin
        - range should be based on the task-at-hand and not from training data's max/min values
          - e.g. PDUs typically have a maximum length defined by RFCs 
      - approximate linear mapping - cheaper than exact linear mapping 
        - "Approximate linear mapping [58] does not guarantee ideal linear characteristic of the mapping, but the overall decay of similarity between feature levels will be approximately linear"
    - circular, useful for modulus/cyclical calculations such as:
      - seasons of the year, hours of the day, months of the year
      - color spaces
      - distributing web requests to a pool of servers (similar to rendezvous/hrw hashing)
    - elliptic, like a circle but longer
    - logarithmic/exponential, shrink of shrink/growth of growth
      - bell curves
    - fibonacci (retracement)
- graphs (uniqly id vertices, bind vertices to create edges, then bundle edges to create graphs)
  - to create directed graphs, permute one of the node HVs before creating the edge HV
  - state machines
    - how to incorporate weight into edges?
      - multiply the edge HVs by a constant random matrix
      - create a discrete linear range HV large enough to support transition weight precision
        - then multiply each edge HV by the range's bin's HV
  - HyperRec, using hdc to make a recommendation system by predicting edges in a directed graph
- bloom filters - a special case of VSA
  - a set is represented by a bit array (vector)
    - an empty set is all zeros
    - a bit array is more memory efficient than storing all samples in memory
  - when adding an element to a bf, the item is hashed with several functions
    - the functions result in an index which is flipped from 0 to 1
  - when checking inness, an element is hashed (using the same set of functions)
    - the resulting indices of the bit vector are then checked for 1 values
    - if indices are 0, the item is definitely not in the set
    - hash collisions may cause FPs
  - no FNs, possible FPs
    - is this thing in your cache? the bf can answer with 'definitely no' or 'maybe yeah'


VSA Uses
--------
- language
  - n-grams (aka k-mers), where n can be letters, words, sentences, or any symbol
  - 't' = [101..111]
  - 'h' = [010..001]
  - 'e' = [101..110]
  - 'the' = bind( perm('t',2), perm('h', 1), 'e')
  - 'thf' = bind( unbind('the', 'e'), 'f')
  - 'tfe' = bind( unbind('the', perm('h', 1)), perm('f', 1))
    - this means that it is trivial to compute ngrams of any size given the vectors of it's constituents
  - tri_grams = bundle('aaa' ... 'the', 'thf', ... 'zzz')
  - trivial to answer the question: which language is this unlabeled text?
    - maintain a set of labeled Language Vectors
    - calculate the Text Vector for the unlabeled document
    - compare the Text Vector to all known Language Vectors
    - whichever Language Vector is most similar is the text's label
    - 10_000 element vectors contain information from 14_348_907 pentagrams as easily as 19_683 trigrams
  - a single vector can represent constituent vectors which represent 1grams, 2grams, 3grams ... infi-grams
- timeseries
  - discretized timeseries can be converted to ngrams and then analyzed the same way as language
  - continuous (streaming) time can be constructed using a lookback window of correlated vectors
    - eventHD
      - see Figure 2.B for a pictoral representation of continuous-time hvs
    - for a window of time +/- N
      1. generate an hv
      2. wait N steps (seconds)
      3. generate a new hv
      4. substitute 1/N bits of the hv from step 1 towards the hv in step 3, repeat N times until you have N "level" hvs ranging from step 1 hv to step 3 hv
      5. goto 2
      - this can be done indefinitely to represent the indefiniteness of time's passage
        - there *must* be some limit to the number of timesteps we can/should hold in memory 
      - bind the lookback-window hv (temporal information) with the signal hvs
        - in the eventHD paper they use spatial data from a camera-like sensor
- learning of centroids (class hv) is done by updating multiple centroids with each new sample
- file similarity
  - encode byte-grams instead of letter-grams or word-grams
  - the byte-alphabet is larger than the letter-alphabet: [a-zA-Z]
  - most common 'letter' in english is "E", most common in files?
    - my guess would be 0x00
- genetics
  - gene-alphabet is tiny (4) and that makes for poor suffix arrays
- vsa can be used for spellcheck and finding optimal string alignment
- hvs can be used for factorization thru resonator networks and the use of fractional power encoding



Misc
====
- hdc accuracy can be improved by icreasing vector lengths or making elements more complex than binary e.g. floats or complex
  - more complex numbers make for more complex hardware needs
  - increasing complexity of each element is "better" than making the vectors longer
- datasets mentioned in literature
  - isolet
  - ucihar
  - mnist
  - UCI Machine Learning Repository
  - UCR Time Series Archive
- Minkowski distance
- when creating vectors, the distribution of element values does not need to be random (50% 1's and 50% 0's)
  - it may be useful to create sparse vectors where the distribution of 1's is 1% of the elements
  - sparse vectors are more easily compressed, making them more memory efficient 
- fractional power encoding
  - if you take a VSA symbol (vector) and raise it to an exponent, something magical happens.. something to do with kernels
  - some literature refers to this as "trajectory association"
  - this only works if the bind op is NOT the inverse of itself
- VSA has relationships with compressed sensing, which makes sense given how bundling of vectors is how VSA "learns"
- how to encode a vector into a vector symbol? multiply it by a constant random matrix (a projection/hat matrix)
- there are methods of making a vector more/less dense
- one of the big issues with HDC/VSA is that there is no standard method of encoding the application-specific data into vectors
  - should i bind with multiplication or permuation?
    - that depends on your use-case
  - "the HV representations must be designed to capture the information that is important for solving the problem and presenting it in a form that can be exploited by the HDC/VSA"
  - 2d images need special encoding steps to ensure nearby pixels are "related" to each other
    - turning a 2d image into a 1d vector simply by concatination is naive
    - there is a need to incorporate both x and y axis data as well as pixel color value
    - partial permutation can address this by creating a radius where similar colors will have similar hvs
    - fractional power encoding can also be used
      - generate role-filler HVs for x and y
      - then raise the x vector to the exponent indicating the column of the pixel
      - do the same for the y
      - bind the pixel value HV with the exponentialized x and y HVs
- HDC can be incorporated into NN to make both better
  - NN frontend to generate HVs
  - HDC frontend to generate vectors for NN
- what happens when a HDC model is trained on "levels" but then tested with samples that are outside of the HDV's range's max/min?
- HDC is prommising for nano-scale tech and FPGAs
- fix sized ternary vectors remind me of nPrint
- multiple time-based signals can be quantized, then the signal at each timestep can be bundled together
  - combining multiple signals into a single vector
- "In general, DL’s [Deep Learning] strength is in learning a mapping from one space to another, given that these spaces are densely populated with examples. HDC, however, shines when there is a specific, known structure that one wishes to encode."
- HDC models can be improved with adversarial mutated samples, just like other models
  - mutate/alter the training data with some strategy (random noise, column/row permuation, etc)
  - train/test on the mutated data
  - inspired by fuzzing techniques
- HDC has capacity limits in the number of symbols
  - you can have in working memory given the need for a cleanup step in retrieval
  - you can bundle together before a centroid becomes as good as a random guess
