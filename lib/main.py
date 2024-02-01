import pygame
from pygame.locals import KEYDOWN, K_RETURN
from snake import *
from food import Food

from api import get_database

pygame.init()
bounds = (600, 600)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake")
block_size = 20

snake = Snake(block_size, bounds)
food = Food(block_size, bounds)

font = pygame.font.SysFont('pixelmix', 30, True)

clock = pygame.time.Clock()

db = get_database()
high_scores = db['High Scores']

documents = list(high_scores.find())

if not documents:
    print("high scores collection is empty")
else:
    for document in documents:
        print(document)


def start_screen():
    start_text = font.render('Press ENTER to Start', True, (255, 255, 255))
    start_text_width, start_text_height = start_text.get_size()
    start_text_x = (bounds[0] - start_text_width) // 2
    start_text_y = (bounds[1] - start_text_height) // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return

        window.fill((0, 0, 0))
        window.blit(start_text, (start_text_x, start_text_y))
        pygame.display.flip()
        clock.tick(15)


start_screen()


def display_game_over():
    text = font.render('Game Over', True, (255, 255, 255))
    text_width, text_height = text.get_size()
    x = (bounds[0] - text_width) // 2
    y = (bounds[1] - text_height) // 2
    window.blit(text, (x, y))
    pygame.display.update()

    # Display "Press Enter to Respawn" message
    respawn_text = font.render(
        'Press ENTER to Continue', True, (255, 255, 255))
    respawn_width, respawn_height = respawn_text.get_size()
    respawn_x = (bounds[0] - respawn_width) // 2
    respawn_y = y + text_height + 20
    blink_timer = 0
    blink_frequency = 500
    visible = True

    # Blink effect
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return

        if pygame.time.get_ticks() - blink_timer > blink_frequency:
            visible = not visible
            blink_timer = pygame.time.get_ticks()

        window.fill((0, 0, 0))
        window.blit(text, (x, y))
        if visible:
            window.blit(respawn_text, (respawn_x, respawn_y))

        pygame.display.flip()
        clock.tick(15)


is_running = True
while is_running:
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
    snake.check_for_food(food)

    # Check for game over
    if snake.check_bounds() == True or snake.check_tail_collision() == True:
        display_game_over()
        snake.respawn()
        food.respawn()

    window.fill((0, 0, 0))
    counter_text = font.render(
        f'{snake.food_eaten}', True, (255, 255, 255))
    counter_text_width, counter_text_height = counter_text.get_size()
    counter_text_x = bounds[0] - counter_text_width - 10
    counter_text_y = 10
    window.blit(counter_text, (counter_text_x, counter_text_y))

    snake.draw(pygame, window)
    food.draw(pygame, window)
    pygame.display.flip()

    clock.tick(15)
