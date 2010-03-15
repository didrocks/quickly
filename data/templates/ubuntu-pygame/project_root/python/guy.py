
"""
guy module - contains the Guy class which represents the sprite
controlled by the player. Managers bullets in addition to 
BaseSprite functionality.

"""

import pygame, random
from base_sprite import BaseSprite
from bullet import Bullet
import project_name_config

class Guy(BaseSprite):
    """
    Guy - The sprite controlled by the player. managers 

    """

    def __init__(self, bullets_group):
        """
        Creates a Guy

        arguments:

        bullets_group - A pygame.SpriteGroup managed by the games
        collision detection system.

        """

        BaseSprite.__init__(self, project_name_config.guy_img)
        self.bullets = bullets_group
        self.hum = pygame.mixer.Sound(project_name_config.guy_eng)
        self.explosionSound = pygame.mixer.Sound(project_name_config.guy_explode)
        self.alive = True
        self.exploding = False
        self.explodestage = 0
        self.visible = True
        self.max_bullets = 4
        self.bigbullets = False
 
    def init_position(self):
        """init_position - resets the Guy's position on screen
        Will reset the Sprite's image to the starting image.
        
        """

        sw = project_name_config.screen_width
        sh = project_name_config.screen_height

        #start off in the center of screen, still, facing up
        self.stop()
        self.x = sw/2
        self.y = sh/2
        self.master_image = pygame.image.load(project_name_config.guy_img)
        self._update_image()
        self.visible = True
        self.alive = True
  
    def accelerate(self):
        """
        accelerate - increase the sprites speed along it's current
        trajectory and plays the sound for the sprite's "moto".

        """

        #only accelerate if the Guy is alive
        if self.alive and not self.exploding:
            BaseSprite.accelerate(self)
            self.hum.play(-1)#loop sound endlessly
  
    def stop_acceleration(self):
        """
        stop_acceleration - tells the sprite to stop accelerating.
        Depending on the game physics that may or my not cause
        the sprite to accually stop.
 
        """

        BaseSprite.stop_acceleration(self)
        self.hum.stop()
 
    def explode(self):
        """explode - starts the Guy's animated exploding sequence.
        Sets the alive to False so the the exploding sprite does
        not collide with sprits in future ticks. The sprite will 
        be removed from the screen after the exploding sequence is 
        complete. To remove the sprite immediately, call kill().

        """

        self.stop()
        if self.alive:
            self.hum.stop()
            self.explosionSound.play()
            self.alive = False
            self.exploding = True
   
    def shoot(self):
        """shoot - fire a bullet. Adds the bullet to the bullet sprite group.
        If the maximum number of bullets premitted would be exceeded, 
        the bullet will not fire. If the guy is exploding, the guy will no
        fire.

        """

        if self.alive:
            #only allow max numbe of  bullets on the screen at a time
            if len(self.bullets.sprites()) < self.max_bullets:
                imgName = project_name_config.guy_bullet
                b = Bullet(self.x,self.y,self.orientation, imgName)
                self.bullets.add(b)

    def hyperspace(self):
        """
        hyperspace - causes the Guy to disappear and reappear in a 
        random screen location. The Guy will stop. The Guy will
        randomly explode 20% of the time that this funciton is used.
 
        """

        self.stop()
        self.x = random.randint(0,project_name_config.screen_width)
        self.y = random.randint(0,project_name_config.screen_height)
        #every now and then, blow up on hyperspace for no reason
        if random.randint(0,5) == 2:
            self.explode()
   
    def stop(self):
        """
        stop - stops all velocity and totation, and sets the Sprite's
        orientation to 0

        """

        self.orientation = 0
        self._rotating_right = False
        self._rotating_left = False
        self.velocity_x = 0
        self.velocity_y = 0
        self._accelerating = False
  
    def update(self):
        """update - Update internal data for a game tick""" 
    
        BaseSprite.update(self)

        #this stops the guy completely
        #for frictionless physics like in a space game
        #you can decrement the velocity or even
        #delete these lines for asteroids-like physics
        if not self._accelerating:
            self.velocity_x = 0
            self.velocity_y = 0
  
        #manage the exploding animation
        if self.exploding: 
            #do an explosion image for each tick
            self.explodestage += 1
            e = self.explodestage
            if e < 8:#there are 7 explosion images
                e = str(e)
                img_name = project_name_config.guy_explode_stage + e  + ".png"
                self.master_image = pygame.image.load(img_name)
                self._update_image()

            else:#explosion is done
                self.visible = False
                self.exploding = False