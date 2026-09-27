# Which addresses appeared in the most connections?


@load ./vsa

module VSA;
export {
  const symbol_dims: count = 10000;
  global codebook: table[addr] of Hvec = table();
  global talkers: Hvec = additive_identity(symbol_dims);
}

event new_connection(c: connection) { 
  if (c$id$orig_h !in codebook) { codebook[c$id$orig_h] = new_hv(symbol_dims); }
  if (c$id$resp_h !in codebook) { codebook[c$id$resp_h] = new_hv(symbol_dims); }
  # clipping would give the bundle a recency bias
  talkers = bundle_no_clip(vector(talkers, codebook[c$id$orig_h]));
  talkers = bundle_no_clip(vector(talkers, codebook[c$id$resp_h]));
}

event zeek_done() {
  for (host in codebook) {
    print host, cossim(codebook[host], talkers);
  }
}
