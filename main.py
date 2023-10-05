import pygame
import random

pygame.init()

BLACK = (0,0,0)
GREY = (128,128,128)
YELLOW = (255,255,0)

width,height =800,800
tile_size = 20
grid_width = width // tile_size
grid_height = height // tile_size
FPS = 60

screen = pygame.display.set_mode((width,height))

clock = pygame.time.Clock()

def gen(num):
    return set([(random.randrange(0,grid_height), random.randrange(0,grid_width)) for _ in range(num)])

def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * tile_size, row * tile_size)
        pygame.draw.rect(screen, YELLOW, (*top_left, tile_size, tile_size))

    for row in range(grid_height):
        pygame.draw.line(screen,BLACK,(0,row * tile_size), (width, row*tile_size))
    for col in range(grid_width):
        pygame.draw.line(screen,BLACK,(col * tile_size,0), (col*tile_size, height))


def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2,3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions



def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x+dx<0 or x+dx>grid_width:
            continue
        for dy in [-1, 0, 1]:
            if y+dy<0 or y+dy>grid_height:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x+dx, y+dy))

    return neighbors


def main():
    running = True
    playing = False
    count = 0
    update_freq = 120
    
    positions=set()
    

    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // tile_size
                row = y // tile_size
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count= 0 

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4,10)* grid_width)


        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
