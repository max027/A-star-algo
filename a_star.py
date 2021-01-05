import pygame
import math
from queue import PriorityQueue

WIDTH=800
win=pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* pathfinding")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class node():
    """
    class for node or spot in grid 
    this class define attribut for each node in grid
    """
    def __init__(self,row,col,width,total_row):
        self.row=row
        self.col=col
        self.y=col*width
        self.x=row*width
        self.total_row=total_row
        self.color= WHITE
        self.width=width
        self.neighbours=[]
    def get_pos(self):
        return self.row,self.col
    def is_open(self):
        return self.color==GREEN
    def is_closed(self):
        return self.color==RED
    def is_barrer(self):
        return self.color==BLACK
    def is_start(self):
        return self.color==ORANGE
    def is_end(self):
        return self.color==TURQUOISE
    def reset(self):
        self.color=WHITE
    def make_start(self):
        self.color=ORANGE
    def make_end(self):
        self.color=TURQUOISE
    def make_open(self):
        self.color=GREEN
    def make_closed(self):
        self.color=RED
    def  make_barrer(self):
        self.color=BLACK
    def make_path(self):
        self.color=PURPLE
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
        """
        here we are updating neighbours by checking which direction is avaliable or
        not a barrier
        """
    def update_nebours(self,grid):
        self.neighbours=[]
        """
        this statment checks if row below is avaliable or is it the end of all row
        """
        if self.row<self.total_row-1 and not grid[self.row + 1][self.col].is_barrer():
            self.neighbours.append(grid[self.row + 1][self.col])
        """
        this check if we can move up or not
        """
        if self.row>0 and not grid[self.row-1][self.col].is_barrer():
            self.neighbours.append(grid[self.row - 1][self.col])
        
        if self.col<self.total_row-1 and not grid[self.row][self.col+1].is_barrer():
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col>0 and not grid[self.row][self.col-1].is_barrer():
            self.neighbours.append(grid[self.row][self.col - 1])

        
    def __lt__(self, other):
      return False

def h(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)

"""
simply reconstruct the given path
"""
def reconstruct_path(came_from,current,draw):
    while current in came_from:
        #our current node is not the start node so simply make camefrom noe current
        current=came_from[current]
        current.make_path()
        #after doing make path and draw draw is a lamda function
    draw()
def algorithm(drawing,grid,start,end):
    #count is used to check f score 
    #if two node are visited we will prefer by f score
    count=0
    open_set=PriorityQueue()
    open_set.put((0,count,start))
    came_from={}
    g_score={spot:float("inf") for row in grid for spot in row}
    """
    {spot:float("inf") for row in grid for spot in row}
    inf means infinity we assume g_score to be inf before start the algo
    it simply list comprension
    """
    g_score[start]=0
    f_score={spot:float("inf") for row in grid for spot in row}
    """
    f_score of start node will be heuristic because we want to asume the 
    approx distance of end node form start
    """
    f_score[start]=h(start.get_pos(),end.get_pos())
    open_set_hash={start}
    """
    it simply check the items are present or not present in PriorityQueue
    we can delet the item from PriorityQueue but not check the items present in
    PriorityQueue
    """

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
        
        current=open_set.get()[2]
        #starting for start node
        open_set_hash.remove(current)
        #sycn the hash node
        if current ==end:
            reconstruct_path(came_from,end,drawing)
            end.make_path()
            return True

        for neighbour in current.neighbours:
            temp_g_score=g_score[current]+1

            if temp_g_score<g_score[neighbour]:
                came_from[neighbour]=current

                g_score[neighbour]=temp_g_score
                f_score[neighbour]=temp_g_score+h(neighbour.get_pos(),end.get_pos())
                if neighbour not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbour],count,neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        
        drawing()
      

        if current!=start:
            current.make_closed()

    return False

def make_grid(rows,width):
    gap=width//rows
    grid=[]
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot=node(i,j,gap,rows)
            grid[i].append(spot)
    return grid

def draw_grid(win,rows,width):
    gap=width//rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j * gap, 0), (j * gap, width))

def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()

def getClicked_pos(pos,row,width):
    gap=width//row
    y,x=pos
    row=y//gap
    col=x//gap
    return row,col

    """
    this is out main entry point we will start here
    """

def main(win,width):
    ROW=40 #number of total rows
    grid=make_grid(ROW,width) #passing in make grid function to make grid
    start =None
    end=None
    run=True #we will  be in loop and id algo is finished loop will be terminated
    startd=False
    while run:
        #before running alog draw grid 
        draw(win,grid,ROW,width)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False #if cross buttion is clicked stop the program

            if pygame.mouse.get_pressed()[0]:#left mouse click
                pos=pygame.mouse.get_pos()# get the pos  
                row,col=getClicked_pos(pos,ROW,width)#get row and col by helper method
                spot=grid[row][col]
                if not start and spot!=end:
                    """
                    if first clicked is not start and also it is not end then
                    make it starting point
                    """
                    start=spot
                    start.make_start()
                elif not end and spot!=start:
                    """
                    if click is not end and also not start make it end
                    """
                    end=spot
                    end.make_end()
                elif spot!=end and spot!=start:
                    """
                    if click is not start as well as end then make it a barrier
                    """
                    spot.make_barrer()

            elif pygame.mouse.get_pressed()[2]:#right mouce click
                pos=pygame.mouse.get_pos()
                row,col=getClicked_pos(pos,ROW,width)
                spot=grid[row][col]
                spot.reset()
                if spot==start:
                    start=None
                if spot==end:
                    end=None

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_nebours(grid)

                    algorithm(lambda: draw(win, grid, ROW, width), grid, start, end)
            
                if event.key==pygame.K_c:
                    start=None
                    end=None
                    grid=make_grid(ROW,width)

    pygame.quit()

main(win,WIDTH)


                    
        



    
