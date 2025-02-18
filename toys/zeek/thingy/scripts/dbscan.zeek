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

function dbscan(input: DBScanInput): DBscanOutput {
  local noise: set[count] = set();
  local clusters: set[set[count]] = set();

  local is_in_cluster = function [clusters] (idx: count): bool {
    # TODO - instead of doing an exhuastive search,
    #        store clusters as bundled hvs and then
    #        use VSA::sim() to check if the hv is in any of the 
    #        centroid bundles
    for (cluster in clusters) {
      if (idx in cluster) { return T; }
    }
    return F;
  };

  local query_region = function [input] (idx: count): set[count] {
    local region: set[count] = set();
    for (n_idx in input$data) {
      if (VSA::sim(input$data[idx], input$data[n_idx]) > input$min_sim ) {
        add region[n_idx];
      }
    }
    return region;
  };

  local visited: set[count] = set();
  local expand_cluster = function [is_in_cluster, query_region, input, visited] (idx: count, neighbors: set[count], cluster: set[count]) {
    add visited[idx];
    add cluster[idx];

    for (n_idx in neighbors) {
      if (n_idx !in visited) {
        add visited[n_idx];
        local nn = query_region(n_idx);
        if (|nn| > input$min_size) {
          neighbors += nn;
        }
      }

      if (!is_in_cluster(n_idx)) {
        add cluster[n_idx];
      }
    }
  };

  for (idx in input$data) {
    if (idx !in visited) {
      add visited[idx];
      local neighbors = query_region(idx);
      if (|neighbors| >= input$min_size) {
        local new_cluster: set[count] = set();
        expand_cluster(idx, neighbors, new_cluster);
        add clusters[new_cluster];
      } else {
        add noise[idx];
      }
    }
  }

  return [$noise=noise, $clusters=clusters];
}
