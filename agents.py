import util
import pygame as pg

class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:

  def registerInitialState(self, state): # inspects the starting state
  """
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    raiseNotDefined()

class SimpleAgent(Agent):
  def __init__(self, index=0):
    self.index = index
    self.isEnd = False

  def getAction(self, state):

    if self.isEnd:
      print("GAME OVER")

    print(keybinding['right'], len(state))
    return 'right'

keybinding = {
  'action':pg.K_s,
  'jump':pg.K_a,
  'left':pg.K_LEFT,
  'right':pg.K_RIGHT,
  'down':pg.K_DOWN
}


class MarioMDP(util.MDP):
  # Return the start state.
    def startState(self):
      return

    # Return set of actions possible from |state|.
    def actions(self, state): raise NotImplementedError("Override me")

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    # Mapping to notation from class:
    #   state = s, action = a, newState = s', prob = T(s, a, s'), reward = Reward(s, a, s')
    # If IsEnd(state), return the empty list.
    def succAndProbReward(self, state, action): raise NotImplementedError("Override me")

    def discount(self): raise NotImplementedError("Override me")

