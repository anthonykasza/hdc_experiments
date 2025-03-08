# In a cluster setting, all nodes need to be working with the same sets of symbols. 

export {
  # endpoint symbols
  const client_hv = VSA::hdv();
  const server_hv = VSA::hdv();

  # 65535 bytes at 4 byte granularity
  option length_max = 65536 / 4;

  # 5 mins at 1/10th of a second granularity
  option interval_max = 5 * 60 * 10;

  # lengeth and interval symbols
  global length_codebook: vector of hypervector = VSA::make_levels(length_max);
  global interval_codebook: vector of hypervector = VSA::make_levels(interval_max);
}

