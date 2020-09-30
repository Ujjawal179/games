#snake game level 3
import pygame,random,sys
from pygame.locals import *

pygame.init()

#             R   G   B
RED   =     (255,  0, 40)
DEEPGRAY  = ( 25, 25, 25)
GRAY =      ( 30, 30, 30)
LIGHTGRAY = ( 40, 40, 40)
WHITE =     (240,240,255)

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
FPS = 60

faces = [[UP,UP,LEFT,RIGHT],
         [DOWN,DOWN,LEFT,RIGHT],
         [UP,DOWN,LEFT,LEFT],
         [UP,DOWN,RIGHT,RIGHT]
        ]
bodys = []
towards = []
HEAD = 0
direction = UP
new_direction = UP
head_animation = True

level = 10   #biger,easier
apple = {}
old_apple = {}
BODY_SIZE = 20
BOARD_LONG = 30
BOARD_WIDE = 20

fpsLim = 20
counter = fpsLim
fps = pygame.time.Clock()
screen = pygame.display.set_mode((BODY_SIZE*BOARD_LONG,BODY_SIZE*BOARD_WIDE))
pygame.display.set_caption('Snake 1.3')

fontObj = pygame.font.SysFont("Impact",256)

def main():
    while True:
        set_up()
        main_loop()
        terminal()

def set_up():
    global bodys,direction,towards
    x = random.randint(2,BOARD_LONG - 2)
    y = random.randint(2,BOARD_WIDE - 2)
    bodys = [{'x':x ,'y':y    },
             {'x':x ,'y':y + 1},
             {'x':x ,'y':y + 2}]
    towards = [UP,UP,UP]
    direction = UP
    get_apple()

def main_loop():
    global counter,screen,bodys,apple,direction,new_direction,fpsLim,towards
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminal()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a):
                    new_direction = faces[direction][LEFT]
                elif (event.key == K_RIGHT or event.key == K_d):
                    new_direction = faces[direction][RIGHT]
                elif (event.key == K_UP or event.key == K_w):
                    new_direction = faces[direction][UP]
                elif (event.key == K_DOWN or event.key == K_s):
                    new_direction = faces[direction][DOWN]
                elif event.key == K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x,mouse_y = event.pos                
                if mouse_x <= BOARD_LONG*(BODY_SIZE//4):
                    new_direction = faces[direction][LEFT]
                    break
                elif mouse_x > BOARD_LONG*3*BODY_SIZE//4:
                    new_direction = faces[direction][RIGHT]
                    break
                elif mouse_y <= BOARD_WIDE*BODY_SIZE//4:
                    new_direction = faces[direction][UP]
                    break
                elif mouse_y > BOARD_WIDE*3*BODY_SIZE//4:
                    new_direction = faces[direction][DOWN]
                
        if counter == 0:    
            if new_direction == UP:
                new_head = {'x':bodys[HEAD]['x'],'y':bodys[HEAD]['y'] - 1}
            elif new_direction == DOWN:
                new_head = {'x':bodys[HEAD]['x'],'y':bodys[HEAD]['y'] + 1}
            elif new_direction == LEFT:
                new_head = {'x':bodys[HEAD]['x'] - 1,'y':bodys[HEAD]['y']}
            elif new_direction == RIGHT:
                new_head = {'x':bodys[HEAD]['x'] + 1,'y':bodys[HEAD]['y']}

            if new_head in bodys:
                return
            if (new_head['x'] in [0,BOARD_LONG + 1] or new_head['y'] in [0,BOARD_WIDE + 1] ):
                return
            if new_head == apple:
                get_apple()
            else:
                del bodys[-1]
                del towards[-1]
                
            bodys.insert(0,new_head)
            towards.insert(0,new_direction)
            counter = fpsLim
            direction = new_direction
            fpsLim = 20 - 2 * (len(bodys)//level)
        else:
            counter -= 1

        screen.fill(DEEPGRAY)
        score_board()
        draw_grid()
        
        draw_head(bodys[HEAD],counter)
        draw_tail(bodys[-1],counter)
        
        for rect in bodys[1:]:
            draw_body(rect)
        draw_apple(apple,counter)

        pygame.display.update()
        fps.tick(FPS)

def draw_body(rect):
    pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE,(rect['y']-1)*BODY_SIZE,BODY_SIZE,BODY_SIZE))

