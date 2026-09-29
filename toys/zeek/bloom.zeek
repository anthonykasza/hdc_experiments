# Inspired by Bloom filters


module VSA::BLOOM;

export {
  # Counting variant
  type BloomFilter: vector of count;

  global new_random_symbol: function(s: string, n: count): BloomFilter;
  global new_hashed_symbol: function(s: string, n: count): BloomFilter;

  global bundle: function(hdvs: vector of BloomFilter): BloomFilter;
  global sim: function(bf1: BloomFilter, bf2: BloomFilter): double;

  option DIMS: count = 10000;
}

function new_random_symbol(s: string, n: count &default=DIMS): BloomFilter {
  local r: BloomFilter = vector();
  local j = n;
  while (j > 0) {
    r[|r|] = 0;
    j -= 1;
  }
  # 1-hot, randomly selected
  r[rand(n)] = 1;
  return r;
}

function new_hashed_symbol(s: string, n: count &default=DIMS): BloomFilter {
  local r: BloomFilter = vector();
  local j = n;
  while (j > 0) {
    r[|r|] = 0;
    j -= 1;
  }

  local hash = fnv1a32(s);
  while (hash > DIMS) { hash = hash - DIMS; }
  # 1-hot, based on hashed input
  r[hash] = 1;
  return r;
}

# Combine high dimensional, very sparse symbols using element-wise addition
function bundle(hdvs: vector of BloomFilter): BloomFilter {
  local idx: count;
  local v: BloomFilter = vector();

  for (element_idx in hdvs[0]) {
    v[element_idx] = 0;
    for (hv_idx in hdvs) {
      v[element_idx] += hdvs[hv_idx][element_idx];
    }
  }

  return v;
}

function sim(bf1: BloomFilter, bf2: BloomFilter): double {
  local dot: double = 0.0;
  local mag1: double = 0.0;
  local mag2: double = 0.0;
  local idx: count;

  for (idx in bf1) {
    dot += bf1[idx] * bf2[idx];
    mag1 += bf1[idx] * bf1[idx];
    mag2 += bf2[idx] * bf2[idx];
  }

  local m1 = sqrt(mag1);
  local m2 = sqrt(mag2);
  if (m1 == 0 || m2 == 0) { return 0.0; }
  return dot / (m1 * m2);
}

# Tests
event zeek_init() {
  print "Orthogonal symbols similar to VSAs";
  local symbol1: BloomFilter = new_random_symbol("something");
  local symbol2: BloomFilter = new_random_symbol("something else");
  local symbol3: BloomFilter = new_random_symbol("something unrelated");
  local bf = bundle(vector(symbol1, symbol2));
  print sim(bf, symbol1);
  print sim(bf, symbol2);
  print sim(bf, symbol3);
  print "";

  print "Hash-based indexing similar to Bloom filters";
  symbol1 = new_hashed_symbol("something");
  symbol2 = new_hashed_symbol("something else");
  symbol3 = new_hashed_symbol("something unrelated");
  bf = bundle(vector(symbol1, symbol2));
  print sim(bf, symbol1);
  print sim(bf, symbol2);
  print sim(bf, symbol3);
  print "";

  print "Frequency weighting";
  symbol1 = new_hashed_symbol("something");
  symbol2 = new_hashed_symbol("something");
  symbol3 = new_hashed_symbol("something");
  local symbol4 = new_hashed_symbol("something else");
  local symbol5 = new_hashed_symbol("something unrelated");
  bf = bundle(vector(
    symbol1, symbol2, symbol3, symbol4
  ));
  print sim(bf, symbol1);
  print sim(bf, symbol4);
  print sim(bf, symbol5);
}
