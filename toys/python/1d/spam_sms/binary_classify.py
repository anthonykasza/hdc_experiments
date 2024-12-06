import sys; sys.path.insert(0, '../../')
from utils import bind, bundle, hdv, permute, cossim

import pandas as pd
import numpy as np
from collections import defaultdict


def split_data(data, train_size):
  n = len(data)
  train_idx = np.random.choice(n, size=int(train_size * n), replace=False)
  test_idx = np.setdiff1d(np.arange(n), train_idx)
  return train_idx, test_idx


def make_message_bundle(msg, n, character_symbols):
  '''Turn a message into a bundle of character-ngrams
  '''
  ngram_bindings = []

  # TODO - think of a better way to incorporate all grams of all sizes.
  #        inspired by infini-grams i tried making `n = len(msg)` so it
  #        trains on grams with unbounded n, but it was reallllly slow.

  for j in range(1, n+1):
    for idx in range(len(msg) - j + 1):
      character_hvs = []
      character_subseq = msg[idx : idx+j]
      for c_idx in range(len(character_subseq)):
        char = character_subseq[c_idx]
        character_hvs.append( permute(character_symbols[ord(char)], c_idx) )
      ngram_bindings.append( bind(*character_hvs) )

  return bundle(*ngram_bindings)



character_symbols = defaultdict(hdv())

df = pd.read_csv('uniq.csv', encoding='latin-1')
labels = np.array(df['v1'], dtype='str')
messages = np.array(df['v2'], dtype='str')
train_indices, test_indices = split_data(labels, train_size=0.02)

n = 10

spam_samples = []
ham_samples = []


# train
for train_idx in range(len(train_indices)):
  print(f'training on: {train_idx}')
  label = labels[train_idx]
  message = messages[train_idx]
  message_bundle = make_message_bundle(message, n, character_symbols)
  if label == 'ham':
    ham_samples.append(message_bundle)
  else:
    spam_samples.append(message_bundle)

learned_spam_class = bundle(*spam_samples)
learned_ham_class = bundle(*ham_samples)


# test
for test_idx in range(len(test_indices)):
  test_label = labels[test_idx]
  test_message = messages[test_idx]
  test_bundle = make_message_bundle(test_message, n, character_symbols)
  test_is_spam = cossim(test_bundle, learned_spam_class)
  test_is_ham = cossim(test_bundle, learned_ham_class)

  # a difference of 0.05 could be explained by random noise in the bundles
  if abs(test_is_ham - test_is_spam) < 0.05 and test_label == 'spam':
    print(f'FN {test_idx} assumed ham, truth is spam {abs(test_is_spam - test_is_ham)}')

  # we predicted spam but the sample is ham
  elif test_label == 'ham' and test_is_ham < test_is_spam:
    print(f'FP {test_idx} predicted spam, truth is ham {abs(test_is_spam - test_is_ham)}')

  # we predicted ham, but the sample is spam
  elif test_label == 'spam' and test_is_ham > test_is_spam:
    print(f'FN {test_idx} predicted ham, truth is spam {abs(test_is_ham - test_is_spam)}')