def draw_tail(rect,counter):
    global bodys,head_animation,towards
    if head_animation == True:
        if towards[-1] == DOWN:  #go downside
            pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE,(rect['y']-1)*BODY_SIZE - counter,BODY_SIZE,BODY_SIZE))
        elif towards[-1] == UP:  #go upside
            pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE,(rect['y']-1)*BODY_SIZE + counter,BODY_SIZE,BODY_SIZE))
        elif towards[-1] == LEFT:  #go left
            pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE + counter,(rect['y']-1)*BODY_SIZE,BODY_SIZE,BODY_SIZE))
        elif towards[-1] == RIGHT:  #go right
            pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE - counter,(rect['y']-1)*BODY_SIZE ,BODY_SIZE,BODY_SIZE))
    else:
        pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE,(rect['y']-1)*BODY_SIZE,BODY_SIZE,BODY_SIZE))
            
def draw_head(rect,counter):
    global bodys,head_animation

    if head_animation == True:
        if direction == UP:
            pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE,(rect['y']-1)*BODY_SIZE + counter,BODY_SIZE,BODY_SIZE))
        elif direction == DOWN:
            pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE,(rect['y']-1)*BODY_SIZE - counter,BODY_SIZE,BODY_SIZE))
        elif direction == LEFT:
            pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE + counter,(rect['y']-1)*BODY_SIZE,BODY_SIZE,BODY_SIZE))
        elif direction == RIGHT:
            pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE - counter,(rect['y']-1)*BODY_SIZE ,BODY_SIZE,BODY_SIZE))
            
        if counter == 6:
            head_animation = False
    else:
        pygame.draw.rect(screen,WHITE,((rect['x']-1)*BODY_SIZE,(rect['y']-1)*BODY_SIZE,BODY_SIZE,BODY_SIZE))
        if counter == 0:
            head_animation = True
            
def draw_apple(rect,counter):
    global apple,old_apple

    if apple == old_apple:
        pygame.draw.rect(screen,RED,((rect['x']-1)*BODY_SIZE,(rect['y']-1)*BODY_SIZE,BODY_SIZE,BODY_SIZE))
    else:
        pygame.draw.rect(screen,RED,((rect['x']-1)*BODY_SIZE + counter//2,(rect['y']-1)*BODY_SIZE + counter//2,(BODY_SIZE-counter//2),(BODY_SIZE-counter//2)))
        if counter == 0:
            old_apple = apple
            
def terminal():
    pygame.quit()
    sys.exit()

def get_apple():
    global apple
    while True:
        apple = {'x':random.randint(3,BOARD_LONG - 3),
                 'y':random.randint(3,BOARD_WIDE - 3)}
        if apple not in bodys:
            break

def draw_grid():
    for x in range(0,BODY_SIZE*BOARD_LONG,BODY_SIZE):
        pygame.draw.line(screen,GRAY,(x,0),(x,BOARD_WIDE*BODY_SIZE))
    for y in range(0,BODY_SIZE*BOARD_WIDE,BODY_SIZE):
        pygame.draw.line(screen,GRAY,(0,y),(BOARD_LONG*BODY_SIZE,y))

def score_board():
    global bodys,screen
    score = len(bodys) - 3
    boardSurfaceobj = fontObj.render(str(score),True,LIGHTGRAY)
    scoreBoard = boardSurfaceobj.get_rect()
    scoreBoard.centerx = (BOARD_LONG*BODY_SIZE//2)
    scoreBoard.centery = (BOARD_WIDE*BODY_SIZE//2)
    screen.blit(boardSurfaceobj,scoreBoard)
                
if __name__ == "__main__":main()
