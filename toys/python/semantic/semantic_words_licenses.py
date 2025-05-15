
context_window_size = 10
word_ids = {}
word_meanings = {}
documents = {}

for doc in ./licenses:
  for word in doc:
    if word is not in word_ids.keys():
      word_ids[word] = new_hv()
      word_meanings[word] = new_hv(all=0)
    context = look back context_window_size and forward 10
    word_meanings[word] = add_hv(*context, word_meanings[word])

  documents[doc] = add_hv(*make_ngrams(doc))
