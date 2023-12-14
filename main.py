import pygame
import random


class Car:
    pass


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, "white", (0, 0, self.width, self.height), 100)


class Obstacle:
    pass


def main():
    size = 1000, 600
    pygame.init()
    screen = pygame.display.set_mode(size)
    board = Board(size[0], size[1])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        board.render(screen)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
