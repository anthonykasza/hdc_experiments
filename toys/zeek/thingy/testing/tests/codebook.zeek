# @TEST-EXEC: zeek $PACKAGE %INPUT >> output 2>&1
# @TEST-EXEC: btest-diff output


event zeek_init() {
  local sim: double;

  sim = VSA::sim(
    VSA::symbol_lookup(10, ::length_codebook),
    VSA::symbol_lookup(11, ::length_codebook)
  );
  print "10 to 11", sim > 0.95;

  sim = VSA::sim(
    VSA::symbol_lookup(10, ::length_codebook),
    VSA::symbol_lookup(85, ::length_codebook)
  );
  print "10 to 85", sim > 0.9, sim < 1.0;

  sim = VSA::sim(
    VSA::symbol_lookup(10, ::length_codebook),
    VSA::symbol_lookup(300, ::length_codebook)
  );
  print "10 to 300", sim > 0.7, sim < 0.9;

  sim = VSA::sim(
    VSA::symbol_lookup(10, ::length_codebook),
    VSA::symbol_lookup(3000, ::length_codebook)
  );
  print "10 to 3000", sim > 0.15, sim < 0.5;

  sim = VSA::sim(
    VSA::symbol_lookup(10, ::length_codebook),
    VSA::symbol_lookup(35000, ::length_codebook)
  );
  print "10 to 35000", sim < 0.09;

  sim = VSA::sim(
    VSA::hdv(),
    VSA::hdv()
  );
  print "rando to rando", sim < 0.09;

}
