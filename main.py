import pygame
import random
import os
import sys

size = 900, 600
pygame.init()
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
obstacle = []
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
running = True
pygame.mixer.music.load("data/pov.mp3")


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.display.set_caption(title="Машинки", icontitle="car.png")


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Car(pygame.sprite.Sprite):
    def __init__(self, *grop):
        super().__init__(*grop)
        self.image = pygame.transform.scale(load_image("car.png", colorkey=-1), (100, 150))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 10 + board.left + random.randint(0, 4) * 120
        self.rect.y = 380

    def update(self, event: pygame.event.Event):
        global running
        if self.rect.x + 120 < size[0] - board.left and (event.key == 1073741903 or event.key == 100):
            self.rect.x += 120
            for ob in obstacle:
                ob: Obstacle
                if pygame.sprite.collide_mask(ob, car):
                    self.rect.x -= 100
                    self.image = pygame.transform.scale(load_image("crash_car2.png", colorkey=-1), (100, 150))
                    board.is_plaing = False
        if self.rect.x - 120 > board.left and (event.key == 1073741904 or event.key == 97):
            self.rect.x -= 120
            for ob in obstacle:
                ob: Obstacle
                if pygame.sprite.collide_mask(ob, car):
                    self.rect.x += 100
                    self.image = pygame.transform.scale(load_image("crash_car2.png", colorkey=-1), (110, 170))
                    board.is_plaing = False


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 150
        self.top = 0
        self.ball = 0
        self.is_plaing = True

    def render(self):
        pygame.draw.rect(screen, "white", (0, 0, self.width, self.height))
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
        font = pygame.font.Font(None, 20)
        text = font.render(f"""Ваш счёт:{board.ball}""", True, "red")
        screen.blit(text, (800, 30))

    def menu_render(self):
        pass

    def set_left_top(self, left, top):
        self.top = top
        self.left = left

    def set_ball(self, clear=None):
        if clear is None:
            self.ball += 1
        else:
            self.ball = 0


board = Board(size[0], size[1])
car = Car()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, *grop, pos=None):
        super().__init__(*grop)
        self.image = pygame.transform.scale(load_image(f"ob{random.randint(0, 2)}.png", colorkey=-1), (100, 150))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        fl = True
        while fl:
            fl = False
            self.rect.x = 10 + board.left + random.randint(0, 4) * 120
            if pos is None:
                self.rect.y = random.randint(-200, -100)
            else:
                self.rect.y = random.randint(40, size[1] - 100)
            self.y = self.rect.y
            for i in all_sprites:
                if pygame.sprite.collide_mask(i, self):
                    fl = True

    def update(self):
        pass


def wait():
    global all_sprites
    pygame.mixer.music.pause()
    all_sprites = pygame.sprite.Group()
    obstacle.clear()
    plaing_not = True
    while plaing_not:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                plaing_not = False

            if event.type == pygame.KEYDOWN:
                main()
                return None
    pygame.quit()


def menu():
    running_menu = True
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
    pygame.quit()


def main():
    global running, car
    car = Car()
    l_d = -3000  # рандомный диапозон создаем машинко когда randint == 2
    l_r = 3000
    board.is_plaing = True
    car.image = pygame.transform.scale(load_image("car2.png", colorkey=-1), (100, 150))
    tick = pygame.time.Clock()
    chet = pygame.USEREVENT + 1
    pygame.time.set_timer(chet, 2000)
    screen.fill("black")
    all_sprites.add(car)
    for ob in range(3):
        obstacle.append(Obstacle(pos=-1))
        all_sprites.add(obstacle[-1])
    all_sprites.draw(screen)
    running = True
    speed = 70
    pygame.mixer.music.play(-1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == 768:
                if event.unicode == ' ':
                    pygame.mixer.music.pause()
                car.update(event)
            if event.type == chet:
                board.set_ball()
                if board.ball % 15 == 0:
                    speed = speed + 15
                    l_d += 200
                    l_r -= 200
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.pause()
        d = tick.tick() / 1000
        for ob in obstacle:
            ob: Obstacle
            if board.is_plaing and not pygame.sprite.collide_mask(ob, car):
                ob.y += d * speed
                ob.rect.y = int(ob.y)
                if len(obstacle) < 3 and random.randint(l_d, l_r) == 1:
                    obstacle.append(Obstacle())
                    all_sprites.add(obstacle[-1])
                if ob.y >= size[1]:
                    del obstacle[obstacle.index(ob)]
            else:

                board.is_plaing = False
                board.render()
                car.image = pygame.transform.scale(load_image("crash_car2.png", colorkey=-1), (110, 170))
                all_sprites.draw(screen)
                font = pygame.font.Font(None, 50)
                text = font.render(f"""Столкновение! Ваш счёт: {board.ball}""", True, "red")
                board.set_ball(clear=-1)

                text_x = size[0] // 2 - text.get_width() // 2
                text_y = size[1] // 2 - text.get_height() // 2
                text_w = text.get_width()
                text_h = text.get_height()
                screen.blit(text, (text_x, text_y))
                pygame.draw.rect(screen, "red", (text_x - 10, text_y - 10,
                                                 text_w + 20, text_h + 20), 1)

                pygame.display.update()
                wait()
                return None
        if len(obstacle) == 0:
            obstacle.append(Obstacle())
            all_sprites.add(obstacle[-1])
        board.render()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
