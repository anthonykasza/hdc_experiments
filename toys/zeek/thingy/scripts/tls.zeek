
export {
  option ngram_size: count = 5;

  global conns_as_ngram_bundle: vector of hypervector = vector();
  global conns_as_uids: vector of string = vector();
  global conns_as_snis: vector of string = vector();
}

redef record SSL::Info += {
  record_hvs: vector of hypervector &default=vector();

  # the time the previous record was written, regardless of which endpoint wrote it
  # TODO - record previous record times for both client_ts and server_ts then `bind(endpoint, length, client_ival, server_ival)`
  previous_record_ts: time &optional;
};


event ssl_encrypted_data(c: connection, is_client: bool, record_version: count, content_type: count, length: count) {
  if (!c$ssl?$previous_record_ts) { c$ssl$previous_record_ts = c$start_time; }
  local interval_hv = ::interval_lookup(interval_to_double(network_time() - c$ssl$previous_record_ts));
  c$ssl$previous_record_ts = network_time();

  c$ssl$record_hvs[|c$ssl$record_hvs|] = VSA::bind(vector(
    ::endpoint_lookup(is_client),
    ::length_lookup(length),
    interval_hv
  ));
}

event connection_state_remove(c: connection) {
  if (! c?$ssl) { return; }
  ::conns_as_ngram_bundle[|::conns_as_ngram_bundle|] = VSA::bundle(
    VSA::embed_tls_records(c$ssl$record_hvs, ::ngram_size)
  );
  ::conns_as_uids[|::conns_as_uids|] = c$uid;
  ::conns_as_snis[|::conns_as_snis|] = c$ssl?$server_name ? c$ssl$server_name : "";
}
