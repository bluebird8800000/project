# 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

# rotate pacman
# powerups
# restart game when player presses space

import pygame
from pgzero.actor import Actor
from pgzero.rect import Rect
import random
from pygame.locals import *

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

pacman_right = pygame.image.load('images/pacman.png')
pacman_left = pygame.image.load('images/pacman (left).png')
pacman_up = pygame.image.load('images/pacman (up).png')
pacman_down = pygame.image.load('images/pacman (down).png')
# pacman = [pacman_right, pacman_left, pacman_up, pacman_down]

pacman_p = [1, 1]
ghosts = []
ghost_start_pos = []
foodleft = 0
lives = 3

clock = pygame.time.Clock()
clock.tick(5)

char_to_image = {
    '.': 'images/dot.png',
    '=': 'images/wall.png',
    '*': 'images/power.png',
    'g': 'images/ghost1.png',
}


with open('level-1.txt', 'w') as f:
    f.write('====================\n'
            '= .................=\n'
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
    global foodleft
    foodleft = 130
    with open(file) as f:
        for line in f:
            row = []
            for block in line:
                row.append(block)
            world.append(row)


def draw(key):
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
    global pacman
    if key[pygame.K_DOWN]:
        # screen.blit(pacman_down, (pacman_p[0] * BLOCK_SIZE, pacman_p[1] * BLOCK_SIZE))
        pacman = pacman_down
        if world[pacman_p[1]+1][pacman_p[0]] != '=':
            pacman_p[1] += 1
            # p_d = 0
    elif key[pygame.K_UP]:
        # screen.blit(pacman_up, (pacman_p[0] * BLOCK_SIZE, pacman_p[1] * BLOCK_SIZE))
        pacman = pacman_up
        if world[pacman_p[1] - 1][pacman_p[0]] != '=':
            pacman_p[1] -= 1
    elif key[pygame.K_RIGHT]:
        # screen.blit(pacman_right, (pacman_p[0] * BLOCK_SIZE, pacman_p[1] * BLOCK_SIZE))
        pacman = pacman_right
        if world[pacman_p[1]][pacman_p[0]+1] != '=':
            pacman_p[0] += 1
    elif key[pygame.K_LEFT]:
        # screen.blit(pacman_left, (pacman_p[0] * BLOCK_SIZE, pacman_p[1] * BLOCK_SIZE))
        pacman = pacman_left
        if world[pacman_p[1]][pacman_p[0]-1] != '=':
            pacman_p[0] -= 1


def eat_food(key):
    global foodleft
    if key[pygame.K_DOWN]:
        if world[pacman_p[1]][pacman_p[0]] == '.':
            world[pacman_p[1]][pacman_p[0]] = None
            foodleft -= 1
    elif key[pygame.K_UP]:
        if world[pacman_p[1]][pacman_p[0]] == '.':
            world[pacman_p[1]][pacman_p[0]] = None
            foodleft -= 1
    elif key[pygame.K_RIGHT]:
        if world[pacman_p[1]][pacman_p[0]] == '.':
            world[pacman_p[1]][pacman_p[0]] = None
            foodleft -= 1
    elif key[pygame.K_LEFT]:
        if world[pacman_p[1]][pacman_p[0]] == '.':
            world[pacman_p[1]][pacman_p[0]] = None
            foodleft -= 1
    print("Food Left:", foodleft)
    if foodleft == 0:
        draw_text("CONGRATULATIONS!", text_font, (170, 255, 0), 20, 400)


text_font = pygame.font.SysFont(None, 50)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


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
                ghost_start_pos.append((x, y))


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
        t = Rect((pacman_p[0])*BLOCK_SIZE, (pacman_p[0]+1)*BLOCK_SIZE, (pacman_p[1])*BLOCK_SIZE, (pacman_p[1]+1)*BLOCK_SIZE)
        t_g = Rect(g.x, g.x+32, g.y, g.y+32)
        t.size = (32, 32)
        t_g.size = (32, 32)
        t.top = (pacman_p[1])*BLOCK_SIZE
        t_g.top = g.y
        if t.colliderect(t_g):
            global lives
            lives -= 1
            reset_sprites()


def reset_sprites():
    pacman_p[1] = 1
    pacman_p[0] = 1
    for g, (x, y) in zip(ghosts, ghost_start_pos):
        g.x = x*BLOCK_SIZE
        g.y = y*BLOCK_SIZE


def move_ahead(sprite):
    oldx, oldy = sprite.x, sprite.y
    if '=' not in blocks_ahead_of(sprite, sprite.dx, 0):
        sprite.x += sprite.dx
    if '=' not in blocks_ahead_of(sprite, 0, sprite.dy):
        sprite.y += sprite.dy
    return oldx != sprite.x or oldy != sprite.y


def game_over_screen():
    if lives == 0:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 100)
        title = font.render('GAME OVER', True, (255, 0, 0))
        screen.blit(title, (100, 250))
        pygame.display.update()


running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    keys = pygame.key.get_pressed()
    on_key_down(keys)

    screen.fill((0, 0, 0))
    draw_text("FOOD LEFT: " + str(foodleft), text_font, (255, 255, 255), 20, 500)
    draw_text("LIVES: " + str(lives), text_font, (255, 255, 255), 20, 450)

    make_ghost_actors()
    draw(keys)
    game_over_screen()
    update()

    eat_food(keys)

    pygame.display.flip()

pygame.quit()
