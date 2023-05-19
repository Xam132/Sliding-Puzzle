import pygame,random,sys,math
from pygame.locals import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GAMESIZE = 3     # in terms of sliding boxes
BOXSIZE = 80
GAPSIZE = 20
XMARGIN = (WINDOW_WIDTH - GAMESIZE*BOXSIZE)//2
YMARGIN = (WINDOW_HEIGHT - GAMESIZE*BOXSIZE)//2

NAVYBLUE = ( 60,  60, 100)
YELLOW   = (255, 255,   0)
GREEN    = (  0, 255,   0)
GRAY     = (128, 128, 128)
ORANGE   = (255, 128,   0)
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
BLUE     = (  0,   0, 255)
OTHER    = ( 30, 144, 255)

BGCOLOR        = NAVYBLUE
BOXCOLOR       = GRAY
TEXTCOLOR      = GREEN
HIGHLIGHTCOLOR = ORANGE

FONTSIZE = 40
FONTTYPE = 'arial'

def solvable(list):
    # To check if given puzzle is solvable or not
    l,n = 0,int(math.sqrt(len(list)+1))
    for i in range(len(list)):
        l += len([_ for _ in list[i:] if _ > list[i]])
    if n % 2 == 0:
        return (l + n - 1) % 2
    else:
        return l % 2

def coords(boxx,boxy):
    coorx = XMARGIN + boxx * (BOXSIZE+GAPSIZE) - GAPSIZE
    coory = YMARGIN + boxy * (BOXSIZE+GAPSIZE) - GAPSIZE
    return coorx,coory

def boxAtLoc(coorx,coory):
    for boxx in range(GAMESIZE):
        for boxy in range(GAMESIZE):
            left,top = coords(boxx,boxy)
            rect = pygame.Rect(left,top,BOXSIZE,BOXSIZE)
            if rect.collidepoint(coorx,coory):
                return (boxx,boxy)
    return (None,None)

def adjacent_blank(board,boxx,boxy):
    # checks if adjacent blocks are 0
    if board[boxx][boxy] == 0:
        return False
    return not (board[max(boxx-1,0)][boxy] != 0 and board[boxx][max(boxy-1,0)] != 0 and board[min(boxx+1,GAMESIZE-1)][boxy] != 0 and board[boxx][min(boxy+1,GAMESIZE-1)] != 0)

def highlight(board,boxx,boxy):
    if adjacent_blank(board,boxx,boxy):
        left,top = coords(boxx,boxy)
        pygame.draw.rect(DISPLAYSURF,HIGHLIGHTCOLOR,(left,top,BOXSIZE,BOXSIZE),4)
        pygame.display.update()

def random_board():
    list = [i for i in range(1,GAMESIZE * GAMESIZE)]
    while True:
        random.shuffle(list)
        if solvable(list):
           break
    list.append(0)
    board = [[list[i*GAMESIZE+j] for j in range(GAMESIZE)]for i in range(GAMESIZE)]
    return board

def draw_board(board):
    quar = BOXSIZE // 4
    half = BOXSIZE // 2
    for i in range(GAMESIZE):
        for j in range(GAMESIZE):
            left,top = coords(i,j)
            if board[i][j] == 0:
                pygame.draw.rect(DISPLAYSURF,WHITE,(left,top,BOXSIZE,BOXSIZE))
            else:
                pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
                text = FONT.render(str(board[i][j]),True,TEXTCOLOR,BOXCOLOR)
                DISPLAYSURF.blit(text,(left+half-8,top+quar,BOXSIZE,BOXSIZE))
            pygame.draw.rect(DISPLAYSURF,BLACK,(left,top,BOXSIZE,BOXSIZE),4)

def start_Animation():
    for i in range(7):
        text = FONT.render('Game Start', True, GREEN, BLUE)
        textRect = text.get_rect()
        DISPLAYSURF.blit(text, textRect)
        board1 = random_board()
        draw_board(board1)
        pygame.display.update()
        FPSCLOCK.tick(FPS//3)
    DISPLAYSURF.fill(BGCOLOR)

def move_Animation(board,boxx,boxy):
    if adjacent_blank(board,boxx,boxy):
        for i in range(GAMESIZE):
            for j in range(GAMESIZE):
                if board[i][j] == 0:
                    board[i][j] = board[boxx][boxy]
                    break
        board[boxx][boxy] = 0
        draw_board(board)

def has_won(board):
    l = 1
    for i in range(GAMESIZE):
        for j in range(GAMESIZE):
            if i == GAMESIZE-1 and j == GAMESIZE-1:
                return True
            elif board[j][i] != l:
                return False
            l += 1

def win_Animation(board):
    col2,col1 = BGCOLOR,OTHER
    text = FONT.render('Congrats! You won', True, GREEN, BLUE)
    textRect = text.get_rect()
    for i in range(11):
        col1, col2 = col2, col1
        DISPLAYSURF.fill(col1)
        draw_board(board)
        DISPLAYSURF.blit(text, textRect)
        pygame.display.update()
        pygame.time.wait(500)
    DISPLAYSURF.fill(BGCOLOR)


def main():
    global DISPLAYSURF,FPSCLOCK,FONT
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Slide Puzzle")
    FONT = pygame.font.SysFont(FONTTYPE,FONTSIZE)
    DISPLAYSURF.fill(BGCOLOR)
    board = random_board()
    start_Animation()
    boxx,boxy = None,None
    while True:
        mouseClick = False
        draw_board(board)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                mouse_x,mouse_y = event.pos
                boxx,boxy = boxAtLoc(mouse_x,mouse_y)
            if event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouseClick = True
                boxx, boxy = boxAtLoc(mouse_x, mouse_y)
        #print(boxx,boxy)
        if boxx != None and boxy != None:
            highlight(board,boxx,boxy)
            if mouseClick:
                move_Animation(board,boxx,boxy)
            if has_won(board):
                win_Animation(board)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                board = random_board()
                start_Animation()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
