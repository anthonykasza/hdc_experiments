module VSA;

export {
  global hdv: function(n: count): vector of int;
  global bundle: function(hdvs: vector of vector of int): vector of int;
  global bind: function(hdvs: vector of vector of int): vector of int;
  global sim: function(hdv1: vector of int, hdv2: vector of int): double;
  global inverse: function(hdv: vector of int): vector of int;
  global dice_roll: function(): int;
}

function inverse(hdv: vector of int): vector of int {
  local v: vector of int = vector();
  for (idx in hdv) {
    v[idx] = hdv[idx] * -1;
  }
  return v;
}

function sim(hdv1: vector of int, hdv2: vector of int): double {
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

  # TODO - consider implementing a finite group which
  #   rests around -pi and +pi
}

function hdv(n: count &default=100000): vector of int {
  local v: vector of int = vector();
  local j = 0;
  while (n > 0) {
    v[j] = dice_roll();
    n -= 1;
    j += 1;
  }
  return v;
}


function bundle(hdvs: vector of vector of int): vector of int {
  local idx: count;
  local v: vector of int = vector();

  for (element_idx in hdvs[0]) {
    # initialize to additive identity
    v[element_idx] = 0;
    for (hv_idx in hdvs) {
      v[element_idx] += hdvs[hv_idx][element_idx];
    }
  }

  return v;
}

function bind(hdvs: vector of vector of int): vector of int {
  local idx: count;
  local v: vector of int = vector();

  for (element_idx in hdvs[0]) {
    # initialize to multiplicative identity
    v[element_idx] = 1;
    for (hv_idx in hdvs) {
      v[element_idx] = v[element_idx] * hdvs[hv_idx][element_idx];
    }
  }

  return v;
}


event zeek_init() {
  # role-filler bindings
  local country = hdv();
  local capital = hdv();
  local currency = hdv();

  # country values
  local usa = hdv();
  local mex = hdv();

  # capital values
  local wdc = hdv();
  local mxc = hdv();

  # currency values
  local usd = hdv();
  local mxn = hdv();

  # maps representing each USA and MEX record
  local usa_map = bundle(vector(
                    bind(vector(country, usa)),
                    bind(vector(capital, wdc)),
                    bind(vector(currency, usd))
                  ));
  print "united states map vector", usa_map[0:3], "...", usa_map[-3:];

  local mex_map = bundle(vector(
                    bind(vector(country, mex)),
                    bind(vector(capital, mxc)),
                    bind(vector(currency, mxn))
                  ));
  print "mexico map vector", mex_map[0:3], "...", mex_map[-3:];


  local analogy = bind(vector(usa_map, mex_map));
  local query = bind(vector(analogy, inverse(usd)));
  print "what is the dollar of mexico?";
  print "how similar is the query to USD?", sim(query, usd);
  print "how similar is the query to MXN?", sim(query, mxn); # hot damn!
  print "how similar is the query to WDC?", sim(query, wdc);
  print "how similar is the query to MXC?", sim(query, mxc);
  print "how similar is the query to USA?", sim(query, usa);
  print "how similar is the query to MEX?", sim(query, mex);
}
