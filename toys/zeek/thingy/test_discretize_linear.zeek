@load ./vsa

event zeek_init() {
  local ranges = VSA::discretize_linear($start=0.0, $stop=10.0, $bins=5);
  for (idx in ranges) {
    print idx, ranges[idx];
  }
}
