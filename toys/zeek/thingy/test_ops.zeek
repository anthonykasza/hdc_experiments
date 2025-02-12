@load ./vsa

event zeek_init() {

  local v1 = VSA::hdv(3);
  local v2 = VSA::hdv(3);
  print v1;
  print v2;

  local hv: hypervector = vector();
  hv = VSA::bundle(vector( v1, v2 ));
  print "bundle", hv;

  hv = VSA::bind(vector( v1, v2 ));
  print "bind", hv;
}
