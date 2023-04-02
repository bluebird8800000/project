import pygame
pygame.init()

screen = pygame.display.set_mode([640, 640])

WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE*BLOCK_SIZE
HEIGHT = WORLD_SIZE*BLOCK_SIZE

world = []
pacman = pygame.image.load('images/pacman.png')

char_to_image = {
    '.': 'images/dot.png',
    '=': 'images/wall.png',
    '*': 'images/power.png',
}



with open('level-1.txt', 'w') as f:
    f.write('====================\n'
            '=................*.=\n'
            '==========.........=\n'
            '=....===......======\n'
            '=..................=\n'
            '=.......=====......=\n'
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
    # pacman = pygame.image.load('images/pacman.png')
    screen.blit(pacman, (1*BLOCK_SIZE, 1*BLOCK_SIZE))

def on_key_down(key):
    if key[pygame.K_DOWN]:
        # pacman.y += BLOCK_SIZE
        screen.blit(pacman, (1 * BLOCK_SIZE, (1+1) * BLOCK_SIZE))
load_level(1)
draw()
pygame.display.flip()
for row in world: print(row)



running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    keys = pygame.key.get_pressed()
    on_key_down(keys)
    pygame.display.flip()

pygame.quit()

