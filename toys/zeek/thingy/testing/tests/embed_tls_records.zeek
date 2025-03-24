# @TEST-EXEC: zeek $PACKAGE %INPUT >> output 2>&1
# @TEST-EXEC: btest-diff output

event zeek_init() {

  local v: vector of hypervector = vector(
    hypervector(-1,-1,-1,-1),
    hypervector(-2,-2,-2,-2),
    hypervector(-3,-3,-3,-3),
    hypervector(-4,-4,-4,-4),
    hypervector(-5,-5,-5,-5),
  );

  print "0", VSA::embed_tls_records(v, 0);
  print "";

  print "1", VSA::embed_tls_records(v, 1);
  print "";

  print "2", VSA::embed_tls_records(v, 2);
  print "";

  print "3", VSA::embed_tls_records(v, 3);
  print "";

  print "4", VSA::embed_tls_records(v, 4);
  print "";

  print "100", VSA::embed_tls_records(v, 100);
  print "";
}
