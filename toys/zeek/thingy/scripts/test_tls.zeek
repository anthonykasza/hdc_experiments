@load .

# NOTE - this script needs some TLS traffic to chew on

event zeek_done() {
  local result = ::dbscan([
    $data=::conns_as_ngram_bundle,
    $min_sim=0.67,
    $min_size=3
  ]);

  print "noise";
  for (noise_idx in result$noise) {
    print ::conns_as_uids[noise_idx];
  }
  print "";

  print "clusters";
  for (cluster in result$clusters) {
    local tmp: string = "";
    for (idx in cluster) {
      tmp += ::conns_as_uids[idx];
      tmp += ", ";
    }
    print tmp;
  }
  print "";
}
