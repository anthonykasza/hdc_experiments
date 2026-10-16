# Circular Normal Representation based on FHRR and MCR


module VSA::CNR;

export {
  type hypervector: record {
    mus: vector of double &default = vector();
    kappas: vector of double &default = vector();
  };

  # VSA/HDC operations
  global new_hv: function(n: count, k: double): hypervector;
  global bind: function(hv1: hypervector, hv2: hypervector): hypervector;
  global unbind: function(hv1: hypervector, hv2: hypervector): hypervector;
  global bundle: function(hv1: hypervector, hv2: hypervector): hypervector;
  global sim: function(hv1: hypervector, hv2: hypervector): double;
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
function new_hv(n: count &default=10, k: double &default=1.0): hypervector {
  local v: hypervector = hypervector();
  local j = 0;
  while (j < n) {
    local phase: count = rand(PI_RANGE);
    local sign: count = rand(2);
    if (sign == 0) {
      v$mus[j] = (phase / PI_PRECISION) as double;
      v$kappas[j] = k;
    } else {
      v$mus[j] = ((phase / PI_PRECISION) * -1) as double;
      v$kappas[j] = k;
    }
    j += 1;
  }
  return v;
}

# Kappa weighted circular mean
function bundle(hv1: hypervector, hv2: hypervector): hypervector {
  local r: hypervector = hypervector();
  for ( idx in hv1$mus ) {
    local k1 = hv1$kappas[idx];
    local k2 = hv2$kappas[idx];

    local real_sum = k1 * cos(hv1$mus[idx]) + k2 * cos(hv2$mus[idx]);
    local imag_sum = k1 * sin(hv1$mus[idx]) + k2 * sin(hv2$mus[idx]);
    r$mus[idx] = atan2(imag_sum, real_sum);

    local total_weight = k1 + k2;
    if (total_weight > 0.0) {
      local magnitude = sqrt(real_sum * real_sum + imag_sum * imag_sum);
      r$kappas[idx] = magnitude / total_weight;
    } else {
      r$mus[idx] = 0.0;
      r$kappas[idx] = 0.0;
    }
  }

  return r;
}

# Addition of angles wrapped to the circle, uncertainty propagates
function bind(hv1: hypervector, hv2: hypervector): hypervector {
  local idx: count;
  local r: hypervector = hypervector();
  for (idx in hv1$mus) {
    r$mus[idx] = wrap_angle(hv1$mus[idx] + hv2$mus[idx]);

    local k1 = hv1$kappas[idx];
    local k2 = hv2$kappas[idx];
    local denom = k1 + k2 - k1 * k2;
    if (denom > 0.0) {
      r$kappas[idx] = (k1 * k2) / denom;
    } else {
      r$kappas[idx] = 0.0;
    }
  }

  return r;
}


# Subtraction of angles wrapped to the circle
function unbind(hv1: hypervector, hv2: hypervector): hypervector {
  local idx: count;
  local r: hypervector = hypervector();
  for (idx in hv1$mus) {
    r$mus[idx] = wrap_angle(hv1$mus[idx] - hv2$mus[idx]);

    local k1 = hv1$kappas[idx];
    local k2 = hv2$kappas[idx];
    local denom = k1 + k2 - k1 * k2;
    if (denom > 0.0) {
      r$kappas[idx] = (k1 * k2) / denom;
    } else {
      r$kappas[idx] = 0.0;
    }
  }

  return r;
}


# Kappa weighted cosine sim
function sim(hv1: hypervector, hv2: hypervector): double {
  local sum: double = 0.0;
  for (idx in hv1$mus) {
    local delta = hv1$mus[idx] - hv2$mus[idx];
    sum += hv1$kappas[idx] * hv2$kappas[idx] * cos(delta);
  }
  return (sum / |hv1$mus| + 1.0) / 2.0;
}

###########################################



# Tests
event zeek_init() {
  srand(42);
  local dims: count = 100;

  print "Kappa: 1.0";
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


  print "Kappa: 0.8";
  local hv1_08 = new_hv(dims, 0.8);
  local hv2_08 = new_hv(dims, 0.8);
  local bud_08 = bundle(hv1_08, hv2_08);
  local bid_08 = bind(hv1_08, hv2_08);

  print "sim hv1 hv2", sim(hv1_08, hv2_08);
  print "sim hv1 bundle", sim(hv1_08, bud_08);
  print "sim hv2 bundle", sim(hv2_08, bud_08);
  print "";
  print "sim hv1 binding", sim(hv1_08, bid_08);
  print "sim hv2 binding", sim(hv2_08, bid_08);
  print "recover hv1", sim(hv1_08, unbind(bid_08, hv2_08));
  print "recover hv2", sim(hv2_08, unbind(bid_08, hv1_08));
  print "";


  print "Kappa: 0.5";
  local hv1_05 = new_hv(dims, 0.5);
  local hv2_05 = new_hv(dims, 0.5);
  local bud_05 = bundle(hv1_05, hv2_05);
  local bid_05 = bind(hv1_05, hv2_05);

  print "sim hv1 hv2", sim(hv1_05, hv2_05);
  print "sim hv1 bundle", sim(hv1_05, bud_05);
  print "sim hv2 bundle", sim(hv2_05, bud_05);
  print "";
  print "sim hv1 binding", sim(hv1_05, bid_05);
  print "sim hv2 binding", sim(hv2_05, bid_05);
  print "recover hv1", sim(hv1_05, unbind(bid_05, hv2_05));
  print "recover hv2", sim(hv2_05, unbind(bid_05, hv1_05));
  print "";


  print "Kappa: 0.3";
  local hv1_03 = new_hv(dims, 0.3);
  local hv2_03 = new_hv(dims, 0.3);
  local bud_03 = bundle(hv1_03, hv2_03);
  local bid_03 = bind(hv1_03, hv2_03);

  print "sim hv1 hv2", sim(hv1_03, hv2_03);
  print "sim hv1 bundle", sim(hv1_03, bud_03);
  print "sim hv2 bundle", sim(hv2_03, bud_03);
  print "";
  print "sim hv1 binding", sim(hv1_03, bid_03);
  print "sim hv2 binding", sim(hv2_03, bid_03);
  print "recover hv1", sim(hv1_03, unbind(bid_03, hv2_03));
  print "recover hv2", sim(hv2_03, unbind(bid_03, hv1_03));
  print "";
}
