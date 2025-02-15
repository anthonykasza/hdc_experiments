@load ./vsa

event zeek_init() {
  local ranges: vector of Range;

  ranges = VSA::discretize_linear([$start=0.0, $stop=10.0], 5);
  print "5";
  for (idx in ranges) {
    print idx, ranges[idx];
  }
  print "";

  ranges = VSA::discretize_linear([$start=0.0, $stop=10.0], 2);
  print "2";
  for (idx in ranges) {
    print idx, ranges[idx];
  }
  print "";

  ranges = VSA::discretize_linear([$start=0.0, $stop=10.0], 1);
  print "1";
  for (idx in ranges) {
    print idx, ranges[idx];
  }
  print "";

  ranges = VSA::discretize_linear([$start=0.0, $stop=10.0], 0);
  print "0";
  for (idx in ranges) {
    print idx, ranges[idx];
  }
  print "";

  ranges = VSA::discretize_linear([$start=0.0, $stop=10.0], 10);
  print "10";
  for (idx in ranges) {
    print idx, ranges[idx];
  }
  print "";

  ranges = VSA::discretize_linear([$start=0.0, $stop=10.0], 9);
  print "9";
  for (idx in ranges) {
    print idx, ranges[idx];
  }
  print "";

  ranges = VSA::discretize_linear([$start=0.0, $stop=10.0], 11);
  print "11";
  for (idx in ranges) {
    print idx, ranges[idx];
  }
  print "";

}
