@load .

event zeek_done() {

  # TODO - expose clustering params as user-friendly exported options
  local result = ::dbscan([
    $data=::conns_as_ngram_bundle,
    $min_sim=0.1,
    $min_size=3
  ]);

  # TODO - use logging framework instead of prunting to scfreen
  print "noise";
  for (noise_idx in result$noise) {
    print ::conns_as_uids[noise_idx] + "/" + ::conns_as_snis[noise_idx];
  }
  print "";

  # TODO - use logging framework instead of prunting to scfreen
  print "clusters";
  for (cluster in result$clusters) {
    local tmp: string = "";
    for (idx in cluster) {
      tmp = tmp + ::conns_as_uids[idx] + "/" + ::conns_as_snis[idx];
      tmp = tmp + ", ";
    }
    print tmp;
  }
  print "";

}
