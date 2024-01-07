import pygame

pygame.init()

pygame.mixer.music.load("data/DDT.mp3")

W, H = 500, 300
sc = pygame.display.set_mode((W, H))

clock = pygame.time.Clock()
FPS = 60
pygame.mixer.music.play(-1)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    clock.tick(FPS)