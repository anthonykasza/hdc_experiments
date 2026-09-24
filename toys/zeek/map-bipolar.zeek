
# Ternary Multiply-Add-Permute

module VSA::MAP::B;

export {
  global hdv: function(n: count): vector of int;
  global bind: function(hdv1: vector of int, hdv2: vector of int): vector of int;
  global unbind: function(hdv1: vector of int, hdv2: vector of int): vector of int;
  global bundle: function(hdv1: vector of int, hdv2: vector of int): vector of int;
  global clip: function(hdv: vector of int): vector of int;
  global cossim: function(hdv1: vector of int, hdv2: vector of int): double;
}

# This default value has to be big, literature suggests at least 10k
function hdv(n: count &default=100000): vector of int {
  local v: vector of int = vector();
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

function clip(hdv: vector of int): vector of int {
  local idx: count;
  local v: vector of int = vector();
  for (idx in hdv) {
    if (hdv[idx] > 0) {
      v[idx] = 1;
    } else if (hdv[idx] < 0) {
      v[idx] = -1;
    } else {
      v[idx] = 0;
    }
  }
  return v;
}

function bundle(hdv1: vector of int, hdv2: vector of int): vector of int {
  local idx: count;
  local v: vector of int = vector();
  for (idx in hdv1) {
    v[idx] = hdv1[idx] + hdv2[idx];
  }
  return clip(v);
}

function bind(hdv1: vector of int, hdv2: vector of int): vector of int {
  local idx: count;
  local v: vector of int = vector();
  for (idx in hdv1) {
    v[idx] = hdv1[idx] * hdv2[idx];
  }
  return v;
}

function unbind(hdv1: vector of int, hdv2: vector of int): vector of int {
  return bind(hdv1, hdv2);
}

function cossim(hdv1: vector of int, hdv2: vector of int): double {
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
