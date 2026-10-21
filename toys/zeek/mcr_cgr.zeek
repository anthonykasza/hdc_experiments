# based on Modular Composite (MCR)
#  and Cyclic Group (CGR) Representations



module VSA::MCR;

export {
  option dims: count = 10000;
  option block_size: count = 64;
  option bundle_method: string = "phasor";

  const PI: double = 3.141592653;
  const TWO_PI: double = PI * 2;
  const HALF_PI: double = PI / 2;

  type hypervector: record {
    phases: vector of count &default = vector();
  };

  type Phasor: record {
    c: double;
    s: double;
  };

  global phases: vector of Phasor = vector();
  global idx_to_phasor: function(idx: count): Phasor;
  global phasor_to_idx: function(p: Phasor): count;

  global new_hv: function(): hypervector;
  global bind: function(hvs: vector of hypervector): hypervector;
  global unbind: function(h1: hypervector, h2: hypervector): hypervector;
  global inverse: function(hv: hypervector): hypervector;
  global bundle: function(hvs: vector of hypervector, method: string): hypervector;
  global similarity: function(h1: hypervector, h2: hypervector): double;
}


# ------------------------------------------------------------
# Angle and trigonometric helpers
# ------------------------------------------------------------

function wrap_angle(x: double): double {
  while (x > PI)
    x -= TWO_PI;

  while (x < -PI)
    x += TWO_PI;

  return x;
}


function sine(x: double): double {
  x = wrap_angle(x);

  if (x > HALF_PI)
    x = PI - x;
  else if (x < -HALF_PI)
    x = -PI - x;

  local x2 = x * x;

  return x * (
    1.0
    - x2 / 6.0
    + (x2 * x2) / 120.0
    - (x2 * x2 * x2) / 5040.0
    + (x2 * x2 * x2 * x2) / 362880.0
  );
}


function cosine(x: double): double {
  return sine(x + HALF_PI);
}


# ------------------------------------------------------------
# Discrete phase alphabet
# ------------------------------------------------------------

# Wrap an integer phase index into [0, block_size).
#
# The intermediate arithmetic is signed so subtraction can
# represent negative phase differences.

function modulo(i: int): count {
  if (VSA::MCR::block_size == 0)
    return 0;

  local m = VSA::MCR::block_size as int;
  local r = i % m;

  if (r < 0)
    r += m;

  return r as count;
}


# Map a discrete phase index to its unit phasor:
#
#   z[k] = exp(i * 2*pi*k/block_size)
#
# The phasor is represented as (cos(theta), sin(theta)).
function idx_to_phasor(idx: count): Phasor {
  return VSA::MCR::phases[idx % VSA::MCR::block_size];
}


# Quantize a phasor to its nearest discrete phase.
#
# Maximize the dot product with each alphabet phasor.
# Iteration is in ascending index order, and strict ">" makes
# the lowest index win exact ties.

function phasor_to_idx(p: Phasor): count {
  if (VSA::MCR::block_size == 0)
    return 0;

  local best_idx: count = 0;
  local first = idx_to_phasor(0);
  local best_dot = p$c * first$c + p$s * first$s;

  local j: count = 1;

  while (j < VSA::MCR::block_size) {
    local q = idx_to_phasor(j);
    local dot = p$c * q$c + p$s * q$s;

    if (dot > best_dot) {
      best_dot = dot;
      best_idx = j;
    }

    j += 1;
  }

  return best_idx;
}


# ------------------------------------------------------------
# Hypervector construction
# ------------------------------------------------------------

function new_hv(): hypervector {
  local h: hypervector = hypervector();
  local j: count = 0;

  if (VSA::MCR::block_size == 0)
    return h;

  while (j < VSA::MCR::dims) {
    h$phases[j] = rand(VSA::MCR::block_size);
    j += 1;
  }

  return h;
}


# ------------------------------------------------------------
# Binding
# ------------------------------------------------------------

# Bind any number of hypervectors by adding their phase indices
# modulo the phase alphabet size.
#
# For two hypervectors:
#   bind(a,b)[j] = (a[j] + b[j]) mod block_size

function bind(hvs: vector of hypervector): hypervector {
  local out: hypervector = hypervector();

  if (|hvs| == 0 || VSA::MCR::block_size == 0)
    return out;

  local j: count = 0;
  while (j < VSA::MCR::dims) {
    local sum: int = 0;
    local i: count = 0;

    while (i < |hvs|) {
      sum += hvs[i]$phases[j] as int;
      i += 1;
    }

    out$phases[j] = modulo(sum);
    j += 1;
  }

  return out;
}


