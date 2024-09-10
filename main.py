import sys
import pygame
from shot import Shot
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCORE_TIME_INCREMENT,
    MAX_LIVES,
    INVINCIBILITY_TIME,
    LIFE_LOST_SCORE_PENALTY,
)


def main():
    pygame.init()
    pygame.font.init()

    # Groups to make entities easier to handle.
    shots = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    # Background Image Source: https://wallpapersden.com/4k-starry-sky-stars-milky-way-galaxy-wallpaper/1280x720/
    background = pygame.image.load("assets/space_background.jpg")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    dt = 0
    score = 0
    lives = MAX_LIVES
    collision_time = 0

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
        screen.blit(background, (0, 0))

        scoreboard = font.render(f"Score: {score}", True, (31, 212, 19))
        lives_hud = font.render(f"Lives: {lives}", True, (31, 212, 19))

        if player.invincible and (
            pygame.time.get_ticks() - collision_time >= INVINCIBILITY_TIME
        ):
            player.invincible = False

        if lives == 0:
            print("Game over!")
            print(f"You had {score} points!!!")
            sys.exit()

        for sprite in updatable:
            sprite.update(dt)

        for asteroid in asteroids:
            if player.has_collided(asteroid) and not player.invincible:
                collision_time = pygame.time.get_ticks()

                lives -= 1
                score -= LIFE_LOST_SCORE_PENALTY

                player.invincible = True

            for shot in shots:
                if asteroid.has_collided(shot):
                    score += asteroid.split()
                    shot.kill()

        for sprite in drawable:
            sprite.draw(screen)

        screen.blit(scoreboard, (10, 10))
        screen.blit(lives_hud, (1160, 10))

        pygame.display.flip()

        # Framerate cap of 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
