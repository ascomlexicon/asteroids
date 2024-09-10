import pygame
from constants import SHOT_RADIUS
from circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
