import pygame
import random
import os
import sys

size = 1000, 600
pygame.init()
screen = pygame.display.set_mode(size)
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
        self.mask = pygame.mask.from_surface(self.image)
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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randint(230, 230 + 120 * 4)
        self.rect.y = random.randint(40, 500)
        self.y = self.rect.y

    def update(self):
        pass
def wait():
    global all_sprites
    all_sprites = pygame.sprite.Group()
    obstacle.clear()
    plaing_not = True
    while plaing_not:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                plaing_not = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main()


def main():
    tick = pygame.time.Clock()
    car = Car()
    screen.fill("black")
    for ob in range(2):
        obstacle.append(Obstacle())
        all_sprites.add(obstacle[-1])
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
        d = tick.tick() / 1000

        for ob in obstacle:
            ob: Obstacle
            if not pygame.sprite.collide_mask(ob, car):
                ob.y += d * 50
                ob.rect.y = int(ob.y)
            else:
                font = pygame.font.Font(None, 50)
                text = font.render("Столкновение!", True, "red")
                text_x = size[0] // 2 - text.get_width() // 2
                text_y = size[1] // 2 - text.get_height() // 2
                text_w = text.get_width()
                text_h = text.get_height()
                screen.blit(text, (text_x, text_y))
                pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                       text_w + 20, text_h + 20), 1)
                pygame.display.update()
                wait()
                return None
        board.render(screen)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
