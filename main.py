import sys
import pygame
from shot import Shot
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from particlefield import ParticleField
from particle import ExplosionParticle, RocketParticle
from constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    FRAME_RATE,
    SCORE_TIME_INCREMENT,
    MAX_LIVES,
    INVINCIBILITY_TIME,
    LIFE_LOST_SCORE_PENALTY,
)


def start_menu(screen: pygame.Surface) -> bool:
    screen.fill("black")
    title_font: pygame.font.Font = pygame.font.SysFont("unscii", 75)
    prompt_font: pygame.font.Font = pygame.font.SysFont("jetbrainsmononerdfontmono", 18)

    title: pygame.Surface = title_font.render("ASTEROIDS", True, "white")
    prompt: pygame.Surface = prompt_font.render("Press ENTER to start", True, "white")

    screen.blit(
        title,
        (
            SCREEN_WIDTH / 2 - title.get_width() / 2,
            SCREEN_HEIGHT / 2 - title.get_height() / 2,
        ),
    )

    screen.blit(
        prompt,
        (
            SCREEN_WIDTH / 2 - prompt.get_width() / 2,
            SCREEN_HEIGHT / 2 + prompt.get_height() / 2 + 20,
        ),
    )

    pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        return True

    return False


def game_over(screen: pygame.Surface, score: float) -> None:
    screen.fill("red")

    large_text: pygame.font.Font = pygame.font.SysFont("unscii", 100)
    score_text: pygame.font.Font = pygame.font.SysFont("unscii", 40)
    prompt_font: pygame.font.Font = pygame.font.SysFont("jetbrainsmononerdfontmono", 24)

    game_over_text: pygame.Surface = large_text.render("GAME OVER", True, "black")
    score_text: pygame.Surface = score_text.render(
        f"You won {round(score)} points!", True, "black"
    )
    prompt: pygame.Surface = prompt_font.render(
        "Press R to RESTART/Q to quit", True, "black"
    )

    screen.blit(
        game_over_text,
        (
            SCREEN_WIDTH / 2 - game_over_text.get_width() / 2,
            SCREEN_HEIGHT / 2 - game_over_text.get_height() / 2,
        ),
    )

    screen.blit(
        score_text,
        (
            SCREEN_WIDTH / 2 - score_text.get_width() / 2,
            SCREEN_HEIGHT / 2 + score_text.get_height() / 2 + 20,
        ),
    )

    screen.blit(
        prompt,
        (
            SCREEN_WIDTH / 2 - prompt.get_width() / 2,
            SCREEN_HEIGHT / 2 + prompt.get_height() / 2 + 60,
        ),
    )

    pygame.display.update()


def game(fps: int, screen: pygame.Surface) -> None:
    explosion_sound: pygame.mixer.Sound = pygame.mixer.Sound(
        "assets/RetroExplosion.mp3"
    )
    explosion_sound.set_volume(0.4)

    # Groups to make entities easier to handle.
    shots: pygame.sprite.Group = pygame.sprite.Group()
    asteroids: pygame.sprite.Group = pygame.sprite.Group()
    updatable: pygame.sprite.Group = pygame.sprite.Group()
    drawable: pygame.sprite.Group = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)

    ExplosionParticle.containers = (updatable, drawable)
    RocketParticle.containers = (updatable, drawable)

    # Variables
    background: pygame.Surface = pygame.image.load("assets/space_background.jpg")
    clock: pygame.time.Clock = pygame.time.Clock()
    player: Player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field: AsteroidField = AsteroidField()
    particle_field: ParticleField = ParticleField()

    dt: float = 0
    score: float = 0
    lives: int = MAX_LIVES
    collision_time: int = 0

    # Timer to signify a second
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.USEREVENT + 1:
                score += SCORE_TIME_INCREMENT

        font: pygame.font.Font = pygame.font.SysFont("unscii", 14)

        screen.fill("black")
        screen.blit(background, (0, 0))

        scoreboard: pygame.Surface = font.render(
            f"Score: {round(score)}", True, (31, 212, 19)
        )
        lives_hud: pygame.Surface = font.render(f"Lives: {lives}", True, (31, 212, 19))

        if player.invincible and (
            pygame.time.get_ticks() - collision_time >= INVINCIBILITY_TIME
        ):
            player.invincible = False

        if lives == 0:
            while True:
                return score

        for sprite in updatable:
            sprite.update(dt)

        for asteroid in asteroids:
            if player.has_collided(asteroid) and not player.invincible:
                collision_time = pygame.time.get_ticks()

                lives -= 1
                score -= LIFE_LOST_SCORE_PENALTY

                if score < 0:
                    score = 0

                player.invincible = True

                particle_field.spawn_explosion(asteroid.position, asteroid.radius)
                pygame.mixer.Sound.play(explosion_sound)
                asteroid.kill()
                continue

            for shot in shots:
                if asteroid.has_collided(shot):
                    particle_field.spawn_explosion(asteroid.position, asteroid.radius)
                    pygame.mixer.Sound.play(explosion_sound)

                    score += asteroid.split()
                    shot.kill()

        for sprite in drawable:
            sprite.draw(screen)

        screen.blit(scoreboard, (10, 10))
        screen.blit(lives_hud, (1160, 10))

        pygame.display.flip()

        dt = clock.tick(fps) / 1000


def main() -> None:
    pygame.init()
    pygame.font.init()

    # Music
    pygame.mixer.music.load("assets/Aftertune - Galaxy.flac")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    is_running: bool = False
    has_quit: bool = False
    on_game_over: bool = False

    while not is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        is_running = start_menu(screen)

    while not has_quit:
        final_score = game(FRAME_RATE, screen)
        on_game_over = True

        while on_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            game_over(screen, final_score)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:
                on_game_over = False

            if keys[pygame.K_q]:
                has_quit = True
                on_game_over = False


if __name__ == "__main__":
    main()
