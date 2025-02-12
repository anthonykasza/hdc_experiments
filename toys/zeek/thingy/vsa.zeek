module GLOBAL;
export {
  type Range: record {
    start: double;
    stop: double;
  };

  type hypervector: vector of int;
}


module VSA;
export {
  option dimensions: count = 1000 * 10;

  global dice_roll: function(): int;
  global hdv: function(n: count, all_zeros: bool): hypervector;
  global bundle: function(hdvs: vector of hypervector): hypervector;
  global bind: function(hdvs: vector of hypervector): hypervector;
  global sim: function(hdv1: hypervector, hdv2: hypervector): double;
  global additive_inverse: function(hdv: hypervector): hypervector;

  global make_levels_linear: function(num_of_levels: count, hdv1: hypervector, hdv2: hypervector): vector of hypervector;
  global discritize_linear: function(r: Range, bins: count): vector of Range;

  const resp_hv: hypervector = vector() &redef;
  const orig_hv: hypervector = vector() &redef;
  const record_len_hv: hypervector = vector() &redef;
}

function discritize_linear(r: Range, bins: count): vector of Range {
  local start = r$start;
  local stop = r$stop;
  local ranges: vector of Range = vector();
  local step: double = (stop - start) / bins;
  local bin_counter: count = 0;
  while (bin_counter < bins) {
    start = bin_counter * step;
    stop = start + step;
    ranges += Range($start=start, $stop=stop);
    bin_counter += 1;
  }
  return ranges;
}

function dice_roll(): int {
  local finite_group_size: count = 5;
  switch rand(finite_group_size) {
    case 0:
      return 2;
    case 1:
      return 1;
    case 2:
      return 0;
    case 3:
      return -1;
    case 4:
      return -2;
  }
}

function hdv(n: count &default=VSA::dimensions, all_zeros: bool &default=F): hypervector {
  local v: vector of int = vector();
  local j = 0;
  while (n > 0) {
    if (all_zeros) {
      v[j] = 0;
    } else {
      v[j] = dice_roll();
    }
    n -= 1;
    j += 1;
  }
  return v;
}
redef orig_hv = hdv();
redef resp_hv = hdv();
redef record_len_hv = hdv();


# linearly discritize_linear the space between two hyper vectors
# num_of_levels = number of levels between hdv1 and hdv2
function make_levels_linear(
  num_of_levels: count,
  hdv1: hypervector &default=hdv(),
  hdv2: hypervector &default=hdv()
): vector of hypervector {
  if (num_of_levels < 1 || num_of_levels > VSA::dimensions) {
    return vector(hdv1, hdv2);
  }

  local changes_per_iteration: count = VSA::dimensions / num_of_levels;
  local levels: vector of hypervector = vector();
  levels += hdv1;
  local level_idx = 1;
  local unchanged_idx: set[count] = set();
  for (idx in hdv1) {
    add unchanged_idx[idx];
  }

  while (level_idx <= num_of_levels) {
    # deep copy the previous level into the next level
    local next_level: hypervector = vector();
    local prev_level = levels[level_idx-1];
    for (deepcopy_idx in prev_level) {
      next_level[deepcopy_idx] = prev_level[deepcopy_idx];
    }

    # while there exist unaltered elements
    local change_counter = 0;
    while (change_counter <= changes_per_iteration) {
      if (|unchanged_idx| > 0) {
        # pick one randomly and mark it as altered
        local random_idx = rand(|unchanged_idx|);
        delete unchanged_idx[random_idx];
        # then change next_level to be more like hdv2
        next_level[random_idx] = hdv2[random_idx];
      } else {
        # if we've altered all the elements then,
        #  levels[0] = hdv1 and levels[-1] = hdv2
        return levels;
      }
      change_counter += 1;
    }
    levels += next_level;
    level_idx += 1;
  }

  levels += hdv2;
  return levels;
}

function additive_inverse(hdv: hypervector): hypervector {
  local v: hypervector = vector();
  for (idx in hdv) {
    # values from dice_roll are symmetrically wrapped around zero
    v[idx] = hdv[idx] * -1;
  }
  return v;
}

function sim(hdv1: hypervector, hdv2: hypervector): double {
  local dot: double = 0.0;
  local mag1: double = 0.0;
  local mag2: double = 0.0;
  local idx: count;

  for (idx in hdv1) {
    dot += hdv1[idx] * hdv2[idx];
    mag1 += hdv1[idx] * hdv1[idx];
    mag2 += hdv2[idx] * hdv2[idx];
  }

  local m1 = sqrt(mag1);
  local m2 = sqrt(mag2);
  if (m1 == 0 || m2 == 0) { return 0.0; }
  return dot / (m1 * m2);
}

function bundle(hdvs: vector of hypervector): hypervector {
  if (|hdvs| == 0) { return hdv(VSA::dimensions, T); }

  local v: hypervector = vector();
  local tmp_hv: hypervector;

  for (hv_idx in hdvs) {
    tmp_hv = hdvs[hv_idx];

    # make v all zeros
    if (|v| == 0) {
      for (element_idx in tmp_hv) {
        v += 0;
      }
    }

    for (element_idx in tmp_hv) {
      v[element_idx] = v[element_idx] + tmp_hv[element_idx];
    }
  }

  return v;
}

function bind(hdvs: vector of hypervector): hypervector {
  local v: hypervector = vector();
  local tmp_hv: hypervector;

  for (hv_idx in hdvs) {
    tmp_hv = hdvs[hv_idx];

    # make v all 1s
    if (|v| == 0) {
      for (element_idx in tmp_hv) {
        v += 1;
      }
    }

    for (element_idx in tmp_hv) {
      v[element_idx] = v[element_idx] * tmp_hv[element_idx];
    }
  }

  return v;
}
