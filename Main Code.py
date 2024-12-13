import pygame

screen=width,height=300,300
cellsize=20
padding =20
row=col=(width-padding*4)//cellsize 

pturn=0


window=pygame.display.set_mode(screen)
Background_Color=(2,2,2)
Dots_Color=(252,91,16)
Dots_Inner_Color=(12,12,12)
Line_Color=(255,255,255)
Player1_color=(155,0,0)
Player2_color=(0,155,0)
Text_color=(0,0,0)
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
    def checkwin(self,cplayer):
        if not self.winner:
            if self.sides==[True]*4:
                self.winner=cplayer
                if self.winner== players[0]:
                    self.color=Player1_color
                else :
                    self.color=Player2_color
                self.text = font.render(self.winner[0], True,Text_color)
                
                return 1
        else:
            return 0

    def update (self,window):
        if self.winner:
            pygame.draw.rect(window,self.color,self.rect)
            window.blit(self.text,(self.rect.centerx, self.rect.centery))
        
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


running=True
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
    p2rect.right, p2rect.y = width-2*padding,15
    window.blit(p1ing,p1rect)
    window.blit(p2ing,p2rect)
    if cplayer==players[0]:
        pygame.draw.line(window,Player1_color,(p1rect.x,p1rect.bottom + 2),(p1rect.right, p1rect.bottom + 2))
    else :
        pygame.draw.line(window,Player1_color,(p2rect.x,p2rect.bottom + 2),(p2rect.right, p2rect.bottom + 2))
    if gameover:
        rect= pygame.Rect((50,100, width-100, height-200))
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

 