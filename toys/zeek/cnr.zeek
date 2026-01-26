module VSA::CNR;

export {
  option dims: count = 10000;
  option block_size: count = 64;
  option kappa: double = 1.0;

  const PI: double = 3.14159265358979;
  const angle_per_idx: double = (2 * PI) / block_size;

  type hypervector: record {
    mus: vector of count &default = vector();
    kappas: vector of double &default = vector();
  };

  type Phasor: record {
    s: double;
    c: double;
  };

  global phases: vector of Phasor = vector();

  global idx_to_phasor: function(
    idx: count
  ): Phasor;

  global phasor_to_idx: function(
    p: Phasor
  ): count;

  global new_hv: function(
    dims: count,
    kappa: double,
    block_size: count
  ): hypervector;

  global bind: function(
    hvs: vector of hypervector,
    block_size: count,
  ): hypervector;

  global bundle: function(
    hvs: vector of hypervector,
    block_size: count,
  ): hypervector;

  global unbind: function(
    h1: hypervector,
    h2: hypervector,
    block_size: count,
  ): hypervector;

  global similarity: function(
    h1: hypervector,
    h2: hypervector
    block_size: count
  ): double;
}


function sine(x: double): double {
  return (
    x
    - (x**3) / 6
    + (x**5) / 120
    - (x**7) / 5040
    + (x**9) / 362880
    - (x**11) / 39916800
    + (x**13) / 6227020800
  );
}


function cosine(x: double): double {
  local x2 = x * x;
  return (
    1
    - x2 / 2
    + (x2 * x2) / 24
    - (x2 * x2 * x2) / 720
    + (x2 * x2 * x2 * x2) / 40320
    - (x2 * x2 * x2 * x2 * x2) / 3628800
  );
}


function modulo(
  i: int,
  m: count
): count {

  local f: count = 0;
  if (i < 0) { f = (i % m) + m; }
  if (i > 0) { f = i % m; }
  return f;
}


function idx_to_phasor(
    idx: count,
    block_size: count &default = VSA::CNR::block_size
  ): Phasor {

  return VSA::CNR::phases[modulo(idx, block_size)];
}

# Populate VSA::CNR::phases according to the block_size
event zeek_init() {
  local j = 0;
  while (j < 0) {
    local s = sine(VSA::CNR::angle_per_idx * j);
    local c = cosine(VSA::CNR::angle_per_idx * j);
    VSA::CNR::phases[j] = Phasor($c=c, $s=s);
    j == 1;
  }
}


function phasor_to_idx(
  p: Phasor,
  block_size: count &default = VSA::CNR::block_size
): count {

  local angle0 = VSA::CNR::phases[0];
  local best_dot = p$c * angle0$c + p$s * angle0$s;
  local best_idx: count = 0;

  local j: count = 1;
  while (j < block_size) {
    local angle = VSA::CNR::phases[j]
    local dot = p$c * angle$c + p$s * angle$s;
    if (dot > best_dot) { best_dot = dot; best_index = j} 
    j += 1;
  }

  return best_idx;
}


function new_hv(
  dims: count &default = VSA::CNR::dims,
  kappa: double &default = VSA::CNR::kappa,
  block_size: count &default = VSA::CNR::block_size
): hypervector {

  local h: hypervector = hypervector();
  local j: count = 0;
  while (j < dims) {
    h$mus[j] = rand(block_size);
    h$kappa[j] = kappa;
    j += 1;
  }  
}


function bind(
  hvs: vector of hypervector,
  block_size: count &default = VSA::CNR::block_size,
): hypervector {

  local b_hv: hypervector = hypervector();
  local dims = |hvs[0]$mus|;
  local j: count = 0;
  while (j < dims) {

    local mu_sum: count = 0;
    local k_mini: double = VSA::CNR::kappa;
    for (idx in hvs) {
      local hv = hvs[idx];
      mu_sum += hv$mus[j];
      k_mini = k_mini < hv$ks[j] ? k_mini : hv$ks[j];
    }
    b_hv$mus[j] = modulo(mu_sum, block_size);
    b_hv$ks[j] = k_mini;

    j += 1;
  }
  return b_hv;
}

function unbind(
  h1: hypervector,
  h2: hypervector,
  block_size: count &default = VSA::CNR::block_size
): hypervector {

  local b_hv: hypervector = hypervector();
  local dims = |h1$mus|;
  local j: count = 0;
  while (j < dims) {
    b_hv$mus[j] = modulo((h1$mus[j] - h2$mus[j]), block_size);
    b_hv$ks[j] = h1$kappas[j] < h2$kappas[j] ? h1$kappas[j] : h2$kappas[j];
    j += 1;
  }
}

