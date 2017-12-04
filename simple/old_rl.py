import helpers

import gym
import numpy as np
import random

# Files are test-weights.pickle, latest-weights.pickle, and best-weights.pickle

def simple_rl(weights={}):
  env = gym.make('SuperMarioBros-1-1-v0')

  qTable = weights
  actionDict = read_in_data('action_space.pickle')

  def get_best_action(state, explorationProb):
    state = str(state)
    if state not in qTable:
      action = env.action_space.sample()
      actionDict[str(action)] = action
      qTable[state] = {}
      qTable[state][str(action)] = 0
      return (0, action)
    else:
      maxAction = (float("-inf"), None)
      for action, score in qTable[state].items():
        if score >= maxAction[0]:
          maxAction = (score, actionDict[action])

      randAction = env.action_space.sample()
      if random.random() < explorationProb:
        if str(randAction) not in qTable[str(state)]:
          actionDict[str(randAction)] = randAction
          qTable[state][str(randAction)] = 0
        return (0, randAction)
      return maxAction

  def generate_reward(state, oldInfo, newInfo):
    if newInfo['life'] == 0:
      return float("-inf")
    if oldInfo == {}:
      return 0

    distanceDelta = newInfo['distance'] - oldInfo['distance']
    scoreDelta = newInfo['score'] - oldInfo['score']
    #timeDelta = 1/(401 - newInfo['time'])
    print("DistanceDelta: {} ScoreDelta: {}".format(distanceDelta, scoreDelta))
    return distanceDelta + scoreDelta

  alpha = 0.618
  for episode in range(1, 101):
    env.lock.acquire()
    s = env.reset()
    env.lock.release()

    done = False
    totalReward, reward = 0, 0
    bestDistance = 0
    oldInfo = {}

    for i in range(0, 100000):
      env.render()

      action = get_best_action(s, 0.2)[1]
      while action == None:
        action = get_best_action(s, 0.2)[1]
        print("WE HAVE A NONE ACTION!!!!")
        print(qTable[str(s)])

      succ, ogReward, done, info = env.step(action)
      reward = generate_reward(succ, oldInfo, info)
      print("OgReward: {}".format(ogReward))
      print("OurReward: {}".format(reward))

      if info['life'] == 0:
        reward = float("-inf")
      if done:
        reward = float("inf")

      print(s)
      print(i, action, reward)

      oldVal = qTable[str(s)][str(action)]
      qTable[str(s)][str(action)] += alpha * (reward + get_best_action(succ, 0.0)[0] - oldVal)

      if info['distance'] > bestDistance:
        bestDistance = info['distance']
      if reward == float("-inf"):
        break

      s = succ
      totalReward += reward
      oldInfo = copy.deepcopy(info)

    print("Episode: {} \t Reward: {} \t Distance: {}".format(episode, reward, bestDistance))

    with open('rewards.txt', 'a') as f:
      f.write(str([episode, totalReward, bestDistance]))
      f.write("\n")
    f.close()

    env.lock.acquire()
    env.close()
    env.lock.release()
    killFCEUX()

    if episode % 5 == 0:
      helpers.write_to_file("weights.pickle", qTable, True)

  os._exit(0)


def reload_from_weights():
  env = gym.make('SuperMarioBros-1-1-v0')

  qTable = helpers.read_in_data('weights.pickle')
  actionDict = helpers.read_in_data('action_space.pickle')

  def get_best_action(state, explorationProb):
    state = str(state)
    if state not in qTable:
      action = env.action_space.sample()
      actionDict[str(action)] = action
      qTable[state] = {}
      qTable[state][str(action)] = 0
      return (0, action)
    else:
      maxAction = (float("-inf"), None)
      for action, score in qTable[state].items():
        if score >= maxAction[0]:
          maxAction = (score, actionDict[action])

      randAction = env.action_space.sample()
      if random.random() < explorationProb:
        if str(randAction) not in qTable[str(state)]:
          actionDict[str(randAction)] = randAction
          qTable[state][str(randAction)] = 0
        return (0, randAction)
      return maxAction

  env.lock.acquire()
  s = env.reset()
  env.lock.release()

  done = False
  totalReward = 0

  for i in range(0, 100000):
    env.render()

    action = get_best_action(s, 0.01)[1]
    while action == None:
      action = get_best_action(s, 0.01)[1]
      print("WE HAVE A NONE ACTION!!!!")
      print(qTable[str(s)])

    succ, reward, done, info = env.step(action)
    print("Reward", reward)

    if info['life'] == 0:
      reward = float("-inf")
    if done:
      reward = float("inf")

    print(s)
    print(i, action, reward)

    s = succ
    totalReward += reward

    if reward == float("-inf"):
      break
  print("Total Reward: {}".format(reward))

  env.lock.acquire()
  env.close()
  env.lock.release()
  killFCEUX()
  os._exit(0)

if __name__ == '__main__':
  simple_rl(read_in_data('weights.pickle'))
  #reload_from_weights()
