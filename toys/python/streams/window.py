import sys; sys.path.insert(0, '../')
from utils import bundle, hdv, cossim, sub


class Window(object):
  '''A fading window memory'''

  def __init__(self, size, fade_rate):
    self.observation_count = 0
    self.leader = hdv(all=0)
    self.size = size
    self.accuracy = 2 # number of decimals places to expect in fade_rate
    self.fade_rate = fade_rate


  def show(self, truth, decimal_places):
    '''Show what the Window remembers'''
    memory = dict([
      (i, round(cossim(truth[i], self.leader), decimal_places))
      for i in range(len(truth))
    ])
    return dict(sorted(memory.items(), key=lambda item: item[1])[-1*self.size:])


  def add(self, new_observation, weight=1.0):
    '''Incorporate a new observation into the Window'''
    self.observation_count += 1
    scale = (10 ** self.accuracy)

    # TODO - adjust weight of incoming observation based on something
    #        1. based on self.self.observation_count?
    #        2. based on how dense the nearest micro-cluster's density is?
    #        3. based on its distance to the nearest higher density area?
    #        4. based on the observation's similarity to the leader bundle?
    percent = int(round(self.fade_rate * weight, self.accuracy) * scale)
    self.leader = sub(self.leader, new_observation, scale-1)[int(percent)]






size = 5
stream_size = 10
truth = []
fade_rate = 0.33
weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

w = Window(size, fade_rate)
for i in range(stream_size):
  sample = hdv()
  w.add(sample, weights[i])
  truth.append(sample)
decimal_places = 4
print("non weighted - a strictly temporal memory.")
print(w.show(truth, decimal_places))
print()




# again, but with variable weights
size = 5
stream_size = 10
truth = []
fade_rate = 0.33
weights = [1, 0.5, 0.5, 1, 0.33, 0.8, 0.1, 0.1, 1, 1.0]

w = Window(size, fade_rate)
for i in range(stream_size):
  sample = hdv()
  w.add(sample, weights[i])
  truth.append(sample)

decimal_places = 4
print("weighted - a temporal memory with weights/densities")
print(w.show(truth, decimal_places))
print()



# again, but with crazy variable weights
size = 5
stream_size = 10
truth = []
fade_rate = 0.33
# this will forget item 7 before item 0
weights = [3, 0.5, 0.5, 1, 0.33, 0.8, 0.1, 0.01, 1, 1]

w = Window(size, fade_rate)
for i in range(stream_size):
  sample = hdv()
  w.add(sample, weights[i])
  truth.append(sample)

decimal_places = 4
print("weighted - a temporal memory with CRAZY weights/densities")
print(w.show(truth, decimal_places))

