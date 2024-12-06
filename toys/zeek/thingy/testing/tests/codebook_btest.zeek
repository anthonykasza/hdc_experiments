# @TEST-EXEC: zeek $PACKAGE %INPUT >> output 2>&1
# @TEST-EXEC: btest-diff output

event zeek_init() {
  local sim: double;

  sim = VSA::sim(::length_lookup(1), ::length_lookup(2));
  print "1 to 2", sim;

  sim = VSA::sim(::length_lookup(1), ::length_lookup(28));
  print "1 to 28", sim;

  sim = VSA::sim(::length_lookup(1), ::length_lookup(34));
  print "1 to 34", sim;

  sim = VSA::sim(::length_lookup(1), ::length_lookup(68));
  print "1 to 68", sim;

  sim = VSA::sim(::length_lookup(1), ::length_lookup(96));
  print "1 to 96", sim;

  sim = VSA::sim(::length_lookup(1), ::length_lookup(123));
  print "1 to 123", sim;

  sim = VSA::sim(::length_lookup(1), ::length_lookup(7115));
  print "1 to 7115", sim;

  sim = VSA::sim(::length_lookup(1), ::length_lookup(11000));
  print "1 to 11000", sim;

  sim = VSA::sim(::length_lookup(1), ::length_lookup(16000));
  print "1 to 16000", sim;

  sim = VSA::sim(::length_lookup(16000), ::length_lookup(7000));
  print "16000 to 7000", sim;

  sim = VSA::sim(::length_lookup(11000), ::length_lookup(15000));
  print "16000 to 15000", sim;

  sim = VSA::sim(::length_lookup(16000), ::length_lookup(1));
  print "16000 to 1", sim;

  sim = VSA::sim(::length_lookup(16000), ::length_lookup(122));
  print "16000 to 122", sim;




  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(0.1));
  print "0.1 to 0.1", sim;

  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(0.6));
  print "0.1 to 0.6", sim;

  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(1.5));
  print "0.1 to 1.5", sim;

  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(3));
  print "0.1 to 3", sim;

  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(15));
  print "0.1 to 15", sim;

  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(25));
  print "0.1 to 25", sim;

  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(61));
  print "0.1 to 61", sim;

  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(125));
  print "0.1 to 125", sim;

  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(250));
  print "0.1 to 250", sim;

  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(299.9));
  print "0.1 to 299.9", sim;

  sim = VSA::sim(::interval_lookup(0.1), ::interval_lookup(301));
  print "0.1 to 301", sim;
}
