import sys
import pygame
from shot import Shot
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    
    shots = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
    asteroid_field = AsteroidField()

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")

        for sprite in updatable:
            sprite.update(dt)
        
        for asteroid in asteroids:
            if player.has_collided(asteroid):
                print("Game over!")
                sys.exit()

        for sprite in drawable:
            sprite.draw(screen)
        
        pygame.display.flip()

        # Framerate cap of 60 FPS
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
