
module VSA;

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


event zeek_init() {
  # keys of the maps
  local country = hdv();
  local capital = hdv();
  local currency = hdv();

  # country values
  local usa = hdv();
  local mex = hdv();
  local hun = hdv();

  # capital values
  local wdc = hdv();
  local mxc = hdv();
  local bud = hdv();

  # currency values
  local usd = hdv();
  local mxn = hdv();
  local huf = hdv();

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
