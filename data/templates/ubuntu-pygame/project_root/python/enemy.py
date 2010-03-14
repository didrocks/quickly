"""
enemy module - contains the enemy class, an extenstion of BaseSprite.


"""

import pygame
from base_sprite import BaseSprite
import project_name_config

class Enemy(BaseSprite):
    """
    Enemy - A very simple enemy that does not move, shoot, turn, etc...
    Basically, a rock that sits there and waits to get collided with
    and killed. This class is not intended to be used as is, but rather
    provides a sample implementation or a base class for a real game.
    
    """

    def __init__(self):
        """Creates an Enemy """

        BaseSprite.__init__(self, project_name_config.enemy_image)
        self.points = 1
        self.accelerationDivisor = 1  
        self.orientation = 0
        self.rotatingRight = False
        self.rotatingLeft = False
        self.rotationRate = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.init_position()
