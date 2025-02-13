@load ./vsa

event zeek_init() {

  local v: vector of int = {0,1,2,3,4,5,6,7,8,9};
  print "2", VSA::ngram(v, 2);
  print "3", VSA::ngram(v, 3);
  print "4", VSA::ngram(v, 4);
}
