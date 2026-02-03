from bsdc_cdt import cpsd_decode_queries


class TriadicMemory:
  def __init__(self):
    self.tables = {}   # pos -> {bit -> {comp_id: count}}
    self.components = [] # comp_id -> SDR

  def register_component(self, hv):
    cid = len(self.components)
    self.components.append(hv)
    return cid

  def learn(self, composite, position_seeds, component_ids):
    queries = cpsd_decode_queries(composite, position_seeds)

    for q, cid in zip(queries, component_ids):
      pos = q["position"]
      sdr = q["query_sdr"]

      if pos not in self.tables:
        self.tables[pos] = {}

      table = self.tables[pos]

      for bit in sdr:
        if bit not in table:
          table[bit] = {}
        table[bit][cid] = table[bit].get(cid, 0) + 1

  def recall(self, composite, position_seeds, min_score=1):
    decoded = []
    queries = cpsd_decode_queries(composite, position_seeds)

    for q in queries:
      pos = q["position"]
      sdr = q["query_sdr"]

      scores = {}

      if pos not in self.tables:
        decoded.append(None)
        continue

      table = self.tables[pos]

      for bit in sdr:
        if bit in table:
          for cid, w in table[bit].items():
            scores[cid] = scores.get(cid, 0) + w

      if not scores:
        decoded.append(None)
        continue

      best_cid = max(scores, key=scores.get)

      if scores[best_cid] < min_score:
        decoded.append(None)
      else:
        decoded.append(self.components[best_cid])

    return decoded
