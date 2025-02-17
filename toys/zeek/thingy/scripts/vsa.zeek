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
  global sim: function(hv1: hypervector, hv2: hypervector): double;
  global perm: function(hv: hypervector, positions: int): hypervector;
  global ngram: function(v: vector of hypervector, n: count): vector of vector of hypervector;
  global symbol_lookup: function(value: double, codebook: table[Range] of hypervector): hypervector;
  global make_levels_linear: function(num_of_levels: count, hv1: hypervector, hv2: hypervector): vector of hypervector;
  global discretize_linear: function(r: Range, bins: count): vector of Range;
}

function ngram(v: vector of hypervector, n: count): vector of vector of hypervector {
  if (n > |v|) { return vector(v); }

  local result: vector of vector of hypervector = vector();
  local tmp: vector of hypervector;
  local j: count;

  for (idx in v) {
    j = 0;
    tmp = vector();
    while (j < n) {
      if (idx + j >= |v|) { return result; }
      tmp += v[idx+j];
      j += 1;
    }
    result += tmp;
  }

  return result;
}


function discretize_linear(r: Range, bins: count): vector of Range {
  if (bins == 0) { return vector(); }

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

function make_levels_linear(
  num_of_levels: count,
  hv1: hypervector &default=hdv(),
  hv2: hypervector &default=hdv()
): vector of hypervector {
  if (num_of_levels < 1 || num_of_levels > VSA::dimensions) {
    return vector(hv1, hv2);
  }

  local levels: vector of hypervector = vector();
  levels[0] = copy(hv1);

  local disc_ranges = discretize_linear([$start=0.0, $stop=|hv1|+0.0], num_of_levels+1);
  for (range_idx in disc_ranges) {
    local r = disc_ranges[range_idx];
    local start = double_to_count(r$start);
    local stop = double_to_count(r$stop);
  
    # copy the previous level into this level
    levels[|levels|] = copy(levels[|levels|-1]);

    # then copy slices of hv2[start:stop] into this level[start:stop]
    levels[|levels|-1][start:stop] = hv2[start:stop];
  }

  return levels;
}

function sim(hv1: hypervector, hv2: hypervector): double {
  local dot: double = 0.0;
  local mag1: double = 0.0;
  local mag2: double = 0.0;
  local idx: count;

  for (idx in hv1) {
    dot += hv1[idx] * hv2[idx];
    mag1 += hv1[idx] * hv1[idx];
    mag2 += hv2[idx] * hv2[idx];
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

function perm(hv: hypervector, positions: int &default=1): hypervector {
  if (positions == 0) { return hv; }

  local n = |hv|;
  local v: hypervector = hdv(n, T);
  positions = positions % n;

  local element_idx: count;
  local v_idx: count;

  # towards the tail
  if (positions > 0) {
    # forwards iterate the elements
    for (element_idx in hv) {
      v_idx = int_to_count((element_idx + positions) % n);
      v[v_idx] = hv[element_idx];
    }

  # towards the head
  } else {
    # backwards iterate the elements
    element_idx = n;
    while (element_idx > 0) {
      element_idx -= 1;
      local i: int = (element_idx + positions) % n;
      if (i < 0) { i = n + i; } 
      v_idx = int_to_count(i);
      v[v_idx] = hv[element_idx];
    }
  }

  return v;
}

function symbol_lookup(value: double, codebook: table[Range] of hypervector): hypervector {
  local start: double;
  local stop: double;

  for (r, hv in codebook) {
    start = r$start;
    stop = r$stop;
    if (value >= start && value <= stop) {
      return hv;
    }
  }

  # if value is not in the codebook, return an all zeros hv
  return VSA::hdv(VSA::dimensions, T);
}
