# TODO: Measure the capacity of various bundling strategies.

# TODO: The Bundle classes in this file all use summation
#       with a probability of 100% - meaning each element
#       will be incorporated into the bundle.
#       Instead, use probabilistic summation, as in
#       sampled_bundle() of ../bundling/bundling_operators.py,
#       and then measure the capacity of bundles using various
#       clipping strategies.


cb_sign10 = CountingBundle(rate=10, clip_func=clip_sign)
cb_sign100 = CountingBundle(rate=100, clip_func=clip_sign)
cb_sign1000 = CountingBundle(rate=1000, clip_func=clip_sign)
cb_dec10 = CountingBundle(rate=10, clip_func=clip_dec)
cb_dec100 = CountingBundle(rate=100, clip_func=clip_dec)
cb_dec1000 = CountingBundle(rate=1000, clip_func=clip_dec)
cb_mean10 = CountingBundle(rate=10, clip_func=clip_dec_mean)
cb_mean100 = CountingBundle(rate=100, clip_func=clip_dec_mean)
cb_mean1000 = CountingBundle(rate=1000, clip_func=clip_dec_mean)

tb_sign10 = ThresholdBundle(thresh=10, clip_func=clip_sign)
tb_sign100 = ThresholdBundle(thresh=100, clip_func=clip_sign)
tb_sign1000 = ThresholdBundle(thresh=1000, clip_func=clip_sign)
tb_dec10 = ThresholdBundle(thresh=10, clip_func=clip_dec)
tb_dec100 = ThresholdBundle(thresh=100, clip_func=clip_dec)
tb_dec1000 = ThresholdBundle(thresh=1000, clip_func=clip_dec)
tb_mean10 = ThresholdBundle(thresh=10, clip_func=clip_dec_mean)
tb_mean100 = ThresholdBundle(thresh=100, clip_func=clip_dec_mean)
tb_mean1000 = ThresholdBundle(thresh=1000, clip_func=clip_dec_mean)

bb_sign = BatchBundle(clip_func=clip_sign)
bb_dec = BatchBundle(clip_func=clip_dec)
bb_mean = BatchBundle(clip_func=clip_dec_mean)

eb_sign = ExplicitBundle(clip_func=clip_sign)
eb_dec = ExplicitBundle(clip_func=clip_dec)
eb_mean = ExplicitBundle(clip_func=clip_dec_mean)
