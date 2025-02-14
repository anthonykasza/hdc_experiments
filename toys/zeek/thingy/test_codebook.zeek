@load ./vsa
@load ./ranges

event zeek_init() {
  print "10 to 11", VSA::sim(
    VSA::symbol_lookup(10, ::length_codebook),
    VSA::symbol_lookup(11, ::length_codebook)
  );

  print "10 to 85", VSA::sim(
    VSA::symbol_lookup(10, ::length_codebook),
    VSA::symbol_lookup(85, ::length_codebook)
  );

  print "10 to 300", VSA::sim(
    VSA::symbol_lookup(10, ::length_codebook),
    VSA::symbol_lookup(300, ::length_codebook)
  );

  print "10 to 3000", VSA::sim(
    VSA::symbol_lookup(10, ::length_codebook),
    VSA::symbol_lookup(3000, ::length_codebook)
  );

  print "10 to 35000", VSA::sim(
    VSA::symbol_lookup(10, ::length_codebook),
    VSA::symbol_lookup(35000, ::length_codebook)
  );

  print "rando to rando", VSA::sim(
    VSA::hdv(),
    VSA::hdv()
  );

}
