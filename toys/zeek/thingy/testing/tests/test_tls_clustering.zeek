# @TEST-EXEC: zeek $PACKAGE %INPUT >> output 2>&1
# @TEST-EXEC: btest-diff output


function make_connection(lengths: vector of count, ivals: vector of double, endpoints: vector of bool): hypervector {
  local records: vector of hypervector = vector();

  for (idx in lengths) {
    local length = lengths[idx];
    local ival = ivals[idx];
    local is_client = endpoints[idx];

    local interval_hv = ::interval_lookup(ival);
    local len_hv = ::length_lookup(length);

    local record_binding = VSA::bind(vector(
      is_client ? ::client_hv : ::server_hv, #gotta love the syntax `bool?::foo:::bar`
      len_hv,
      interval_hv
    ));

    # ordered HVs representing TLS records
    records[|records|] = record_binding;
  }

  # connections are bundles of record-ngrams
  return ::make_ngram_bundle(records);
}


# deterministic ordering
function my_order(myset: set[count]): vector of count {
  local v: vector of count = vector();
  for (number in myset) {
    v[|v|] = number;
  }
  sort(v);
  return v;
}


event zeek_init() {
  local lengths: vector of count;
  local ivals: vector of double;
  local endpoints: vector of bool;
  local conn: hypervector;

  # Connection 0, cluster
  print "processing conn0";
  lengths = {10, 10, 100, 100, 10, 10};
  ivals = {0.1, 0.1, 0.2, 0.2, 0.1, 0.1};
  endpoints = {T, F, F, T, F, T};
  conn = make_connection(lengths, ivals, endpoints);
  ::conns_as_ngram_bundle[|::conns_as_ngram_bundle|] = conn;
  ::conns_as_uids[|::conns_as_uids|] = "conn0";

  # Connection 1, cluster
  print "processing conn1";
  lengths = {11, 11, 101, 101, 11, 11};
  ivals = {0.2, 0.2, 0.4, 0.4, 0.2, 0.2};
  endpoints = {T, F, F, T, F, T};
  conn = make_connection(lengths, ivals, endpoints);
  ::conns_as_ngram_bundle[|::conns_as_ngram_bundle|] = conn;
  ::conns_as_uids[|::conns_as_uids|] = "conn1";

  # Connection 2, cluster
  print "processing conn2";
  lengths = {1, 1, 1, 11, 11, 101, 101, 11, 11, 1, 1, 1};
  ivals = {0.1, 0.1, 0.1, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.1, 0.1, 0.1};
  endpoints = {F, T, T, T, T, F, F, T, F, T, F, F, F};
  conn = make_connection(lengths, ivals, endpoints);
  ::conns_as_ngram_bundle[|::conns_as_ngram_bundle|] = conn;
  ::conns_as_uids[|::conns_as_uids|] = "conn2";


  # Connection 3, noise
  print "processing conn3";
  lengths = {5, 43, 12, 10, 10, 12000, 1000, 32, 15000};
  ivals = {10, 200, 0.1, 0.1, 30, 60, 10, .1, .1};
  endpoints = {T, T, T, T, T, F, F, F, F};
  conn = make_connection(lengths, ivals, endpoints);
  ::conns_as_ngram_bundle[|::conns_as_ngram_bundle|] = conn;
  ::conns_as_uids[|::conns_as_uids|] = "conn3";

  # Connection 4, noise
  print "processing conn4";
  lengths = {13049, 8059, 9397, 691, 193, 953, 2027, 11807, 251, 15581, 9311};
  ivals = {130.49, 80.59, 93.97, 6.91, 1.93, 9.53, 20.27, 118.07, 2.51, 155.81, 93.11};
  endpoints = {T, F, T, F, T, F, T, F, T, F, T};
  conn = make_connection(lengths, ivals, endpoints);
  ::conns_as_ngram_bundle[|::conns_as_ngram_bundle|] = conn;
  ::conns_as_uids[|::conns_as_uids|] = "conn4";



  # Connection 5, cluster
  print "processing conn5";
  lengths = {10, 10, 100, 100, 10, 10};
  ivals = {0.1, 0.1, 0.2, 0.2, 0.1, 0.1};
  endpoints = {T, F, F, T, F, T};
  conn = make_connection(lengths, ivals, endpoints);
  ::conns_as_ngram_bundle[|::conns_as_ngram_bundle|] = conn;
  ::conns_as_uids[|::conns_as_uids|] = "conn5";


  local result = ::dbscan([
    $data=::conns_as_ngram_bundle,
    $min_sim=0.66,
    $min_size=3
  ]);
  # NOTE - if min_sim is set to 0.75, sometimes conn2 is included
  #        in the cluster and sometimes it is not

  print "";
  print "noise", my_order(result$noise);
  for (cluster in result$clusters) {
    print "cluster", my_order(cluster);
  }
  print "";
}
