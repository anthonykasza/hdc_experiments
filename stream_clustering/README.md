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
    - TODO - read more about MR-Stream, DSCLU, and OPCluStream, 

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
  - uses weighted kmeans, so it cannot support arbirary number of clusters :(
  - often forms spherical cluster, not arbitrary shaped ones :(

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
  - grid based
  - "As a density-based approach, D-stream is flexible in detect- ing nonspherical clusters. However, the grid partitioning remains constant over time, although the underlying stream might evolve in different ways"
  - adjacent dense grids are merged during final clustering step


- Density-based clustering of data streams at multiple resolutions
  - MR-Stream
  - adjacent dense grids are merged during final clustering step
  - a quadtree is used for "dynamically creating grids at multiple resolutions"
    - different grids(cubes) of a field(space) may require different sampling rates



- An EM-Based Algorithm for Clustering Data Streams in Sliding Windows
  - SWEM

- Clustering Stream Data by Exploring the Evolution of Density Mountain
  - EDMStream

- A Clustering Algorithm for Evolving Data Streams Using Temporal Spatial Hyper Cube
  - BOCEDS TSHC

- FISHDBC: Flexible, Incremental, Scalable, Hierarchical Density-Based Clustering for Arbitrary Data and Distance
  - FISHDBC
  - https://github.com/matteodellamico/flexible-clustering/blob/master/flexible_clustering/fishdbc.py

- [rivers stream clustering ](https://github.com/online-ml/river/tree/main/river/cluster)

- MOA: Massive Online Analysis
  - [CapyMOA](https://github.com/adaptive-machine-learning/CapyMOA)



- HDC clustering papers
  - HDCluster: An Accurate Clustering Using Brain-Inspired High-Dimensional Computing
  - TODO 



Open Questions
==============
- what is soft/fuzzy clustering? can it be incremental? since it operates on probabilities, can we emulate it with HDC?
- can we utilize a minimum spanning tree for merging microclusters?
- since we are using a VSA, are there any codebook searching tricks we can utilize to improve performance?
- for what reasons is R*-tree a good way to implement DBSCAN?
  - how can R*-tree strcutures take advantage of HDC properties?


