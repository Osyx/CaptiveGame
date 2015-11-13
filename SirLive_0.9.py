################################################################################
##                                                                            ##
##                                  Captive                                   ##
##                          Made by: Oscar Falkman                            ##
##                                                                            ##
################################################################################

################################################################################
##
##  Add: Coins, actual levels, restart.
##  Fix: Platforms are off when lvl up. (Perhaps not necessary)
##  Fix: Try to split the code into modules.
##  Replace: Nothing
##  *Tft = Taken from the internet
##
################################################################################

#############################      Import Area      ############################
# Import modules and initialize them.
from ctypes import windll
import pygame, random, math, time, win32gui, win32con, os
pygame.init()

##############################    Function Area   ##############################

####   Tft* internet. ####
#   http://bit.ly/1EecwN6
def search_for_window():
    global captive
    toplist = []
    winlist = []

# Get all window ids'
    def enum_callback(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

# Searching for which id the window has, so I later can modify it
    win32gui.EnumWindows(enum_callback, toplist)
    captive = [(hwnd, title) for hwnd, title in winlist if 'captive' in title.lower()]
    captive = captive[0]
    win32gui.SetForegroundWindow(captive[0])

def minimize_window():
    win32gui.ShowWindow(captive[0], win32con.SW_MINIMIZE)

def maximize_window():
    win32gui.ShowWindow(captive[0], win32con.SW_MAXIMIZE)
####    Tft internet End    ####

# Define functions

def difficulty_popup():
    global speed
    minimize_window()
    diff = str(input("Choose between easy, medium or hard: ").lower())
    maximize_window()
    if diff == "easy":
        print("Easy")
        speed = [1, "Easy"]

    elif diff == "medium":
        speed = [2, "Medium"]
        print("Medium")

    elif diff == "hard":
        print("Hard")
        speed = [3, "Hard"]

    elif diff == "extreme":
        print("Extreme")
        speed = [10, "Dafuq"]

    else:
        print("Unvalid user input, defaulting to easy")
        speed = [1, "Easy"]

def start_screen_keys():
    global done, game_running, game_over, party_mode
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
            game_over = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                game_running = True
                difficulty_popup()

            # Test it ;) Press P instead of space on startscreen
            if event.key == pygame.K_p:
                print("PARTY MODE ACTIVATED")
                party_mode = True
                difficulty_popup()
                game_running = True


def start_screen():
    global press_start
    screen.blit(intro_pic,(0,0))
    if press_start >= 90:
        screen.blit(start_text, (249, 300))
        if press_start > 180:
            press_start = 0
    screen.blit(p_text, (215, 320))
    pygame.display.flip()
    clock.tick(90)
    press_start += 1

def keypresses():
    global d_pressed, a_pressed, space_pressed, game_running, done, game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            game_over = False
            done = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                d_pressed = True

            if event.key == pygame.K_LEFT:
                a_pressed = True

            if event.key == pygame.K_SPACE:
                space_pressed = True

            if event.key == pygame.K_r:
                game_over = False

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT:
                d_pressed = False

            if event.key == pygame.K_LEFT:
                a_pressed = False

            if event.key == pygame.K_SPACE:
                space_pressed = False


def keypresses_actions():
    global d_pressed, a_pressed, space_pressed, sir_live_dirc, sir_live_pic, jump, x
    if d_pressed:
        if sir_live_dirc == "Left":
                sir_live_pic = sir_live_walk1
        else:
            pass
        sir_live_dirc = "Right"
        if x <= 559:
            x = x + 2

    if a_pressed:
        if sir_live_dirc == "Right":
                sir_live_pic = pygame.transform.flip(sir_live_pic, 1,0)
        else:
            pass
        sir_live_dirc = "Left"
        if x >= 1:
            x = x - 2

    if space_pressed:
        if jump_counter < 16:
                if allow_jump:
                    jump = True
        else: pass

def set_window_on_top():
    global window_x, window_y, party_mode
    if party_mode:
        window_x = x + 100
        window_y = y - 20

####   Tft internet. ####
    SetWindowPos = windll.user32.SetWindowPos
    SetWindowPos(pygame.display.get_wm_info()['window'], -1, window_x, window_y, 0, 0, 0x0001)
####   Tft internet End ####

def level_check():
    global new_level, window_y, level, world, time_start, speed
    if new_level:
        window_y = 150
        level = int(level)
        level += 1
        speed[0] += 0.20
        time_start = time.time()
        new_level = False

    if int(level) >= 10:
        level = 1
        world = int(world)
        world += 1

def level_screen(level, world):
    global wait, coins, health
    while wait < 200:
        screen.blit(pre_level_pic, (0,0))
        level_text = font3.render((str(level)),True,WHITE)
        world_text = font3.render((str(world)),True,WHITE)
        coin_text = font3.render((str(coins)),True,YELLOW)
        health_text = font3.render(str((health)),True,RED)
        screen.blit(coin_text, (250, 179))
        screen.blit(health_text, (250, 242))
        screen.blit(level_text, (375, 110))
        screen.blit(world_text, (430,110))
        flip_screen()
        wait += 1

def ingame_clock():
    global done, counting_time, game_over, game_time_start, time_start, game_over, game_running
    time_now = time.time()
    game_time_start = (time_now - time_start) *10
    counting_time = 300 - game_time_start
    if (counting_time <= 0):
        game_running = False
        game_over = True

def placement_detection():
    global y, x, first_plat, second_plat, third_plat, in_air, passed_edge, new_level
    if y > platform1_y - 50 and y < platform1_y - 40:
                first_plat = True
                in_air = False

    elif y > platform2_y - 50 and y < platform2_y - 40:
        in_air = False
        first_plat = False
        second_plat = True

    elif y > platform3_y - 50 and y < platform3_y - 40:
        in_air = False
        second_plat = False
        third_plat = True

    elif y > 400:
        x = 10
        y = platform1_y - 50
        new_level = True

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

def vertical_movement():
    global jump, passed_edge, jump_counter, allow_jump, y
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

def check_if_dead():
    global x, y, enemy_shots_location, game_running, game_over, health, show_ouch
    if len(enemy_shots_location) != 0:
                for i in range (len(enemy_shots_location)):
                    if (i == len(enemy_shots_location)):
                            i = 0
                    if enemy_shots_location[i][0] >= x+10 and enemy_shots_location[i][0] <= x + 23:
                        if enemy_shots_location[i][1] >= y+9.5 and enemy_shots_location[i][1] <= y + 50:
                            del enemy_shots_location[i]
                            show_ouch = True
                            health -= 1
                            if health <= 0:
                                game_running = False
                                game_over = True

def enemy_idle_management():
    global enemy_wait, draw_shot, speed
    if enemy_wait >= 100:
        draw_shot = True
        enemy_wait = 0
    enemy_wait += speed[0]

def enemy_shots():
    global draw_shot, enemy_shots_location, delete, delete_value, speed
    if draw_shot:
        haha = [enemy_x + 20, enemy_y + 25]
        enemy_shots_location.append(haha)
        draw_shot = False
    if delete:
        del enemy_shots_location[delete_value]
        delete = False
    else:
        pass
    for k in range(len(enemy_shots_location)):
        if len(enemy_shots_location) > 0:
            if enemy_shots_location[k][0] >= 600:
                delete_value = k
                delete = True
            else:
                enemy_shots_location[k][0] = enemy_shots_location[k][0] + speed[0]
        else:
            pass

def draw_timer():
    global counting_time, health, coins, level, world
    if counting_time >= 100:
        split_x = 3

    elif counting_time < 100 and counting_time >= 10:
        split_x = 2

    else:
        split_x = 1

    counting_time = str((counting_time))
    counting_time = str((counting_time[0:split_x]))
    coin_text = font.render((str(coins)),True,YELLOW)
    level_text = font4.render((str(level)),True,WHITE)
    world_text = font4.render((str(world)),True,WHITE)
    level = str(level)
    world = str(world)
    health_text = font.render(str((health)),True,RED)
    timer_text = font.render((counting_time),True,WHITE)
    screen.blit(timer_text, (45, 2))
    screen.blit(coin_text, (537, 2))
    screen.blit(health_text, (575, 2))
    screen.blit(level_text, (330, 2))
    screen.blit(world_text, (350, 2))

def draw_background():
    screen.blit(background_pic, (0,0))

def draw_objects():
    global enemy_shots_location, delete, delete_value, show_ouch, ouch_wait
    screen.blit(sir_live_pic, (x,y))
    if show_ouch:
        screen.blit(ouch_text, (x + 42, y + 1))
        ouch_wait -= 1
        if ouch_wait <= 0:
            show_ouch = False
            ouch_wait = 10
    if len(enemy_shots_location) != 0:
        for shots in range(len(enemy_shots_location)):
            pygame.draw.ellipse(screen, RED, [enemy_shots_location[shots][0],enemy_shots_location[shots][1],5,5], 0)
    screen.blit(enemy1, (enemy_x, enemy_y))

def draw_platforms():
    pygame.draw.rect(screen, BLACK,(0, platform1_y,400,10), 0)
    pygame.draw.rect(screen, BLACK,(600,platform2_y,-400,10), 0)
    pygame.draw.rect(screen, BLACK,(0,platform3_y,400,10), 0)

def check_if_gameover():
    global game_over
    while game_over:
        level_text = font5.render((str(level)),True,WHITE)
        world_text = font5.render((str(world)),True,WHITE)
        coin_text = font5.render((str(coins)),True,YELLOW)
        keypresses()
        screen.blit(game_over_screen, (0,0))
        screen.blit(coin_text, (312, 233))
        screen.blit(level_text, (350, 208))
        screen.blit(world_text, (460,208))
        flip_screen()

def print_result():
    if not party_mode:
        print("Result: You made it to level", level, "on world", world, "playing on", speed[1])
    else:
        print("Result: You made it to level", level, "on world", world, "playing on", speed[1], "in party mode!")

def save_result():
    #Write score visible to user in All_Scores.txt
    your_name = input("Your name? Will be used for All_Scores.txt: ")
    if not party_mode:
        points_write = "Result:", your_name, "made it to level", level, "on world", world, "playing on", speed[1],
    else:
        points_write = "Result:", your_name, "made it to level", level, "on world", world, "playing on", speed[1], 'in party mode!'
    with open ("All_Scores.txt", "a") as HighScores:
        HighScores.write(str(points_write)[1:200])
        HighScores.write("\n")
        HighScores.close

def flip_screen():
    pygame.display.flip()
    clock.tick(90)

################################    Load Area   ################################

# Setup game enviroment
size = (600,400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Captive")
current_path = os.path.dirname(os.path.realpath(__file__))

# Setup game clock.
clock = pygame.time.Clock()

# Define colorvariables
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (242,255,0)

# Import fonts
font = pygame.font.SysFont('Calibri', 15, True, False)
font2 = pygame.font.SysFont('Calibri', 20, True, False)
font3 = pygame.font.SysFont('Calibri', 60, True, False)
font4 = pygame.font.SysFont('Calibri', 16, True, False)
font5 = pygame.font.SysFont('Calibri', 25, True, False)

# Render static text
start_text = font2.render("Press Space",True,WHITE)
p_text = font4.render("Press P for 'Party Mode'",True,WHITE)
ouch_text = font2.render("Ouch!",True,WHITE)

# Set the images paths
intropic_path = current_path + "\Data\CaptiveStart.png"
levelview_path = current_path + "\Data\LevelView.png"
prelevelscreen_path = current_path + "\Data\PreLevelScreen.png"
figurerightside_path = current_path + "\Data\FigureRightSide.png"
figurerightsidestill_path = current_path + "\Data\FigureRightSideStill.png"
gameover_path = current_path + "\Data\GameOver.png"
enemyv2_path= current_path + "\Data\Enemyv2.png"

# Load images into memory
intro_pic = pygame.image.load(intropic_path).convert()
background_pic = pygame.image.load(levelview_path).convert()
pre_level_pic = pygame.image.load(prelevelscreen_path).convert()
sir_live_walk1 = pygame.image.load(figurerightside_path)
sir_live_walk2 = pygame.image.load(figurerightsidestill_path)
game_over_screen = pygame.image.load(gameover_path).convert()
enemy1 = pygame.image.load(enemyv2_path)

# Set the program icon
pygame.display.set_icon(enemy1)

#Flip image so it faces the other way
enemy1 = pygame.transform.flip(enemy1, 1,0)

# Downscale character sprites
sir_live_walk1 = pygame.transform.scale(sir_live_walk1, (41,50))
sir_live_walk2 = pygame.transform.scale(sir_live_walk2, (41,50))

###############################    Define Area   ###############################

# Define variables
window_x = 400
window_y = 150
sir_live_dirc = "Right"
platform1_y = 131
platform2_y = platform1_y + 131
platform3_y = platform2_y + 131
x = 10
y = platform1_y - 49
enemy_x = 20
enemy_y = platform2_y - 55
speed = [1, "Easy"]
health = 3
coins = 0
jump_counter = 0
press_start = 90
wait = 0
enemy_wait = 100
ouch_wait = 10
counting_time = 0
game_time_start = 300
delete_value = 0
level = 1
world = 1

# Start the clock
time_start = time.time()

# Set first "sprite" image
sir_live_pic = sir_live_walk1

# Define lists
enemy_shots_location = [[550, 232], [450, 232], [350, 232], [250, 232], [150, 232]]

# Define Booleans
allow_jump = True
enemies_missing = True
first_plat = True
new_level = False
party_mode = False
show_ouch = False
draw_shot = False
game_over = False
delete = False
d_pressed = False
a_pressed = False
space_pressed = False
game_running = False
done = False
second_plat = False
third_plat = False
foot = False
passed_edge = False
in_air = False
jump = False

################################    Game Loop   ################################
while not done:
    search_for_window()
    start_screen_keys()
    start_screen()
    while game_running:

################################    Event Area   ###############################
        keypresses()
        keypresses_actions()

##############################    Function Area   ##############################
        set_window_on_top()
        level_check()
        enemy_idle_management()
        enemy_shots()
        placement_detection()
        check_if_dead()
        vertical_movement()
        ingame_clock()

################################    Draw Area   ################################
        level_screen(level, world)
        draw_background()
        draw_timer()
        draw_objects()
        draw_platforms()
        flip_screen()

##############################   End of Game Loop   ############################
    check_if_gameover()

################################    Exit Area   ################################
pygame.quit()
print_result()
save_result()