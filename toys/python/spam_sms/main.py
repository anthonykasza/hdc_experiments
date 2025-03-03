# Thank yous
#   SpamHD: Memory-Efficient Text Spam Detection using Brain-Inspired Hyperdimensional Computing
#   https://github.com/AikawaMafuyu/HamHD
#   https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset


import sys; sys.path.insert(0, '../')
from utils import bind, bundle, hdv, permute, cossim

import random

import pandas as pd
import numpy as np



def make_message_bundle(msg, n, character_symbols):
  ngram_bindings = []

  for j in range(1, n+1):
    #print(f'  ngrams of size: {j}')
    for idx in range(len(msg) - j + 1):
      character_hvs = []
      character_subseq = msg[idx : idx+j]
      for c_idx in range(len(character_subseq)):
        char = character_subseq[c_idx]
        character_hvs.append( permute(character_symbols[ord(char)], c_idx) )
      ngram_bindings.append( bind(*character_hvs) )

  return bundle(*ngram_bindings)



df = pd.read_csv('spam.csv', encoding='latin-1')
labels = np.array(df['v1'], dtype='str')
messages = np.array(df['v2'], dtype='str')

# one symbol per byte as latin-1 is a 1 byte encoding
character_symbols = [hdv() for x in range(256)]

train_size = 100
n = 10

spam_samples = []
ham_samples = []

# TODO - cross validate instead of using the first k samples
for idx in range(len(labels))[:train_size]:
  print(f'training on sample: {idx}')
  label = labels[idx]
  message = messages[idx]
  message_bundle = make_message_bundle(message, n, character_symbols)
  if label == 'ham':
    ham_samples.append(message_bundle)
  else:
    spam_samples.append(message_bundle)

learned_spam_class = bundle(*spam_samples)
learned_ham_class = bundle(*ham_samples)

# After training on the first k samples, we test on the remaining sample
for test_idx in range(train_size, len(labels)):
  test_label = labels[test_idx]
  test_message = messages[test_idx]
  test_bundle = make_message_bundle(test_message, n, character_symbols)
  test_is_spam = cossim(test_bundle, learned_spam_class)
  test_is_ham = cossim(test_bundle, learned_ham_class)

  # print stuff if the class bundles predicted incorrectly
  if test_label == 'ham' and test_is_ham < test_is_spam:
    print(f'{test_idx+train_size} ham predicted as spam')
    print(test_message)
    print()
  elif test_label == 'spam' and test_is_ham > test_is_spam:
    print(f'{test_idx+train_size} spam predicted as ham')
    print(test_message)
    print()
  elif test_is_ham == test_is_spam:
    print(f'{test_idx+train_size} undetermined')
    print(test_message)
    print()


# I didn't do much robust testing but from eyeballing it,
#  it looks like we can easily get 90% accuracy on testing
#  with only 100 training examples and ngrams of up to size 10
