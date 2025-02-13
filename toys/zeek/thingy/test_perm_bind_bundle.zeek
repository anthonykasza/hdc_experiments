@load ./vsa

export {
}

event zeek_init() {
  local a: vector of hypervector = vector();
  a += hypervector(0, -11, 2, 3, 4);
  a += hypervector(0, 2, -4, 6, 8);
  a += hypervector(1, -3, 5, 7, 9);
  a += hypervector(3, -5, 7, 9, 11);
  a += hypervector(5, -4, 3, 2, 1);
  a += hypervector(5, 10, -15, 20, 25);
  a += hypervector(1, 10, -100, 1000, 10000);
  a += hypervector(10, -9, 8, 7, 6);
  a += hypervector(8, -3, 6, 11, 4);

  local b: vector of hypervector;

  local groups: vector of vector of hypervector;
  local group: vector of hypervector;
  local tmp: vector of hypervector;
  local gram_hv: hypervector;
  local grams_hv: hypervector;

  groups = VSA::ngram(a, 3);
  for (idx in groups) {
    group = groups[idx];
    print group;
  }

  for (group_idx in groups) {
    group = groups[group_idx];
    tmp = vector();
    # permute or dont
    for (hv_idx in group) {
      tmp[|tmp|] = VSA::perm(group[hv_idx], hv_idx);
    }
    # bind the permuted hvs
    gram_hv = VSA::bind(tmp);
    b[|b|] = gram_hv;
    # bundle the gram_hv into the grams_hv
    grams_hv = VSA::bundle(vector( grams_hv, gram_hv ));
  }

  for (i in b) {
    local sim = VSA::sim(b[i], grams_hv);
    print b[i], grams_hv, sim;
  }
}
