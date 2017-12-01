from . import setup,tools
from .states import main_menu,load_screen,level1
from . import constants as c

# CHANGE - Added an optional agent parameter
class MarioLevel():
  def __init__(self, agent=None):
    """Add states to control here."""
    self.run_it = tools.Control(setup.ORIGINAL_CAPTION)
    self.state_dict = {c.MAIN_MENU: main_menu.Menu(),
                  c.LOAD_SCREEN: load_screen.LoadScreen(),
                  c.TIME_OUT: load_screen.TimeOut(),
                  c.GAME_OVER: load_screen.GameOver(),
                  c.LEVEL1: level1.Level1(agent=agent)}

    self.run_it.setup_states(self.state_dict, c.MAIN_MENU)

  def run(self):
    self.run_it.main()

  def progress(self, action=None):
    self.run_it.progress(action=action)

  def getGameInfo(self):
    return self.run_it.state.game_info

  def isEnd(self):
    return self.run_it.done

  def getMario(self):
    return self.run_it.state.mario






