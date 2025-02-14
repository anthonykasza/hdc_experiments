
export {
  global length_codebook: table[Range] of hypervector = {
    # By 32, with jitter
    [Range($start=0, $stop=29)] = VSA::hdv(),
    [Range($start=29, $stop=58)] = VSA::hdv(),
    [Range($start=58, $stop=87)] = VSA::hdv(),
    [Range($start=87, $stop=122)] = VSA::hdv(),
    # By 64, with jitter
    [Range($start=122, $stop=190)] = VSA::hdv(),
    [Range($start=190, $stop=260)] = VSA::hdv(),
    [Range($start=260, $stop=320)] = VSA::hdv(),
    [Range($start=320, $stop=287)] = VSA::hdv(),
    [Range($start=387, $stop=444)] = VSA::hdv(),
    [Range($start=444, $stop=503)] = VSA::hdv(),
    # By 128, with jitter
    [Range($start=503, $stop=644)] = VSA::hdv(),
    [Range($start=644, $stop=764)] = VSA::hdv(),
    [Range($start=764, $stop=900)] = VSA::hdv(),
    [Range($start=900, $stop=1031)] = VSA::hdv(),
    # By 512, with jitter
    [Range($start=1031, $stop=1519)] = VSA::hdv(),
    [Range($start=1519, $stop=1991)] = VSA::hdv(),
    [Range($start=1991, $stop=2597)] = VSA::hdv(),
    [Range($start=2597, $stop=3060)] = VSA::hdv(),
    # By 1024, with jitter
    [Range($start=3060, $stop=4002)] = VSA::hdv(),
    [Range($start=4002, $stop=5117)] = VSA::hdv(),
    [Range($start=5117, $stop=6137)] = VSA::hdv(),
    [Range($start=6137, $stop=7111)] = VSA::hdv(),
    # By 2024, with jitter
    [Range($start=7111, $stop=9191)] = VSA::hdv(),
    [Range($start=9191, $stop=11198)] = VSA::hdv(),
    [Range($start=11198, $stop=13131)] = VSA::hdv(),
    [Range($start=13131, $stop=15215)] = VSA::hdv(),
    # By 6072, with jitter
    [Range($start=15215, $stop=21307)] = VSA::hdv(),
    [Range($start=21307, $stop=27399)] = VSA::hdv(),
    # The rest, maximally large
    [Range($start=27399, $stop=35536)] = VSA::hdv()
  } &ordered;

  global interval_codebook: table[Range] of hypervector = {
    [Range($start=0.0, $stop=0.01)] = VSA::hdv(),
    [Range($start=0.01, $stop=0.1)] = VSA::hdv(),
    [Range($start=0.1, $stop=0.5)] = VSA::hdv(),
    [Range($start=0.5, $stop=1.0)] = VSA::hdv(),
    [Range($start=1.0, $stop=2.12)] = VSA::hdv(),
    [Range($start=2.12, $stop=5.0)] = VSA::hdv(),
    [Range($start=5.0, $stop=13.0)] = VSA::hdv(),
    [Range($start=13.0, $stop=22.0)] = VSA::hdv(),
    [Range($start=22.0, $stop=51.0)] = VSA::hdv(),
    [Range($start=51.0, $stop=283.0)] = VSA::hdv(),
    [Range($start=283.0, $stop=2888.0)] = VSA::hdv(),
  } &ordered;
}