# ------------------------------------------------------------
# Unbinding and inversion
# ------------------------------------------------------------

# Subtract phase indices modulo the alphabet size.
#
# unbind(bind(a,b),b) recovers a exactly, provided the
# dimensions and phase alphabet are the same.

function unbind(h1: hypervector, h2: hypervector): hypervector {
  local out: hypervector = hypervector();

  if (VSA::MCR::block_size == 0)
    return out;

  local j: count = 0;
  while (j < VSA::MCR::dims) {
    local diff =
      (h1$phases[j] as int) -
      (h2$phases[j] as int);

    out$phases[j] = modulo(diff);
    j += 1;
  }

  return out;
}


# The multiplicative inverse of a phase is its negative phase.

function inverse(hv: hypervector): hypervector {
  local out: hypervector = hypervector();

  if (VSA::MCR::block_size == 0)
    return out;

  local j: count = 0;
  while (j < VSA::MCR::dims) {
    out$phases[j] = modulo(-(hv$phases[j] as int));
    j += 1;
  }

  return out;
}


# ------------------------------------------------------------
# Bundling method 1: discrete majority voting (CGR)
# ------------------------------------------------------------

# Count the number of occurrences of every phase index in
# each dimension.
#
# The phase with the highest count wins.
# Exact ties are resolved by choosing the lowest index.
#
# Example votes, block_size = 4:
#   [1, 1, 2, 1, 3] -> 1 selected with 3 votes. clear winner.
#   [3, 0, 3, 0]    -> 3 randomly selected with 2 votes. tied with 0.

function bundle_majority(hvs: vector of hypervector): hypervector {
  local out: hypervector = hypervector();

  if (|hvs| == 0 || VSA::MCR::block_size == 0)
    return out;

  local j: count = 0;
  while (j < VSA::MCR::dims) {
    local counts: vector of count = vector();
    local k: count = 0;

    while (k < VSA::MCR::block_size) {
      counts[k] = 0;
      k += 1;
    }

    local i: count = 0;

    while (i < |hvs|) {
      local phase = hvs[i]$phases[j] % VSA::MCR::block_size;
      counts[phase] += 1;
      i += 1;
    }

    local winner: count = 0;
    local best_count: count = counts[0];
    k = 1;

    # Strict ">" preserves the lowest index on ties.
    while (k < VSA::MCR::block_size) {
      if (counts[k] > best_count) {
        winner = k;
        best_count = counts[k];
      }

      k += 1;
    }

    out$phases[j] = winner;
    j += 1;
  }

  return out;
}


# ------------------------------------------------------------
# Bundling method 2: normalized complex-vector addition
# ------------------------------------------------------------

# At each dimension, add the unit phasors:
#
#   z = sum(exp(i * theta_k))
#
# Normalize the resultant vector, then quantize it to the
# nearest phase in the discrete alphabet.
#
# Normalization does not change its direction, but makes the
# operation explicitly a normalized-vector representation.
#
# If the resultant magnitude is zero, no direction exists;
# deterministically choose phase index zero.

function bundle_phasor(hvs: vector of hypervector): hypervector {
  local out: hypervector = hypervector();

  if (|hvs| == 0 || VSA::MCR::block_size == 0)
    return out;

  local j: count = 0;
  while (j < VSA::MCR::dims) {
    local real_sum: double = 0.0;
    local imag_sum: double = 0.0;

    local i: count = 0;

    while (i < |hvs|) {
      local p = idx_to_phasor(hvs[i]$phases[j]);

      real_sum += p$c;
      imag_sum += p$s;

      i += 1;
    }

    local magnitude = sqrt(
      real_sum * real_sum +
      imag_sum * imag_sum
    );

    if (magnitude == 0.0) {
      out$phases[j] = 0;
    }
    else {
      # Normalize the resultant complex vector.
      local normalized: Phasor = Phasor(
        $c=real_sum / magnitude,
        $s=imag_sum / magnitude
      );

      out$phases[j] = phasor_to_idx(normalized);
    }

    j += 1;
  }

  return out;
}


# Bundling method 3: random selection
#
# For each dimension, select one input hypervector at random
# and copy its phase index into the output.
#
# Each input contributes approximately 1 / |hvs| of the
# resulting bundle's elements in expectation.

