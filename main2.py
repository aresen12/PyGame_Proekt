import pygame
import random
import os
import sys
import sqlite3

size = 900, 600
pygame.init()
size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
obstacle = []
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
running = True
pygame.display.set_caption(title="Машинки")
pygame.mixer.music.load("data/pov.mp3")
tg = 0.1 * size[1] / (0.2 * size[0])


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


class Button:
    def __init__(self, command=None, text=None, x=0, y=0, color_key=None, width=30, height=100, color="blue",
                 color_text="red", img=None):
        self.command = command
        self.text = text
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.color = color
        self.color_text = color_text
        self.font = pygame.font.Font(None, 25)
        if img:
            try:
                self.img = pygame.transform.scale(load_image(img, colorkey=color_key), (height, width))
            except FileNotFoundError:
                print("файл не найден!")
        else:
            self.img = None

    def render(self):
        if self.img:
            screen.blit(self.img, (self.x, self.y))
        else:
            rect = pygame.draw.rect(screen, self.color, (self.x, self.y, self.height, self.width))
            text = self.font.render(str(self.text), True, self.color_text)
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
        if board.three_d:
            self.image = pygame.transform.scale(load_image(f"car{number}_3d.jpg", colorkey=-1), (130, 130))
        else:
            self.image = pygame.transform.scale(load_image(f"car{number}.png", colorkey=-1), (90, 150))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 10 + board.left + 2 * 100
        self.rect.y = size[1] - 300
        self.number = number

    def update(self, event: pygame.event.Event):
        global running
        if self.rect.x + 120 < size[0] - board.left and (event.key == 1073741903 or event.key == 100):
            if not board.three_d:
                self.rect.x += 120
            else:
                self.rect.x += size[0] * 0.12
            for ob in obstacle:
                ob: Obstacle
                if pygame.sprite.collide_mask(ob, car):
                    self.rect.x -= 100
                    self.image = pygame.transform.scale(load_image(f"crash_car{car.number}.png", colorkey=-1),
                                                        (100, 150))
                    board.is_playing = False
        if self.rect.x - 120 > board.left and (event.key == 1073741904 or event.key == 97):
            if not board.three_d:
                self.rect.x -= 120
            else:
                self.rect.x -= size[0] * 0.12
            for ob in obstacle:
                ob: Obstacle
                if pygame.sprite.collide_mask(ob, car):
                    self.rect.x += 100
                    self.image = pygame.transform.scale(load_image(f"crash_car{car.number}.png", colorkey=-1),
                                                        (100, 150))
                    board.is_playing = False

    def pl_number(self):
        if self.number < 2:
            self.number += 1
            self.image = pygame.transform.scale(load_image(f"car{self.number}.png", colorkey=-1), (90, 150))
            return True
        else:
            return False

    def set_three_d(self):
        if not board.three_d:
            self.image = pygame.transform.scale(load_image(f"car{self.number}.png", colorkey=-1), (90, 150))
        else:
            self.image = pygame.transform.scale(load_image(f"car{self.number}_3d.jpg", colorkey=-1), (90, 150))

    def mn_number(self):
        if self.number > 1:
            self.number -= 1
            self.image = pygame.transform.scale(load_image(f"car{self.number}.png", colorkey=-1), (100, 150))
            return True
        else:
            return False

    def clear_im(self):
        if board.three_d:
            self.image = pygame.transform.scale(load_image(f"car{self.number}_3d.jpg", colorkey=-1), (100, 100))
        else:
            self.image = pygame.transform.scale(load_image(f"car{self.number}.png", colorkey=-1), (100, 150))
        self.number_pos = random.randint(0, 4)
        self.rect.x = 10 + board.left + self.number_pos * 120
        self.rect.y = size[1] - 200


