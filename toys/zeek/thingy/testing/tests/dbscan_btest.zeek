# @TEST-EXEC: zeek $PACKAGE %INPUT >> output 2>&1
# @TEST-EXEC: btest-diff output

event zeek_init() {
  local d: vector of hypervector = vector();

  # cluster 1
  local signal1 = VSA::hdv();
  d[|d|] = VSA::bundle(vector( VSA::hdv(), signal1) );
  d[|d|] = VSA::bundle(vector( VSA::hdv(), signal1) );
  d[|d|] = VSA::bundle(vector( VSA::hdv(), signal1) );

  # cluster 2
  local signal2 = VSA::hdv();
  d[|d|] = VSA::bundle(vector( VSA::hdv(), signal2) );
  d[|d|] = VSA::bundle(vector( VSA::hdv(), signal2) );
  d[|d|] = VSA::bundle(vector( VSA::hdv(), signal2) );

  # cluster 3
  local signal3 = VSA::hdv();
  d[|d|] = VSA::bundle(vector( VSA::hdv(), signal3) );
  d[|d|] = VSA::bundle(vector( VSA::hdv(), signal3) );
  d[|d|] = VSA::bundle(vector( VSA::hdv(), signal3) );
  
  # noise
  d[|d|] = VSA::hdv();


  local i: DBScanInput = [
    $data=d,
    $min_sim=0.25,
    $min_size=3
  ];
  local o = ::dbscan(i);

  print "noise", |o$noise|;
  print "clusters";
  for (cluster in o$clusters) {
    print |cluster|;
  }
}
