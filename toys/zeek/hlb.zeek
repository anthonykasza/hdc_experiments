# Based on Hadamard-derived Linear Binding


module VSA::HLB;

export {
  global new_hv: function(n: count): vector of double;
  global bind: function(hv1: vector of double, hv2: vector of double): vector of double;
  global unbind: function(hv1: vector of double, hv2: vector of double): vector of double;
  global bundle: function(hv1: vector of double, hv2: vector of double): vector of double;
  global inverse: function(hv: vector of double): vector of double;
  global cossim: function(hv1: vector of double, hv2: vector of double): double;
}

function generate_element(center: int, variance: double): double {
  local max_resolution: count = 1000000;
  local uniform: double = rand(max_resolution) / max_resolution;
  local stretch_shift: double = (uniform * 2) - 1;
  return center + (stretch_shift * variance);
}

function new_hv(n: count &default=10): vector of double {
  local v: vector of double = vector();
  local variance: double = 1 / sqrt(n);
  local j = 0;
  while (j < n) {
    local r: count = rand(2);
    if (r == 0) {
      v[j] = generate_element(1, variance);
    } else {
      v[j] = generate_element(-1, variance);
    }
    j += 1;
  }
  return v;
}

function bundle(hv1: vector of double, hv2: vector of double): vector of double {
  local idx: count;
  local v: vector of double = vector();
  for (idx in hv1) {
    v[idx] = hv1[idx] + hv2[idx];
  }
  return v;
}

function bind(hv1: vector of double, hv2: vector of double): vector of double {
  local idx: count;
  local v: vector of double = vector();
  for (idx in hv1) {
    v[idx] = hv1[idx] * hv2[idx];
  }
  return v;
}

function inverse(hv: vector of double): vector of double {
  local idx: count;
  local v: vector of double = vector();
  for (idx in hv) {
    v[idx] = 1 / hv[idx];
  }
  return hv;
}

function unbind(hv1: vector of double, hv2: vector of double): vector of double {
  return bind(hv1, inverse(hv2));
}

function cossim(hv1: vector of double, hv2: vector of double): double {
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


event zeek_init() {
  local dims: count = 10000;

  # keys of the maps
  local country = new_hv(dims);
  local capital = new_hv(dims);
  local currency = new_hv(dims);

  # country values
  local usa = new_hv(dims);
  local mex = new_hv(dims);
  local hun = new_hv(dims);

  # capital values
  local wdc = new_hv(dims);
  local mxc = new_hv(dims);
  local bud = new_hv(dims);

  # currency values
  local usd = new_hv(dims);
  local mxn = new_hv(dims);
  local huf = new_hv(dims);

  # a map of the keys and United States's values
  local tmp1 = bind(country, usa);
  local tmp2 = bind(capital, wdc);
  local tmp3 = bind(currency, usd);
  local tmp4 = bundle(tmp1, tmp2);
  local usa_map = bundle(tmp3, tmp4);
  print "united states map vector", usa_map[0:3], "...", usa_map[-3:];

  # a map of the keys and Mexico's values
  tmp1 = bind(country, mex);
  tmp2 = bind(capital, mxc);
  tmp3 = bind(currency, mxn);
  tmp4 = bundle(tmp1, tmp2);
  local mex_map = bundle(tmp3, tmp4);
  print "mexico map vector", mex_map[0:3], "...", mex_map[-3:];

  # a map of the keys and Hungary's values
  tmp1 = bind(country, hun);
  tmp2 = bind(capital, bud);
  tmp3 = bind(currency, huf);
  tmp4 = bundle(tmp1, tmp2);
  local hun_map = bundle(tmp3, tmp4);

  print "hungary map vector", hun_map[0:3], "...", hun_map[-3:];
  print "";

  # this analogy represents a table of all countries and their mapped values
  local analogy = bind(hun_map, bind(usa_map, mex_map));

  # we can query the analogy by removing things from it
  local query = unbind(unbind(analogy, hun_map), usd);
  print "what is the dollar of mexico?";
  print "how similar is the query to USD?", cossim(query, usd);
  print "how similar is the query to MXN?", cossim(query, mxn);
  print "how similar is the query to HUF?", cossim(query, huf);
  print "";
  print "";

  # we can query the analogy is different ways
  query = unbind(unbind(analogy, usa_map), mxc);
  print "what is the mexico city of hungary?";
  print "how similar is the query to Washington DC?", cossim(query, wdc);
  print "how similar is the query to Mexico City?  ", cossim(query, mxc);
  print "how similar is the query to Budapest?     ", cossim(query, bud);
  print "";
  # none of these vectors are similar to bud because they currecies, not capitals
  print "how similar is the query to USD?", cossim(query, usd);
  print "how similar is the query to MXN?", cossim(query, mxn);
  print "how similar is the query to HUF?", cossim(query, huf);
  print "";
  # none of these vectors are similar to bud because they countries, not capitals
  print "how similar is the query to United States?", cossim(query, usa);
  print "how similar is the query to Mexico?       ", cossim(query, mex);
  print "how similar is the query to Hungary?      ", cossim(query, hun);
}
