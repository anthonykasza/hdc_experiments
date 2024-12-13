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



Definitions
-----------
- Vector Symbolic Architecture - computing architectures which utilize large vectors to represent symbols
  - Vector - indexed lists
    - element types
      - binary
      - bipolar/tripolar
      - real
      - integers
      - imaginary
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
    - high/hyper-dimensional computing
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
  - Frequency
    - HRRF is measurably better than the rest in some cases
- Vector Derived Binding
- Matrix Binding of Additive Terms


Operations 
----------
- addition - summing two vectors into a single vector preserves information from both consituents
  - cos(A) !~ cos(B)
  - cos(A) ~ cos(A+B)
  - cos(B) ~ cos(A+B)
  - cos(A+B) == cos(B+A)
- multiplication - multiplying two vectors into a single sector ensures all three has low similarity
  - distributes over add
  - multiplication "binds" multiple vectors into a single vector
    - things can be "unbound" from the resulting vector by multiplying it with a constituent's inverse
      - which is itself in binary/bipolar representations
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



Composing Data Structures
-------------------------
- sets (bundle)
- dicts (bind)
- sequences (permute)
- bins/ranges/levels (permute then bundle)
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


Sequence Embedding
------------------
- language
  - ngrams, where n can be letters, words, sentences, or any symbol
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
- file similarity
  - encode byte-grams instead of letter-grams or word-grams


