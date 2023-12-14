import pygame
import random
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Car:
    pass


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 100
        self.top = 80

    def render(self, screen: pygame.Surface, all_sprites):
        pygame.draw.rect(screen, "white", (0, 0, self.width, self.height), 100)
        pygame.draw.rect(screen, (128, 128, 128), (self.left, self.top, self.width - self.left * 2, self.height - self.top * 2))
        all_sprites.draw(screen)

    def set_left_top(self, left, top):
        self.top = top
        self.left = left


class Obstacle:
    pass


def main():
    size = 1000, 600
    pygame.init()
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite(all_sprites)
    image = load_image("car.png", -1)
    image1 = pygame.transform.scale(image, (100, 150))
    sprite.image = image1
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = 110
    sprite.rect.y = 370
    all_sprites.draw(screen)
    board = Board(size[0], size[1])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        board.render(screen, all_sprites)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
