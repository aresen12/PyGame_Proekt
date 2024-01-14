import pygame
import random
import os
import sys
import sqlite3

size = 900, 600
pygame.init()
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
obstacle = []
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
running = True
pygame.display.set_caption(title="Машинки")
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
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


grass = load_image('grass.jpg')
fon = pygame.transform.scale(grass, (900, 600))


class Button:
    def __init__(self, command=None, text=None, x=0, y=0, width=0, height=0, color="blue", color_text="red"):
        self.command = command
        self.text = text
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.color = color
        self.color_text = color_text

    def render(self):
        rect = pygame.draw.rect(screen, self.color, (self.x, self.y, self.height, self.width))
        font = pygame.font.Font(None, 25)
        text = font.render(str(self.text), True, self.color_text)
        screen.blit(text, text.get_rect(center=rect.center))

    def update(self, event):
        if self.y <= event.pos[1] <= self.y + self.width and self.x <= event.pos[0] <= self.x + self.height:
            if not (self.command is None):
                self.command()
        return None

    def set_text(self, text: str):
        self.text = text.strip()


class Car(pygame.sprite.Sprite):
    def __init__(self, *grop, number=1):
        super().__init__(*grop)
        self.image = pygame.transform.scale(load_image(f"car{number}.png", colorkey=-1), (100, 150))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.number_pos = random.randint(0, 4)
        self.rect.x = 10 + board.left + self.number_pos * 120
        self.rect.y = 425
        self.number = number

    def update(self, event: pygame.event.Event):
        global running
        if self.rect.x + 120 < size[0] - board.left and (event.key == 1073741903 or event.key == 100):
            self.rect.x += 120
            for ob in obstacle:
                ob: Obstacle
                if pygame.sprite.collide_mask(ob, car):
                    self.rect.x -= 100
                    self.image = pygame.transform.scale(load_image("crash_car.png", colorkey=-1), (100, 150))
                    board.is_playing = False
        if self.rect.x - 120 > board.left and (event.key == 1073741904 or event.key == 97):
            self.rect.x -= 120
            for ob in obstacle:
                ob: Obstacle
                if pygame.sprite.collide_mask(ob, car):
                    self.rect.x += 100
                    self.image = pygame.transform.scale(load_image("crash_car.png", colorkey=-1), (100, 150))
                    board.is_playing = False


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 150
        self.top = 0
        self.ball = 0
        self.is_playing = True
        self.pos_y = -600
        self.image = load_image('road.jpg')

    def render(self, y=0):
        pygame.draw.rect(screen, "white", (0, 0, self.width, self.height))
        pygame.draw.rect(screen, (128, 128, 128),
                         (self.left, self.top, self.width - self.left * 2, self.height - self.top * 2))
        for i in range(1, 6):
            pygame.draw.line(screen, "white", (self.left + (120 * i), self.top),
                             (self.left + (120 * i), self.height - self.top), 2)
        self.pos_y += y
        if int(self.pos_y) in range(-600 + 165 * 3 - 2, -600 + 165 * 3 + 3):
            self.pos_y = - 600
        screen.blit(self.image, (150, self.pos_y))
        all_sprites.draw(screen)
        font = pygame.font.Font(None, 20)
        pygame.draw.rect(screen, "blue", (800, 100, 90, 30))
        screen.blit(font.render("Меню", True, "red"), (810, 110))
        text = font.render(f"""Ваш счёт:{board.ball}""", True, "red")
        screen.blit(text, (800, 30))

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


menu_flag = False
new_game = False


def new():
    global menu_flag
    menu_flag = True


def menu_fun():
    global new_game
    new_game = True


def wait():
    pygame.mixer.music.load("data/bax.mp3")
    pygame.mixer.music.play()
    global all_sprites, new_game, menu_flag
    menu_flag = False
    new_game = False
    buttons = [Button(text="Меню", x=370, y=330, width=30, height=100, command=menu_fun),
               Button(text="заново", x=510, y=330, width=30, height=100, command=new)]
    all_sprites = pygame.sprite.Group()
    obstacle.clear()
    playing_not = True
    while playing_not:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing_not = False
            if event.type == pygame.KEYDOWN:
                if event.unicode == " ":
                    main()
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.update(event)
        for button in buttons:
            button.render()
        if new_game:
            new()
            return None
        if menu_flag:
            main()
            return None
        pygame.display.update()
    pygame.quit()
    sys.exit()


