import util
import pygame as pg
from copy import deepcopy
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
    return (0, 1000, 0, 110, 498)

  # Return set of actions possible from |state|.
  def actions(self, state):
    return ['action', 'down', 'jump', 'left', 'left_jump', 'right', 'right_jump', 'long_jump']

  # Return a list of (newState, prob, reward) tuples corresponding to edges
  # coming out of |state|.
  # Mapping to notation from class:
  #   state = s, action = a, newState = s', prob = T(s, a, s'), reward = Reward(s, a, s')
  # If IsEnd(state), return the empty list.
  def succAndProbReward(self, state, action, game=None):
    def calculateReward(s):
        # State information order:
        # 0 - Score
        # 1 - Time
        # 2 - Coin Total
        # 3 - Mario X Position
        # 4 - Mario Y Position
      return (s[0]*3) + s[3]

    transitions = []
    probs = 1.0/len(self.actions(state))
    for option in self.actions(state):
      tempGame = game
      tempGame.progress(action=option)

      newGameInfo = tempGame.getGameInfo()
      if 'state' not in newGameInfo.keys(): continue
      print ("this is the new state {}".format(newGameInfo))
      newState = newGameInfo['state']
      if tempGame.isEnd():
        transitions.append((newState, probs, -1*float("inf")))
      else:
        transitions.append((newState, probs, calculateReward(newState)))
    return transitions

  def discount(self):
    return 0.1

