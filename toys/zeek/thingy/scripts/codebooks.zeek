# In a cluster setting, all nodes need to be working with the same sets of symbols. 

export {
  # endpoint symbols
  const client_hv = VSA::hdv();
  const server_hv = VSA::hdv();

  # NOTE: 1 byte granularity up to 16k
  option length_steps: vector of count = {
    16, 16, 16, 16, 64, 64, 64, 100, 100, 100,
    1000, 1000, 2000, 3000, 3000, 4000,
    500, 500, 500, 500
  };

  # NOTE: 1/10th second granularity up to 300 seconds
  option interval_steps: vector of count = {
    1, 1, 1, 1, 1,
    2, 2, 2, 4,
    5, 5, 5, 5, 5, 5,
    10, 10, 10, 10, 10,

    10, 20, 30,
    75, 100, 100, 150,
    300, 300, 300,

    300, 400, 500
  };

  # length and interval symbols
  global length_codebook: vector of hypervector = VSA::make_levels(length_steps);
  global interval_codebook: vector of hypervector = VSA::make_levels(interval_steps);

  global length_lookup: function(length: count): hypervector;
  global interval_lookup: function(ival: double): hypervector;
}

function length_lookup(length: count): hypervector {
  local start: count = 0;
  local stop: count;

  for (idx in ::length_steps) {
    local step = ::length_steps[idx];
    stop = start + step;
    if (length > start && length <= stop) {
      return ::length_codebook[idx];
    }

    start = start + step;
  }

  # if we didn't find it, return the most distant
  return ::length_codebook[|::length_codebook|-1];
}

function interval_lookup(ival: double): hypervector {
  # NOTE: 1/10th second granularity
  ival = ival * 10;

  local start: double = 0.0;
  local stop: double;

  for (idx in ::interval_steps) {
    local step = ::interval_steps[idx];
    stop = start + step;
    if (ival > start && ival <= stop) {
      return ::interval_codebook[idx];
    }

    start = start + step;
  }

  # if we didn't find it, return the most distant
  return ::interval_codebook[|::interval_codebook|-1];
}

