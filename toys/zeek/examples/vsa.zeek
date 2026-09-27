# Bipolar MAP

module VSA;

export {
  type Hvec: vector of int;

  global new_hv: function(n: count): Hvec;
  global bind: function(hv1: Hvec, hv2: Hvec): Hvec;
  global unbind: function(hv1: Hvec, hv2: Hvec): Hvec;
  global bundle: function(hdvs: vector of Hvec): Hvec;
  global clip: function(hv: Hvec): Hvec;
  global permute: function(hv: Hvec, shift: count): Hvec;
  global cossim: function(hv1: Hvec, hv2: Hvec): double;

  global additive_identity: function(n: count): Hvec;
}

function additive_identity(n: count): Hvec {
  local v: Hvec = vector();
  local idx = 0;
  while (idx < n) {
    v[idx] = 0;   # all zeros
    idx += 1;
  }
  return v;
}

# TODO
function permute(hv: Hvec, shift: count): Hvec { return hv; }

function new_hv(n: count &default=10): Hvec {
  local v: Hvec = vector();
  local j = 0;
  while (n > 0) {
    local r: count = rand(2);
    if (r == 0) {
      v[j] = 1;
    } else {
      v[j] = -1;
    }
    n -= 1;
    j += 1;
  }
  return v;
}

function clip(hv: Hvec): Hvec {
  local idx: count;
  local v: Hvec = vector();
  for (idx in hv) {
    if (hv[idx] > 0) {
      v[idx] = 1;
    } else if (hv[idx] < 0) {
      v[idx] = -1;
    } else {
      v[idx] = 0;
    }
  }
  return v;
}

function bundle(hdvs: vector of Hvec): Hvec {
  local idx: count;
  local v: Hvec = vector();

  for (element_idx in hdvs[0]) {
    # initialize to additive identity
    v[element_idx] = 0;
    for (hv_idx in hdvs) {
      v[element_idx] += hdvs[hv_idx][element_idx];
    }
  }
  return clip(v);
}

function bundle_no_clip(hdvs: vector of Hvec): Hvec {
  local idx: count;
  local v: Hvec = vector();

  for (element_idx in hdvs[0]) {
    # initialize to additive identity
    v[element_idx] = 0;
    for (hv_idx in hdvs) {
      v[element_idx] += hdvs[hv_idx][element_idx];
    }
  }
  return v;
}

function bind(hv1: Hvec, hv2: Hvec): Hvec {
  local idx: count;
  local v: Hvec = vector();
  for (idx in hv1) {
    v[idx] = hv1[idx] * hv2[idx];
  }
  return v;
}

function unbind(hv1: Hvec, hv2: Hvec): Hvec {
  return bind(hv1, hv2);
}

function cossim(hv1: Hvec, hv2: Hvec): double {
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
