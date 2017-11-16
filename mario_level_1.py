#!/usr/bin/env python
__author__ = 'justinarmstrong'

"""
This is an attempt to recreate the first level of
Super Mario Bros for the NES.
"""

import sys
import pygame as pg
from data.main import MarioLevel
import cProfile

from agents import SimpleAgent


if __name__=='__main__':
    game = MarioLevel()
    game.run()
    pg.quit()
    sys.exit()
