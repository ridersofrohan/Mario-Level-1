#!/usr/bin/env python
__author__ = 'justinarmstrong'

"""
This is an attempt to recreate the first level of
Super Mario Bros for the NES.
"""

import sys
import pygame as pg
from data.main import main
import cProfile

from agents import SimpleAgent


if __name__=='__main__':
    # CHANGE - Added an optional agent parameter
    for i in range(0, 10):
      agent = SimpleAgent()
      main(agent=agent)
      print("HEREHRHEHREHRH")
    # pg.quit()
    # sys.exit()
