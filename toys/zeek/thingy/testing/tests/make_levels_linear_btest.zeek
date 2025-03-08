# @TEST-EXEC: zeek $PACKAGE %INPUT >> output 2>&1
# @TEST-EXEC: btest-diff output


# num_of_levels = 0, changes_per_iteration = 9
# levels = [
#  [0, 1, 2, 3, 4, 5, 6, 7, 8],
#  [1, 1, 1, 1, 1, 1, 1, 1, 1],
# ]

# num_of_levels = 1, changes_per_iteration = 4.5
# levels = [
#  [0, 1, 2, 3, 4, 5, 6, 7, 8],
#  [1, 1, 1, 1, 4, 5, 6, 7, 8],
#  [1, 1, 1, 1, 1, 1, 1, 1, 1],
# ]

# num_of_levels = 2, changes_per_iteration = 3
# levels = [
#  [0, 1, 2, 3, 4, 5, 6, 7, 8],
#  [1, 1, 1, 3, 4, 5, 6, 7, 8],
#  [1, 1, 1, 1, 1, 1, 6, 7, 8],
#  [1, 1, 1, 1, 1, 1, 1, 1, 1],
# ]

# num_of_levels = 3, changes_per_iteration = 2.25
# levels = [
#  [0, 1, 2, 3, 4, 5, 6, 7, 8],
#  [1, 1, 2, 3, 4, 5, 6, 7, 8],
#  [1, 1, 1, 1, 4, 5, 6, 7, 8],
#  [1, 1, 1, 1, 1, 1, 6, 7, 8],
#  [1, 1, 1, 1, 1, 1, 1, 1, 1],
# ]

# num_of_levels = 4, changes_per_iteration = 1.8
# levels = [
#  [0, 1, 2, 3, 4, 5, 6, 7, 8],
#  [1, 1, 2, 3, 4, 5, 6, 7, 8],
#  [1, 1, 1, 1, 4, 5, 6, 7, 8],
#  [1, 1, 1, 1, 1, 5, 6, 7, 8],
#  [1, 1, 1, 1, 1, 1, 1, 7, 8],
#  [1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]

# num_of_levels = 7, changes_per_iteration = 1.125
# levels = [
#  [0, 1, 2, 3, 4, 5, 6, 7, 8],
#  [1, 1, 2, 3, 4, 5, 6, 7, 8],
#  [1, 1, 1, 3, 4, 5, 6, 7, 8],
#  [1, 1, 1, 1, 4, 5, 6, 7, 8],
#  [1, 1, 1, 1, 1, 5, 6, 7, 8],
#  [1, 1, 1, 1, 1, 1, 6, 7, 8],
#  [1, 1, 1, 1, 1, 1, 1, 7, 8],
#  [1, 1, 1, 1, 1, 1, 1, 1, 8],
#  [1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]

event zeek_init() {
  local v1: vector of int = {0, 1, 2, 3, 4, 5, 6, 7, 8};
  local v2: vector of int = {1, 1, 1, 1, 1, 1, 1, 1, 1};


  local hyperspace = VSA::make_levels(3, v1, v2);
  for (idx in hyperspace) {
    print idx, hyperspace[idx];
    if (idx == 0) { next; }
    print VSA::sim(hyperspace[idx], hyperspace[idx-1]);
  }
  print VSA::sim(hyperspace[0], hyperspace[|hyperspace|-1]);
  print "";

  hyperspace = VSA::make_levels(2, v1, v2);
  for (idx in hyperspace) {
    print idx, hyperspace[idx];
    if (idx == 0) { next; }
    print VSA::sim(hyperspace[idx], hyperspace[idx-1]);
  }
  print VSA::sim(hyperspace[0], hyperspace[|hyperspace|-1]);
  print "";

  hyperspace = VSA::make_levels(1, v1, v2);
  for (idx in hyperspace) {
    print idx, hyperspace[idx];
    if (idx == 0) { next; }
    print VSA::sim(hyperspace[idx], hyperspace[idx-1]);
  }
  print VSA::sim(hyperspace[0], hyperspace[|hyperspace|-1]);
  print "";

  hyperspace = VSA::make_levels(0, v1, v2);
  for (idx in hyperspace) {
    print idx, hyperspace[idx];
    if (idx == 0) { next; }
    print VSA::sim(hyperspace[idx], hyperspace[idx-1]);
  }
  print VSA::sim(hyperspace[0], hyperspace[|hyperspace|-1]);
  print "";

}
