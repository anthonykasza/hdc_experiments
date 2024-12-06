
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
  global hdv: function(n: count): hypervector;
  global hdv_all1: function(n: count): hypervector;
  global hdv_all0: function(n: count): hypervector;
  global bundle: function(hdvs: vector of hypervector): hypervector;
  global bind: function(hdvs: vector of hypervector): hypervector;
  global discretize_linear: function(r: Range, bins: count): vector of Range;
  global sim: function(hv1: hypervector, hv2: hypervector): double;
  global smear: function(num_of_levels: count, hv1: hypervector, hv2: hypervector): vector of hypervector;
}


function dice_roll(): int {
  local finite_group_size: count = 7;
  switch rand(finite_group_size) {
    case 0:
      return 3; #is 3 a good approximation for pi?
    case 1:
      return 2;
    case 2:
      return 1;
    case 3:
      return 0;
    case 4:
      return -1;
    case 5:
      return -2;
    case 6:
      return -3;
  }
}

function hdv_all1(n: count &default=VSA::dimensions): hypervector {
  local v: vector of int = vector();
  local j = 0;
  while (n > 0) {
    v[j] = 1; # all 1s
    n -= 1;
    j += 1;
  }
  return v;
}

function hdv_all0(n: count &default=VSA::dimensions): hypervector {
  local v: vector of int = vector();
  local j = 0;
  while (n > 0) {
    v[j] = 0; # all 0s
    n -= 1;
    j += 1;
  }
  return v;
}

function hdv(n: count &default=VSA::dimensions): hypervector {
  local v: vector of int = vector();
  local j = 0;
  while (n > 0) {
    v[j] = dice_roll(); # random
    n -= 1;
    j += 1;
  }
  return v;
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

function smear(
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
  return |dot / (m1 * m2)|;
}

function bundle(hdvs: vector of hypervector): hypervector {
  local v: hypervector = hdv_all0();
  if (|hdvs| == 0) { return v; }
  local tmp_hv: hypervector;

  for (hv_idx in hdvs) {
    tmp_hv = hdvs[hv_idx];

    for (element_idx in tmp_hv) {
      v[element_idx] = v[element_idx] + tmp_hv[element_idx];
    }
  }

  return v;
}

function bind(hdvs: vector of hypervector): hypervector {
  local v: hypervector = hdv_all1();
  if (|hdvs| == 0) { return v; }
  local tmp_hv: hypervector;

  for (hv_idx in hdvs) {
    tmp_hv = hdvs[hv_idx];

    for (element_idx in tmp_hv) {
      v[element_idx] = v[element_idx] * tmp_hv[element_idx];
    }
  }

  return v;
}
