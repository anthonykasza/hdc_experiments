import sys; sys.path.insert(0, '../')
from utils import bundle, hdv, cossim, sub


class Window(object):
  '''A fading window memory'''

  def __init__(self, size):
    self.observation_count = 0

    # different fading rate strategies
    self.fade_rates = [0.10, 0.33, 0.85]

    # keep a leader bundle for each fading rate
    self.leaders = [hdv(all=0)] * 3

    # the lookback window size is the same for all fading rates
    self.size = size
    # TODO - consider using different sized windows similar to
    #        different fade_rates?


  def show(self, truth, decimal_places):
    '''Show what the Window remembers'''
    memories = {}
    for idx in range(len(self.leaders)):
      leader = self.leaders[idx]
      fade_rate = self.fade_rates[idx]

      memory = dict([
        (i, round(cossim(truth[i], leader), decimal_places))
        for i in range(len(truth))
      ])
      memories[fade_rate] = dict(sorted(memory.items(), key=lambda item: item[1])[-1 * self.size:])
    return memories


  def add(self, new_observation, weight=1.0):
    '''Incorporate a new observation into the Window'''
    self.observation_count += 1
    accuracy = 2
    scale = (10 ** accuracy)
    for idx in range(len(self.leaders)):
      leader = self.leaders[idx]
      fade_rate = self.fade_rates[idx]
      percent = int(round(fade_rate * weight, accuracy) * scale)
      self.leaders[idx] = sub(leader, new_observation, scale-1)[int(percent)]







size = 5
stream_size = 10
truth = []
weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

w = Window(size)
for i in range(stream_size):
  sample = hdv()
  w.add(sample, weights[i])
  truth.append(sample)
decimal_places = 4
print("non weighted - a strictly temporal memory.")
for fade_rate,memory in w.show(truth, decimal_places).items():
  print(f'{fade_rate}: {memory}')
print()



# again, but with variable weights
size = 5
stream_size = 10
truth = []
weights = [1, 0.5, 0.5, 1, 0.33, 0.8, 0.1, 0.1, 1, 1]

w = Window(size)
for i in range(stream_size):
  sample = hdv()
  w.add(sample, weights[i])
  truth.append(sample)

decimal_places = 4
print("weighted - a temporal memory with weights/densities.")
for fade_rate,memory in w.show(truth, decimal_places).items():
  print(f'{fade_rate}: {memory}')
print()



# no more CRAZY. weights need to be between 0 and 1.
