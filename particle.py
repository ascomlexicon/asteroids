import pygame
import random
from constants import PARTICLE_RADIUS


class Particle(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, span: float) -> None:
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.lifespan: float = span

    def update(self, dt: float) -> None:
        if self.lifespan <= 0:
            self.kill()
        else:
            self.position += self.velocity * dt
            self.lifespan -= dt

    def draw(self, screen: pygame.Surface) -> None:
        pass


class ExplosionParticle(Particle):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, random.uniform(0.5, 1.5))

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "grey", self.position, PARTICLE_RADIUS)


class RocketParticle(Particle):
    pass
