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
        y = self.bounds[1] // 2 - 50
        for i, score in enumerate(self.high_score_list):
            high_score_text = self.font.render(
                f'{i+1}. {list(score.keys())[0]}: {list(score.values())[0]}', True, (255, 255, 255))
            self.window.blit(high_score_text, (self.bounds[0] // 2 - 100, y))
            y += 30
        pygame.display.flip()
        self.save_high_score()
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
        scores_doc = self.high_scores.find_one({"_id": "SCORES"})

        if scores_doc is None:
            scores_doc = {"_id": "SCORES", "scores": []}
            self.high_scores.insert_one(scores_doc)

        new_score = {"ZACK": self.snake.food_eaten}

        scores_doc["scores"].append(new_score)
        scores = sorted([list(score.values())[0]
                        for score in scores_doc["scores"]], reverse=True)
        scores_doc["scores"] = [{"ZACK": score} for score in scores[:10]]

        self.high_scores.update_one({"_id": "SCORES"}, {"$set": scores_doc})
