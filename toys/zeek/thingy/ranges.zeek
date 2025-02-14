
export {
  global length_codebook: table[Range] of hypervector = table() &ordered;
  global interval_codebook: table[Range] of hypervector = table() &ordered;
}

function generate_codebook(space: vector of double, steps: vector of count): table[Range] of hypervector {
  local codebook: table[Range] of hypervector = table() &ordered;
  local start: double;
  local stop: double;
  local step: count;

  # subtract 2 to account for the beginning and ending hvs
  local level_hvs: vector of hypervector = VSA::make_levels_linear(|space|-2);

  for (idx in steps) {
    step = steps[idx];
    start = space[idx];
    stop = space[idx+1];

    local length_range_hvs = VSA::make_levels_linear(step, level_hvs[idx], level_hvs[idx+1]);
    local length_range_values = VSA::discretize_linear([$start=start, $stop=stop], step);
    for (j_idx in length_range_values) {
      local r: Range = length_range_values[j_idx];
      local hv: hypervector = length_range_hvs[j_idx];
      codebook[[$start=start+r$start, $stop=start+r$stop]] = hv;
    }
  }
  return codebook;
}


event zeek_init() {
  local len_space: vector of double = vector(0.0, 122, 503, 1031, 3060, 7111, 15215, 23299, 35536);
  local len_steps: vector of count = vector(4,6,4,4,4,4,2,1);
  ::length_codebook = generate_codebook(len_space, len_steps);

  local ival_space: vector of double = vector(0.0, 0.03, 0.1, 0.55, 1.2, 2.12, 5.3, 13.1, 21.8, 53.12, 283.4, 2888.0);
  local ival_steps: vector of count = vector(2,2,2,2,2,2,2,2,2,2,2);
  ::interval_codebook = generate_codebook(ival_space, ival_steps);
}

