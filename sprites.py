import pygame as pg

from pygame.sprite import Sprite

from settings import *

from random import randint

vec = pg.math.Vector2

# player class
class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # these are the properties (think of a mold for an object in production)
        self.game = game
        self.image = pg.Surface((50,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/1.2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
    def input(self):

        # reset variables
        dx = 0
        dy = 0
       
        # method that allows the object to move based off user input
        keystate = pg.key.get_pressed()
        
        if keystate[pg.K_a]:
            dx = -PLAYER_ACC
            self.acc.x = -PLAYER_ACC
       
        if keystate[pg.K_d]:
            dy = -PLAYER_ACC
            self.acc.x = PLAYER_ACC

        # keeps it inbounds

        if self.rect.left + self.acc.x < 0:
            self.acc.x = -self.rect.left
        if self.rect.right + self.acc.x > WIDTH:
            self.acc.x = WIDTH - self.rect.right
       
    # allows the player to jump 
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
    def inbounds(self):
        if self.rect.x > WIDTH - 50:
            self.pos.x = WIDTH - 25
            self.vel.x = 0
            print("i am off the right side of the screen...")
        if self.rect.x < 0:
            self.pos.x = 25
            self.vel.x = 0
            print("i am off the left side of the screen...")
        if self.rect.y > HEIGHT:
            self.pos.y = HEIGHT - 25
            self.vel.y = 0
            print("i am off the bottom of the screen")
        if self.rect.y < 0:
            self.pos.y = 25
            self.vel.y = 0
            print("i am off the top of the screen...")
        
    def mob_collide(self):
        hits = pg.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            print("you collided with an enemy ")
            self.game.score += 1
            print(SCORE)

    def update(self):
        # means do this over and over and over again
        self.acc = vec(0, PLAYER_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        self.rect.y += SCROLL

class Mob(Sprite):
    def __init__(self,width,height, color):
        Sprite.__init__(self)
        # self.width = width
        # self.height = height
        # self.image = pg.Surface((self.width,self.height))
        # self.color = color
        # self.image.fill(self.color)
        # # self.rect = self.image.get_rect()
        # # self.rect.center = (WIDTH/2, HEIGHT/2)
        # self.pos = vec(WIDTH/2, HEIGHT/2)
        # self.vel = vec(randint(1,5),randint(1,5))
        # self.acc = vec(1,1)
        # self.cofric = 0.01
    # ...
    def inbounds(self):
        if self.rect.x > WIDTH:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.x < 0:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y < 0:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y > HEIGHT:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric

        
    def update(self):
        self.inbounds()
        # self.pos.x += self.vel.x
        # self.pos.y += self.vel.y
        self.pos += self.vel
        self.rect.center = self.pos

# acts as a mold for platforms 
class Platform(Sprite):
    def __init__(self, width, height, x, y, color, variant):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.variant = variant




        
