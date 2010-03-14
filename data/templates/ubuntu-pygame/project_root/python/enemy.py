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
        self.explosion_sound = pygame.mixer.Sound(project_name_config.enemy_explode_sound)
        self.explode_stage = 0
        self.exploding = False
        self.init_position()
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        BaseSprite.update(self)
        if self.exploding: 
            #do an explosion image for each tick
            self.explode_stage += 1
            e = self.explode_stage
            if e < 8:
                e = str(e)
                img_name = project_name_config.enemy_explode_stage + e  + ".png"
                self.master_image = pygame.image.load(img_name)
                self._update_image()
                return

            else:#explosion is done
                self.visible = False
                self.exploding = False
                self.kill()
                return


    def explode(self):
        """explode - called when enemy is destroyed in
        game play. Sets the alive flag to False, and sets a flag to
        start animating an explosion in the update function. Also
        plays the explosion sound.

        """

        if self.alive:
            self.explosion_sound.play()
            self.alive = False
            self.exploding = True

