import subprocess
import os
from os import path
import copy

def killFCEUX():
  subprocess.call(["killall", "-9", "fceux"])

import gym
import numpy as np
import random
import pickle

# Function to read in weights and create a dictionary and a action table
def read_in_weights(filename):
  qTable = eval(open(filename).read())
  print(qTable)

# Function to write the data to the appropriate filename
def write_to_file(filename, data, overwrite=False):
  if overwrite:
    #try statement to remove previous file before writing new file
    try:
      os.remove(filename)
    except OSError:
      pass
    pickle.dump(data, filename)

  with open(filename, 'a') as f:
    f.write(data)
    f.write("\n")
  f.close()


class RandomAgent(object):
  def __init__(self, action_space):
    self.action_space = action_space

  def act(self, observation, reward, done):
    #return [0,0,0,1,0,0] # always right
    return [0,0,0,0,0,0] # dont move
    #return [self.action_space.sample()]


def main():
  env = gym.make('SuperMarioBros-1-1-v0')
  agent = RandomAgent(env.action_space)

  for i in range(2):
    env.lock.acquire()
    observation = env.reset()
    env.lock.release()

    for t in range(1000):
      env.render()
      print(observation)
      action = agent.act(observation, None, None)
      observation, reward, done, info = env.step(action)
      print(info)
      if done:
        print("Episode finished after {} timesteps".format(t+1))
        break

    env.lock.acquire()
    env.close()
    env.lock.release()
    killFCEUX()
  os._exit(0)


def simple_rl():
  env = gym.make('SuperMarioBros-1-1-v0')

  qTable = {}
  actionDict = {}

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
    print(distanceDelta, scoreDelta)
    return distanceDelta + scoreDelta


  alpha = 0.618
  for episode in range(1, 25):
    env.lock.acquire()
    s = env.reset()
    env.lock.release()

    if episode % 5 == 0:
      write_to_file("weights.txt", str(qTable), True)

    done = False
    totalReward, reward = 0, 0
    oldInfo = {}

    for i in range(0, 100000):
      env.render()

      action = get_best_action(s, 0.2)[1]
      while action == None:
        action = get_best_action(s, 0.2)[1]
        print("WE HAVE A NONE ACTION!!!!")
        print(qTable[str(s)])


      succ, reward, done, info = env.step(action)
      print("Reward", reward)
      reward = generate_reward(succ, oldInfo, info)
      print("Reward", reward)

      if info['life'] == 0:
        reward = float("-inf")

      if done:
        reward = float("inf")

      print(s)
      print(i, action, reward)

      oldVal = qTable[str(s)][str(action)]
      qTable[str(s)][str(action)] += alpha * (reward + get_best_action(succ, 0.0)[0] - oldVal)

      s = succ
      totalReward += reward
      oldInfo = copy.deepcopy(info)

      if reward == float("-inf"):
        break

    print("Episode: {} \t Reward: {}".format(episode, reward))
    write_to_file('rewards.txt', str([episode, totalReward]), False)

    env.lock.acquire()
    env.close()
    env.lock.release()
    killFCEUX()
  os._exit(0)


if __name__ == '__main__':
  #simple_rl()
  read_in_weights("weights.txt")

