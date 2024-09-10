import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MIN_SCORE


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def split(self) -> float:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return ASTEROID_MIN_SCORE

        new_angle: float = random.uniform(20, 50)
        new_radius: float = self.radius - ASTEROID_MIN_RADIUS

        velocity1: pygame.Vector2 = self.velocity.rotate(new_angle)
        velocity2: pygame.Vector2 = self.velocity.rotate(-new_angle)

        asteroid1: Asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2: Asteroid = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid1.velocity = velocity1 * 1.2
        asteroid2.velocity = velocity2 * 1.2

        return (self.radius / ASTEROID_MIN_RADIUS) * ASTEROID_MIN_SCORE

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "grey", self.position, self.radius)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
