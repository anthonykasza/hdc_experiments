# Fourier Holographic Reduced Representation


module VSA::FHRR;

export {
  # VSA/HDC operations
  global new_hv: function(n: count): vector of double;
  global bind: function(hv1: vector of double, hv2: vector of double): vector of double;
  global unbind: function(hv1: vector of double, hv2: vector of double): vector of double;
  global bundle: function(hv1: vector of double, hv2: vector of double): vector of double;
  global inverse: function(hv: vector of double): vector of double;
  global sim: function(hv1: vector of double, hv2: vector of double): double;
  global fpe: function(hv: vector of double, scalar: double): vector of double;
  # TODO: permute

  # Used in trig math
  const PI: double = 3.1415926535;
  const TWO_PI: double = PI * 2;
  const HALF_PI: double = PI / 2;

  # Used to generate random phases
  const PI_RANGE: count      = 31415926535;
  const PI_PRECISION: double = 10000000000;
}


###########################################
# Trig approximation functions
# TODO: wrap C implemenetations as a script bifs

function wrap_angle(x: double): double {
  while (x > PI)  { x -= TWO_PI; }
  while (x < -PI) { x += TWO_PI; }
  return x;
}

function sin(x: double): double {
  x = wrap_angle(x);

  if (x > HALF_PI) {
    x = PI - x;
  } else if (x < -HALF_PI) {
    x = -PI - x;
  }

  local x2 = x * x;

  return x * (
    1.0
    - x2 / 6.0
    + (x2 * x2) / 120.0
    - (x2 * x2 * x2) / 5040.0
    + (x2 * x2 * x2 * x2) / 362880.0
  );
}

function cos(x: double): double {
  return sin(x + HALF_PI);
}

function atan(x: double): double {
  local a = x;
  if (a < 0) {
    a = -a;
  }
  return (
    PI / 4.0 * x
    - x * (a - 1.0) * (0.2447 + 0.0663 * a)
  );
}

function atan2(y: double, x: double): double {
  if (x > 0) { return atan(y / x); }
  if (x < 0 && y >= 0) { return atan(y / x) + PI;}
  if (x < 0 && y < 0) { return atan(y / x) - PI; } 
  if (x == 0 && y > 0) { return HALF_PI; } 
  if (x == 0 && y < 0) { return -HALF_PI; } 
  return 0.0;
}
#
###########################################





###########################################
# Vector symbolic architecture operations
# TODO: make all of these C bifs

# The Vector Function Architecture papers show the distribution
#  sampled from in new_hv() influences the kernel induced by
#  fpe() and sim()
#  We sample uniformly so the kernel is sinc
# Additionally, the Waterloo folks showed that FHRR's use of
#  phases can be reframed as spikes. So Loihi, maybe?
function new_hv(n: count &default=10): vector of double {
  local v: vector of double = vector();
  local j = 0;
  while (j < n) {
    local phase: count = rand(PI_RANGE);
    local sign: count = rand(2);
    if (sign == 0) {
      v[j] = (phase / PI_PRECISION) as double;
    } else {
      v[j] = ((phase / PI_PRECISION) * -1) as double;
    }
    j += 1;
  }
  return v;
}

# This bundles AND normalizes all in 1 step
#  The angle is kept but the magnitude is discarded
function bundle(hv1: vector of double, hv2: vector of double): vector of double {
  local idx: count;
  local r: vector of double = vector();

  for (idx in hv1) {
    # TODO: multibundle
    local hv1_r = cos(hv1[idx]);
    local hv1_i = sin(hv1[idx]);

    local hv2_r = cos(hv2[idx]);
    local hv2_i = sin(hv2[idx]);

    local real_sum = hv1_r + hv2_r;
    local imag_sum = hv1_i + hv2_i;

    r[idx] = atan2(imag_sum, real_sum);
  }

  return r;
}

# Addition of angles wrapped to the circle
function bind(hv1: vector of double, hv2: vector of double): vector of double {
  local idx: count;
  local r: vector of double = vector();
  for (idx in hv1) {
    r[idx] = wrap_angle(hv1[idx] + hv2[idx]);
  }
  return r;
}

# Subtraction of angles wrapped to the circle
function unbind(hv1: vector of double, hv2: vector of double): vector of double {
  local idx: count;
  local r: vector of double = vector();
  for (idx in hv1) {
    r[idx] = wrap_angle(hv1[idx] - hv2[idx]);
  }
  return r;
}

# Summed cossine of differences divided by hv dimensionality
function sim(hv1: vector of double, hv2: vector of double): double {
  local sum: double = 0.0;
  for (idx in hv1) {
    sum = sum + cos(hv1[idx] - hv2[idx]);
  }
  return sum / |hv1|;
}

# Fractional power encoding unlocks the ability to embed
#  multivariate continuous tuples (feature vectors) into 
#  high dimensional spaces similar to random fourier features, neato
function fpe(hv: vector of double, scalar: double): vector of double {
  local r: vector of double = vector();
  for (idx in hv) {
    # While most hypervectors are clipped to -PI thru PI,
    #  these elements grow unbounded
    r[idx] = hv[idx] * scalar;
  }
  return r;
}
#
###########################################



# Tests
event zeek_init() {
  srand(42);

  local dims: count = 128;
  local hv1 = new_hv(dims);
  local hv2 = new_hv(dims);
  local bud = bundle(hv1, hv2);
  local bid = bind(hv1, hv2);

  print "sim hv1 hv2", sim(hv1, hv2);
  print "sim hv1 bundle", sim(hv1, bud);
  print "sim hv2 bundle", sim(hv2, bud);
  print "";
  print "sim hv1 binding", sim(hv1, bid);
  print "sim hv2 binding", sim(hv2, bid);
  print "recover hv1", sim(hv1, unbind(bid, hv2));
  print "recover hv2", sim(hv2, unbind(bid, hv1));
  print "";
  print "hv1 to hv1**2", sim(hv1, fpe(hv1, 2));
  print "hv1 to hv1**3", sim(hv1, fpe(hv1, 3));
  print "hv1 to hv1**3.5", sim(hv1, fpe(hv1, 3.5));
  print "hv1 to hv1**4", sim(hv1, fpe(hv1, 4));
  print "";
  print "hv1**2 to hv1**2", sim(fpe(hv1, 2), fpe(hv1, 2));
  print "hv1**2 to hv1**3", sim(fpe(hv1, 2), fpe(hv1, 3));
  print "hv1**2 to hv1**3.5", sim(fpe(hv1, 2), fpe(hv1, 3.5));
  print "hv1**2 to hv1**4", sim(fpe(hv1, 2), fpe(hv1, 4));
}
