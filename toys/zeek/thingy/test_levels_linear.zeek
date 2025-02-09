@load ./vsa

event zeek_init() {
  local v1 = VSA::hdv();
  local v2 = VSA::hdv();


  local hyperspace = VSA::make_levels_linear(3, v1, v2);
  for (idx in hyperspace) {
    print idx, hyperspace[idx][0:7];
  }
  print "";

  hyperspace = VSA::make_levels_linear(0, v1, v2);
  for (idx in hyperspace) {
    print idx, hyperspace[idx][0:7];
  }
  print "";

  hyperspace = VSA::make_levels_linear(0);
  for (idx in hyperspace) {
    print idx, hyperspace[idx][0:7];
  }
}
