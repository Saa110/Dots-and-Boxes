import pygame

# Initialize pygame to get screen info
pygame.init()
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Calculate window size as percentage of screen (e.g., 80% of screen width and height)
WINDOW_WIDTH = int(screen_width * 0.8)
WINDOW_HEIGHT = int(screen_height * 0.8)

# Grid size options
GRID_SIZES = {
    '8x8': 8,
    '11x11': 11,
    '13x13': 13
}

# Default grid size
selected_grid_size = 8  # Default to 8x8
cellsize = min((WINDOW_WIDTH - 80) // selected_grid_size, (WINDOW_HEIGHT - 100) // selected_grid_size)
padding = 20
row = col = selected_grid_size

pturn = 0

# Define screen dimensions
screen = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(screen)
Background_Color = (2, 2, 2)
Dots_Color = (252, 91, 16)
Dots_Inner_Color = (12, 12, 12)
Line_Color = (255, 255, 255)
Player1_color = (155, 0, 0)
Player2_color = (0, 155, 0)
Text_color = (0, 0, 0)

# Initialize fonts
title_font = pygame.font.SysFont('cursive', 50)
font = pygame.font.SysFont('cursive', 20)

def show_startup_screen():
    window.fill(Background_Color)
    
    # Title
    title_text = title_font.render("DOTS AND BOXES", True, Dots_Color)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))
    window.blit(title_text, title_rect)
    
    # Subtitle
    subtitle_text = font.render("CHOOSE SIZE", True, Line_Color)
    subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    window.blit(subtitle_text, subtitle_rect)
    
    # Instructions
    instructions = [
        "Press 1 for 8x8 grid",
        "Press 2 for 11x11 grid",
        "Press 3 for 13x13 grid"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, Line_Color)
        rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50 + i*30))
        window.blit(text, rect)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    size = 8 if event.key == pygame.K_1 else (11 if event.key == pygame.K_2 else 13)
                    change_grid_size(size)
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
    return True

def reset_cells():
    pos=None
    cur_cell= None
    up=bottom=left=right=False
    return pos, cur_cell,up,bottom,left,right
def reset_score():
    fillcount=0
    scores= [0]*2
    gameover= False
    return fillcount,scores, gameover
def reset_player():
    turn=0
    players=['1asd','2asdawdasdawd']
    cplayer=players[turn]
    nturn=False
    return turn,players,cplayer,nturn
pos, cur_cell,up,bottom,left,right=reset_cells()
turn,players,cplayer,nturn= reset_player()
fillcount,scores, gameover = reset_score()
gameover=True

class Cell:
    def __init__(self,r,c):
        self.r=r
        self.c=c
        self.index=self.r*row +self.c
        self.rect= pygame.Rect((c*cellsize +2*padding,r*cellsize + 3*padding),(cellsize,cellsize))
        self.left=self.rect.left
        self.top=self.rect.top
        self.right=self.rect.right
        self.bottom=self.rect.bottom
        self.edges=[ [(self.left,self.top),(self.right,self.top)],
                     [(self.right,self.top),(self.right,self.bottom)],
                     [(self.right,self.bottom),(self.left,self.bottom)],
                     [(self.left,self.bottom),(self.left,self.top)]
                     ]
        self.sides=[False,False,False,False]
        self.winner= None
        self.text_rect = None
    def checkwin(self,cplayer):
        if not self.winner:
            if self.sides==[True]*4:
                self.winner=cplayer
                if self.winner== players[0]:
                    self.color=Player1_color
                else :
                    self.color=Player2_color
                self.text = font.render(self.winner[0], True,Text_color)
                self.text_rect = self.text.get_rect(center=self.rect.center)
                return 1
        else:
            return 0

    def update (self,window):
        if self.winner:
            pygame.draw.rect(window,self.color,self.rect)
            window.blit(self.text, self.text_rect)
        
        for index, side in enumerate(self.sides):
            if side:
                pygame.draw.line(window,Line_Color,(self.edges[index][0]),(self.edges[index][1]),2)
def create_cells():

    cells=[]
    for r in range(row):
        for c in range(col):
            cell=Cell(r,c)
            cells.append(cell)
    return cells

cells= create_cells()
    


pygame.init()
font= pygame.font.SysFont('cursive',20)

