from collections import Counter
import re
import sys
sys.path.insert(0, '../')
from utils import hdv, bundle, bind, cossim

with open('books/pg11.txt', 'r') as file:
  text = file.read()
cleaned_text = re.sub(r'[^a-zA-Z\s’\'-]', ' ', text)
cleaned_text = re.sub(r'[\n]', ' ', cleaned_text)
cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
cleaned_text = re.sub(r' ’', ' ', cleaned_text)
words = cleaned_text.lower().split()


# word are measured by the company they keep
semantic_vectors = {}

# atomic symbols
ri_vectors = {}

# word counts to identify stop words and grammatical helpers
word_counts = Counter(words)


# the size around the focus
context_window_size = 5

# static vectors representing before or after the focus
before_hv = hdv()
after_hv = hdv()


for focus_idx in range(len(words)):
  focus = words[focus_idx]

  # too few words seen at beginning
  if focus_idx < context_window_size:
    semantic_vectors[focus] = hdv(all=0)
    ri_vectors[focus] = hdv()
    continue

  # too few words remaining at end
  if focus_idx >= len(words) - context_window_size:
    break

  # focus word not previously seen
  if focus not in ri_vectors.keys():
    semantic_vectors[focus] = hdv(all=0)
    ri_vectors[focus] = hdv()

  context_words_vectors = []
  for i in range((-1*context_window_size), (context_window_size+1)):
    if i == 0:
      continue
    context_word = words[focus_idx+i]

    # context word not previously seen
    if context_word not in ri_vectors.keys():
      semantic_vectors[context_word] = hdv(all=0)
      ri_vectors[context_word] = hdv()

    context_word_ri_vector = ri_vectors[context_word]
    if i < 0:
      context_words_vectors.append(bind(context_word_ri_vector, before_hv))
    if i > 0:
      context_words_vectors.append(bind(context_word_ri_vector, after_hv))

  context_words_vectors.append(semantic_vectors[focus])
  semantic_vectors[focus] = bundle(*context_words_vectors)


query = 'teacup'
query = 'white'
query = 'rabbit'
query_vector = ri_vectors[query]
for word in semantic_vectors.keys():
  print(f'{cossim(query_vector, semantic_vectors[word])}\t{query}\t{word}')
