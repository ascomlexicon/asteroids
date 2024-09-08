import sys
import pygame
from shot import Shot
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCORE_TIME_INCREMENT

def main():
    pygame.init()
    pygame.font.init()
    
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
    score = 0
    
    # Timer to signify a second
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.USEREVENT + 1:
                score += SCORE_TIME_INCREMENT
        
        font = pygame.font.SysFont("unscii", 14)

        screen.fill("black")

        scoreboard = font.render(f"Score: {score}", True, (31, 212, 19))
        screen.blit(scoreboard, (10, 10))

        for sprite in updatable:
            sprite.update(dt)
        
        for asteroid in asteroids:
            if player.has_collided(asteroid):
                print("Game over!")
                print(f"You had {score} points!!!")
                sys.exit()
            
            for shot in shots:
                if asteroid.has_collided(shot):
                    score += asteroid.split()
                    shot.kill()

        for sprite in drawable:
            sprite.draw(screen)
        
        pygame.display.flip()

        # Framerate cap of 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
