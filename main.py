import pygame
import random
import os
import sys

all_sprites = pygame.sprite.Group()
obstacle = []


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


class Car(pygame.sprite.Sprite):
    def __init__(self, *grop):
        super().__init__(*grop)
        self.image = pygame.transform.scale(load_image("car.png"), (100, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 230
        self.rect.y = 370

    def update(self, event: pygame.event.Event):
        if event.key == 1073741903:
            self.rect.x += 120
        if event.key == 1073741904:
            self.rect.x -= 120
        if event.key == 97:
            self.rect.x -= 120
        if event.key == 100:
            self.rect.x += 120


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 100
        self.top = 30

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, "white", (0, 0, self.width, self.height), 100)
        pygame.draw.rect(screen, (128, 128, 128),
                         (self.left, self.top, self.width - self.left * 2, self.height - self.top * 2))
        for i in range(1, 6):
            if i == 1:
                pygame.draw.line(screen, "white", (self.left + (120 * i), self.top),
                                 (self.left + (120 * i), self.height - self.top), 2)
            else:
                pygame.draw.line(screen, "white", (self.left + (120 * i), self.top),
                                 (self.left + (120 * i), self.height - self.top), 2)
        all_sprites.draw(screen)

    def set_left_top(self, left, top):
        self.top = top
        self.left = left


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, *grop):
        super().__init__(*grop)
        self.image = pygame.transform.scale(load_image("police.png"), (100, 150))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(230, 230 + 120 * 4)
        self.rect.y = random.randint(40, 500)

    def update(self):
        pass


def main():
    size = 1000, 600
    pygame.init()
    screen = pygame.display.set_mode(size)
    car = Car()
    all_sprites.add(car)
    all_sprites.draw(screen)
    board = Board(size[0], size[1])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == 768:
                car.update(event)
        board.render(screen)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
