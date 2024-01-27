import pygame
from snake import *

pygame.init()
bounds = (300, 300)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake")
block_size = 20
snake = Snake(block_size, bounds)
clock = pygame.time.Clock()

is_running = True
while is_running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window.fill((0, 0, 0))
    snake.draw(pygame, window)
    pygame.display.flip()
    clock.tick(10)
