import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MIN_SCORE

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return ASTEROID_MIN_SCORE
        
        new_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        velocity1, velocity2 = self.velocity.rotate(new_angle), self.velocity.rotate(-new_angle)
        
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        
        asteroid1.velocity = velocity1 * 1.2
        asteroid2.velocity = velocity2 * 1.2

        return (self.radius // ASTEROID_MIN_RADIUS) * ASTEROID_MIN_SCORE

    def draw(self, screen):
        pygame.draw.circle(screen, "grey", self.position, self.radius)
        
    def update(self, dt):
        self.position += self.velocity * dt
