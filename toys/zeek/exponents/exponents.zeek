@load ./vsa

function range(c: count): vector of count {
  local v: vector of count = vector();
  local n: count = 0;

  while (n < c) {
    v[|v|] = n;
    n += 1;
  }

  return v;
}


event zeek_init() {
  # some number. it's simple to think in powers of 2
  local number: hypervector = VSA::hdv();

  # if number == 2, then number_to_expo10 == 1024
  local number_to_expo10: hypervector = VSA::hdv_all1(); # multiplicative identity
  local expo_steps: vector of hypervector = vector();
  for (idx in range(10)) {
    number_to_expo10 = VSA::bind(vector( number_to_expo10, number ));
    expo_steps[|expo_steps|] = number_to_expo10;
  }
  local expo_steps_bundle: hypervector = VSA::bundle(expo_steps);

  # 10 levels, but we are specifying 2 of them: number and number_to_expo10. so, 10-2
  local linear_steps: vector of hypervector = VSA::smear(10-2, number, number_to_expo10);
  local linear_steps_bundle: hypervector = VSA::bundle(linear_steps);

  # the progression is neat to see
  for (idx in range(10)) {
    local expo_step = expo_steps[idx];
    local linear_step = linear_steps[idx];
    print "idx", idx,
          "ls2es", VSA::sim(linear_step, expo_step),

          "ls2esb", VSA::sim(linear_step, expo_steps_bundle),
          "ls2lsb", VSA::sim(linear_step, linear_steps_bundle),

          "es2esb", VSA::sim(expo_step, expo_steps_bundle),
          "es2lsb", VSA::sim(expo_step, linear_steps_bundle);
  }
}
