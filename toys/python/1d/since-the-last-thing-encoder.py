

def since_the_last_thing(thing, iterable):
  '''Count the things since the last thing'''
  if thing not in iterable:
    return []

  v = []
  since_prev_thing = 0

  for idx in range(len(iterable)):
    if iterable[idx] == thing:
      v.append(since_prev_thing)
      since_prev_thing = 0
    else:
      since_prev_thing += 1

  return v


# Templates are pretty easy to spot in space-encodings
print( since_the_last_thing(" ", "how many spaces are in this CRAZY message?") )
print( since_the_last_thing(" ", "how many spaces are in this ENCRYPTED message?") )
print( since_the_last_thing(" ", "how many spaces are in this _ _ message?") )
print( since_the_last_thing(" ", "how many spaces are in this           message?") )

# I wonder how what the vectors would look like for punctuation characters
# on long texts like an entire book. End-of-sentence and mid-sentence.
