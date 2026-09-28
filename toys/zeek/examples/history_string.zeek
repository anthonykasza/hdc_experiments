# Embed the conn history state string


@load ./vsa

module VSA;
export {
  const symbol_dims: count = 10000;
  global history_codebook: table[string] of Hvec = {
    ["s"] = new_hv(symbol_dims),
    ["h"] = new_hv(symbol_dims),
    ["a"] = new_hv(symbol_dims),
    ["d"] = new_hv(symbol_dims),
    ["f"] = new_hv(symbol_dims),
    ["c"] = new_hv(symbol_dims),
    ["g"] = new_hv(symbol_dims),
    ["t"] = new_hv(symbol_dims),
    ["w"] = new_hv(symbol_dims),
    ["i"] = new_hv(symbol_dims),
    ["q"] = new_hv(symbol_dims),
    ["x"] = new_hv(symbol_dims),

    ["S"] = new_hv(symbol_dims),
    ["H"] = new_hv(symbol_dims),
    ["A"] = new_hv(symbol_dims),
    ["D"] = new_hv(symbol_dims),
    ["F"] = new_hv(symbol_dims),
    ["C"] = new_hv(symbol_dims),
    ["G"] = new_hv(symbol_dims),
    ["T"] = new_hv(symbol_dims),
    ["W"] = new_hv(symbol_dims),
    ["I"] = new_hv(symbol_dims),
    ["Q"] = new_hv(symbol_dims),
    ["X"] = new_hv(symbol_dims),

    ["^"] = new_hv(symbol_dims)
  };
  global codebook: table[string] of Hvec = table();
}


# Sequence embedding without using ngrams
function embed(history: string): Hvec {
  local v: Hvec = vector();
  local letters: vector of Hvec = vector();
  local idx: count = 0;
  local char: string;

  for (char in history) {
    local letter_symbol = copy(history_codebook[char]);
    if (idx > 1) { permute(letter_symbol, idx-2); }
    if (idx > 0) { permute(letter_symbol, idx-1); }
    letters[idx] = permute(letter_symbol, idx);
    letters[idx] = permute(letter_symbol, idx+1);
    letters[idx] = permute(letter_symbol, idx+2);
    idx += 1;
  }

  return bundle(letters);
}



event zeek_init() {
  local tests: set[string] = {
    "SH", "SHad", "g", "sSaDd", "sSadD",
    "sSadTTtt", "sSadTtt"
  }; 
  for (test in tests) {
    codebook[test] = embed(test);
  }
}

event zeek_done() {
  for (inner in codebook) {
    for (outer in codebook) {
      # pairwise similarities
      print cossim(codebook[inner], codebook[outer]),
            inner,
            outer;
    }
  }
}
