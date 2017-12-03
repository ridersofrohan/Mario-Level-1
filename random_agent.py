import subprocess
import os
from os import path
import copy
import ast
import pickle

def killFCEUX():
  subprocess.call(["killall", "-9", "fceux"])

import gym

class RandomAgent(object):
  def __init__(self, action_space):
    self.action_space = action_space

  def act(self, observation, reward, done):
    #return [0,0,0,1,0,0] # always right
    #return [0,0,0,0,0,0] # dont move
    return [self.action_space.sample()]

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

if __name__ == '__main__':
  main()
