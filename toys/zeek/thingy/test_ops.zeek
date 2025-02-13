@load ./vsa

event zeek_init() {

  local v1 = VSA::hdv(3);
  local v2 = VSA::hdv(3);
  print v1;
  print v2;
  print "";

  local hv: hypervector = vector();
  hv = VSA::bundle(vector( v1, v2 ));
  print "bundle", hv;
  print "";

  hv = VSA::bind(vector( v1, v2 ));
  print "bind", hv;
  print "";

  v1 = {1,2,3};
  print "hv", v1;
  print "perm 1", VSA::perm(v1, 1);
  print "perm -1", VSA::perm(v1, -1);
  print "perm -2", VSA::perm(v1, -2);
  print "perm -3", VSA::perm(v1, -3);
  print "";
}
