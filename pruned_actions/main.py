# Used a simplified action set

import helpers

import gym
import numpy as np
import random
import copy

def simple_rl(weights={}):
  env = gym.make('SuperMarioBros-1-1-v0')

  qTable = weights
  actions = {
    0: [0, 0, 0, 0, 0, 0],  # Nothing
    1: [1, 0, 0, 0, 0, 0],  # Up
    2: [0, 0, 1, 0, 0, 0],  # Down
    3: [0, 1, 0, 0, 0, 0],  # Left
    4: [0, 1, 0, 0, 1, 0],  # Left + A
    5: [0, 1, 0, 0, 0, 1],  # Left + B
    6: [0, 1, 0, 0, 1, 1],  # Left + A + B
    7: [0, 0, 0, 1, 0, 0],  # Right
    8: [0, 0, 0, 1, 1, 0],  # Right + A
    9: [0, 0, 0, 1, 0, 1],  # Right + B
    10: [0, 0, 0, 1, 1, 1],  # Right + A + B
    11: [0, 0, 0, 0, 1, 0],  # A
    12: [0, 0, 0, 0, 0, 1],  # B
    13: [0, 0, 0, 0, 1, 1],  # A + B
  }

  def random_action():
    return random.sample(actions.keys(), 1)[0]

  def get_best_action(state, explorationProb):
    state = str(state)
    if state not in qTable:
      action = random_action()
      qTable[state] = {}
      qTable[state][action] = 0
      return (0, action)
    else:
      maxAction = (float("-inf"), None)
      if random.random() < explorationProb:
        action = random_action()
        if action not in qTable[str(state)]:
          qTable[state][action] = 0
        maxAction = (0, action)
      else:
        for action, score in qTable[state].items():
          if score >= maxAction[0]:
            maxAction = (score, action)
      return maxAction

  def generate_reward(state, oldInfo, newInfo):
    if oldInfo == {}:
      return 0

    distanceDelta = newInfo['distance'] - oldInfo['distance']
    scoreDelta = newInfo['score'] - oldInfo['score']
    #timeDelta = 1/(401 - newInfo['time'])
    print("DistanceDelta: {} ScoreDelta: {}".format(distanceDelta, scoreDelta))
    return distanceDelta + scoreDelta

  for episode in range(89, 500):
    env.lock.acquire()
    s = env.reset()
    env.lock.release()

    done = False
    totalReward, reward = 0, 0
    bestDistance = 0
    oldInfo = {}

    n = 0.618
    for i in range(1, 100000):
      env.render()

      action = get_best_action(s, 0.2)[1]
      while action == None:
        action = get_best_action(s, 0.2)[1]
        print("WE HAVE A NONE ACTION!!!!")
        print(qTable[str(s)])

      succ, ogReward, done, info = env.step(actions[action])
      reward = generate_reward(succ, oldInfo, info)
      print("OgReward: {}".format(ogReward))
      print("OurReward: {}".format(reward))

      if info['life'] == 0:
        reward = -10
      if done:
        reward = 20

      print(s)
      print(i, actions[action], reward)

      oldVal = qTable[str(s)][action]
      qTable[str(s)][action] += n * (reward + get_best_action(succ, 0.0)[0] - oldVal)
      totalReward += reward

      if info['distance'] > bestDistance:
        bestDistance = info['distance']
      if reward == -10:
        break

      s = succ
      oldInfo = copy.deepcopy(info)

    print("Episode: {} \t Reward: {} \t Distance: {}".format(episode, totalReward, bestDistance))

    with open('rewards.txt', 'a') as f:
      f.write(str([episode, totalReward, bestDistance]))
      f.write("\n")
    f.close()

    if episode % 5 == 0:
      helpers.write_to_file("weights.pickle", qTable, True)

    env.lock.acquire()
    env.close()
    env.lock.release()
    helpers.killFCEUX()
  os._exit(0)

if __name__ == '__main__':
  simple_rl()
  #simple_rl(helpers.read_in_data('weights.pickle'))
