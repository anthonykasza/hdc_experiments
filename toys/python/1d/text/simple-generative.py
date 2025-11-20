import sys
import re
import string
from collections import defaultdict

sys.path.insert(0, '../../')
from utils import hdv, bundle, bind, cossim


with open('books/pg11.txt', 'r') as file:
  text = file.read()
cleaned_text = re.split(r'\*\*\* START OF THE PROJECT GUTENBERG EBOOK ALICE\'S ADVENTURES IN WONDERLAND \*\*\*', text, maxsplit=1)[1]
cleaned_text = re.sub(r'[\n]', ' ', cleaned_text)
cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
cleaned_text = re.sub(r' ’', ' ', cleaned_text)
cleaned_text = re.sub(r'’', '', cleaned_text)
cleaned_text = re.sub(r'‘', '', cleaned_text)
cleaned_text = re.sub(r'“', '', cleaned_text)
cleaned_text = re.sub(r'”', '', cleaned_text)
cleaned_text = re.sub(r'—', '', cleaned_text)
cleaned_text = cleaned_text.translate(str.maketrans('', '', string.punctuation))

words = cleaned_text.lower().split()
word_contexts = defaultdict(list)
context_size = 3

for focus_idx in range(len(words)):
  focus = words[focus_idx]

  # too few words seen at beginning
  if focus_idx < context_size:
    continue

  # too few words remaining at end
  if focus_idx >= len(words) - context_size:
    break

  # context_size before, context_size after
  #word_contexts[focus].append(words[focus_idx-3])
  #word_contexts[focus].append(words[focus_idx-2])
  #word_contexts[focus].append(words[focus_idx-1])
  word_contexts[focus].append(words[focus_idx+1])
  word_contexts[focus].append(words[focus_idx+2])
  word_contexts[focus].append(words[focus_idx+3])


atoms = {word: hdv() for word in set(words)}
semantic_hv = {}

for focus, context_words in word_contexts.items():
  semantic_hv[focus] = bundle(*[atoms[word] for word in context_words])

# One can imagine binding information into context_words
#  such as its parts-of-speech or positional information


# use the hdc model to generative a sentence
sentence_len = 7
next_word = 'alice'
sentence = [next_word]

for i in range(sentence_len):
  seed_hv = atoms[next_word]
  next_sim = -1
  for word in semantic_hv.keys():
    if cossim(seed_hv, semantic_hv[word]) > next_sim:
      next_word = word
      next_sim = cossim(seed_hv, semantic_hv[word])
  sentence.append(next_word)
print(' '.join(sentence))
