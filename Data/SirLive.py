import pygame
pygame.init()

size = (600,400)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
x = 10
y = 20
WHITE = (255,255,255)
BLACK = (0,0,0)
background_pic = pygame.image.load("LevelView.png").convert()
sir_live_walk1 = pygame.image.load("FigureRightSide.png")
sir_live_walk2 = pygame.image.load("FigureRightSideStill.png")
sir_live_walk1 = pygame.transform.scale(sir_live_walk1, (41,50))
sir_live_walk2 = pygame.transform.scale(sir_live_walk2, (41,50))
sir_live_pic = sir_live_walk1
sir_live_dirc = "Right"
done = False
first_plat = True
second_plat = False
third_plat = False
foot = False
passed_edge = False
in_air = False
jump = False
walking = 0
allow_jump = True
jump_counter = 0

while not done:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    if event.type == pygame.KEYDOWN:

        if event.key == pygame.K_d:
            if sir_live_dirc == "Left":
                sir_live_pic = sir_live_walk1
            sir_live_dirc = "Right"
            x = x + 2

        if event.key == pygame.K_a:
            if sir_live_dirc == "Right":
                sir_live_pic = pygame.transform.flip(sir_live_pic, 1,0)
            sir_live_dirc = "Left"
            x = x - 2

        if event.key == pygame.K_r:
            x = 10
            y = 20

        if event.key == pygame.K_SPACE:
            if jump_counter < 16:
                if allow_jump:
                    jump = True

    if y > 19 and y < 29:
        first_plat = True
        in_air = False

    elif y > 150 and y < 171:
        in_air = False
        first_plat = False
        second_plat = True

    elif y > 279 and y < 300:
        in_air = False
        second_plat = False
        third_plat = True

    else:
        first_plat = False
        second_plat = False
        third_plat = False
        in_air = True

    if in_air:
        passed_edge = True
    elif x >= 382 and first_plat:
        passed_edge = True
    elif x <= 164 and second_plat:
        passed_edge = True
    elif x >= 382 and third_plat:
        passed_edge = True

    else:
        passed_edge = False
    if jump:
        for i in range(0,4, 1):
            if i == 3:
                jump = False
                jump_counter += 1
            y -= i

    elif passed_edge:
        allow_jump = False
        jump_counter = 0
        for i in range(0,3, 1):
            y += i
    else:
        allow_jump = True

    screen.blit(background_pic, (0,0))
    screen.blit(sir_live_pic, (x,y))
    pygame.draw.rect(screen, BLACK,(0,69,400,10), 0)
    pygame.draw.rect(screen, BLACK,(600,200,-400,10), 0)
    pygame.draw.rect(screen, BLACK,(0,331,400,10), 0)
    pygame.display.flip()
    clock.tick(90)
pygame.quit()
