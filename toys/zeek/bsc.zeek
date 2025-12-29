module VSA;

export {
  global hdv: function(n: count): vector of bool;
  global bundle: function(hdvs: vector of vector of bool): vector of bool;
  global bind: function(hdvs: vector of vector of bool): vector of bool;
  global sim: function(hdv1: vector of bool, hdv2: vector of bool): double;
  global inverse: function(hdv: vector of bool): vector of bool;
  global coin_toss: function(): bool;
  global tie_break: vector of bool &redef;

  global percent_true: function(hdv: vector of bool): double;
}

function percent_true(hdv: vector of bool): double {
  local s: double = 0.0;
  for (idx in hdv) { s += hdv[idx] ? 1.0 : 0.0; }
  return (s / |hdv|) * 100;
}

function inverse(hdv: vector of bool): vector of bool {
  local v: vector of bool = vector();
  for (idx in hdv) {
    if (hdv[idx]) {
      v[idx] = F;
    } else {
      v[idx] = T;
    }
  }
  return v;
}

function sim(hdv1: vector of bool, hdv2: vector of bool): double {
  local different: double = 0.0;
  for (idx in hdv1) {
    if (hdv1[idx] != hdv2[idx]) { different += 1.0; }
  }
  return different / |hdv1|;
}

function coin_toss(): bool {
  if (rand(2) == 0) { return T; }
  return F;
}

function hdv(n: count &default=100000): vector of bool {
  local v: vector of bool = vector();
  local j = 0;
  while (n > 0) {
    v[j] = coin_toss();
    n -= 1;
    j += 1;
  }
  return v;
}
# as soon as hdv() is defined, define the HV that will break ties
redef VSA::tie_break = hdv();


function bundle(hdvs: vector of vector of bool): vector of bool {
  local idx: count;
  local v: vector of bool = vector();

  for (element_idx in hdvs[0]) {

    # count the Ts and Fs
    local total: int = 0;
    for (hv_idx in hdvs) {
      if (hdvs[hv_idx][element_idx]) {
        total += 1;
      } else {
        total -= 1;
      }
    }

    # majority vote, "clipped" to T or F, ties broken deterministically
    if (total > 0) {
      v[element_idx] = T;
    } else if (total == 0 && VSA::tie_break[element_idx]) {
      v[element_idx] = T;
    } else {
      v[element_idx] = F;
    }
  }

  return v;
}

function bind(hdvs: vector of vector of bool): vector of bool {
  local idx: count;
  local v: vector of bool = vector();

  for (element_idx in hdvs[0]) {
    v[element_idx] = T;
    for (hv_idx in hdvs) {
      # This is XOR because v[element_idx] is true when
      #    v[element_idx] and hdvs[hv_idx][element_idx] differ
      v[element_idx] = v[element_idx] != hdvs[hv_idx][element_idx];
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
