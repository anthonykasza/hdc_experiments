# In a cluster setting, all nodes need to be working with the same sets of symbols. 

export {
  const endpoint_hv = VSA::hdv();
  const numeric_hv = VSA::hdv();

  global length_lookup: function(length: count): hypervector;
  global interval_lookup: function(ival: double): hypervector;
}

function endpoint_lookup(is_client: bool): hypervector {
  # i'm pretty sure we could encode up to `VSA::dimensions` endpoints
  if (is_client) {
    return VSA::perm(endpoint_hv, 1);
  } else {
    return VSA::perm(endpoint_hv, -1);
  }
}

function length_lookup(length: count): hypervector {
  # 2^15, 1-byte sized categorical 'buckets'
  local magic = length;
  return VSA::perm(numeric_hv, magic);
}

function interval_lookup(ival: double): hypervector {
  # 3000, 1/10 second sized categorical 'buckets'
  local magic = double_to_count(ival * 10);
  return VSA::perm(numeric_hv, magic * -1);
}
