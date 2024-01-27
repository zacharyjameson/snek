import pygame
from snake import *
from food import Food

pygame.init()
bounds = (300, 300)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake")
block_size = 20

snake = Snake(block_size, bounds)
food = Food(block_size, bounds)

clock = pygame.time.Clock()

is_running = True
while is_running:
    pygame.time.delay(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake.steer(Direction.LEFT)
    elif keys[pygame.K_RIGHT]:
        snake.steer(Direction.RIGHT)
    elif keys[pygame.K_UP]:
        snake.steer(Direction.UP)
    elif keys[pygame.K_DOWN]:
        snake.steer(Direction.DOWN)

    snake.move()
    window.fill((0, 0, 0))
    snake.draw(pygame, window)
    food.draw(pygame, window)
    pygame.display.flip()
    clock.tick(10)
