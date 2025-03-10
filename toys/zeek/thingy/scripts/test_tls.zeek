@load .

# NOTE - this script needs some TLS traffic to chew on

event zeek_done() {
  local result = ::dbscan([
    $data=::conns_as_ngram_bundle,
    $min_sim=0.9,
    $min_size=3
  ]);

  print "noise";
  for (noise_idx in result$noise) {
    print ::conns_as_uids[noise_idx] + "/" + ::conns_as_snis[noise_idx];
  }
  print "";

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
