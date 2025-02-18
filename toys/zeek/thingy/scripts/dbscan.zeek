@load ./vsa

export {
  type DBScanInput: record {
    data: vector of hypervector;
    min_sim: double;
    min_size: count;
    sim_func: function(hv1: hypervector, hv2: hypervector): double &default=VSA::sim;
  };

  type DBscanOutput: record {
    noise: set[count];
    clusters: set[set[count]];
  };

  global dbscan: function(input: DBScanInput): DBscanOutput;
}

function is_in_cluster(idx: count, clusters: set[set[count]]): bool {
  # TODO - instead of doing an exhuastive search,
  #        store clusters as bundled hvs and then
  #        use VSA::sim() to check if the hv is in any of the 
  #        centroid bundles
  for (cluster in clusters) {
    if (idx in cluster) { return T; }
  }
  return F;
}

function query_region(idx: count, input: DBScanInput): set[count] {
  local region: set[count] = set();
  for (n_idx in input$data) {
    if (VSA::sim(input$data[idx], input$data[n_idx]) > input$min_sim ) {
      add region[n_idx];
    }
  }
  return region;
}

function expand_cluster(
  idx: count,
  neighbors: set[count],
  cluster: set[count],
  input: DBScanInput,
  visited: set[count],
  clusters: set[set[count]]
) {
  add visited[idx];
  add cluster[idx];

  local copy_of_neighbors = copy(neighbors);

  for (n_idx in copy_of_neighbors) {
    if (n_idx !in visited) {
      add visited[n_idx];
      local nn = query_region(n_idx, input);
      if (|nn| > input$min_size) {
        # modify the original neighbors, which is why we needed to copy()
        neighbors += nn;
      }
    }
    if (!is_in_cluster(n_idx, clusters)) {
      add cluster[n_idx];
    }
  }
}

function dbscan(input: DBScanInput): DBscanOutput {
  local noise: set[count] = set();
  local clusters: set[set[count]] = set();
  local visited: set[count] = set();

  for (idx in input$data) {
    if (idx !in visited) {
      add visited[idx];
      local neighbors = query_region(idx, input);
      if (|neighbors| >= input$min_size) {
        local new_cluster: set[count] = set();
        expand_cluster(idx, neighbors, new_cluster, input, visited, clusters);
        add clusters[new_cluster];
      } else {
        add noise[idx];
      }
    }
  }

  return [$noise=noise, $clusters=clusters];
}
