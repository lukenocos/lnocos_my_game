# File created by Luke Nocos
# Agenda:
# GIT GITHUB
# Build file and folder structures
# Create Libraries

# Sources: http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/


'''
My Goal:

Create more platforms and make it so that the player can continue to move upwards
by jumping on platforms

Figure out how to create a boundaries 

Add score

Change the background 
'''
# import libs
import pygame as pg
import random
import os
# import settings 
from settings import *
from sprites import *
import random

# from pg.sprite import Sprite


# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
 
# create game class in order to pass properties to the sprites file 
class Game:
    def __init__(self):
        # init game window 
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # sets bg as the variable that loads the cloud background image
        bg = pg.image.load('CLOUD.jpg')
        global bg_image
        # transforms the image into the same scale of the width and height of the screen
        bg_image = pg.transform.scale(bg, (WIDTH, HEIGHT))
        pg.display.set_caption("my game")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # starting a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        # creates platforms
        self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        self.plat2 = Platform(200, 25, 150, 450, (150,150,150), "normal")
        self.plat3 = Platform(200, 25, 500, 250, (150,150,150), "normal")
        self.plat4 = Platform(200, 25, 150, 75, (150,150,150), "normal")
        self.plat5 = Platform(200, 25, 350, -150, (150,150,150), "normal")
        self.plat6 = Platform(200, 25, 500, -350, (150,150,150), "normal")
        self.plat7 = Platform(200, 25, 100, -550, (150,150,150), "normal")
        self.plat8 = Platform(200, 25, 400, -750, (150,150,150), "normal")
        self.plat9 = Platform(200, 25, 250, -950, (150,150,150), "normal")
        self.plat10 = Platform(200, 25, 450, -1150, (150,150,150), "normal")
        self.plat11 = Platform(200, 25, 770, -1350, (150,150,150), "normal")
        self.plat12 = Platform(200, 25, 340, -1550, (150,150,150), "normal")
        self.plat13 = Platform(200, 25, 150, -1350, (150,150,150), "dissapearing")

        # adds the image of the platform to the screen
        self.all_sprites.add(self.plat1)
        self.all_sprites.add(self.plat2)
        self.all_sprites.add(self.plat3)
        self.all_sprites.add(self.plat4)
        self.all_sprites.add(self.plat5)
        self.all_sprites.add(self.plat6)
        self.all_sprites.add(self.plat7)
        self.all_sprites.add(self.plat8)
        self.all_sprites.add(self.plat9)
        self.all_sprites.add(self.plat10)
        self.all_sprites.add(self.plat11)
        self.all_sprites.add(self.plat12)
        self.all_sprites.add(self.plat13)

        # add platforms onto the screen so that the player can land on it
        self.platforms.add(self.plat1)
        self.platforms.add(self.plat2)
        self.platforms.add(self.plat3)
        self.platforms.add(self.plat4)
        self.platforms.add(self.plat5)
        self.platforms.add(self.plat6)
        self.platforms.add(self.plat7)
        self.platforms.add(self.plat8)
        self.platforms.add(self.plat9)
        self.platforms.add(self.plat10)
        self.platforms.add(self.plat11)
        self.platforms.add(self.plat12)
        self.platforms.add(self.plat13)

        # add player to game
        self.all_sprites.add(self.player)
        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump() 
    
    def update(self):
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            # create a variation of types of platforms 
            if hits:
                if hits[0].variant == "dissapearing":
                    hits[0].kill()
                elif hits[0].variant == "icey":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                    PLAYER_FRICTION = 0
                elif hits[0].variant == "bouncey":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -PLAYER_JUMP
                else:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0

        # infinite scroller that continues upwards 
        '''
        if the player reaches a quarter of the height of the screen, 
        the players y-position increases by its vertical velocity, moving the player
        up the screen. All platforms undergo the same movement in order to move the platforms 
        upwards on the screen. If a platform reaches the bottom of the screen, it is removed
        and the score is increased.
        
        '''
        if self.player.rect.top <= HEIGHT / 4:
            # abs is absolute value of the variable
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    # as the scroller moves vertically, the score increases by 10 
                    self.score += 10
                    print(self.score)

                    
        # resets player when it falls
        '''
        if player reaches the bottom of the screen, 
        the player is respawned at the starting position and the player is killed

        checks if the player is falling off the bottom of the screen and moves 
        all sprites upwards, creating a falling effect

        '''
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        # len returns the length of an object
        # returns object to start 
        if len(self.platforms) == 0:
            self.playing = False
        
    def draw(self):
        # blits the cloud image in the background 
        self.screen.blit(bg_image, (0,0))
        # displays the score of the game at the top left corner using self.score
        self.draw_text("Score: " + str(self.score), 30, BLACK, 0, 0)
        self.all_sprites.draw(self.screen)
        # is a method because it is now inside the class and needs self 
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        # text_rect.midstop = (x,y)
        self.screen.blit(text_surface, text_rect)
    
    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)
    
    

# instantiate the game class
g = Game()

# start the game loop
while g.running:
    g.new()    

pg.quit()