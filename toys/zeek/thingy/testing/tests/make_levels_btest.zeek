# @TEST-EXEC: zeek $PACKAGE %INPUT >> output 2>&1
# @TEST-EXEC: btest-diff output

event zeek_init() {
  local v1: vector of int = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  local v2 = VSA::hdv(10);
  local steps: vector of count;
  local levels: vector of hypervector;

  steps = vector(1, 1, 1, 1, 1, 1, 1, 1, 1, 1);
  levels = VSA::make_levels(steps, v1, v2);
  for (idx in levels) {
    print idx, levels[idx];
    if (idx == 0) { next; }
    print VSA::sim(levels[idx], levels[idx-1]);
  }
  print VSA::sim(levels[0], levels[|levels|-1]);
  print "";

  steps = vector(1, 0, 1, 0, 1, 0, 1, 0, 1, 0);
  levels = VSA::make_levels(steps, v1, v2);
  for (idx in levels) {
    print idx, levels[idx];
    if (idx == 0) { next; }
    print VSA::sim(levels[idx], levels[idx-1]);
  }
  print VSA::sim(levels[0], levels[|levels|-1]);
  print "";

  steps = vector(0, 1, 2, 3, 4, 0);
  levels = VSA::make_levels(steps, v1, v2);
  for (idx in levels) {
    print idx, levels[idx];
    if (idx == 0) { next; }
    print VSA::sim(levels[idx], levels[idx-1]);
  }
  print VSA::sim(levels[0], levels[|levels|-1]);
  print "";

  steps = vector(0, 1, 2, 3, 4, 0, 0, 0, 0);
  levels = VSA::make_levels(steps, v1, v2);
  for (idx in levels) {
    print idx, levels[idx];
    if (idx == 0) { next; }
    print VSA::sim(levels[idx], levels[idx-1]);
  }
  print VSA::sim(levels[0], levels[|levels|-1]);
  print "";

  steps = vector(|v1|);
  levels = VSA::make_levels(steps, v1, v2);
  for (idx in levels) {
    print idx, levels[idx];
    if (idx == 0) { next; }
    print VSA::sim(levels[idx], levels[idx-1]);
  }
  print VSA::sim(levels[0], levels[|levels|-1]);
  print "";
}
