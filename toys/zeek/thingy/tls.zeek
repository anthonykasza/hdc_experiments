
export {
  global length_codebook: table[Range] of hypervector = {
    # By 32, with jitter
    [Range($start=0, $stop=29)] = VSA::hdv(),
    [Range($start=29, $stop=58)] = VSA::hdv(),
    [Range($start=58, $stop=87)] = VSA::hdv(),
    [Range($start=87, $stop=122)] = VSA::hdv(),
    # By 64, with jitter
    [Range($start=122, $stop=190)] = VSA::hdv(),
    [Range($start=190, $stop=260)] = VSA::hdv(),
    [Range($start=260, $stop=320)] = VSA::hdv(),
    [Range($start=320, $stop=287)] = VSA::hdv(),
    [Range($start=387, $stop=444)] = VSA::hdv(),
    [Range($start=444, $stop=503)] = VSA::hdv(),
    # By 128, with jitter
    [Range($start=503, $stop=644)] = VSA::hdv(),
    [Range($start=644, $stop=764)] = VSA::hdv(),
    [Range($start=764, $stop=900)] = VSA::hdv(),
    [Range($start=900, $stop=1031)] = VSA::hdv(),
    # By 512, with jitter
    [Range($start=1031, $stop=1519)] = VSA::hdv(),
    [Range($start=1519, $stop=1991)] = VSA::hdv(),
    [Range($start=1991, $stop=2597)] = VSA::hdv(),
    [Range($start=2597, $stop=3060)] = VSA::hdv(),
    # By 1024, with jitter
    [Range($start=3060, $stop=4002)] = VSA::hdv(),
    [Range($start=4002, $stop=5117)] = VSA::hdv(),
    [Range($start=5117, $stop=6137)] = VSA::hdv(),
    [Range($start=6137, $stop=7111)] = VSA::hdv(),
    # By 2024, with jitter
    [Range($start=7111, $stop=9191)] = VSA::hdv(),
    [Range($start=9191, $stop=11198)] = VSA::hdv(),
    [Range($start=11198, $stop=13131)] = VSA::hdv(),
    [Range($start=13131, $stop=15215)] = VSA::hdv(),
    # By 6072, with jitter
    [Range($start=15215, $stop=21307)] = VSA::hdv(),
    [Range($start=21307, $stop=27399)] = VSA::hdv(),
    # The rest, maximally large
    [Range($start=27399, $stop=35536)] = VSA::hdv()
  } &ordered;

  global interval_codebook: table[Range] of hypervector = {
    [Range($start=0.0, $stop=0.01)] = VSA::hdv(),
    [Range($start=0.01, $stop=0.1)] = VSA::hdv(),
    [Range($start=0.1, $stop=0.5)] = VSA::hdv(),
    [Range($start=0.5, $stop=1.0)] = VSA::hdv(),
    [Range($start=1.0, $stop=2.12)] = VSA::hdv(),
    [Range($start=2.12, $stop=5.0)] = VSA::hdv(),
    [Range($start=5.0, $stop=13.0)] = VSA::hdv(),
    [Range($start=13.0, $stop=22.0)] = VSA::hdv(),
    [Range($start=22.0, $stop=51.0)] = VSA::hdv(),
    [Range($start=51.0, $stop=283.0)] = VSA::hdv(),
    [Range($start=283.0, $stop=2888.0)] = VSA::hdv(),
  } &ordered;

  # constant hypervectors representing which endpont wrote the record
  const client_hv = VSA::hdv();
  const server_hv = VSA::hdv();

  # ngram size
  option tls_record_ngram_size: count = 3;

  # counting stuff
  global client_byte_counter: count = 0;
  global server_byte_counter: count = 0;

  global conns_as_client_len_bundles: vector of hypervector = vector();
  global conns_as_server_len_bundles: vector of hypervector = vector();
  global conns_as_client_ival_bundles: vector of hypervector = vector();
  global conns_as_server_ival_bundles: vector of hypervector = vector();

  global conns_as_roll_filler_bundles: vector of hypervector = vector();
  global conns_as_uids: vector of string = vector();
}

redef record SSL::Info += {
  # each element is a roll-filler binding hv of: bind(endpoint, length, interval)
  roll_filler_hvs: vector of hypervector &default=vector();

  client_len_hvs: vector of hypervector &default=vector();
  server_len_hvs: vector of hypervector &default=vector();

  client_ival_hvs: vector of hypervector &default=vector();
  server_ival_hvs: vector of hypervector &default=vector();
};

