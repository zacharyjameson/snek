# game.py
import pygame
from pygame.locals import KEYDOWN, K_RETURN
from snake import Snake, Direction
from food import Food
from api import get_database


class Game:
    def __init__(self):
        self.bounds = (600, 600)
        self.window = pygame.display.set_mode(self.bounds)
        self.clock = pygame.time.Clock()
        self.clock_tick_rate = 10
        self.snake = Snake(20, self.bounds)
        self.food = Food(20, self.bounds)
        self.db = get_database()
        self.high_scores = self.db['High Scores']
        scores_doc = self.high_scores.find_one({"_id": "SCORES"})
        if scores_doc is None:
            self.high_score_list = []
        else:
            self.high_score_list = scores_doc['scores']
        self.new_score = {"NEW_PLAYER": 0}
        self.font = pygame.font.SysFont('pixelmix', 30, True)
        self.start_screen()

    def start_screen(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        running = False

            self.window.fill((0, 0, 0))
            start_text = self.font.render(
                'Welcome to Snake!', True, (255, 255, 255))
            self.window.blit(
                start_text, (self.bounds[0] // 2 - 100, self.bounds[1] // 2 - 50))
            press_return_text = self.font.render(
                'Press Enter to start', True, (255, 255, 255))
            self.window.blit(press_return_text,
                             (self.bounds[0] // 2 - 100, self.bounds[1] // 2))
            pygame.display.flip()

        self.run()

    def increment_speed(self):
        self.clock_tick_rate += .25

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.snake.steer(Direction.LEFT)
            elif keys[pygame.K_RIGHT]:
                self.snake.steer(Direction.RIGHT)
            elif keys[pygame.K_UP]:
                self.snake.steer(Direction.UP)
            elif keys[pygame.K_DOWN]:
                self.snake.steer(Direction.DOWN)

            self.snake.move()
            if self.snake.check_for_food(self.food):
                self.food.respawn()
                self.increment_speed()

            if self.snake.check_bounds() or self.snake.check_tail_collision():
                self.new_score = {"NEW_PLAYER": self.snake.food_eaten}
                self.game_over()

            self.window.fill((0, 0, 0))
            self.snake.draw(pygame, self.window)
            self.food.draw(pygame, self.window)
            score_text = self.font.render(
                f'Score: {self.snake.food_eaten}', True, (255, 255, 255))
            self.window.blit(score_text, (10, 10))
            pygame.display.flip()

            self.clock.tick(self.clock_tick_rate)
        pygame.quit()

    def game_over(self):
        self.window.fill((0, 0, 0))
        game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
        self.window.blit(
            game_over_text, (self.bounds[0] // 2 - 100, self.bounds[1] // 2 - 175))
        score_text = self.font.render(
            f'Final Score: {self.snake.food_eaten}', True, (255, 255, 255))
        self.window.blit(
            score_text, (self.bounds[0] // 2 - 100, self.bounds[1] // 2 - 150))
        press_return_text = self.font.render(
            'Press ENTER to play again', True, (255, 255, 255))
        press_return_text_rect = press_return_text.get_rect(
            center=(self.bounds[0] // 2, self.bounds[1] // 2 - 100))
        self.window.blit(press_return_text, press_return_text_rect)
        self.check_for_high_score()
        self.display_top_ten()
        pygame.display.flip()
        waiting = True
        clock = pygame.time.Clock()
        flash = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        waiting = False
                        self.snake.respawn()
                        self.food.respawn()
                        self.clock_tick_rate = 10
                        self.snake.food_eaten = 0
                        self.run()
            if flash:
                self.window.blit(press_return_text, press_return_text_rect)
            else:
                self.window.blit(self.font.render(
                    'Press ENTER to play again', True, (0, 0, 0)), press_return_text_rect)
            flash = not flash
            pygame.display.flip()
            clock.tick(2)
        pygame.quit()

    def save_high_score(self):
        self.high_scores.update_one(
            {"_id": "SCORES"}, {"$set": {"scores": self.high_score_list}})

    def check_for_high_score(self):
        for old_score in self.high_score_list:
            if self.snake.food_eaten > list(old_score.values())[0]:
                print("New high score! You beat: ",
                      list(old_score.values())[0])
                player_name = self.get_player_name()
                print(player_name)
                if not player_name:
                    print("no player name found")
                    player_name = "NONE"
                self.new_score = {player_name: self.snake.food_eaten}
                self.high_score_list.append(self.new_score)
                self.high_score_list = sorted(
                    self.high_score_list, key=lambda x: list(x.values())[0], reverse=True)[:10]
                print("Check for high score high score list",
                      self.high_score_list)
                self.save_high_score()
                break
            else:
                print(list(old_score.values())[
                      0], "is not a high score. Try again!")

    def display_top_ten(self):
        y = self.bounds[1] // 2 - 50
        for i, score in enumerate(self.high_score_list):
            high_score_text = self.font.render(
                f'{i+1}. {list(score.keys())[0]}: {list(score.values())[0]}', True, (255, 255, 255))
            self.window.blit(high_score_text, (self.bounds[0] // 2 - 100, y))
            y += 30

    def get_player_name(self):
        name = ""
        active = True
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 4 and event.unicode.isalnum():
                        name += event.unicode.upper()

            self.window.fill((0, 0, 0))
            prompt_text = self.font.render(
                'Player Name: ', True, (255, 255, 255))
            name_text = self.font.render(name, True, (255, 255, 255))
            self.window.blit(
                prompt_text, (self.bounds[0] // 2 - 150, self.bounds[1] // 2 - 50))
            self.window.blit(
                name_text, (self.bounds[0] // 2 - 50, self.bounds[1] // 2))
            pygame.display.flip()

        return name
