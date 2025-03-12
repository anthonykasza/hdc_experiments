
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
  # TODO - record previous record times for both client_ts and server_ts then `bind(endpoint, length, client_ival, server_ival)`
  previous_record_ts: time &optional;
};


event ssl_encrypted_data(c: connection, is_client: bool, record_version: count, content_type: count, length: count) {

  # 1. find the interval hv
  if (!c$ssl?$previous_record_ts) { c$ssl$previous_record_ts = c$start_time; }
  local interval_hv = ::interval_lookup(interval_to_double(network_time() - c$ssl$previous_record_ts));
  c$ssl$previous_record_ts = network_time();

  # 2. find the length hv
  local len_hv = ::length_lookup(length);

  # 3. bind everything and append into connection context
  c$ssl$role_filler_hvs[|c$ssl$role_filler_hvs|] = VSA::bind(vector(
    is_client ? client_hv : server_hv,
    len_hv,
    interval_hv
  ));
}

# given a list of HVs (one per record written to the wire), make the connection's bundle
function make_ngram_bundle(hvs: vector of hypervector, ngram_size: count &default=::ngram_size): hypervector {
  if (|hvs| == 0) { return VSA::hdv(VSA::dimensions, T); }
  
  local groups: vector of vector of hypervector;
  local group: vector of hypervector;
  local tmp: vector of hypervector;
  local ngram_hv: hypervector;
  local list_of_ngrams: vector of hypervector = vector();

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
    # append the ngram_hv binding to a list
    list_of_ngrams[|list_of_ngrams|] = ngram_hv;
  }

  # bundle all the bindings and return
  return VSA::bundle(list_of_ngrams);
}

# bundle role-filler hvs set in `ssl_encrypted_data` and store them
event connection_state_remove(c: connection) {
  if (! c?$ssl) { return; }
  ::conns_as_ngram_bundle[|::conns_as_ngram_bundle|] = make_ngram_bundle(c$ssl$role_filler_hvs);
  ::conns_as_uids[|::conns_as_uids|] = c$uid;
  ::conns_as_snis[|::conns_as_snis|] = c$ssl?$server_name ? c$ssl$server_name : "";
}
# In a cluster setting, the results of make_ngram_bundle()
#  would need to be sent from the worker processing the conenction
#  to the proxy/manager where the stream-clustering of hv occurs
