@load ./vsa
@load ./codebooks
@load ./tls

event zeek_init() {
  local a: vector of hypervector = vector();
  a[|a|] = hypervector(0, -11, 2, 3, 4);
  a[|a|] = hypervector(0, 2, -4, 6, 8);
  a[|a|] = hypervector(1, -3, 5, 7, 9);
  a[|a|] = hypervector(3, -5, 7, 9, 11);
  a[|a|] = hypervector(5, -4, 3, 2, 1);
  a[|a|] = hypervector(5, 10, -15, 20, 25);
  a[|a|] = hypervector(1, 10, -100, 1000, 10000);
  a[|a|] = hypervector(10, -9, 8, 7, 6);
  a[|a|] = hypervector(8, -3, 6, 11, 4);

  local b: hypervector = make_ngram_bundle(a);

  for (idx in a) {
    local sim = VSA::sim(a[idx], b);
    print a[idx], b, sim;
  }
}