def change_grid_size(size):
    global selected_grid_size, cellsize, row, col, cells
    selected_grid_size = size
    cellsize = min((WINDOW_WIDTH - 80) // selected_grid_size, (WINDOW_HEIGHT - 100) // selected_grid_size)
    row = col = selected_grid_size
    cells = create_cells()

# Start the game
if show_startup_screen():
    running = True
    while running:
        window.fill(Background_Color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type== pygame.MOUSEBUTTONDOWN:
                pos=event.pos
            if event.type== pygame.MOUSEBUTTONUP:
                pos=None
            if event.type== pygame.KEYDOWN:
                if event.key== (pygame.K_q or pygame.K_ESCAPE):
                    running=False
                if event.key == pygame.K_r:
                    pos, cur_cell,up,bottom,left,right=reset_cells()
                    fillcount,scores, gameover = reset_score()
                    turn,players,cplayer,nturn= reset_player()
                    cells= create_cells()   
                if event.key == pygame.K_1:
                    change_grid_size(8)
                if event.key == pygame.K_2:
                    change_grid_size(11)
                if event.key == pygame.K_3:
                    change_grid_size(13)
                if not gameover:
                    if event.key == pygame.K_UP:
                        up=True
                    if event.key == pygame.K_DOWN:
                        bottom=True
                    if event.key == pygame.K_RIGHT:
                        right=True
                    if event.key == pygame.K_LEFT:
                        left=True
            if event.type== pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up=False
                if event.key == pygame.K_DOWN:
                    bottom=False
                if event.key == pygame.K_RIGHT:
                    right=False
                if event.key == pygame.K_LEFT:
                    left=False
        
        for r in range(row+1):
            for c in range(col+1):
                pygame.draw.circle(window,Dots_Color,(c*cellsize +2*padding,r*cellsize + 3*padding), 2)
        for cell in cells:
            cell.update(window)
            if pos and cell.rect.collidepoint(pos):
                cur_cell=cell
        if cur_cell:
            index= cur_cell.index
            if not cur_cell.winner:
                pygame.draw.circle(window,Dots_Color,(cur_cell.rect.centerx,cur_cell.rect.centery),2)
            if up and not cur_cell.sides[0]:
                cur_cell.sides[0]=True
                if index - row>=0:
                    cells[index-row].sides[2]=True
                nturn=True
            if bottom and not cur_cell.sides[2]:
                cur_cell.sides[2]=True
                if index + row<len(cells):
                    cells[index+row].sides[0]=True
                nturn=True
            if left and not cur_cell.sides[3]:
                cur_cell.sides[3]=True
                if index%col>0:
                    cells[index-1].sides[1]=True
                nturn=True
            if right and not cur_cell.sides[1]:
                cur_cell.sides[1]=True
                if index%col!=col-1:
                    cells[index+1].sides[3]=True
                nturn=True
            res= cur_cell.checkwin(cplayer)
            if res:
                fillcount+=1
                scores[turn]+=1
                turn-1
                nturn=False
            if nturn :
                turn= (turn + 1)% len(players)
                cplayer=players[turn]
                nturn=False
                if fillcount>=len(cells)-1:
                    print(scores)
                    gameover=True

        p1ing = font.render(f'Player 1 : {scores[0]}', True, Player1_color)
        p1rect = p1ing.get_rect()
        p1rect.x,p1rect.y= 2*padding, 15
        p2ing = font.render(f'Player 2 : {scores[1]}',True,Player2_color)
        p2rect = p2ing.get_rect()
        p2rect.right, p2rect.y = WINDOW_WIDTH-2*padding,15
        window.blit(p1ing,p1rect)
        window.blit(p2ing,p2rect)
        if cplayer==players[0]:
            pygame.draw.line(window,Player1_color,(p1rect.x,p1rect.bottom + 2),(p1rect.right, p1rect.bottom + 2))
        else :
            pygame.draw.line(window,Player1_color,(p2rect.x,p2rect.bottom + 2),(p2rect.right, p2rect.bottom + 2))
        if gameover:
            rect= pygame.Rect((50,100, WINDOW_WIDTH-100, WINDOW_HEIGHT-200))
            pygame.draw.rect(window,Background_Color,rect)
            pygame.draw.rect(window,Dots_Color,rect)
            
            over= font.render('Gamer Over', True, Text_color)
            window.blit(over,(rect.centerx - over.get_width()//2, rect.y+10))
            if scores[0]> scores[1]:
                winner = players[0]
                winnercolor=Player1_color
            elif scores[0] < scores[1]:
                winner = players[1]
                winnercolor=Player2_color
            else :
                winner= "Tie"
                winnercolor=Text_color
            winnerimg=font.render(f'Player {winner} WON', True, winnercolor)
            window.blit(winnerimg,((rect.centerx - winnerimg.get_width()//2, rect.centery -10)))
            msg ="Press r to restart and q to quit"
            msgimg= font.render(msg,True, Text_color)
            window.blit(msgimg,((rect.centerx - msgimg.get_width()//2, rect.centery +20)))
        pygame.display.update()
pygame.quit()

 