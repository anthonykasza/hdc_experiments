import sys; sys.path.insert(0, '../')
from utils import bind, bundle, hdv, permute, cossim

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN



def my_cossim(a, b):
  return 1 - cossim(a, b)


def make_message_bundle(msg, n, character_symbols):
  '''Turn a message into a bundle of character-ngrams'''
  ngram_bindings = []
  for j in range(1, n+1):
    for idx in range(len(msg) - j + 1):
      character_hvs = []
      character_subseq = msg[idx : idx+j]
      for c_idx in range(len(character_subseq)):
        char = character_subseq[c_idx]
        character_hvs.append( permute(character_symbols[ord(char)], c_idx) )
      ngram_bindings.append( bind(*character_hvs) )
  return bundle(*ngram_bindings)


# one symbol per byte as latin-1 is a 1 byte encoding
character_symbols = [hdv() for x in range(256)]
df = pd.read_csv('spam.csv', encoding='latin-1')
labels = np.array(df['v1'], dtype='str')
messages = np.array(df['v2'], dtype='str')


msg_emb_fname = './message_embeddings.pkl'
if os.path.exists(msg_emb_fname):
  with open(msg_emb_fname, 'rb') as f:
    message_embeddings = pickle.load(f)

else:
  # embed
  n = 10
  message_embeddings = []
  for idx in range(len(labels)):
    if idx % 15 == 0:
      print(f'embedding {idx}')
    label = labels[idx]
    message = messages[idx]
    message_embeddings.append(make_message_bundle(message, n, character_symbols))

  with open(msg_emb_fname, 'wb') as f:
    pickle.dump(message_embeddings, f)


dbscan = DBSCAN(eps=0.25, min_samples=3, metric=my_cossim)
dbscan.fit(message_embeddings)
for idx in range(len(labels)):
  print(dbscan.labels_[idx], labels[idx], messages[idx])
