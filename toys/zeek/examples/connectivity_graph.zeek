# Embed a connectivity graph

@load ./vsa

module VSA;
export {
  # In practice dimensionality should be near 10k
  const symbol_dims: count = 3;
  const resp_role_hv: Hvec = new_hv(symbol_dims);

  global node_codebook: table[addr] of Hvec;
  global edge_codebook: table[addr, addr] of Hvec;

  global make_node: function(node: addr);
  global make_edge: function(orig: addr, resp: addr);
  global make_graph: function(edges: table[addr, addr] of Hvec): Hvec;
}

function make_node(node: addr) {
  local h: Hvec = VSA::new_hv(symbol_dims);
  node_codebook[node] = h;
}

function make_edge(orig: addr, resp: addr) {
  local o_hv = node_codebook[orig];
  local r_hv = node_codebook[resp];

  # We need to indicate edge direction somehow.
  # Much literature uses a cyclic shift to indicate
  #  edge direction but we use a role binding, which
  #  is equivalent.
  # Another option would be to change architectures 
  #  to one with a non-commutative binding operation.
  local edge_hv = VSA::bind(
    o_hv,
    bind(r_hv, resp_role_hv)
  );
  edge_codebook[orig, resp] = edge_hv;
}

function make_graph(edges: table[addr, addr] of Hvec): Hvec {
  local symbols: vector of Hvec;
  local j = 0;
  for ([orig, resp] in edges) {
    symbols[j] = edges[orig, resp];
  }
  return VSA::bundle(symbols);
}

event new_connection(c: connection) { 
  if (c$id$orig_h !in node_codebook) { make_node(c$id$orig_h); }
  if (c$id$resp_h !in node_codebook) { make_node(c$id$resp_h); }
  make_edge(c$id$orig_h, c$id$resp_h);
}

event zeek_done() {
  print "Connection graph embedding size: ", |edge_codebook|;
  if (|edge_codebook| > 0) {
    print make_graph(edge_codebook);
  }
}
