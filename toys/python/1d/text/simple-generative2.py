import random
import sys
import re
import string
from collections import defaultdict, Counter

sys.path.insert(0, '../../')
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

# filter stop words
words = cleaned_text.lower().split()
word_count = len(set(words))
global_word_count = Counter(words)
stop_words = []
stop_word_threshold = 0.2
for word, count in dict(global_word_count).items():
  if count / word_count > stop_word_threshold:
    stop_words.append(word)
words = [word for word in words if word not in stop_words]


word_contexts = defaultdict(list)
context_size = 3

for focus_idx in range(len(words)):
  focus = words[focus_idx]
  if focus_idx >= len(words) - context_size:
    break
  # the 3 next words
  word_contexts[focus].append(words[focus_idx+1])
  word_contexts[focus].append(words[focus_idx+2])
  word_contexts[focus].append(words[focus_idx+3])

sentence_len = 7
topk_k = 3
next_word = 'alice'
sentence = [next_word]

# Recommendation Architecture
for i in range(sentence_len):
  for word in word_contexts.keys():
    # cluster: find a pattern
    c = Counter(word_contexts[next_word])
    choices = list(dict(c.most_common(topk_k)).keys())
    # compete: make a selection
    next_word = random.choice( choices )
  sentence.append(next_word)
print(' '.join(sentence))