class Board:
    def __init__(self, width, height, three_d=True):
        self.block = 60  # высота разметки
        self.width = width
        self.height = height
        self.left = 150
        self.top = 0
        self.ball = 0
        self.is_playing = True
        self.pos_y = -self.block * 2
        self.level = 0
        self.speed = 100
        if three_d:
            self.three_d = not three_d
            self.set_stereo()
        self.font = pygame.font.Font(None, 20)
        self.st_pos = -self.block * 2

    def set_stereo(self):
        if self.three_d:
            self.three_d = False
            if size[0] > 900:
                self.left = (size[0] - 600) // 2
            self.pos_y = -self.height
        else:
            self.pos_y = 0.4 * self.height
            if self.left != 150:
                self.left = 150
            self.three_d = True
        try:
            car.set_three_d()
        except NameError:
            pass

    def render(self, y=0):
        pygame.draw.rect(screen, "#004d00", (0, 0, self.width, self.height))
        pygame.draw.rect(screen, (128, 128, 128),
                         (self.left, self.top, self.width - self.left * 2, self.height - self.top * 2))
        for i in range(1, 5):
            for j in range(0, size[1] // self.block + 2, 2):
                pygame.draw.rect(screen, "white", (self.left + (120 * i), self.pos_y + self.block * j, 10, self.block))
        self.pos_y += y
        if int(self.pos_y) - int(self.st_pos) >= self.block * 2:
            self.pos_y -= self.block * 2
            self.st_pos = self.pos_y
        all_sprites.draw(screen)
        pygame.draw.rect(screen, "blue", (size[0] * 0.9, 100, 90, 30))
        screen.blit(self.font.render("Меню", True, "red"), (size[0] * 0.9, 110))
        text = self.font.render(f"""Ваш счёт:{board.ball}""", True, "red")
        screen.blit(text, (size[0] * 0.9, 30))

    def three_d_render(self, y=0):
        pygame.draw.rect(screen, "#004d00", (0, 0, self.width, self.height))
        pygame.draw.polygon(screen, (128, 128, 128),
                            [(int(0.1 * self.width), self.height), (int(0.3 * self.width), int(0.4 * self.height)),
                             (int(0.7 * self.width), int(0.4 * self.height)), (int(0.9 * self.width), self.height)])
        for i in range(6):
            for j in range(-6, 8, 2):
                w = 0.4 * self.width + 0.055 * self.width * j
                w2 = self.width * 0.3 - 0.0275 * self.width * j
                if j < 0:
                    w = 0.4 * self.width
                    w2 = self.width * 0.3
                pygame.draw.rect(screen, (128, 128, 128),
                                 (w2, self.pos_y + j * 60,
                                  w, 60))
            pygame.draw.line(screen, "white", (
                board.width * 0.3 + 0.4 / 5 * self.width * i, self.height * 0.4),
                             (self.width * 0.1 + self.width * 0.8 / 5 * i,
                              self.height), 10)
        self.pos_y += y
        if int(self.pos_y) >= self.height:
            self.pos_y -= 0.6 * self.height
        #     self.st_pos = self.pos_y
        all_sprites.draw(screen)
        pygame.draw.rect(screen, "#38aecc", (0, 0, self.width, int(self.height * 0.4)))

        pygame.draw.rect(screen, "blue", (size[0] * 0.9, 100, 90, 30))
        screen.blit(self.font.render("Меню", True, "red"), (size[0] * 0.9, 110))
        text = self.font.render(f"""Ваш счёт: {board.ball}""", True, "red")
        screen.blit(text, (size[0] * 0.9, 30))

    def set_left_top(self, left, top):
        self.top = top
        self.left = left

    def set_ball(self, clear=None):
        if clear is None:
            self.ball += 1
        else:
            self.ball = 0
            self.is_playing = True
            if self.three_d:
                self.pos_y = 0.4 * self.width
            else:
                self.pos_y = -(size[1])

    def gener(self, l_d, l_r):
        if len(obstacle) == 0:
            obstacle.append(Obstacle())
            all_sprites.add(obstacle[-1])
        if len(obstacle) < 3 and random.randint(l_d, l_r) == 1:
            obstacle.append(Obstacle())
            all_sprites.add(obstacle[-1])

    def set_level(self, level=0):
        self.speed = 100 + (level * 200)
        self.level = level

    def set_hard(self, level=2):
        self.speed = 100 + (level * 200)
        self.level = level

    def set_midle(self, level=1):
        self.speed = 100 + (level * 200)
        self.level = level


board = Board(size[0], size[1])
car = Car()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, *grop, pos=None):
        super().__init__(*grop)
        self.width_k_height = 150 / 90
        self.number = random.randint(0, 2)
        if board.three_d:
            self.st_width = random.randint(5, 10)
            self.image = pygame.transform.scale(load_image(f"ob{self.number}_3d.png", colorkey=-1),
                                                (self.st_width, self.st_width * self.width_k_height))
        else:
            self.image = pygame.transform.scale(load_image(f"ob{self.number}.png", colorkey=-1), (90, 150))
            self.st_width = 40
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        fl = True
        if not board.three_d:
            while fl:
                fl = False
                self.rect.x = 10 + board.left + random.randint(0, 4) * 120
                self.x = self.rect.x
                if pos is None:
                    self.rect.y = random.randint(-250, -150)
                else:
                    self.rect.y = random.randint(40, size[1] - 100)
                self.y = self.rect.y
                for i in all_sprites:
                    if pygame.sprite.collide_mask(i, self):
                        fl = True
        else:
            while fl:
                fl = False
                self.rect.x = 10 + (size[0] * 0.3) + random.randint(0, 4) * (0.08 * size[0])
                self.x = self.rect.x
                self.rect.y = int(board.height * 0.4)
                self.y = self.rect.y
                for i in all_sprites:
                    if pygame.sprite.collide_mask(i, self):
                        fl = True

    def update(self, l_d, l_r, d):
        self.mask = pygame.mask.from_surface(self.image)
        car.mask = pygame.mask.from_surface(car.image)
        if board.is_playing and not pygame.sprite.collide_mask(self, car):
            if not board.three_d:
                self.y += d * board.speed
                self.rect.y = int(self.y)
            else:
                self.y += d * board.speed
                if self.rect.y < int(board.height * 0.4):
                    self.rect.y = int(board.height * 0.4)
                    self.y = self.rect.y
                if self.y - self.rect.y < 1:
                    return True
                self.st_width += 2 * (self.y - self.rect.y) * tg
                self.rect.y = int(self.y)
                if 100 > self.st_width:
                    self.image = pygame.transform.scale(load_image(f"ob{self.number}_3d.png", colorkey=-1),
                                                        (abs(int(self.st_width)),
                                                         abs(int(self.st_width * self.width_k_height))))
                    self.mask = pygame.mask.from_surface(self.image)
                self.rect.x = self.x
                if self.st_width > 25:
                    self.rect.y = int(self.y)
                all_sprites.draw(screen)
            board.gener(l_d, l_r)
            if self.y >= size[1]:
                del obstacle[obstacle.index(self)]
            return True
        return False


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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id               INTEGER NOT NULL
                     CONSTRAINT genres_pk PRIMARY KEY AUTOINCREMENT
                     UNIQUE
                     NOT NULL,
    username TEXT    NOT NULL,
    password TEXT    NOT NULL
);

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
        if self.check_username() and self.check_password(menu.password):
            bd = sqlite3.connect("rating_system.db")
            curr = bd.cursor()
            curr.execute("""DELETE FROM user""")
            curr.execute(f'''INSERT INTO user (id, username) VALUES (1, '{self.username}')''', )
            bd.commit()
            bd.close()
            menu.sing = False
            menu.username = self.username
            return "успешная авторизация"
        elif self.check_username():
            return "неверный пароль"
        if menu.password == "":
            return "uni"
        else:
            return "create new user"

    def create_user(self):
        bd = sqlite3.connect("rating_system.db")
        curr = bd.cursor()
        curr.execute(f'''INSERT INTO users (username, password) VALUES ( '{self.username}', '{menu.password}')''', )
        bd.commit()
        bd.close()
        self.sistem()
        menu.sing = False

    def sing_out(self):
        global username, menu
        username = None
        self.username = None
        menu = Menu()
        car.clear_im()
        board.set_level(0)
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

    def check_password(self, password):
        self.connection = sqlite3.connect("rating_system.db")
        self.cursor = self.connection.cursor()

        res = self.cursor.execute(f"""SELECT password FROM users
                                  WHERE username = '{self.username}'""").fetchone()
        self.connection.close()
        if res[0] == self.set_password(password):
            return True
        return False

    def check_username(self):
        self.connection = sqlite3.connect("rating_system.db")
        self.cursor = self.connection.cursor()

        res = self.cursor.execute(f"""SELECT * FROM users
                                  WHERE username = '{self.username}'""").fetchone()
        self.connection.close()
        if res is None:
            return False
        return True

    def set_password(self, password):
        return password


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
    close_btn = Button(color_text="white", color="red", x=int(size[0] - 150), y=100, text="Закрыть", width=30,
                       height=100,
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
        self.password = ""
        if self.username is None:
            self.sing = True
            self.password2 = False
        else:
            self.sing = False

    def render(self, buttons):
        fon = pygame.transform.scale(load_image('cars2.jpg'), (size[0], size[1]))
        screen.blit(fon, (0, 0))
        font2 = pygame.font.Font(None, 25)
        screen.blit(font2.render(str(self.username), True, "#a35713"), (0.9 * size[0], 50))
        screen.blit(font2.render("Вы Вошли как:", True, "#a35713"), (0.9 * size[0], 20))
        fon = pygame.transform.scale(load_image(f"men{car.number}.jpg", colorkey=-1), (353, 200))
        screen.blit(fon, (size[0] * 0.45, size[1] * 0.7))
        for button in buttons:
            button.render()
        if board.level == 0:
            pygame.draw.circle(screen, 'green', (130, 40), 10)
        elif board.level == 1:
            pygame.draw.circle(screen, 'green', (130, 80), 10)
        else:
            pygame.draw.circle(screen, 'green', (130, 110), 10)

    def sing_up(self):
        screen.fill((228, 189, 114))
        k = 484 / 600
        fon = pygame.transform.scale(load_image('font.jpg'), (k * size[1], size[1]))
        screen.blit(fon, (size[0] * 0.25, 0))
        font = pygame.font.Font(None, 50)
        text2 = font.render("Введите своё имя", True, "red")
        screen.blit(text2, (size[0] * 0.5, 200))
        text_surf = font.render(self.text, True, (255, 0, 0))
        screen.blit(text_surf, text_surf.get_rect(center=screen.get_rect().center))

    def write_password(self, text="", buttons=list()):
        screen.fill((228, 189, 114))
        k = 484 / 600
        fon = pygame.transform.scale(load_image('font.jpg'), (k * size[1], size[1]))
        screen.blit(fon, (size[0] * 0.25, 0))
        font = pygame.font.Font(None, 50)
        text2 = font.render("Введите пароль", True, "red")
        screen.blit(text2, (size[0] * 0.5, 200))
        screen.blit(font.render(text, True, "red"), (size[0] * 0.5, size[1] * 0.8))
        text_surf = font.render(self.password, True, (255, 0, 0))
        screen.blit(text_surf, text_surf.get_rect(center=screen.get_rect().center))
        if text != '':
            for but in buttons:
                but.render()

    def updata(self, event):
        if self.sing:
            if event.key == pygame.K_RETURN and self.text.strip() != "":
                global username
                self.text = self.text.strip()
                table.username = self.text
                self.password2 = True
                return table.sistem()
            elif event.key == pygame.K_BACKSPACE:
                if self.password2:
                    self.password = self.password[:-1]
                else:
                    self.text = self.text[:-1]
                return "uni"
            elif event.unicode != "":
                if self.password2:
                    self.password += event.unicode
                else:
                    self.text += event.unicode
                return "uni"

    def watching_results(self):
        fon = pygame.transform.scale(load_image('cars2.jpg'), (size[0], size[1]))
        screen.blit(fon, (0, 0))
        pygame.draw.rect(screen, "#f48932", (30, 30, size[0] - 60, size[1] - 60))
        pygame.draw.rect(screen, "#a35713", (50, 50, size[0] - 100, size[1] - 100))
        font2 = pygame.font.Font(None, 20)
        font = pygame.font.Font(None, 50)
        screen.blit(font.render(f"Доска почёта", True, "white"),
                    (size[0] * 0.5, 100))
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
    y_n = [Button(text="yes", y=int(size[1] * 0.7), command=table.create_user, x=int(size[0] * 0.5)),
           Button(text="no", command=table.sing_out, y=int(size[1] * 0.7), x=int(size[0] * 0.6))]
    buttons = [
        Button(color="grey", color_text="white", height=45, width=30, command=car.pl_number, text=">",
               y=int(0.8 * size[1]), x=int(size[0] * 0.7) + 70),
    ]
    run = True
    mn_btn = Button(color="grey", color_text="white", height=45, width=30, command=car.mn_number, text="<",
                    y=int(0.8 * size[1]),
                    x=int(size[0] * 0.7) - 400)
    buttons.append(mn_btn)
    pygame.mixer.music.pause()
    button_out = Button(color="#a35713", color_text="white", x=int(0.9 * size[0]), y=100, height=100, width=30,
                        command=table.sing_out,
                        text="Выход")
    buttons.append(button_out)
    start_btn = Button(color="#a35713", color_text="white", x=int(size[0] * 0.3), y=int(size[1] * 0.7), height=100,
                       width=30,
                       command=main, text="Старт")
    pokaz_btn = Button(color="#a35713", color_text="white", x=(size[1] // 2), y=190, height=150, width=60,
                       command=results_look, text="Доска Почета")
    buttons.append(start_btn)
    buttons.append(pokaz_btn)
    midle_btn = Button(text="Средний", color="#a35713", color_text="white", command=board.set_midle, x=20, y=60,
                       width=30, height=100)
    hard_btn = Button(text="cложный", color="#a35713", color_text="white", command=board.set_hard, x=20, y=90,
                      width=30, height=100)
    lite_btn = Button(text="легкий", color="#a35713", color_text="white", command=board.set_level, x=20, y=30,
                      width=30, height=100)
    buttons.append(lite_btn)
    buttons.append(midle_btn)
    buttons.append(hard_btn)
    text = ''
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                fl = menu.updata(event)
                print(fl)
                if fl == "create new user":
                    text = "create new user?"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not (menu.username is None):
                    for button in buttons:
                        button.update(event)
                else:
                    for b in y_n:
                        b.update(event)

        if menu.username is None:
            if not menu.password2:
                menu.sing_up()
            else:
                menu.write_password(text, y_n)
        else:
            menu.render(buttons)
        pygame.display.update()
    return None


def main():
    pygame.mixer.music.load("data/pov.mp3")
    global running, all_sprites, board
    l_d = -3000  # рандомный диапазон создаем машинку когда randint == 2
    l_r = 3000
    board.is_playing = True
    car.clear_im()
    tick = pygame.time.Clock()
    chet = pygame.USEREVENT + 1
    pygame.time.set_timer(chet, 2000)
    all_sprites.add(car)
    all_sprites.draw(screen)
    running = True
    pygame.mixer.music.play(-1)
    button = [
        Button(img="camera.png", text="", x=10, y=10, width=40, height=30, command=board.set_stereo, color_key=-1)]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == 768:
                car.update(event)
            if event.type == chet:
                board.set_ball()
                if board.ball % 3 == 0:
                    board.speed = board.speed + 30
                    if l_d > -200:
                        l_d += 200
                    if l_r < 200:
                        l_r -= 200
                if board.ball == 60:
                    pygame.mixer.music.load("data/Super_bal.MP3")
                    pygame.mixer.music.play(-1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in button:
                    i.update(event)
                if size[0] * 0.9 <= event.pos[0] <= size[0] * 0.9 + 90 and 100 <= event.pos[1] <= 130:
                    obstacle.clear()
                    all_sprites = pygame.sprite.Group()
                    board.set_ball(clear=-1)
                    start_game()
                    return None
        d = tick.tick() / 1000
        for ob in obstacle:
            ob: Obstacle
            if not ob.update(l_d, l_r, d):
                board.is_playing = False
                if board.three_d:
                    board.three_d_render(d * board.speed)
                else:
                    board.render(d * board.speed)
                pygame.mixer.music.pause()
                font = pygame.font.Font(None, 50)
                car.image = pygame.transform.scale(load_image(f"crash_car{car.number}.png", colorkey=-1), (100, 150))
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
        board.gener(l_d, l_r)
        if board.three_d:
            board.three_d_render(d * int(board.speed * 1.3))
        else:
            board.render(d * int(board.speed * 1.3))
        for b in button:
            b.render()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    start_game()
