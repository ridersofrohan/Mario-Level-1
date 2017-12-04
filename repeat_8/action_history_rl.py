# Keeps track of the previous action that it took to get to a state

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

  def get_best_action(state, previousAction, explorationProb):
    state = str(state)
    if state not in qTable:
      action = random_action()
      qTable[state] = {
        previousAction: {
          action: 0
        }
      }
      return (0, action)
    elif previousAction not in qTable[state]:
      qTable[state][previousAction] = {}

    maxAction = (float("-inf"), None)
    if random.random() < explorationProb or len(qTable[state][previousAction]) == 0:
      action = random_action()
      if action not in qTable[str(state)][previousAction]:
        qTable[state][previousAction][action] = 0
      maxAction = (0, action)
    else:
      for action, score in qTable[state][previousAction].items():
        if score >= maxAction[0]:
          maxAction = (score, action)
    return maxAction

  def generate_reward(state, oldInfo, newInfo):
    if oldInfo == {}:
      return 0

    distanceDelta = newInfo['distance'] - oldInfo['distance']
    #scoreDelta = newInfo['score'] - oldInfo['score']
    #timeDelta = 1/(401 - newInfo['time'])
    print("DistanceDelta: {}".format(distanceDelta))
    return distanceDelta

  n = 0.618
  y = .95
  for episode in range(1, 501):
    env.lock.acquire()
    s = env.reset()
    env.lock.release()

    succ, done, gameOver = None, False, False
    totalReward, reward, previousAction, bestDistance = 0, 0, 0, 0
    oldInfo, info = {}, {}

    for i in range(1, 100000):
      env.render()

      action = get_best_action(s, previousAction, 0.2)[1]
      while action == None:
        action = get_best_action(s, previousAction, 0.2)[1]
        print("WE HAVE A NONE ACTION!!!!")
        print(qTable[str(s)][previousAction])

      # repeat the action 8 times to try and make him hold a
      for _ in range(4):
        succ, ogReward, done, info = env.step(actions[action])
        reward = generate_reward(succ, oldInfo, info)
        print("OgReward: {}".format(ogReward))
        print("OurReward: {}".format(reward))
        if info['life'] == 0 or done:
          break

        print(s)
        print(i, actions[action], reward)

      reward = generate_reward(succ, oldInfo, info)

      if info['life'] == 0:
        reward = -10
        gameOver = True
      if done:
        reward = 2000

      oldVal = qTable[str(s)][previousAction][action]
      qTable[str(s)][previousAction][action] += n * (reward + y*get_best_action(succ, action, 0.0)[0] - oldVal)
      totalReward += reward

      if info['distance'] > bestDistance:
        bestDistance = info['distance']

      if gameOver or done:
        break

      s = succ
      oldInfo = copy.deepcopy(info)
      previousAction = action

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
  simple_rl(helpers.read_in_data('weights.pickle'))