username = None


class Table:
    def __init__(self, username, ball):
        if username is None:
            username = self.get_user()
        self.username = username
        self.ball = ball
        self.connection = sqlite3.connect('rating_system.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Results (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        result INTEGER
        )
        ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user (
    id    INTEGER NOT NULL
                  CONSTRAINT genres_pk PRIMARY KEY AUTOINCREMENT,
    username TEXT
);
''')
        self.connection.commit()
        self.connection.close()

    def updata_user(self):
        self.connection = sqlite3.connect("rating_system.db")
        self.cursor = self.connection.cursor()
        results = self.cursor.execute(f'SELECT result FROM Results WHERE username = "{self.username}"').fetchone()
        self.ball = board.ball
        print(results)
        if results is None:
            self.cursor.execute('INSERT INTO Results (username, result) VALUES (?, ?)', (self.username,
                                                                                         self.ball))
            self.connection.commit()
        elif results[0] < board.ball:
            self.cursor.execute(f'UPDATE Results SET result = {board.ball} WHERE username = "{self.username}"')
            self.connection.commit()
        self.connection.close()

    def get_score(self):
        self.connection = sqlite3.connect("rating_system.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('SELECT result FROM Results WHERE username = ?', (self.username,))
        record = self.cursor.fetchall()
        self.connection.close()
        try:
            return record[0][0]
        except IndexError:
            return board.ball

    def get_user(self):
        bd = sqlite3.connect("rating_system.db")
        curr = bd.cursor()
        res = curr.execute("""SELECT username FROM user""").fetchone()
        bd.close()
        if not (res is None):
            return res[0]
        else:
            return None

    def sistem(self):
        bd = sqlite3.connect("rating_system.db")
        curr = bd.cursor()
        curr.execute("""DELETE FROM user""")
        curr.execute(f'''INSERT INTO user (id, username) VALUES (1, '{self.username}')''', )
        bd.commit()
        bd.close()

    def sing_out(self):
        global board, car, username, menu
        username = None
        self.username = None
        menu = Menu()
        board = Board(size[0], size[1])
        car = Car()
        bd = sqlite3.connect("rating_system.db")
        curr = bd.cursor()
        curr.execute("""DELETE FROM user""")
        bd.commit()
        bd.close()

    def get_results(self):
        self.connection = sqlite3.connect("rating_system.db")
        self.cursor = self.connection.cursor()
        res = self.cursor.execute("SELECT * FROM results").fetchall()
        self.connection.close()
        return res


table = Table(None, board.ball)
username = table.username
watching = True


def close_wind():
    global watching
    watching = False


def results_look():
    global watching
    watching = True
    buttons = []
    close_btn = Button(color_text="white", color="#a35713", x=800, y=100, text="Закрыть", width=30, height=100,
                       command=close_wind)
    buttons.append(close_btn)
    while watching:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                watching = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                close_btn.update(event)
        menu.watching_results()
        for button in buttons:
            button.render()
        pygame.display.update()


class Menu:
    def __init__(self):
        self.username = table.username
        self.text = ""
        if self.username is None:
            self.sing = True
        else:
            self.sing = False

    def render(self, buttons):
        fon = pygame.transform.scale(load_image('garage.jpg'), (900, 600))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        font2 = pygame.font.Font(None, 25)
        # text = font.render("Добро", True, (255, 255, 255))
        # screen.blit(text, ((size[1] // 2) + 200, 190))
        # screen.blit(font.render("Пожаловать!", True, (255, 255, 255)), (size[1] // 2 + 150, 230))
        screen.blit(font2.render(str(self.username), True, "#a35713"), (750, 50))
        screen.blit(font2.render("Вы Вошли как:", True, "#a35713"), (750, 20))
        fon = pygame.transform.scale(load_image('yel_car.png', colorkey=-1), (353, 200))
        screen.blit(fon, (370, 385))
        for button in buttons:
            button.render()

    def sing_up(self):
        screen.fill((228, 189, 114))
        fon = pygame.transform.scale(load_image('font.jpg'), (484, 600))
        screen.blit(fon, (225, 0))
        font = pygame.font.Font(None, 50)
        text2 = font.render("Введите своё имя", True, "red")
        screen.blit(text2, (size[1] // 2, 200))
        text_surf = font.render(self.text, True, (255, 0, 0))
        screen.blit(text_surf, text_surf.get_rect(center=screen.get_rect().center))

    def updata(self, event):
        if self.sing:
            if event.key == pygame.K_RETURN and self.text.strip() != "":
                global username
                self.text = self.text.strip()
                self.username = self.text
                table.username = self.text
                username = self.username
                self.sing = False
                table.sistem()
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode != "":
                self.text += event.unicode
        else:
            main()

    def watching_results(self):
        fon = pygame.transform.scale(load_image('board.png'), (900, 600))
        screen.blit(fon, (0, 0))
        font2 = pygame.font.Font(None, 20)
        res = table.get_results()
        if not (res is None):
            height = 230
            res.sort(key=lambda x: x[2], reverse=True)
            for user in range(len(res)):
                if user > 7:
                    break
                screen.blit(font2.render(f"{user + 1}. {res[user][1].strip()}: {res[user][2]}", True, "white"),
                            (450, height))
                height += 30


menu = Menu()


def start_game():
    buttons = []
    run = True
    pygame.mixer.music.pause()
    button_out = Button(color="#a35713", color_text="white", x=750, y=100, height=100, width=30, command=table.sing_out,
                        text="Выход")
    buttons.append(button_out)
    start_btn = Button(color="#a35713", color_text="white", x=size[0] // 2 - 275, y=525, height=100, width=30,
                       command=main, text="Старт")
    pokaz_btn = Button(color="#a35713", color_text="white", x=(size[1] // 2 + 200), y=190, height=150, width=60,
                       command=results_look, text="Доска Почета")
    buttons.append(start_btn)
    buttons.append(pokaz_btn)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                menu.updata(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.update(event)
        screen.fill("purple")
        if menu.username is None:
            menu.sing_up()
        else:
            menu.render(buttons)
        pygame.display.update()
    return None


def main():
    pygame.mixer.music.load("data/pov.mp3")
    global running, all_sprites, board, car
    l_d = -3000  # рандомный диапазон создаем машинку когда randint == 2
    l_r = 3000
    board.is_playing = True
    car = Car()
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
    speed = 100
    pygame.mixer.music.play(-1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == 768:
                car.update(event)
            if event.type == chet:
                board.set_ball()
                if board.ball % 3 == 0:
                    speed = speed + 30
                    if l_d > -200:
                        l_d += 200
                    if l_r < 200:
                        l_r -= 200
                if board.ball == 60:
                    pygame.mixer.music.load("data/Super_bal.MP3")
                    pygame.mixer.music.play(-1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 800 <= event.pos[0] <= 890 and 100 <= event.pos[1] <= 130:
                    obstacle.clear()
                    all_sprites = pygame.sprite.Group()
                    board = Board(size[0], size[1])
                    start_game()
                    return None
        d = tick.tick() / 1000
        for ob in obstacle:
            ob: Obstacle
            if board.is_playing and not pygame.sprite.collide_mask(ob, car):
                ob.y += d * speed
                ob.rect.y = int(ob.y)
                if len(obstacle) < 3 and random.randint(l_d, l_r) == 1:
                    obstacle.append(Obstacle())
                    all_sprites.add(obstacle[-1])
                if ob.y >= size[1]:
                    del obstacle[obstacle.index(ob)]
            else:
                board.is_playing = False
                board.render(d * speed)
                pygame.mixer.music.pause()
                font = pygame.font.Font(None, 50)
                car.image = pygame.transform.scale(load_image("crash_car.png", colorkey=-1), (100, 150))
                all_sprites.draw(screen)
                text = font.render(f"""Столкновение! Ваш счёт: {board.ball}, рекорд: {table.get_score()}""",
                                   True, "red")
                table.updata_user()
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
        board.render(d * speed)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    start_game()
