import pygame
import math
import constants as const
from ui import draw_glow_circle


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = const.PADDLE_SIZE
        self.speed = const.PADDLE_SPEED
        self.mass = const.PADDLE_MASS
        self.angle = 0

    def check_vertical_bounds(self, height):
        if self.y - self.radius <= 0:
            self.y = self.radius
        elif self.y + self.radius > height:
            self.y = height - self.radius

    def check_left_boundary(self, width):
        if self.x - self.radius <= 0:
            self.x = self.radius
        elif self.x + self.radius > int(width / 2):
            self.x = int(width / 2) - self.radius

    def check_right_boundary(self, width):
        if self.x + self.radius > width:
            self.x = width - self.radius
        elif self.x - self.radius < int(width / 2):
            self.x = int(width / 2) + self.radius

    def move(self, up, down, left, right, time_delta):
        dx, dy = self.x, self.y
        self.x += (right - left) * self.speed * time_delta
        self.y += (down - up) * self.speed * time_delta

        dx = self.x - dx
        dy = self.y - dy

        self.angle = math.atan2(dy, dx)

    def draw(self, screen, color):
        pos = (int(self.x), int(self.y))
        # outer glow
        draw_glow_circle(screen, color, pos, self.radius, glow_radius=int(self.radius * 2))
        # inner highlight ring
        lighter = tuple(min(c + 60, 255) for c in color[:3])
        pygame.draw.circle(screen, lighter, pos, self.radius - 6, 2)
        # small center dot
        pygame.draw.circle(screen, (255, 255, 255, 180), pos, 5)

    def get_pos(self):
        return self.x, self.y

    def reset(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
