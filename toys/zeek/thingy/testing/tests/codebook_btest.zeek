# @TEST-EXEC: zeek $PACKAGE %INPUT >> output 2>&1
# @TEST-EXEC: btest-diff output


event zeek_init() {
  local sim: double;

  sim = VSA::sim(::length_codebook[1], ::length_codebook[double_to_count(2/4)]);
  print "1 to 2", sim;

  sim = VSA::sim(::length_codebook[1], ::length_codebook[double_to_count(28/4)]);
  print "1 to 28", sim;

  sim = VSA::sim(::length_codebook[1], ::length_codebook[double_to_count(34/4)]);
  print "1 to 34", sim;

  sim = VSA::sim(::length_codebook[1], ::length_codebook[double_to_count(68/4)]);
  print "1 to 68", sim;

  sim = VSA::sim(::length_codebook[1], ::length_codebook[double_to_count(96/4)]);
  print "1 to 96", sim;

  sim = VSA::sim(::length_codebook[1], ::length_codebook[double_to_count(123/4)]);
  print "1 to 123", sim;

  sim = VSA::sim(::length_codebook[1], ::length_codebook[double_to_count(7115/4)]);
  print "1 to 7115", sim;

  sim = VSA::sim(::length_codebook[1], ::length_codebook[double_to_count(11000/4)]);
  print "1 to 11000", sim;

  sim = VSA::sim(::length_codebook[1], ::length_codebook[double_to_count(23298/4)]);
  print "1 to 23298", sim;

  sim = VSA::sim(::length_codebook[1], ::length_codebook[double_to_count(65534/4)]);
  print "1 to 65534", sim;


  sim = VSA::sim(::length_codebook[double_to_count(11000/4)], ::length_codebook[double_to_count(7000/4)]);
  print "11000 to 7000", sim;

  sim = VSA::sim(::length_codebook[double_to_count(11000/4)], ::length_codebook[double_to_count(11002/4)]);
  print "11000 to 11005", sim;

  sim = VSA::sim(::length_codebook[double_to_count(11000/4)], ::length_codebook[double_to_count(12237/4)]);
  print "11000 to 12237", sim;

  sim = VSA::sim(::length_codebook[double_to_count(11000/4)], ::length_codebook[double_to_count(65534/4)]);
  print "11000 to 65534", sim;

  sim = VSA::sim(
    VSA::hdv(),
    VSA::hdv()
  );
  print "rando to rando", sim < 0.09;
}
