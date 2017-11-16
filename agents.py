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


keybinding = {
  'action':pg.K_s,
  'jump':pg.K_a,
  'left':pg.K_LEFT,
  'right':pg.K_RIGHT,
  'down':pg.K_DOWN
}


class SimpleAgent(Agent):
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    print(keybinding['right'], len(state))
    return 'right'
