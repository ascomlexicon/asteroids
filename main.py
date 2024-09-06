import pygame
from constants import *

def main():
    pygame.init()
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")
        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
