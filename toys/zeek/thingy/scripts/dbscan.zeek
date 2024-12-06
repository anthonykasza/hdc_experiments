@load ./vsa

export {
  type DBScanInput: record {
    data: vector of hypervector;
    min_sim: double;
    min_size: count;
    sim_func: function(hv1: hypervector, hv2: hypervector): double &default=VSA::sim;
  };

  type DBscanResult: record {
    noise: set[count];
    clusters: set[set[count]];
  };

  global dbscan: function(input: DBScanInput): DBscanResult;
}

# TODO - convert dbscan() from single-step offline to 2-step online
#  incremental density based clustering
#  - https://github.com/online-ml/river/tree/main/river/cluster
#  - https://github.com/DataOmbudsman/incdbscan/blob/master/images/illustration_circles.gif
function dbscan(input: DBScanInput): DBscanResult {
  local noise: set[count] = set();
  local clusters: set[set[count]] = set();
  local visited: set[count] = set();

  local is_in_cluster = function [clusters] (idx: count): bool {
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

  local expand_cluster = function [visited, input, is_in_cluster, query_region] (
    idx: count,
    neighbors: set[count],
    cluster: set[count]
  ) {
    add visited[idx];
    add cluster[idx];

    local copy_of_neighbors = copy(neighbors);

    for (n_idx in copy_of_neighbors) {
      if (n_idx !in visited) {
        add visited[n_idx];
        local nn = query_region(n_idx);
        if (|nn| > input$min_size) {
          # modify the original neighbors, which is why we needed to copy()
          neighbors += nn;
        }
      }
      if (!is_in_cluster(n_idx)) {
        add cluster[n_idx];
      }
    }
  };

  # do the dang thang
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