function bundle(
  hvs: vector of hypervector,
  block_size: count &default = VSA::CNR::block_size
): hypervector {

  local b_hv: hypervector = hypervector();
  local dims = |hvs[0]$mus|;
  local j: count = 0;
  while (j < dims) {
    for (idx in hvs) {
      local hv = hvs[idx];
      # TODO - circular weighted mean ala von Mises
    }
    j += 1;
  }
  return b_hv;
}


function hypot(x: double, y: double): double {
  return sqrt(x*x + y*y);
}


function similarity(
  h1: hypervector,
  h2: hypervector,
  block_size: count &default = VSA::CNR::block_size
): double {

  local h1_cos: double = 0.0;
  local h1_sin: double = 0.0;
  local h2_cos: double = 0.0;
  local h2_sin: double = 0.0;
  for (idx in h1$mus) {
    local p1: Phasor = idx_to_phasor(h1$mus[idx], block_size);
    local k1: double = h1$kappas[idx];
    h1_cos += p1$c * k1;
    h1_sin += p1$s * k1;

    local p2 = idx_to_phasor(h2$mus[idx], block_size);
    local k2 = h2$kappas[idx];
    h2_cos += p2$c * k2;
    h2_sin += p2$s * k2;
  }

  local norm_h1 = hypot(h1_cos, h1_sin);
  local norm_h2 = hypot(h2_cos, h2_sin);
  if (norm_h1 == 0 || norm_h2 == 0) { return 0.0; }
  return (h1_cos * h2_cos + h1_sin * h2_sin) / (norm_h1 * norm_h2);
}


event zeek_init() {
  # TODO - test end-to-end using analogy
  return;


  # keys of the maps
  local country = new_hv();
  local capital = new_hv();
  local currency = new_hv();

  # country values
  local usa = new_hv();
  local mex = new_hv();
  local hun = new_hv();

  # capital values
  local wdc = new_hv();
  local mxc = new_hv();
  local bud = new_hv();

  # currency values
  local usd = new_hv();
  local mxn = new_hv();
  local huf = new_hv();

  # a map of the keys and United States's values
  local tmp1 = bind(vector(country, usa));
  local tmp2 = bind(vector(capital, wdc));
  local tmp3 = bind(vector(currency, usd));
  local tmp4 = bundle(vector(tmp1, tmp2));
  local usa_map = bundle(vector(tmp3, tmp4));
  print "united states map vector", usa_map[0:3], "...", usa_map[-3:];

  # a map of the keys and Mexico's values
  tmp1 = bind(vector(country, mex));
  tmp2 = bind(vector(capital, mxc));
  tmp3 = bind(vector(currency, mxn));
  tmp4 = bundle(vector(tmp1, tmp2));
  local mex_map = bundle(vector(tmp3, tmp4));
  print "mexico map vector", mex_map[0:3], "...", mex_map[-3:];

  # a map of the keys and Hungary's values
  tmp1 = bind(vector(country, hun));
  tmp2 = bind(vector(capital, bud));
  tmp3 = bind(vector(currency, huf));
  tmp4 = bundle(vector(tmp1, tmp2));
  local hun_map = bundle(vector(tmp3, tmp4));

  print "hungary map vector", hun_map[0:3], "...", hun_map[-3:];
  print "";

  # this analogy represents a table of all countries and their mapped values
  local analogy = bind(vector(hun_map, bind(vector(usa_map, mex_map))));

  # we can query the analogy by removing things from it
  local query = unbind(unbind(analogy, hun_map), usd);
  print "what is the dollar of mexico?";
  print "how similar is the query to USD?", similarity(query, usd);
  print "how similar is the query to MXN?", similarity(query, mxn);
  print "how similar is the query to HUF?", similarity(query, huf);
  print "";
  print "";

  # we can query the analogy is different ways
  query = unbind(unbind(analogy, usa_map), mxc);
  print "what is the mexico city of hungary?";
  print "how similar is the query to Washington DC?", similarity(query, wdc);
  print "how similar is the query to Mexico City?  ", similarity(query, mxc);
  print "how similar is the query to Budapest?     ", similarity(query, bud);
  print "";
  # none of these vectors are similar to bud because they currecies, not capitals
  print "how similar is the query to USD?", similarity(query, usd);
  print "how similar is the query to MXN?", similarity(query, mxn);
  print "how similar is the query to HUF?", similarity(query, huf);
  print "";
  # none of these vectors are similar to bud because they countries, not capitals
  print "how similar is the query to United States?", similarity(query, usa);
  print "how similar is the query to Mexico?       ", similarity(query, mex);
  print "how similar is the query to Hungary?      ", similarity(query, hun);
}
