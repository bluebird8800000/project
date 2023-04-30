#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
#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

import pygame
from pgzero.actor import Actor
import random

pygame.init()

screen = pygame.display.set_mode([640, 640])

WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE*BLOCK_SIZE
HEIGHT = WORLD_SIZE*BLOCK_SIZE

world = []
pacman = pygame.image.load('images/pacman.png')
pacman_p = [1, 1]
ghosts = []

char_to_image = {
    '.': 'images/dot.png',
    '=': 'images/wall.png',
    '*': 'images/power.png',
    'g': 'ghost1.png',
}


with open('level-1.txt', 'w') as f:
    f.write('====================\n'
            '=..................=\n'
            '=====...==.........=\n'
            '=....===......======\n'
            '=...g..............=\n'
            '=.......=====......=\n'
            '=...==........==...=\n'
            '=.......=====......=\n'
            '=..................=\n'
            '====================\n')

def load_level(number):
    file = "level-%s.txt" % number
    with open(file) as f:
        for line in f:
            row = []
            for block in line:
                row.append(block)
            world.append(row)

def draw():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                img = pygame.image.load(char_to_image[block])
                screen.blit(img, (x*BLOCK_SIZE, y*BLOCK_SIZE))
    screen.blit(pacman, (pacman_p[0]*BLOCK_SIZE, pacman_p[1]*BLOCK_SIZE))

def on_key_down(key):
    if key[pygame.K_DOWN]:
        if world[pacman_p[1]+1][pacman_p[0]] != '=':
            pacman_p[1] += 1
    elif key[pygame.K_UP]:
        if world[pacman_p[1] - 1][pacman_p[0]] != '=':
            pacman_p[1] -= 1
    elif key[pygame.K_RIGHT]:
        if world[pacman_p[1]][pacman_p[0]+1] != '=':
            pacman_p[0] += 1
    elif key[pygame.K_LEFT]:
        if world[pacman_p[1]][pacman_p[0]-1] != '=':
            pacman_p[0] -= 1

def make_ghost_actors():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            if block == 'g':
                g = Actor(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE), anchor=('left', 'top')
                world[y][x] = None
                for g in ghosts: g.draw()


load_level(1)
make_ghost_actors()
for row in world: print(row)


running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    keys = pygame.key.get_pressed()
    on_key_down(keys)

    screen.fill((0,0,0))
    draw()

    pygame.display.flip()

pygame.quit()

