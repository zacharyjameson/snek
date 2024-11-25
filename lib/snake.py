# snake.py
from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Snake:
    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds
        self.food_eaten = 0
        self.respawn()

    def respawn(self):
        self.length = 3
        self.direction = Direction.RIGHT
        self.body = [(200, 200), (220, 200), (240, 200)]

    def move(self):
        head = self.body[-1]
        if self.direction == Direction.UP:
            new_head = (head[0], head[1] - self.block_size)
        elif self.direction == Direction.DOWN:
            new_head = (head[0], head[1] + self.block_size)
        elif self.direction == Direction.LEFT:
            new_head = (head[0] - self.block_size, head[1])
        elif self.direction == Direction.RIGHT:
            new_head = (head[0] + self.block_size, head[1])
        self.body.append(new_head)
        if len(self.body) > self.length:
            self.body.pop(0)

    def steer(self, direction):
        if direction == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif direction == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        elif direction == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif direction == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

    def eat(self):
        self.food_eaten += 1
        self.length += 1

    def check_for_food(self, food):
        head = self.body[-1]
        if head == (food.x, food.y):
            self.eat()
            return True
        return False

    def check_tail_collision(self):
        head = self.body[-1]
        for pos in self.body[:-1]:
            if head == pos:
                return True
        return False

    def check_bounds(self):
        head = self.body[-1]
        if head[0] < 0 or head[0] >= self.bounds[0] or head[1] < 0 or head[1] >= self.bounds[1]:
            return True
        return False

    def draw(self, game, window):
        for pos in self.body:
            game.draw.rect(window, (0, 0, 255),
                           (pos[0], pos[1], self.block_size, self.block_size))
