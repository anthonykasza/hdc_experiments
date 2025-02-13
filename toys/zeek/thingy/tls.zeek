
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
  const orig_hv = VSA::hdv();
  const resp_hv = VSA::hdv();

  # counting stuff
  global orig_byte_counter: count = 0;
  global resp_byte_counter: count = 0;
  global orig_write_counter: count = 0;
  global resp_write_counter: count = 0;

  # bundles, one for each tls connections processed
  global tls_connection_hvs: vector of hypervector = vector();
  global tls_connection_ids: vector of string = vector();
}

redef record SSL::Info += {
  # each element is a roll-filler binding hv of: bind(endpoint, length, interval)
  roll_filler_hyperspace: vector of hypervector &default=vector();

  # each element is a length n-gram binding of: bind( perm(l[0],0), perm(l[1],1), perm(l[2],2) ) 
  client_len_trigram_hyperspace: vector of hypervector &default=vector();
  server_len_trigram_hyperspace: vector of hypervector &default=vector();

  # each element is an interval n-gram binding of: bind( perm(i[0],0), perm(i[1],1), perm(i[2],2) ) 
  client_ival_trigram_hyperspace: vector of hypervector &default=vector();
  server_ival_trigram_hyperspace: vector of hypervector &default=vector();
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

  # bind the endpoint, length, and time hypervectors into one
  #   and append the result to the connection's vector of HV
  if (is_client) {
    ::orig_byte_counter += length;
    ::orig_write_counter += 1;
    c$ssl$roll_filler_hyperspace += VSA::bind(vector( orig_hv, len_hv, interval_hv ));
  } else {
    ::resp_byte_counter += length;
    ::resp_write_counter += 1;
    c$ssl$roll_filler_hyperspace += VSA::bind(vector( resp_hv, len_hv, interval_hv ));
  }

  # TODO - accumulate endpoint len and ival vectors
}

event connection_state_remove(c: connection) {
  if (c?$ssl) {
    ::tls_connection_hvs += VSA::bundle(c$ssl$roll_filler_hyperspace);
    ::tls_connection_ids += c$uid;

    # TODO - embed endpoint len and ival ngrams, then bundle
    #   VSA::bundle(c$ssl$client_len_trigram_hyperspace)
    #   VSA::bundle(c$ssl$server_len_trigram_hyperspace)
    #   VSA::bundle(c$ssl$client_ival_trigram_hyperspace)
    #   VSA::bundle(c$ssl$server_ival_trigram_hyperspace)
  }
}

# inefficiently find tls connections which are likely related or duplicates
event zeek_done() {
  for (i in ::tls_connection_hvs) {
    for (j in ::tls_connection_hvs) {
      if (i == j) { next; }
      local sim = VSA::sim(::tls_connection_hvs[i], ::tls_connection_hvs[j]);
      if (sim > 0.8) {
        # i would wager that pairs with sim >0.8 have similar fingerprints or are destined for the same SNI
        print ::tls_connection_ids[i], ::tls_connection_ids[j], sim;
      }
    }
  }
}
