
export {
  option ngram_size: count = 3;
  global make_ngram_bundle: function(hvs: vector of hypervector, ngram_size: count): hypervector;

  global conns_as_ngram_bundle: vector of hypervector = vector();
  global conns_as_uids: vector of string = vector();
  global conns_as_snis: vector of string = vector();
}

redef record SSL::Info += {
  # vector of ordered role-filler hvs: bind(endpoint, length, interval)
  role_filler_hvs: vector of hypervector &default=vector();

  # the time the previous record was written, regardless of which endpoint wrote it
  # TODO - consider tracking both client_ts and server_ts, then
  #        bind(endpoint, length, client_ival, server_ival)
  previous_record_ts: time &optional;
};

# TODO - consider making len_hv and interval_hv bundles
#        for example, len_hv could be a bundle of all the previous lengths up to this observation. lengths from records too far in the past will be "forgetten" due to the capacity of the bundling operation
event ssl_encrypted_data(c: connection, is_client: bool, record_version: count, content_type: count, length: count) {
  # for the first tls record, use the connection's start time as the previous_record_ts
  if (!c$ssl?$previous_record_ts) { c$ssl$previous_record_ts = c$start_time; }
  local interval_hv = VSA::symbol_lookup(interval_to_double(network_time() - c$ssl$previous_record_ts), ::interval_codebook);
  # update the connection's previous_record_ts to now
  c$ssl$previous_record_ts = network_time();

  local len_hv = VSA::symbol_lookup(length, ::length_codebook);

  # bind the endpoint, length, and time hypervectors into one and append the result to the connection's vector of HV
  c$ssl$role_filler_hvs[|c$ssl$role_filler_hvs|] = VSA::bind(vector(
    is_client ? client_hv : server_hv,
    len_hv,
    interval_hv
  ));

  # TODO - online ngrams instead of batch at connection expiration.
  #        instead of storing the same number of hv as records in the connection,
  #        only store a max of ngram_size hv per connection
  #   store ngram_size-1 ngram hvs in c$ssl
  #   store nram_bundle_hv in c$ssl
  #   if |ngram_hvs| > ngram_size-1
  #     cut a new ngram hv
  #     bundle the new ngram hv into c$ssl$ngram_bundle
  #     repalce the oldest ngram hv with the newly cut ngram hv in c$ssl

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
  groups = VSA::make_groups(hvs, ngram_size);
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
  ::conns_as_snis[|::conns_as_snis|] = c$ssl?$server_name ? c$ssl$server_name : "";
}

