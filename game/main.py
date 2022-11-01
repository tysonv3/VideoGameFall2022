# content from kids can code: http://kidscancode.org/blog/

# import libraries and modules
# from platform import platform

from os import kill
import pygame as pg
from pygame.sprite import Sprite
import random

vec = pg.math.Vector2

# game settings 
WIDTH = 1280
HEIGHT = 720
FPS = 30

# player settings
PLAYER_GRAVITY = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# score
SCORE = 0

# defining draw_text allows us to display the score
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# sprites...
class Player(Sprite):
    def __init__(self):
        # defines player sprite parameters
        Sprite.__init__(self)
        self.image = pg.Surface((25, 25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    # what happens when a key gets pressed: horizontal movement
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -5
            # self.acc.y = 0
            # print(self.vel)
        if keys[pg.K_RIGHT]:
            self.acc.x = 5
            # self.acc.y = 0
        if keys[pg.K_UP]:
            self.acc.y = -5
            # self.acc.x = 0
        if keys[pg.K_DOWN]:
            self.acc.y = 5
            # self.acc.x = 0
    # should be vertical jump but doesnt work yet
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -40
    # updating all movement and acceleration and gravity
    def update(self):
        global SCORE
        self.acc = vec(0, PLAYER_GRAVITY)
        self.controls()
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        '''source: andrew. He helped me figure out that if the player were to hit any of the walls, the player would die.
        This was an issue for me because the top and left wall would make the player die, but the bottom and right wall
        would print died into the terminal until you stop touching it. This was solved with this.'''
        if hits:
            print("died")
            self.kill()
        hits = pg.sprite.spritecollide(self, enemies, True)
        if hits:
            SCORE += 1
        # friction
        self.acc.x += self.vel.x * -0.1
        self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.rect.midbottom = self.pos
    
# creates platform class
# platforms is sublass of sprite
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# this creates the enemy sprite class        
class Enemy(Sprite):
    def __init__(self, x, y, color, w, h,):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.w = w
        self.h = h
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = vec(self.x, self.y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        # self.movex = movex
        # self.movey = movey       
        self.coordinates = [x,y] 

# source: https://stackoverflow.com/questions/62963170/how-do-i-randomly-spawn-enemy-elsewhere-after-collision-in-pygame
'''It was intended to define the new coordinates when the enemy gets hit by the player and to respawn/move to a new place for the
player to eat. I thought that this part of the code would allow for that to happen.'''
# this defines the new coordinates for the enemy once it gets hit
def new_coordinate():
    return random.randint(0, 720-25)
# this draws the player rectangle and the enemy rectangle, and would do it every time the enemy gets hit by the player
def draw(player_rect, enemy_rect):
    if pg.sprite.spritecollide(enemy_rect):
        enemy_rect = pg.rect(new_coordinate(), new_coordinate(), 15, 15)
        enemy_rect = pg.draw.rect(screen, colors, enemy_rect)
    else:
        enemy_rect = pg.draw.rect(screen, colors, enemy_rect)

    player_rect = pg.draw.rect(screen, GREEN, player_rect)

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("walmart snake")
clock = pg.time.Clock()
  
# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
enemies = pg.sprite.Group()

# instantiate the player class
player = Player()
# this instantiates the left wall 
leftwall = Platform(0, 0, 1, 720)
# this instantiates the ground
ground = Platform(0, 719, 1280, 1)
# this instantiates the top wall
topwall = Platform(0, 0, 1280, 2)
# this instantiates the right wall
rightwall = Platform(1279, 0, 2, 720)

# this adds enemies and the amount of enemies we want
colors = [RED]
for i in range(1):
    x = random.randint(0, WIDTH)
    y = random.randint(15, HEIGHT - 40)
    movex = random.randint(-2, 2)
    movey = random.randint(-2, 2)
    color = random.choice(colors)
    e = Enemy(x, y, color, 15, 15)
    all_sprites.add(e)
    enemies.add(e)
    print(e)

# add player to all sprites group
all_sprites.add(player, leftwall, ground, topwall, rightwall)
all_platforms.add(leftwall, ground, topwall, rightwall)

# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    
    ############ Update ##############
    # update all sprites
    all_sprites.update()
    all_platforms.update()
    # I thought this would check if the enemies hit the player and when that was true, but wasn't really needed
    pg.sprite.spritecollide(player, enemies, True)

    ############ Draw ################
    # draw the background screen
    screen.fill(BLACK)
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    # draw all sprites
    all_sprites.draw(screen)

    pg.display.flip()

pg.quit()