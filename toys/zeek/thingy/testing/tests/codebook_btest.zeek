# @TEST-EXEC: zeek $PACKAGE %INPUT >> output 2>&1
# @TEST-EXEC: btest-diff output


event zeek_init() {
  local sim: double;

  # same range, same hv
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(2, ::length_codebook)
  );
  print "1 to 2", sim;

  # same range, same hv
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(29, ::length_codebook)
  );
  print "1 to 28", sim;

  # same range, 1 hv away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(34, ::length_codebook)
  );
  print "1 to 34", sim;

  # same range, 2 hv away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(68, ::length_codebook)
  );
  print "1 to 68", sim;

  # same range, 3 hv away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(96, ::length_codebook)
  );
  print "1 to 96", sim;

  # same range, 4 hv away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(122, ::length_codebook)
  );
  print "1 to 122", sim;

  # 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(123, ::length_codebook)
  );
  print "1 to 123", sim;

  # 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(130, ::length_codebook)
  );
  print "1 to 130", sim;

  # more than 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(7115, ::length_codebook)
  );
  print "1 to 7115", sim;

  # more than 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(11000, ::length_codebook)
  );
  print "1 to 11000", sim;

  # more than 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(12500, ::length_codebook)
  );
  print "1 to 12500", sim;

  # more than 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(15210, ::length_codebook)
  );
  print "1 to 15210", sim;

  # more than 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(15220, ::length_codebook)
  );
  print "1 to 15220", sim;

  # more than 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(23298, ::length_codebook)
  );
  print "1 to 23298", sim;

  # more than 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(23299, ::length_codebook)
  );
  print "1 to 23299", sim;

  # more than 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(23300, ::length_codebook)
  );
  print "1 to 23300", sim;

  # more than 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(65534, ::length_codebook)
  );
  print "1 to 65534", sim;

  # more than 1 range away
  sim = VSA::sim(
    VSA::symbol_lookup(1, ::length_codebook),
    VSA::symbol_lookup(70000, ::length_codebook)
  );
  print "1 to 70000", sim;

  print "";


  sim = VSA::sim(
    VSA::symbol_lookup(11000, ::length_codebook),
    VSA::symbol_lookup(7000, ::length_codebook)
  );
  print "11000 to 7000", sim;

  sim = VSA::sim(
    VSA::symbol_lookup(11000, ::length_codebook),
    VSA::symbol_lookup(7500, ::length_codebook)
  );
  print "11000 to 7500", sim;

  sim = VSA::sim(
    VSA::symbol_lookup(11000, ::length_codebook),
    VSA::symbol_lookup(11005, ::length_codebook)
  );
  print "11000 to 11005", sim;

  # TODO - why is there a hard edge between 12237 and 12238?
  sim = VSA::sim(
    VSA::symbol_lookup(11000, ::length_codebook),
    VSA::symbol_lookup(12237, ::length_codebook)
  );
  print "        ", "11000 to 12237", sim;
  sim = VSA::sim(
    VSA::symbol_lookup(11000, ::length_codebook),
    VSA::symbol_lookup(12238, ::length_codebook)
  );
  print "        ", "11000 to 12238", sim;

  sim = VSA::sim(
    VSA::symbol_lookup(11000, ::length_codebook),
    VSA::symbol_lookup(13000, ::length_codebook)
  );
  print "11000 to 13000", sim;

  sim = VSA::sim(
    VSA::symbol_lookup(11000, ::length_codebook),
    VSA::symbol_lookup(20000, ::length_codebook)
  );
  print "11000 to 20000", sim;

  sim = VSA::sim(
    VSA::symbol_lookup(11000, ::length_codebook),
    VSA::symbol_lookup(65534, ::length_codebook)
  );
  print "11000 to 65534", sim;

  print "";

  sim = VSA::sim(
    VSA::hdv(),
    VSA::hdv()
  );
  print "rando to rando", sim < 0.09;

}
