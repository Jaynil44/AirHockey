import pygame
import random as rand
import math
import constants as const
from ui import draw_glow_circle


class Puck:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = const.PUCK_SIZE
        self.speed = const.PUCK_SPEED
        self.mass = const.PUCK_MASS
        self.angle = 0

    def move(self, time_delta):
        self.x += math.sin(self.angle) * self.speed * time_delta
        self.y -= math.cos(self.angle) * self.speed * time_delta
        self.speed *= const.FRICTION

    def check_boundary(self, width, height):
        if self.x + self.radius > width:
            self.x = 2 * (width - self.radius) - self.x
            self.angle = -self.angle
        elif self.x - self.radius < 0:
            self.x = 2 * self.radius - self.x
            self.angle = -self.angle

        if self.y + self.radius > height:
            self.y = 2 * (height - self.radius) - self.y
            self.angle = math.pi - self.angle
        elif self.y - self.radius < 0:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle

    def add_vectors(self, vector1, vector2):
        angle1, length1 = vector1
        angle2, length2 = vector2
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2
        length = math.hypot(x, y)
        angle = math.pi / 2 - math.atan2(y, x)
        return angle, length

    def collision_paddle(self, paddle):
        dx = self.x - paddle.x
        dy = self.y - paddle.y
        distance = math.hypot(dx, dy)

        if distance > self.radius + paddle.radius:
            return False

        tangent = math.atan2(dy, dx)
        temp_angle = math.pi / 2 + tangent
        total_mass = self.mass + paddle.mass

        vec_a = (self.angle, self.speed * (self.mass - paddle.mass) / total_mass)
        vec_b = (temp_angle, 2 * paddle.speed * paddle.mass / total_mass)
        (self.angle, self.speed) = self.add_vectors(vec_a, vec_b)

        if self.speed > const.MAX_SPEED:
            self.speed = const.MAX_SPEED

        vec_a = (paddle.angle, paddle.speed * (paddle.mass - self.mass) / total_mass)
        vec_b = (temp_angle + math.pi, 2 * self.speed * self.mass / total_mass)
        temp_speed = paddle.speed
        (paddle.angle, paddle.speed) = self.add_vectors(vec_a, vec_b)
        paddle.speed = temp_speed

        offset = 0.5 * (self.radius + paddle.radius - distance + 1)
        self.x += math.sin(temp_angle) * offset
        self.y -= math.cos(temp_angle) * offset
        paddle.x -= math.sin(temp_angle) * offset
        paddle.y += math.cos(temp_angle) * offset
        return True

    def round_reset(self, player):
        if player == 1:
            self.x = 3 * const.WIDTH // 4
        if player == 2:
            self.x = const.WIDTH // 4
        self.y = const.HEIGHT // 2
        self.angle = 0
        self.speed = 0

    def reset(self, speed, player):
        if player == 1:
            self.angle = rand.uniform(-math.pi, 0)
        elif player == 2:
            self.angle = rand.uniform(0, math.pi)
        self.speed = speed
        self.x = const.WIDTH // 2
        self.y = const.HEIGHT // 2

    def end_reset(self, speed):
        self.angle = 0
        self.speed = speed
        self.x = const.WIDTH // 2
        self.y = const.HEIGHT // 2

    def draw(self, screen):
        pos = (int(self.x), int(self.y))
        # glow bloom
        draw_glow_circle(screen, const.WHITE, pos, self.radius,
                         glow_radius=int(self.radius * 2.2))
        # subtle inner ring
        pygame.draw.circle(screen, (200, 200, 220), pos, self.radius - 4, 2)

    def get_pos(self):
        print(self.x, self.y)
