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
  for idx in range(len(msg) - n + 1):
    character_hvs = []
    character_subseq = msg[idx : idx+n]
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

# TODO - incorporate ngrams of various sizes as done in Language Geometry using Random Indexing
n = 3

spam_samples = []
ham_samples = []

for idx in range(len(labels))[:1000]:
  print(idx)
  label = labels[idx]
  message = messages[idx]
  message_bundle = make_message_bundle(message, n, character_symbols)
  if label == 'ham':
    ham_samples.append(message_bundle)
  else:
    spam_samples.append(message_bundle)

learned_spam_class = bundle(*spam_samples)
learned_ham_class = bundle(*ham_samples)

# TODO - make the better train/test strategy more robust than "pick one and check"
random_idx = random.choice(range(1000, len(labels)))
test_label = labels[random_idx]
test_message = messages[random_idx]
test_bundle = make_message_bundle(test_message, n, character_symbols)
test_is_spam = cossim(test_bundle, learned_spam_class)
test_is_ham = cossim(test_bundle, learned_ham_class)

print(f'{random_idx} {test_label}')
print(f'{test_message}')
print(f'spam: {test_is_spam}')
print(f'ham: {test_is_ham}')


