# In a cluster setting, all nodes need to be working
#  with the same sets of symbols. 

export {
  # endpoint symbols
  const client_hv = VSA::hdv();
  const server_hv = VSA::hdv();

  # bytes symbols
  global length_codebook: table[Range] of hypervector = table() &ordered;

  # time symbols
  global interval_codebook: table[Range] of hypervector = table() &ordered;
}

# TODO - fix this. the ranges of codebooks are not properly correlated for some reason
#        see the codebook btest for examples of what's happening
function generate_codebook(space: vector of double, steps: vector of count): table[Range] of hypervector {
  # 1. make the vector of HVs
  local levels: count = 0;
  for (idx in steps) { levels += steps[idx]; }
  # subtract 2 to account for the beginning and ending hvs
  local level_hvs: vector of hypervector = VSA::make_levels_linear(levels-2);

  # 2. make the vector of Ranges
  local start: double;
  local stop: double;
  local step: count;
  local value_ranges: vector of Range = vector();
  for (idx in steps) {
    step = steps[idx];
    start = space[idx];
    stop = space[idx+1];

    # this is value_ranges.extend() and NOT value_ranges.append()
    value_ranges += VSA::discretize_linear([$start=start, $stop=stop], step);
  }

  # 3. make and return the codebook
  local codebook: table[Range] of hypervector = table() &ordered;
  for (idx in value_ranges) {
    local r: Range = value_ranges[idx];
    local hv: hypervector = level_hvs[idx];
    codebook[r] = hv;
  }
  return codebook;
}


event zeek_init() {
  # *_space needs to be 1 element longer than *_steps

  local len_space: vector of double = vector(0.0, 122, 503, 1031, 3060, 7111, 15215, 23299, 35536);
  local len_steps: vector of count = vector(4,6,4,4,4,4,2,1);
  ::length_codebook = generate_codebook(len_space, len_steps);

  local ival_space: vector of double = vector(0.0, 0.03, 0.1, 0.55, 1.2, 2.12, 5.3, 13.1, 21.8, 53.12, 283.4, 2888.0);
  local ival_steps: vector of count = vector(2,2,2,2,2,2,2,2,2,2,2);
  ::interval_codebook = generate_codebook(ival_space, ival_steps);
}
