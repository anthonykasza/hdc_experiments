import sys; sys.path.insert(0, '../')
from utils import bundle, hdv, cossim, sub


class Window(object):
  '''A fading memory'''

  def __init__(self, fade_rate, size):
    self.fade_rate = fade_rate
    self.observation_count = 0
    self.leader = hdv(all=0)
    self.size = size
    self.accuracy = 2 # number of decimals places to expect in fade_rate


  def show(self, truth, decimal_places):
    '''Show what the Window remembers'''
    memory = dict([
      (i, round(cossim(truth[i], self.leader), decimal_places))
      for i in range(len(truth))
    ])
    return dict(sorted(memory.items(), key=lambda item: item[1])[-1*self.size:])


  def add(self, new_observation):
    '''Incorporate a new observation into the Window'''
    self.observation_count += 1
    if self.observation_count > self.size:
      self.forget()
    scale = 10 ** self.accuracy
    self.leader = sub(self.leader, new_observation, scale-1)[int( round(self.fade_rate, self.accuracy) * scale) ]


  def forget(self):
    '''Adjust the leader to forget the oldest observation,
       while maintaining its distance to the previous `size` observations
    '''
    pass





fade_rate = 0.33
size = 5
stream_size = 50
truth = []


# make a new Window and give it a stream of random data
w = Window(fade_rate, size)
for i in range(stream_size):
  sample = hdv()
  w.add(sample)

  truth.append(sample)


# show what the Window remembers
decimal_places = 4
print(w.show(truth, decimal_places))



# What happens to the output when you adjust the Window's `fade_rate` and `size`?
# What about changing the stream_size?