event ssl_encrypted_data(c: connection, is_client: bool, record_version: count, content_type: count, length: count) {
  local start: double;
  local stop: double;

  # find the proper length HV
  local len_hv: hypervector;
  for (r, hv in ::length_codebook) {
    start = r$start;
    stop = r$stop;
    if (length >= start && length <= stop) {
      len_hv = hv;
      break;
    }
  }

  # find the proper time HV  
  local interval_hv: hypervector;
  local duration = interval_to_double(network_time() - c$start_time);
  for (r, hv in ::interval_codebook) {
    start = r$start;
    stop = r$stop;
    if (duration >= start && duration <= stop) {
      interval_hv = hv;
      break;
    }
  }
  # NOTE: interval_hv is the interval since the previous record, regardless
  #       if it was written by the client or the server
  #       this will influence ...

  # bind the endpoint, length, and time hypervectors into one
  #   and append the result to the connection's vector of HV
  if (is_client) {
    ::client_byte_counter += length;
    c$ssl$client_len_hvs[|c$ssl$client_len_hvs|] = len_hv;
    c$ssl$client_ival_hvs[|c$ssl$client_ival_hvs|] = interval_hv;
    c$ssl$roll_filler_hvs[|c$ssl$roll_filler_hvs|] = VSA::bind(vector( client_hv, len_hv, interval_hv ));
  } else {
    ::server_byte_counter += length;
    c$ssl$server_len_hvs[|c$ssl$server_len_hvs|] = len_hv;
    # ... the interval value here. the interval could be since the previous client or server record
    c$ssl$server_ival_hvs[|c$ssl$server_ival_hvs|] = interval_hv;
    c$ssl$roll_filler_hvs[|c$ssl$roll_filler_hvs|] = VSA::bind(vector( server_hv, len_hv, interval_hv ));
  }
}

event connection_state_remove(c: connection) {
  if (! c?$ssl) { return; }

  local groups: vector of vector of hypervector;
  local group: vector of hypervector;
  local tmp: vector of hypervector;
  local ngram_hv: hypervector;
  local ngram_accumulator_hv: hypervector;

  ngram_accumulator_hv = VSA::hdv(VSA::dimensions, T);
  groups = VSA::ngram(c$ssl$client_len_hvs, tls_record_ngram_size);
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
  ::conns_as_client_len_bundles[|::conns_as_client_len_bundles|] = ngram_accumulator_hv;

# TODO - do the same block as above but for each of the following:
#    ::conns_as_server_len_bundles[||] = VSA::bundle(c$ssl$server_len_hvs);
#    ::conns_as_client_ival_bundles[||] = VSA::bundle(c$ssl$client_ival_hvs);
#    ::conns_as_server_ival_bundles[||] = VSA::bundle(c$ssl$server_ival_hvs);

    ::conns_as_roll_filler_bundles[|::conns_as_roll_filler_bundles|] = VSA::bundle(c$ssl$roll_filler_hvs);
    ::conns_as_uids[|::conns_as_uids|] = c$uid;
}

# inefficiently find tls connections which are likely related or duplicates
event zeek_done() {
  for (i in ::conns_as_uids) {
    for (j in ::conns_as_uids) {
      if (i == j) { next; }

      # role fillers
      local rf_sim = VSA::sim(::conns_as_roll_filler_bundles[i], ::conns_as_roll_filler_bundles[j]);
      if (rf_sim > 0.88) {
        print "rolefiller sim", ::conns_as_uids[i], ::conns_as_uids[j], rf_sim;
      }

      # client lengths
      local cl_sim = VSA::sim(::conns_as_client_len_bundles[i], ::conns_as_client_len_bundles[j]);
      if (cl_sim > 0.88) {
        print "client len sim", ::conns_as_uids[i], ::conns_as_uids[j], cl_sim;
      }

#      # server lengths
#      local sl_sim = VSA::sim(::conns_as_server_len_bundles[i], ::conns_as_server_len_bundles[j]);
#      if (sl_sim > 0.88) {
#        print "server len sim", ::conns_as_uids[i], ::conns_as_uids[j], sl_sim;
#      }

#      # client intervals
#      local ci_sim = VSA::sim(::conns_as_client_ival_bundles[i], ::conns_as_client_ival_bundles[j]);
#      if (ci_sim > 0.88) {
#        print "client ival sim", ::conns_as_uids[i], ::conns_as_uids[j], ci_sim;
#      }

#      # server intervals
#      local si_sim = VSA::sim(::conns_as_server_ival_bundles[i], ::conns_as_server_ival_bundles[j]);
#      if (si_sim > 0.88) {
#        print "server ival sim", ::conns_as_uids[i], ::conns_as_uids[j], si_sim;
#      }
    }
  }
}
