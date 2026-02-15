# Inspired by Context-Dependent Thinning
#
# This architecture could easily be expanded
#  to include magnitudes and position
#  instead of assuming all magnitudes are 1


module VSA::CDT;

export {
  option SIZE: count = 200;
  option MAX_VAL: count = SIZE * SIZE;

  type hyperset: set[count];
  type Counter: record { pos: count; freq: count; };

  global new_hs: function(size: count, max_val: count): hyperset;
  global bundle: function(hss: set[hyperset]): hyperset;
  global bind: function(hss: set[hyperset]): hyperset;
  global similarity: function(h1: hyperset, h2: hyperset): double;
}


# Union, unbounded growth
function bundle(hss: set[hyperset]): hyperset {
  local accumulation: hyperset = set();
  for (hs in hss) {
    accumulation = accumulation | hs;
  }
  return accumulation;
}


# Union, thinned by frequency
function bind(hss: set[hyperset]): hyperset {
  local position_frequencies:
    table[count] of count
  = table() &default_insert = 1;

  # Count position "votes"
  for (hs in hss) {
    for (element in hs) {
      position_frequencies[element] += 1;
    }
  }

  # Sort frequency table as vector of Counter
  local v: vector of Counter = vector();
  for (position in position_frequencies) {
    local frequency: count = position_frequencies[position];
    v[|v|] = Counter($pos=position, $freq=frequency);
  }
  sort(v, function(a: Counter, b: Counter): int {
    if (a$freq < b$freq) { return -1; }
    return 1;
  });

  # Pull topk from sorted vector and return
  local topk: hyperset = hyperset();
  for (each in v[0 : VSA::CDT::SIZE]) {
    add topk[ v[each]$pos ];
  }
  return topk;
}


# Return a new hyperset symbol
function new_hs(
  size: count &default=SIZE,
  max_val: count &default=MAX_VAL
): hyperset {
  local hs: hyperset = set();
  local j = 0;
  while (j < SIZE) {
    local element: count = rand(max_val);
    if (element in hs) { next; }
    add hs[element];
    j += 1;
  }
  return hs;
}


# Intersection
function similarity(h1: hyperset, h2: hyperset): double {
  if ((|h1| == 0) || (|h2| == 0)) {
    return 0.0;
  }
  # Even when explicitly told that score is a double, the
  #  expression returns a count then stores it as double.
  #  Hence the "1.0 *"
  local smaller_set_size = |h1| < |h2| ? |h1| : |h2|;
  local score: double = 1.0 * |h1 & h2| / smaller_set_size;
  return score;
}


# Tests
event zeek_init() {
  # new symbols
  local symbol1 = new_hs();
  local symbol2 = new_hs();
  local symbol3 = new_hs();

  # new symbol similarity
  print similarity(symbol1, symbol2);
  print similarity(symbol1, symbol3);
  print similarity(symbol2, symbol3);

  # bundle
  local bu = bundle(set(symbol1, symbol2, symbol3));
  print "";

  # bundle similarity
  print similarity(bu, symbol1);
  print similarity(bu, symbol2);
  print similarity(bu, symbol3);

  # bind
  local bi = bind(set(symbol1, symbol2, symbol3));
  print "";

  # bind similarity
  print similarity(bi, symbol1);
  print similarity(bi, symbol2);
  print similarity(bi, symbol3);
}
