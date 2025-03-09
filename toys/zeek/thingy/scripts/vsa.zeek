module GLOBAL;
export {
  type hypervector: vector of int;
}


module VSA;
export {
  # 65536 / 4 ish
  option dimensions: count = 17000;

  global dice_roll: function(): int;
  global hdv: function(n: count, all_zeros: bool): hypervector;
  global hdv_all1: function(n: count): hypervector;
  global bundle: function(hdvs: vector of hypervector): hypervector;
  global bind: function(hdvs: vector of hypervector): hypervector;
  global sim: function(hv1: hypervector, hv2: hypervector): double;
  global perm: function(hv: hypervector, positions: int): hypervector;
  global make_groups: function(v: vector of hypervector, n: count): vector of vector of hypervector;
  global make_levels: function(num_of_levels: count, hv1: hypervector, hv2: hypervector): vector of hypervector;
}

function make_groups(v: vector of hypervector, n: count): vector of vector of hypervector {
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

function make_levels(num_of_levels: count, hv1: hypervector &default=VSA::hdv(), hv2: hypervector &default=VSA::hdv()): vector of hypervector {
  if (num_of_levels < 2 || num_of_levels > VSA::dimensions) {
    return vector(hv1, hv2);
  }

  local levels: vector of hypervector = vector();
  levels[0] = hv1;
  local level_counter: count = 1;

  local start: count = 0;
  local stop: count = |hv1|;
  local step: count = double_to_count((stop - start) / num_of_levels);
  # TODO - support a way of adjusting the step. Instead of a single
  #        static step per iteration of the following loop, a dynamic
  #        step would allow for arbitrary correlation 'resolutions' e.g.
  #        exponential, fractal, mixed-linear

  while (level_counter <= num_of_levels) {
    # copy the previous level into this level
    levels[|levels|] = copy(levels[|levels|-1]);

    # copy slices of hv2 into this level
    levels[|levels|-1][start:start+step] = hv2[start:start+step];

    start = start + step;
    level_counter = level_counter + 1;
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
