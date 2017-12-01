import subprocess
import os

def killFCEUX():
  subprocess.call(["killall", "-9", "fceux"])

import gym
import numpy as np
import random

class RandomAgent(object):
  def __init__(self, action_space):
    self.action_space = action_space

  def act(self, observation, reward, done):
    return self.action_space.sample()


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
        if score > maxAction[0]:
          maxAction = (score, actionDict[action])

      randAction = env.action_space.sample()
      if random.random() < explorationProb:
        if str(randAction) not in qTable[str(state)]:
          actionDict[str(randAction)] = randAction
          qTable[state][str(randAction)] = 0
        return (0, randAction)
      return maxAction

  alpha = 0.618
  for episode in range(0, 10):
    env.lock.acquire()
    s = env.reset()
    env.lock.release()

    done = False
    G, reward = 0, 0

    for i in range(0, 1000):
      print(s)
      env.render()

      action = get_best_action(s, 0.2)[1]
      print(i, action)
      succ, reward, done, info = env.step(action)

      oldVal = qTable[str(s)][str(action)]
      qTable[str(s)][str(action)] += alpha * (reward + get_best_action(succ, 0.0)[0] - oldVal)
      G += reward
      s = succ
    print("Episode: {} \t Reward: {}".format(episode, G))

    env.lock.acquire()
    env.close()
    env.lock.release()
    killFCEUX()
  os._exit(0)


if __name__ == '__main__':
  simple_rl()
