import random, pygame, sys
from pygame.locals import *
from random import randint
import copy
import math
import time
#defining the window size and other different specifications of the window
FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
boxsize = min(WINDOWWIDTH,WINDOWHEIGHT)//4;
margin = 5
thickness = 0
start_time=0
#defining the RGB for various colours used
WHITE= (255, 255, 255)
BLACK= (  0,   0,   0)
RED = (255,   0,   0)
GREEN= (  0, 255,   0)
DARKGREEN= (  0, 155,   0)
DARKGRAY= ( 40,  40,  40)
LIGHTSALMON=(255, 160, 122)
ORANGE=(221, 118, 7)
LIGHTORANGE=(227,155,78)
CORAL=(255, 127, 80)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 0, 150)
colorback=(189,174,158)
colorblank=(205,193,180)
colorlight=(249,246,242)
colordark=(119,110,101)

fontSize=[100,85,70,55,40]

dictcolor1={
0:colorblank,
2:(238,228,218),
4:(237,224,200),
8:(242,177,121),
16:(245,149,99),
32:(246,124,95),
64:(246,95,59),
128:(237,207,114),
256:(237,204,97),
512:(237,200,80),
1024:(237,197,63),
2048:(237,194,46),
4096:(237,190,30),
8192:(239,180,25) }

dictcolor2={
2:colordark,
4:colordark,
8:colorlight,
16:colorlight,
32:colorlight,
64:colorlight,
128:colorlight,
256:colorlight,
512:colorlight,
1024:colorlight,
2048:colorlight,
4096:colorlight,
8192:colorlight }
BGCOLOR = LIGHTORANGE
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

TABLE=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

def main():
    global FPSCLOCK, screen, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('2048')

    showStartScreen()

    while True:
        runGame(TABLE)
        gameover()

def startGameTimer():
    global start_time
    start_time = pygame.time.get_ticks()  # Set initial time to 5 minutes

def getGameTime():
    return pygame.time.get_ticks() - start_time

def openTutorial():
    tutorial_text = [
         "2048 Game Tutorial",
        "",
        "Welcome to the 2048 game tutorial!",
        "The goal is to slide tiles on a grid to combine them and",
        "create a tile with the number 2048.",
        "Use the arrow keys to move the tiles in the desired direction.",
        "Tiles with the same number will merge when they collide.",
        "The game ends when there are no more possible moves.",
        "",
        "Enjoy playing in Dark Mode by clicking 'DARKMODE'!",
        "If you can't clear the game within 5 minutes, the game will",
        "end.",
        "",
        "Have fun playing!",
    ]
    tutorial_font = pygame.font.Font('freesansbold.ttf', 19)
    
    while True:
        screen.fill(BGCOLOR)
        
        for i, line in enumerate(tutorial_text):
            line_surface = tutorial_font.render(line, True, WHITE)
            line_rect = line_surface.get_rect()
            line_rect.topleft = (50, 50 + i * 30)
            screen.blit(line_surface, line_rect)

        createButton("BACK", 80, 540, 480, 80, showStartScreen)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    showStartScreen()
                return
            
