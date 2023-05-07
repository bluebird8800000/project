# 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

import pygame
from pgzero.actor import Actor
import random

pygame.init()

screen = pygame.display.set_mode([640, 640])

WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE*BLOCK_SIZE
HEIGHT = WORLD_SIZE*BLOCK_SIZE

SPEED = 2
GHOST_SPEED = 1

world = []
pacman = pygame.image.load('images/pacman.png')
pacman_p = [1, 1]
ghosts = []

char_to_image = {
    '.': 'images/dot.png',
    '=': 'images/wall.png',
    '*': 'images/power.png',
    'g': 'images/ghost1.png',
}


with open('level-1.txt', 'w') as f:
    f.write('====================\n'
            '=..................=\n'
            '=====...==.........=\n'
            '=..................=\n'
            '=....===......======\n'
            '===................=\n'
            '=.......=====......=\n'
            '=...==........==...=\n'
            '=.......=====......=\n'
            '=...g..............=\n'
            '====================\n')


def load_level(number):
    file = "level-%s.txt" % number
    # food_left = 0
    with open(file) as f:
        for line in f:
            row = []
            for block in line:
                row.append(block)
                # if block == '.':
                #     food_left += 1
            world.append(row)


def draw():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                img = pygame.image.load(char_to_image[block])
                screen.blit(img, (x*BLOCK_SIZE, y*BLOCK_SIZE))
    screen.blit(pacman, (pacman_p[0]*BLOCK_SIZE, pacman_p[1]*BLOCK_SIZE))
    for g in ghosts:
        screen.blit(g._orig_surf, g.pos)


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


# def eat_food(key):
#     if key[pygame.K_DOWN]:
#         if world[pacman_p[1]+1][pacman_p[0]] == '.':
#             food_left += 1
#     elif key[pygame.K_UP]:
#         if world[pacman_p[1] - 1][pacman_p[0]] == '.':
#             pacman_p[1] -= 1
#     elif key[pygame.K_RIGHT]:
#         if world[pacman_p[1]][pacman_p[0]+1] == '.':
#             pacman_p[0] += 1
#     elif key[pygame.K_LEFT]:
#         if world[pacman_p[1]][pacman_p[0]-1] == '.':
#             pacman_p[0] -= 1


load_level(1)
for row in world:
    print(row)


def make_ghost_actors():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            if block == 'g':
                g = Actor(char_to_image[block].replace('images/', ''), (x*BLOCK_SIZE, y*BLOCK_SIZE), anchor=('left', 'top'))
                g.dx = random.choice([-GHOST_SPEED, GHOST_SPEED])
                g.dy = random.choice([-GHOST_SPEED, GHOST_SPEED])
                world[y][x] = None
                screen.blit(g._orig_surf, g.pos)
                ghosts.append(g)


def blocks_ahead_of(sprite, dx, dy):
    x = sprite.x + dx
    y = sprite.y + dy

    ix, iy = int(x//BLOCK_SIZE), int(y//BLOCK_SIZE)
    rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE

    blocks = [world[iy][ix]]
    if rx:
        blocks.append(world[iy][ix+1])
    if ry:
        blocks.append(world[iy+1][ix])
    if rx and ry:
        blocks.append(world[iy+1][ix+1])

    return blocks


def set_random_dir(sprite, speed):
    sprite.dx = random.choice([-speed, speed])
    sprite.dy = random.choice([-speed, speed])


def update():
    for g in ghosts:
        if '=' not in blocks_ahead_of(g, g.dx, 0):
            g.x += g.dx
        if '=' not in blocks_ahead_of(g, 0, g.dy):
            g.y += g.dy
        if not move_ahead(g):
            set_random_dir(g, GHOST_SPEED)


def move_ahead(sprite):
    # Record current pos, so we can see if the sprite moved
    oldx, oldy = sprite.x, sprite.y
    if '=' not in blocks_ahead_of(sprite, sprite.dx, 0):
        sprite.x += sprite.dx
    if '=' not in blocks_ahead_of(sprite, 0, sprite.dy):
        sprite.y += sprite.dy
    # Return whether we moved
    return oldx != sprite.x or oldy != sprite.y


running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    keys = pygame.key.get_pressed()
    on_key_down(keys)

    screen.fill((0, 0, 0))

    make_ghost_actors()
    draw()
    update()

    pygame.display.flip()


pygame.quit()
