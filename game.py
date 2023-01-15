import pathlib
import random

import pygame
from pygame.locals import *

codes = {
    'body': 1,
    'head': 3,
    'point': 10,
    'field': 0,
}


class Snake:
    def __init__(
        self,
        size = [28, 28],
    ):
        self.rows, self.cols = size
        self.speed = self.default_speed = 10
        self.passed = 0
        self.score = 0
        self.is_loss = False
        self.snake = []
        self.points = []
        self.absorbed = False
        self.grid = self.create_grid()
        self.direction = 'left'

    def create_grid(self):
        row, col = self.rows // 2, self.cols // 2
        snake = [(row, col)]
        for i in range(random.randint(3, 6)):
            snake += [(row, col + i + 1)]
        self.snake = snake
        self.points = self.get_points(3)
        return self.get_grid(self.snake, self.points)

    def get_grid(self, snake, points):
        grid = [[0] * self.cols for _ in range(self.rows)]
        for point in points:
            grid[point[0]][point[1]] = codes['point']
        for i in range(len(snake)):
            chunk = snake[i]
            if i == 0:
                grid[chunk[0]][chunk[1]] = codes['head']
            else:
                grid[chunk[0]][chunk[1]] = codes['body']
        return grid

    def set_direction(self, new_dir):
        if sorted([new_dir, self.direction]) not in [sorted(['right', 'left']), sorted(['top', 'bottom'])]:
            self.direction = new_dir

    def get_points(self, count=3):
        points = []
        for i in range(count):
            while True:
                rect = (random.randint(0, self.cols-1), random.randint(0, self.cols-1))
                if rect not in self.snake and rect not in self.points:
                    points.append(rect)
                    break
        return points

    def step(self):
        self.passed += 1

        snake = self.snake
        head = snake[0]

        points = self.points
        if self.passed % (random.randint(10, 15)) == 0 and len(self.points) < 3:
            p_count = int(3 * (1.5 * self.speed // self.default_speed))
            points = [*points, *self.get_points(p_count if p_count < 10 else 9)]

        match self.direction:
            case 'left':
                new_snake = [(head[0], head[1] - 1 if head[1] - 1 >= 0 else self.cols - 1)]
            case 'top':
                new_snake = [(head[0] - 1 if head[0] - 1 >= 0 else self.rows - 1, head[1])]
            case 'right':
                new_snake = [(head[0], head[1] + 1 if head[1] + 1 < self.cols else self.cols - head[1] - 1)]
            case 'bottom':
                new_snake = [(head[0] + 1 if head[0] + 1 < self.rows else self.rows - head[0] - 1, head[1])]
        new_snake += [snake[0]]

        for i in range(2, len(snake)):
            new_snake.append(snake[i - 1])
            if i == len(snake)-1 and self.absorbed:
                new_snake.append(snake[i])
                self.absorbed = False

        for point in points:
            if point in snake:
                self.absorbed = True
                if self.speed < 30 and random.randint(0, 1):
                    self.speed += 1
                self.score += (2 * self.speed) // self.default_speed
                points.remove(point)

        if len(snake) != len(set(snake)):
            self.is_loss = True
        else:
            self.snake = new_snake
            self.points = points
            self.grid = self.get_grid(snake, points)
