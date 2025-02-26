An attempt to learn more about clustering in the context of HDC.


References
==========
- A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise
  - DBSCAN
  - what is clustering? "class identification, i.e. the grouping of the objects of a data- base into meaningful subclasses"
  - density-based clustering is very good at finding clusters of arbitrary shape (the algo isn't reliant on centroids)
  - dbscan requires few parameters. e.g. in constrast to kmeans, density-based clustering requires no upfront knowledge of how many clusters should exist
  - clustering algo types:
    - partitioning, divide a space into subspaces
    - hierarchical, add nodes to grow a tree
      - dendrograms can be grown 2 ways:
        - agglomerative, merging from the leaves to the root
        - divisive, splitting from the root to the leaves
      - Ejcluster
        - introduced the idea of a "sufficiently small" reachability distance
        - has unrealistic complexity, O(n^2)
  - DBSCAN works with any distance metric, so HDC's cossim/hamdis will plug right in
  - the concept of DBSCAN
    - samples are either part of a cluster or are noise
    - clusters are built by doing an epsilon (radius) search around sample points to build reachability neighborhoods (clusters)
      - clusters contain border points and core points
        - how would the algo handle border neighborhoods and core neighborhoods?
    - points can be reachable and/or connected. figure 3: density-reachability and density-connectivity
      - NOT ALL points in a cluster can reach each other (within each other's epsilon). but ALL points in a cluster are connected (reachable through a chain of intermediary points within epsilon from each other)
    1. "choose an arbitrary point from the database satisfying the core point condition as a seed"
    2. "retrieve all points that are density-reachable from the seed obtaining the cluster containing the seed"
  - how to choose an appropriate epsilon value for your dataset?
    - the best way to choose a good epsilon value is to use the density of the least dense (thinnest) cluster
    - HDBSCAN, a variant of DBSCAN
      - instead of using a single global epsilon, support regions of varying density
  - demos
    - https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html
    - https://scikit-learn.org/stable/auto_examples/cluster/plot_hdbscan.html
    - https://github.com/scikit-learn-contrib/hdbscan/tree/master/notebooks

- Incremental Clustering for Mining in a Data Warehousing Environment
  - IncrementalDBSCAN, DBSCAN on _updates_
    - DBSCAN was designed to run on a static database
    - a data warehouse is database that receives dynamic _updates_ (hourly, daily, bursty)
  - On the original DBSCAN: "The key idea of density-based clustering is that for each object of a cluster the neighborhood of a given radius (Eps) has to contain at least a minimum number of objects (MinPts), i.e. the cardinality of the neighborhood has to ex- ceed some threshold."
  - "Note that a cluster is uniquely determined by any of its core objects."
    - so, a cluster can be represented as an array of its core objects (aka dense regions)
      - not all core objects in an array are reachable but they are all connected
        - could we create hv bundles (centroids) of core objects which make up dense regions of a cluster? a cluster would then be an arrary of dense regions represented as hv bundles... each dense region would also have an array of perimeter objects. bundles are nice because they automagically forget things and we can clip them if they get too large (for non-binary/ternary VSA)
          - core `->` core: merge cores
          - core `->` perimeter `<-` core: note the data as perimeter to both cores
          - core `->` perimeter `<->` perimeter <- core: 
            - `->`, and `<->` edges could have different eps
      - this plays into the importance of tracking core and perimeter data points for each cluster
  - how's it different than DBSCAN?
    - changes, only the data point's reachable neighbors will be affected
      - adding data point, see Figure 4 and Figure 5
      - deleting data point, see Figure 6
    - region queries (finding a point's neighbors) are expensive, so minimizing them will make the algo more better. IncrDBSCAN only does region queries on the _updates_ and so is more better than adding the data to the entire database and then running traditional DBSCAN on it
  - demos
    - https://github.com/DataOmbudsman/incdbscan (not the same author as the paper)

- Data Stream Clustering Algorithms: A Review
  - 2.4 Density-based methods
    - grid-based clustering is nice because partitions can be calculated upfront 

- Knowledge Discovery in Databases II [Lecture 8: Velocity: Data Streams: Clustering](https://www.dbs.ifi.lmu.de/Lehre/KDD_II/WS1516/skript/KDD2-4-DataStreamsClustering.pdf)?
  - slide 22: A taxonomy of stream clustering approaches
  - ordering of data can vary in a stream. algo needs to find same clusters regardless of sample ordering
  - slide 34-47 algorith overviews

- An evaluation of data stream clustering algorithms
  - "Due to the infinite nature of data streams, it is impossible to store all these data in memory or even in disk, so we have the constraint of a single pass over the data, typically upon their arrival"
  - "it is difficult to know upon the arrival of an object whether it is an outlier or the first member of a new cluster"
  - "in a stream setting, one has to configure the number of clusters over time"
  - windowing strategies for streams
    - landmark - from some starting index to the current index. when a new landmark is set, discard all cached objects
    - sliding - fixed size lookback, discard the oldest object as a new one arrives
    - damped - the newest objects have the highest weight, "the damped window model does not discard objects completely, rather older objects contribute less as they are assigned lower weights"
      - this is how a bundle works, at least in binary VSA. in non-binary VSA, bundling may grow unless normalized periodically
    - tilted - time has different granularities
  - summarizing streams
    - cluster feature (CF), can be used to calculate centroid, radius, and diameter of a cluster
      - parameters:
        - n, the number of data objects
        - lin_sum, the linear sum of the data objects
        - sqr_lin_sum, the squared sum of the dataobjects
    - micro-cluster (MC)
      - parameters:
        - all from CF
        - ts_lin_sum, sum of the timestamps of lin_sum
        - ts_sqr_lin_sum, the sum of the squares of the timestamps of sqr_lin_sum
    - core-micro-clusters (C-MC)
      - core-micro-clusters, CMC
        - contain more than minPts samples
        - can be represented by an array of bundles representing dense regions
      - potential-core-micro-clusters
        - clusters formed from an intial run of dbscan
      - outlier-micro-clusters
        - contain less than minPts samples
        - have a timestamp associated with them so they fade as more samples are processed
        - each outlier cluster can be a bundle representing a single dense region
      - "The core-micro-cluster summary has been employed by DenStream [17], rDenStream [37], C-DenStream [46], HDDStream [40], MuDi-Stream [7], HDenStream [36], and PreDeConStream [28]"
    - temporal CF
    - prototype arrays
    - grids
    - coreset tree
  - clustering approaches
    - partitioning, you must know the number of clusters upfront
    - density-based, clusters of arbitrary shapes can be discovered and noise can be handled
    - grid-based, clustering on space partitions
    - model-based
  - see tables 1, 2, and 7
  - summary
    - damped and tilted windows are best
    - 2-phase algos are better than single-pass
    - density and grid-based are best
    - "CF-based summaries for stream clustering like microclusters and core-micro-clusters are the most efficient"

- Clustering Data Streams Based on Shared Density Between Micro-Clusters
  - DBSTREAM
  - shared density graph, "instead on relying on assumptions about the distribution of data points assigned to a micro-cluster (often a Gaussian distribution around a center), it estimates the density in the shared region between micro-clusters directly from the data"
  - background
    - streams
      - ordered data
      - potentially infinite
      - no random access to the data, one at a time
      - potential for concept drift
    - most reclustering (offline) steps merge micro-clusters based on their centers, weights (aka density aka count of samples), and sometimes dispersion
  - online
    - micro-cluster centroid (mean)
    - micro-cluster weight (count of samples which made up the mean)
    - dispersion around the centroid (variance)
    - some information about connectivity is required
    - leader clustering: depends on stream ordering. why then does dbstream use leader-based clustering?
    - competitive learning: all existing centroids are shifted towards the centroid of a newly created MC at the time the MC is created
      - does this meant that MC centers formed earlier in the stream will incorporate more noise points? why would we want to do that?
    - fig 2 shows how the shared density between micro-clusters is used to merge micro-clusters
    - a garbage collection step is used to purge old/thin MCs from memory
  - offline
    - micro-cluster distance (`sim(centroid1_bundle, centroid2_bundle)`)
      - prevent MCs from collapsing
    - micro-cluster connectivity (density of area between micro-clusters)
      - ensure highly connected MCs are reclustered into a single mass
    - based on density of MCs and density of areas between MCs (aka shared density aka intersection)
  - instead of using epsilon neighborhood for density (as in DBSCAN), DBSTREAM uses a density estimate (similar to DenStream)
  - instead of using reachability (as in DBSCAN), DBSTREAM uses connectivity of MC (similar to CHAMELEON)
  - DBSTREAM uses a global connectivity threshold to partition the connectivity graph and find connected components (unlike D-Stream's concept of 'grid attraction')
    - DBSTREAM uses ideas from competitive learning to permit MC drift

- A Framework for Clustering Evolving Data Streams
  - CluStream
  - uses kmeans
    - supports weighted clusters :)
    - uses a radius around a centroid
      - cannot arbitrary shaped clusters :(
    - cannot support arbirary number of clusters :(
    - cannot support outliers/noise :(

- Density-Based Clustering over an Evolving Data Stream with Noise
  - "DenStream, an effective and efficient method for clustering an evolving data stream"
  - density-based
  - clusters come and go over time
  - extensions and variants: SDStream, C-DenStream, rDenStream, HDDStream, 
  - micro-clusters which are reachable are merged during final clustering step
  - the weight of a MC can be calculated in a few ways:
    - the count of samples composing the MC
    - the average distance each sample composing the MC is from the centroid of the MC
    - the maximum distance a sample composing the MC is from the centroid of the MC
  - "influence areas" - seem to be when clusters overlap:
    - core overlaps with core
    - core overlaps with perimeter
    - perimeter overlaps with perimeter

- Density-Based Clustering for Real-Time Stream Data
  - D-Stream
  - grid-density based
    - "As a density-based approach, D-stream is flexible in detecting nonspherical clusters. However, the grid partitioning remains constant over time, although the underlying stream might evolve in different ways"
      - can detect arbitrary sized clusters :)
      - grid "layout" cannot be adjusted during runtime :(
    - most grids are sparse. perhaps this would be a good candidate for a style of sparse block code VSA?
    - i think the `codebooks` in thingy/scripts/ sound very similar to a "grid" 
    - it only considers density and not connectivity of adjacent grid cells. d-stream is measurably better than clustream but still kind of meh
  - online:
    - each grid is tracked as a tuple `(last_updated: count, last_removed_as_noise: count, grid_density: double, status: {SPORADIC, NORMAL})`
    - a global `sample_step_count` will need to be kept for comparing to `last_updated` and `last_removed_as_noise`
    - map incoming samples into a predertermined static grid
    - each grid cell has a last_updated time decay and a grid_density decay which allow for drift
    - outliers will appear as grid cells of low density and long last_updated times
  - offline:
    - `cluster()` can be called at any and all timesteps 
    - adjacent grid "cells" are merged based on their density
    - neighboring grids
    - grid groups
    - inside and outside grids
    - grid cluster


- Density-based clustering of data streams at multiple resolutions
  - MR-Stream
  - "we assume that the input stream data has n dimensions and forms an dimensional space S."
    - `n = 10_000`, `hyperspace: vector of hypervector;`
  - "partition the space S into well-defined partitions"
    - scripts in toys/ call this make_level_linear or smear
  - "We use a tree-like data structure to mirror the space partitioning so that each tree node corresponds to a cell"
    - a quadtree is used for "dynamically creating grids at multiple resolutions"
      - different grids(cubes) of a field(space) may require different sampling rates
    - could one use a bundle, or a bundle of bundles, instead of a tree-like structure?
  - "We assign a weight value to each record of the data stream. This weight value decreases over time if the record do not appear again frequent enough in the stream."
    - could one use a bundle to weight/fade/reinforce incoming data records?
  - adjacent dense grids are merged during final clustering step


- An EM-Based Algorithm for Clustering Data Streams in Sliding Windows
  - SWEM
  - sliding window
  - "We develop splitting and merging operations in order to discretely redistribute components in the entire data space"
    - this reminds me of what i was attempting to accomplish in `redistribute_time()`
      - if we moved a centroid we need to incorporate it into the timebundle and some forget the old centroid from the timebundle... how?
  - SWEM is measurably better than clustream but still kind of meh
    - it's also 15 years old


- Clustering Stream Data by Exploring the Evolution of Density Mountain
  - EDMStream
  - "experimental results on synthetic and real datasets show that, comparing to the state-of-the-art stream clustering algorithms, e.g., D-Stream, DenStream, DBSTREAM and MR-Stream, our algorithm is able to response to a cluster update much faster"
  - assumptions:
    - cluster centers are surrounded by neighbors of lower local density (dense centers surrounded by a less dense perimeter)
    - cluster centers are far from other points of higher density
  - the paper uses the term "cluster-cell" but it sounds similar to a micro-cluster
  - the paper uses a dependency-tree to represent density mountains
  - "it can dynamically adjust the cluster separation strategy". does this mean it uses a dynamic grid instead of a static one (like D-Stream)?
  - density peaks (DP)
    - local density
    - distance from more dense regions
    - fgure 3 reminds me of leader clustering
    - figure 4 compares DBSCAN to DPclustering
      - both use reachability but DBSCAN uses connectivity and DP uses traceability
        - traceability is non-symmetric
        - DBSCAN is an undirected graph
        - DP is a directed graph
      - when would the direction of the red arrow between A and B switch?
      - when a new cluster emerges, how would the start/stop points of the red arrows change?
      - do cluster density peaks (centroids) move around? by how much? how frequently do centroids move a meaningful amount?
  - since density mountain peaks are tracked using a tree (representing a grid), i wonder if an HDC-based tree structure could be used.


- A Clustering Algorithm for Evolving Data Streams Using Temporal Spatial Hyper Cube
  - BOCEDS TSHC
  - "Temporal Spatial Hyper Cube (TSHC) The hyper-cube is a quantization level that is supposed to map various values to one value in each coordinate to reduce the resolution of data storing and eliminate the effect of slight changes that do not influence the meaning of the data (type of filtering)"
  - grids are great but static grids are such a drag
    - "change the values of the quantization or the cube granularities every time new data arrived in the buffer to enable an adaptive cube"
      - so the quantization/leveling grid adjusts as new observations arrive
      - let's say we have a living thing, a single cell, under a microscope. as the cell divides and grows, we will need to adjust the magnification of the microscope to see the thing
        - when would we need to decrease the magnification of the microscope? as time progresses and densities fade?
  - figure 1. i like that they included a flow chart of how they conducted their research
  - i count 2 typos in figure 3. i'm glad to know i'm not the only one that makes typing mistakes.
  - parameters which users must specify
    - a decay factor (batch size)
    - minPts in a cluster
    - how far micro-clusters can be from each other


- FISHDBC: Flexible, Incremental, Scalable, Hierarchical Density-Based Clustering for Arbitrary Data and Distance
  - [FISHDBC](https://github.com/matteodellamico/flexible-clustering)
  - influenced by [HDBSCAN](https://github.com/scikit-learn-contrib/hdbscan) and [HNSW](https://github.com/nmslib/hnswlib)
    - "[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) is a key method for approximate nearest neighbor search in high-dimensional vector databases, for example in the context of embeddings"
      - HNSW sounds like a cleanup memory for hypervectors


- Online Clustering for Evolving Data Streams with Online Anomaly Detection
  - considers temporal proximity as well as spacial proximity of observations
  - data stream clustering approaches:
    - data summarization
      - create sumstats of observations with help of a sliding window
      - cluster labels are not available in real-time, but instead are done in an offline step
      - stream density clustering (DenStream, D-Stream) is located in this group because they use a 2-step online + offline strategy
    - real-time clustering (online). clusters are updated as data arrives
      - sequential k-means
        - competitive neural networks
      - this is where the paper contribution is located
    - time-series clustering. observations near in time are usually near in value
      - observations arrive in time order

- [river's stream clustering](https://github.com/online-ml/river/tree/main/river/cluster)
- [Du-Team's algorithms](https://github.com/Du-Team)
- MOA: Massive Online Analysis
  - [CapyMOA](https://github.com/adaptive-machine-learning/CapyMOA)


- HDC clustering papers
  - there are quite a few papers which make contributions to FPGA/hardware but not many which utilize HDC/VSA to improve the clustering algorithms
  - HDCluster: An Accurate Clustering Using Brain-Inspired High-Dimensional Computing
  - Robust Clustering using Hyperdimensional Computing
    - HDCluster's "performance is dependent on the selection of the initial hypervector". i found this to be true with my implementation of kbundles, too. the accuracy depended on the intial point selected for each centroid.
    - makes hdcluster more robust by initializing in a more better way
    - 3 algos which tweak k-means
    - 1 algo which is affinity propagation
      - the VSA's similarity metric is fed into the traditional AP algo
    - does not address streaming data
    - in some cases, projecting samples into HDC causes worse clustering results
    - i like that the authors tried different VSA (binary/non-binary) and different encoding methods (records and ngrams) in their comparison 
      - HDC is HIGHLY dependant on the encodings
  - *Trajectory clustering of road traffic in urban environments using incremental machine learning in combination with hyperdimensional computing*
    - "a novel unsupervised incremental learning approach for road traffic congestion detection and profiling, dynamically over time"
    - this seems pretty neat for real-time car/truck routing. i imagine it would work for packet routing too.
    - this is a very excellent paper
    - *DOES address streaming data*
      - incrementally outside of HDC/VSA using IKASL
      - "This example shows the capability of the proposed technique to incrementally learn from a trajectory dataset and automatically self-structure into more granular pathways at different time-widows based on the patterns in the data"
    - how
      - embed variable-length commuter trip trajectories with a VSA. they use ternary
        - put bluetooth scanners around town and count cars. tire TPMSs could probably be used to track unique vehicles.
        - each intersection is assigned an atomic hypervector
        - each trajectory subsequence is an ngram of intersections passed. `trigram = bind( perm(hv0, 0), perm(hv1, 1), perm(hv2, 2) )`
        - ngrams are bundled to form a "bag of ngrams" bundle `Tro = bundle( trigram0, trigram1, trigram2 ... )`
        - they DO NOT encode time into their hypervectors. instead they use "Incremental knowledge acquisition and self learning" to handle temporal intervals between embeddings
          - perhaps encoding tls record intervals in thingy/ isn't a great approach
          - perhaps instead, encode length ngrams only and timestamp their embedding before passing to a streaming/incremental clustering algo
      - transforms hypervectors into feature vectors for Incremental Knowledge Acquiring Self-Learning (IKASL)
      - permit shifts of popularity of ngrams over time to reflect changing traffic conditions
      - they even consider weekend and rushhour traffic patterns
  - HyperSpec: Ultrafast Mass Spectra Clustering in Hyperdimensional Space
    - 2 hyperspaces (bucketing/leveling):
      - peak m/z locality
      - peak m/z intensity
    - `bind(locality_level_hv, intensity_level_hv)`
    - they "pack" bits because systems' smallest data type is usually a byte
      - dimensions / 32 bits = number of `int`s needed to store 1 hypervector
      - i ran into this issue, too, while implementing a binary VSA in Zeek's scripting language. zeek's `bool` is the same number of bits as its `int`
    - clustering options are: dbscan and hierarchical
      - shows that other algos can operate on hypervectors, not just kmeans
      - does not address streaming data



Open Questions and Thoughts
===========================
- lots of papers use this term, "evolving data stream", to describe hwo their algorithm operates
  - types of cluster _evolutions_
    - emerge: birth
    - disappear: death
    - split: from one to many
    - merge: from many to one
    - adjust: drift/move/shift, change of outlier influence
- 2-step schemes:
  1. online summary statistics about the observed samples
  2. (offline) at any timestep clusters can be generated from the summary statistics in 1
- window types
  - sliding, one in one out. all have equal weights
  - landmark, all data between two landmarks is emptied when processed
  - dampened, unequally weighted samples. old data eventually decays away
- concept drift types
  - sudden
  - gradual
  - incremental
  - recurring
- anomaly detection in streams, very similar to timeseries
  - statistical
  - distance
  - density
  - clustering
- dynamic time warp
- discrete wavelet transform
- longest common subsequence