def showTimer():
    remaining_time = max(0, 5 * 60 - getGameTime() // 1000)  # Calculate remaining time
    timer_message = f'Time: {remaining_time} seconds'
    timer_font = pygame.font.Font('freesansbold.ttf', 20)
    timer_surf = timer_font.render(timer_message, True, WHITE)
    timer_rect = timer_surf.get_rect()
    timer_rect.topleft = (10, 10)
    screen.blit(timer_surf, timer_rect)

def createButton(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # DARKMODE가 활성화되었는지 확인
    dark_mode_active = BGCOLOR == BLACK

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if dark_mode_active:
            pygame.draw.rect(screen, BLACK, (x, y, width, height))
        else:
            pygame.draw.rect(screen, LIGHTBLUE, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        if dark_mode_active:
            pygame.draw.rect(screen, DARKGRAY, (x, y, width, height))
        else:
            pygame.draw.rect(screen, BLUE, (x, y, width, height))

    smallText = pygame.font.Font('freesansbold.ttf', 50)
    text_color = WHITE
    TextSurf = smallText.render(text, True, text_color)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(TextSurf, TextRect)

def showStartScreen():
    global BGCOLOR
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('2048', True, WHITE, ORANGE)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_RETURN:
                    return

        screen.fill(BGCOLOR)
        display_rect = pygame.transform.rotate(titleSurf1, 0)
        rectangle = display_rect.get_rect()
        rectangle.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 8)
        screen.blit(display_rect, rectangle)

        createButton("NEW GAME", 80, 180, 480, 80, newGame)
        createButton("TUTORIAL", 80, 300, 480, 80, openTutorial)
        createButton("QUIT", 80, 420, 480, 80, terminate)
        createButton("DARKMODE", 80, 540, 480, 80, lambda: toggleDarkMode(activate_dark_mode=True))  # activate_dark_mode를 True로 설정

        if checkForKeyPress():
            return

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def toggleDarkMode(activate_dark_mode=True):
    global BGCOLOR, dictcolor1, dictcolor2
    if activate_dark_mode:
        if BGCOLOR == BLACK:
            BGCOLOR = LIGHTORANGE
            dictcolor1[0] = colorblank
            dictcolor2[2] = colordark
            dictcolor2[4] = colordark
            # 필요한 경우 다른 색상 변경 추가
        else:
            BGCOLOR = BLACK
            dictcolor1[0] = (0, 0, 0)
            dictcolor1[2] = (40, 40, 40)
            dictcolor1[4] = (80, 80, 80)
            dictcolor1[8] = (120, 120, 120)
            dictcolor1[16] = (160, 160, 160)
            dictcolor1[32] = (51, 0, 25)
            dictcolor1[64] = (0, 60, 0)
            dictcolor1[128] = (0, 0, 60)
            dictcolor1[256] = (0, 64, 64)
            dictcolor1[512] = (102, 51, 0)
            dictcolor1[1024] = (51, 0, 102)
            dictcolor1[2048] = (0, 0, 0)
            dictcolor1[4096] = (0, 0, 0)
            dictcolor1[8192] = (0, 0, 0)
            dictcolor2[2] = colorlight
            dictcolor2[4] = colorlight

    showStartScreen()
def newGame():
    runGame(TABLE)

def randomfill(TABLE):
    # search for zero in the game table and randomly fill the places
    flatTABLE = sum(TABLE,[])
    if 0 not in flatTABLE:
        return TABLE
    empty=False
    w=0
    while not empty:
        w=randint(0,15)
        if TABLE[w//4][w%4] == 0:
            empty=True
    z=randint(1,5)
    if z==5:
        TABLE[w//4][w%4] = 4
    else:
        TABLE[w//4][w%4] = 2
    return TABLE

def gameOver(TABLE):
    # returns False if a box is empty or two boxes can be merged
    x = [-1, 0, 1, 0 ]
    y = [0 , 1, 0, -1]
    for pi in range(4):
        for pj in range(4):
            if TABLE[pi][pj] == 0:
                return False
            for point in range(4):
                if pi+x[point] > -1 and pi+x[point] < 4 and pj+y[point] > -1 and pj+y[point] < 4 and TABLE[pi][pj] == TABLE[pi+x[point]][pj+y[point]]:
                    return False
    return True

def showGameOverMessage():
# to show game over screen
    titleFont = pygame.font.Font('freesansbold.ttf', 60)
    titleSurf1 = titleFont.render('Game Over', True, WHITE, ORANGE)
    showMainMenu()

    while True:
        screen.fill(BGCOLOR)
        display_rect = pygame.transform.rotate(titleSurf1, 0)
        rectangle = display_rect.get_rect()
        rectangle.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        screen.blit(display_rect, rectangle)

        showMainMenu()
        pygame.display.update()
        if checkForKeyPress():
            if len(pygame.event.get()) > 0:
                main()
        FPSCLOCK.tick(FPS)
def showGameOverMessageWithTime():
    # 게임 오버 메시지 표시 코드는 그대로 유지

    # 게임 오버 메시지 아래에 경과된 시간 표시
    elapsed_time = getGameTime() // 1000  # 밀리초를 초로 변환
    time_message = f'Time Over'
    time_font = pygame.font.Font('freesansbold.ttf', 30)
    time_surf = time_font.render(time_message, True, WHITE)
    time_rect = time_surf.get_rect()
    time_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 50)
    screen.blit(time_surf, time_rect)

    showMainMenu()
    pygame.display.update()
    time.sleep(3)  # 3초 동안 메시지 표시 후 종료
    main()
def showMainMenu():
# to display main menu
    pressKeySurf = BASICFONT.render('Press a key for main menu', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 250, WINDOWHEIGHT - 30)
    screen.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    #checking if a key is pressed or not
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def show(TABLE):
    #showing the table
    screen.fill(colorback)
    myfont = pygame.font.SysFont("Arial", 60, bold=True)
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, dictcolor1[TABLE[i][j]], (j*boxsize+margin,
                                              i*boxsize+margin,
                                              boxsize-2*margin,
                                              boxsize-2*margin),
                                              thickness)
            if TABLE[i][j] != 0:
                order=int(math.log10(TABLE[i][j]))
                myfont = pygame.font.SysFont("Arial", fontSize[order] , bold=True)
                label = myfont.render("%4s" %(TABLE[i][j]), 1, dictcolor2[TABLE[i][j]] )
                screen.blit(label, (j*boxsize+2*margin, i*boxsize+9*margin))

    showTimer()            
    pygame.display.update()

def runGame(TABLE):
    TABLE = randomfill(TABLE)
    TABLE = randomfill(TABLE)
    show(TABLE)
    startGameTimer()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                print("quit")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                desired_key = None
                if event.key == pygame.K_UP:
                    desired_key = "w"
                elif event.key == pygame.K_DOWN:
                    desired_key = "s"
                elif event.key == pygame.K_LEFT:
                    desired_key = "a"
                elif event.key == pygame.K_RIGHT:
                    desired_key = "d"

                if desired_key:
                    new_table = key(desired_key, copy.deepcopy(TABLE))
                    if new_table != TABLE:
                        TABLE = randomfill(new_table)
                        show(TABLE)
                    if gameOver(TABLE):
                        showGameOverMessage()

        show(TABLE)  # Move the show function outside the event loop to continuously update the display

        remaining_time = max(0, 5 * 60 - getGameTime() // 1000)
        if remaining_time == 0:
            showGameOverMessageWithTime()
            running = False

        FPSCLOCK.tick(FPS)



def key(DIRECTION,TABLE):
    if   DIRECTION =='w':
        for pi in range(1,4):
            for pj in range(4):
                if TABLE[pi][pj] !=0: TABLE=moveup(pi,pj,TABLE)
    elif DIRECTION =='s':
        for pi in range(2,-1,-1):
            for pj in range(4):
                if TABLE[pi][pj] !=0: TABLE=movedown(pi,pj,TABLE)
    elif DIRECTION =='a':
        for pj in range(1,4):
            for pi in range(4):
                if TABLE[pi][pj] !=0: TABLE=moveleft(pi,pj,TABLE)
    elif DIRECTION =='d':
        for pj in range(2,-1,-1):
            for pi in range(4):
                if TABLE[pi][pj] !=0: TABLE=moveright(pi,pj,TABLE)
    return TABLE

def movedown(pi,pj,T):
    justcomb=False
    while pi < 3 and (T[pi+1][pj] == 0 or (T[pi+1][pj] == T[pi][pj] and not justcomb)):
        if T[pi+1][pj] == 0:
            T[pi+1][pj] = T[pi][pj]
        elif T[pi+1][pj]==T[pi][pj]:
            T[pi+1][pj] += T[pi][pj]
            justcomb=True
        T[pi][pj]=0
        pi+=1
    return T

def moveleft(pi,pj,T):
    justcomb=False
    while pj > 0  and (T[pi][pj-1] == 0 or (T[pi][pj-1] == T[pi][pj] and not justcomb)):
        if T[pi][pj-1] == 0:
            T[pi][pj-1] = T[pi][pj]   
        elif T[pi][pj-1]==T[pi][pj]:
            T[pi][pj-1] += T[pi][pj]
            justcomb=True
        T[pi][pj]=0
        pj-=1
    return T

def moveright(pi,pj,T):
    justcomb=False
    while pj < 3 and (T[pi][pj+1] == 0 or (T[pi][pj+1] == T[pi][pj] and not justcomb)):
        if T[pi][pj+1] == 0:
            T[pi][pj+1] = T[pi][pj]
        elif T[pi][pj+1]==T[pi][pj]:
            T[pi][pj+1] += T[pi][pj]
            justcomb=True
        T[pi][pj] = 0
        pj+=1
    return T

def moveup(pi,pj,T):
    justcomb=False
    while pi > 0 and (T[pi-1][pj] == 0 or (T[pi-1][pj] == T[pi][pj] and not justcomb)):
        if T[pi-1][pj] == 0:
            T[pi-1][pj] = T[pi][pj] 
        elif T[pi-1][pj]==T[pi][pj]:
            T[pi-1][pj] += T[pi][pj]
            justcomb=True
        T[pi][pj]=0
        pi-=1
    return T

def leaderboard():
    s = 'to show leaderboard'

def terminate():
    pygame.quit()
    sys.exit()

main()