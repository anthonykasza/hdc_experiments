
export {
  option ngram_size: count = 3;
  global make_ngram_bundle: function(hvs: vector of hypervector, ngram_size: count): hypervector;

  global conns_as_ngram_bundle: vector of hypervector = vector();
  global conns_as_uids: vector of string = vector();
}

redef record SSL::Info += {
  # vector of ordered role-filler hvs: bind(endpoint, length, interval)
  role_filler_hvs: vector of hypervector &default=vector();
};

event ssl_encrypted_data(c: connection, is_client: bool, record_version: count, content_type: count, length: count) {
  # TODO - find the equivalent event in the QUIC analyzer and mke this work for QUIC too

  local len_hv = VSA::symbol_lookup(length, ::length_codebook);
  local interval_hv = VSA::symbol_lookup(interval_to_double(network_time() - c$start_time), ::interval_codebook);

  # bind the endpoint, length, and time hypervectors into one
  #  and append the result to the connection's vector of HV
  c$ssl$role_filler_hvs[|c$ssl$role_filler_hvs|] = VSA::bind(vector(
    is_client ? client_hv : server_hv,
    len_hv,
    interval_hv
  ));

  # TODO - make everything streaming instead of batch. this likely means
  #  replacing make_ngram_bundle() with something else
  #     if (|c$ssl$ngrams_hvs| >= ngram_size) {
  #       new_ngram_hv = make_ngram(c$ssl$ngrams_hvs);
  #       # c$ssl$ngrams_hvs is now 1 item larger than ngram_size
  #       c$ssl$ngrams_hvs[|c$ssl$ngrams_hvs|] = new_ngram_hv;
  #       # pop the head off of c$ssl$ngrams_hvs
  #       c$ssl$ngrams_hvs[0:ngram_size-1] = c$ssl$ngrams_hvs[1:ngram_size];
  #       del c$ssl$ngrams_hvs[|ngram_size|];
  #       # incorporate new_ngram_hv into the conn's ngram_bundle
  #       c$ssl$ngram_bundle = VSA::bundle(vector( c$ssl$ngram_bundle, new_ngram_hv ));
  #     }

}

# given a list of ordered hvs, return a single hv representing all ngrams bundled together
function make_ngram_bundle(hvs: vector of hypervector, ngram_size: count &default=::ngram_size): hypervector {
  if (|hvs| == 0) { return VSA::hdv(VSA::dimensions, T); }
  
  local groups: vector of vector of hypervector;
  local group: vector of hypervector;
  local tmp: vector of hypervector;
  local ngram_hv: hypervector;
  local ngram_accumulator_hv: hypervector;

  ngram_accumulator_hv = VSA::hdv(|hvs[0]|, T);
  groups = VSA::ngram(hvs, ngram_size);
  for (group_idx in groups) {
    group = groups[group_idx];
    tmp = vector();
    # permute
    for (hv_idx in group) {
      tmp[|tmp|] = VSA::perm(group[hv_idx], hv_idx);
    }
    # bind the permuted hvs
    ngram_hv = VSA::bind(tmp);
    # bundle the ngram_hv into the ngram_accumulator_hv
    ngram_accumulator_hv = VSA::bundle(vector( ngram_accumulator_hv, ngram_hv ));
  }

  return ngram_accumulator_hv;
}

# bundle role-filler hvs set in `ssl_encrypted_data` and store them
event connection_state_remove(c: connection) {
  if (! c?$ssl) { return; }
  ::conns_as_ngram_bundle[|::conns_as_ngram_bundle|] = make_ngram_bundle(c$ssl$role_filler_hvs);
  ::conns_as_uids[|::conns_as_uids|] = c$uid;
}