function bundle_random_selection(
  hvs: vector of hypervector
): hypervector {
  local out: hypervector = hypervector();

  if (|hvs| == 0)
    return out;

  local n = |hvs|;
  local j: count = 0;
  while (j < VSA::MCR::dims) {
    local selected = rand(n);
    out$phases[j] = hvs[selected]$phases[j];
    j += 1;
  }

  return out;
}


# Bundling method 4: round robin
#
# Similar in expectation to random selection but
#  ensures even constituent contributions
#
function bundle_round_robin(
  hvs: vector of hypervector
): hypervector {
  local out: hypervector = hypervector();

  if (|hvs| == 0)
    return out;

  local n = |hvs|;
  local j: count = 0;
  while (j < VSA::MCR::dims) {
    local selected = j % n;
    out$phases[j] = hvs[selected]$phases[j];
    j += 1;
  }

  return out;
}

# ------------------------------------------------------------
# Public bundle API
# ------------------------------------------------------------

function bundle(
  hvs: vector of hypervector,
  method: string &default = VSA::MCR::bundle_method
): hypervector {
  if (method == "majority")
    return bundle_majority(hvs);

  if (method == "phasor")
    return bundle_phasor(hvs);

  if (method == "randsel")
    return bundle_random_selection(hvs);

  if (method == "rrobin")
    return bundle_round_robin(hvs);

  print fmt("MCR: unknown bundle method '%s'; using phasor", method);

  return bundle_phasor(hvs);
}


# ------------------------------------------------------------
# Similarity
# ------------------------------------------------------------

# Mean cosine of the angular difference at each dimension.
#
# For phase indices a and b:
#
#   sim(a,b) = mean(cos(2*pi*(a-b)/block_size))
#
# Identical hypervectors have similarity 1.
# For random independent phases, expected similarity is 0
# when the phase alphabet is symmetric and sufficiently large.

function similarity(h1: hypervector, h2: hypervector): double {
  if (VSA::MCR::block_size == 0 || |h1$phases| == 0)
    return 0.0;

  local sum: double = 0.0;
  local j: count = 0;
  while (j < VSA::MCR::dims) {
    local diff =
      (h1$phases[j] as int) -
      (h2$phases[j] as int);

    local angle =
      TWO_PI * (diff as double) / VSA::MCR::block_size;

    sum += cosine(angle);
    j += 1;
  }

  return sum / VSA::MCR::dims;
}


# precompute phasor lookup table based on configured block_size
event zeek_init() {
  local j: count = 0;

  while (j < VSA::MCR::block_size) {
    local angle =
      TWO_PI * j / VSA::MCR::block_size;

    VSA::MCR::phases[j] = Phasor(
      $c=cosine(angle),
      $s=sine(angle)
    );

    j += 1;
  }
}


# ------------------------------------------------------------
# Tests
# ------------------------------------------------------------

event zeek_init() {
  srand(42);

  local a = new_hv();
  local b = new_hv();
  local c = new_hv();

  # Exact binding/unbinding recovery.
  local ab = bind(vector(a, b));

  print "MCR binding/unbinding";
  print "sim(a,a):", similarity(a, a);
  print "sim(b,a):", similarity(b, a);
  print "sim(a, unbind(bind(a,b),b)):",
    similarity(a, unbind(ab, b));

  print "";

  # Both bundling methods.
  local majority = bundle(
    vector(a, b, c),
    "majority"
  );

  local phasor = bundle(
    vector(a, b, c),
    "phasor"
  );

  local rs = bundle(
    vector(a, b, c),
    "randsel"
  );

  local rr = bundle(
    vector(a, b, c),
    "rrobin"
  );

  print "Majority bundle (CGR)";
  print "sim(a, majority):", similarity(a, majority);
  print "sim(b, majority):", similarity(b, majority);
  print "sim(c, majority):", similarity(c, majority);

  print "";

  print "Normalized phasor bundle (MCR)";
  print "sim(a, phasor):", similarity(a, phasor);
  print "sim(b, phasor):", similarity(b, phasor);
  print "sim(c, phasor):", similarity(c, phasor);

  print "";

  print "Random selection";
  print "sim(a, rs):", similarity(a, rs);
  print "sim(b, rs):", similarity(b, rs);
  print "sim(c, rs):", similarity(c, rs);

  print "";

  print "Round Robin";
  print "sim(a, rr):", similarity(a, rr);
  print "sim(b, rr):", similarity(b, rr);
  print "sim(c, rr):", similarity(c, rr);

}
