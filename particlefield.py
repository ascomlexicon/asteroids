import pygame
import random
from constants import ASTEROID_MIN_RADIUS
from particle import ExplosionParticle, RocketParticle


class ParticleField(pygame.sprite.Sprite):
    direction: list[pygame.Vector2] = [
        pygame.Vector2(0, 1),  # North
        pygame.Vector2(1, 0),  # East
        pygame.Vector2(0, -1),  # South
        pygame.Vector2(-1, 0),  # West
    ]

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)

    def spawn_explosion(self, epicenter: pygame.Vector2, object_radius: float) -> None:
        particles: list[ExplosionParticle] = [
            ExplosionParticle(epicenter.x, epicenter.y)
            for _ in range(round(object_radius / ASTEROID_MIN_RADIUS) * 25)
        ]

        for exploded_particle in particles:
            movement_direction: pygame.Vector2 = random.choice(
                self.direction
            ) * random.randint(40, 100)
            deflection_angle: float = random.uniform(0, 90)

            exploded_particle.velocity = movement_direction.rotate(deflection_angle)
