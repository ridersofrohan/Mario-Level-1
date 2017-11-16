import util
import pygame as pg
import random

class Agent:
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    raiseNotDefined()


class SimpleAgent(Agent):
  def __init__(self, index=0):
    self.index = index
    self.isEnd = False

  def getAction(self):
    options = ['jump', 'right', 'right_jump', 'long_jump']
    return random.choice(options)


class MarioMDP(util.MDP):
  # Return the start state.
  def startState(self):
    return {'death': False, 'coin_total': 0, 'score': 0, 'time': 401, 'y': 498, 'x': 110}

  # Return set of actions possible from |state|.
  def actions(self, state):
    return ['down', 'jump', 'left', 'left_jump', 'right', 'right_jump', 'long_jump']

  # Return a list of (newState, prob, reward) tuples corresponding to edges
  # coming out of |state|.
  # Mapping to notation from class:
  #   state = s, action = a, newState = s', prob = T(s, a, s'), reward = Reward(s, a, s')
  # If IsEnd(state), return the empty list.
  def succAndProbReward(self, state, action):
    pass

  def discount(self):
    return 0.1

