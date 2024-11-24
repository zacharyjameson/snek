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
        self.snake = Snake(20, self.bounds)
        self.food = Food(20, self.bounds)
        self.db = get_database()
        self.high_scores = self.db['High Scores']
        high_score_doc = self.high_scores.find_one({"_id": "ZACK"})
        if high_score_doc:
            self.high_score = high_score_doc["score"]
        else:
            self.high_score = 0
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

    def run(self):
        running = True
        game_speed = 15
        clock_tick_rate = 60
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.snake.steer(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.steer(Direction.RIGHT)
                    elif event.key == pygame.K_UP:
                        self.snake.steer(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.steer(Direction.DOWN)

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
                    self.snake.eat()

                if self.snake.check_bounds() or self.snake.check_tail_collision():
                    self.game_over()

                self.window.fill((0, 0, 0))
                self.snake.draw(pygame, self.window)
                self.food.draw(pygame, self.window)
                score_text = self.font.render(
                    f'Score: {self.snake.length - 3}', True, (255, 255, 255))
                self.window.blit(score_text, (10, 10))
                pygame.display.flip()

                self.clock.tick(clock_tick_rate)
                pygame.time.delay(1000 // game_speed)

        pygame.quit()

    def game_over(self):
        self.window.fill((0, 0, 0))
        game_over_text = self.font.render('Game Over', True, (255, 255, 255))
        self.window.blit(
            game_over_text, (self.bounds[0] // 2 - 100, self.bounds[1] // 2 - 50))
        score_text = self.font.render(
            f'Final Score: {self.snake.length - 3}', True, (255, 255, 255))
        self.window.blit(
            score_text, (self.bounds[0] // 2 - 100, self.bounds[1] // 2))
        high_score_text = self.font.render(
            f'High Score: {self.high_score}', True, (255, 255, 255))
        self.window.blit(
            high_score_text, (self.bounds[0] // 2 - 100, self.bounds[1] // 2 + 50))
        press_return_text = self.font.render(
            'Press Enter to play again', True, (255, 255, 255))
        self.window.blit(press_return_text,
                         (self.bounds[0] // 2 - 100, self.bounds[1] // 2 + 100))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        waiting = False
                        self.save_high_score()
                        self.snake.respawn()
                        self.food.respawn()
                        self.run()
        pygame.quit()

    def save_high_score(self):
        documents = list(self.high_scores.find())
        if not documents:
            self.high_scores.insert_one(
                {"_id": "ZACK", "score": self.snake.length - 3})
        else:
            max_score = max(doc['score'] for doc in documents)
            if self.snake.length - 3 > max_score:
                self.high_scores.update_one(
                    {"_id": "ZACK"}, {"$set": {"score": self.snake.length - 3}})
