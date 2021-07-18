import pygame
import sys
import random
import time
from math import inf as infinity
from collections import deque

pygame.init()

width = 500; height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()

#colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#lists
grid = []
occupied = []
stack = []
visited = []
unvisited_nodes = []
end = 0
start = 0

#row and columns
col = int(input("# of Columns: "))

row = int(input("# of Rows: "))

total = col*row
row_width = width // col  #x
col_height = height // row #y
startcoord = (0,0)
endcoord = (0,0)
if(col%2==0 and row%2==0):
    endcoord = ((col-2)*row_width, (row-2)*col_height)
elif(col%2==1 and row%2==0):
    endcoord = ((col - 1) * row_width, (row - 2) * col_height)
elif (col % 2 == 0 and row % 2 == 1):
    endcoord = ((col - 2) * row_width, (row - 1) * col_height)
else:
    endcoord = ((col - 1) * row_width, (row - 1) * col_height)


class Node:
    distance = None
    visited = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        print(self.x,self.y)
        return str(self.distance)

    def distance_to(self, other):
        return 1


def firstcell(x,y):

    pygame.draw.rect(screen, GREEN , (x , y , (row_width), (col_height )))

    pygame.display.update()

def lastcell(x,y):
    #for thing in occupied:
       # pygame.draw.rect(screen, BLUE, (thing[0], thing[1], (row_width), (col_height)))
    pygame.draw.rect(screen, RED , (x , y , (row_width), (col_height )))

    pygame.display.update()

def up(x,y):
    pygame.draw.rect(screen, WHITE, (x, y-(col_height*2), (row_width), (col_height*2)))
    pygame.display.update()

def down(x, y):
    pygame.draw.rect(screen, WHITE, (x , y + (col_height ), (row_width), (col_height*2)))
    pygame.display.update()

def left(x, y):
    pygame.draw.rect(screen, WHITE, (x - (row_width*2), y , (row_width*2), (col_height)))
    pygame.display.update()

def right(x, y):
    pygame.draw.rect(screen, WHITE, (x + (row_width), y , (row_width*2), (col_height)))
    pygame.display.update()

def get_neighbors(node):
    neighbors = []
    if ((node.x + row_width, node.y)) in occupied:
        neighbors.append((node.x + row_width, node.y, occupied.index((node.x + row_width, node.y))))

    if ((node.x - row_width, node.y)) in occupied:
        neighbors.append((node.x - row_width, node.y, occupied.index((node.x - row_width, node.y))))
    if ((node.x, node.y+col_height)) in occupied:
        neighbors.append((node.x, node.y+col_height, occupied.index((node.x , node.y+col_height))))
    if ((node.x, node.y-col_height)) in occupied:
        neighbors.append((node.x , node.y-col_height, occupied.index((node.x , node.y-col_height))))
    return neighbors



#draws grid
def draw_grid():
    #if(row%2==0 and col%2==0):

    for i in range(row):
        x = 0
        if(i == 0):
            y = 0
        else:
            y = y + col_height

        for j in range(col):
            if(i%2==0 and j%2==0):
                pygame.draw.rect(screen, WHITE , (x , y , (row_width ), (col_height )))
                grid.append((x,y))

            x += row_width

        pygame.display.update()

#################################################
#generates maze iterative implementation
def makeMaze(x,y):
    stack.append((x,y))
    occupied.append((x,y))
    while len(stack)>0:

        cell = []

        if (x+(row_width*2),y) not in occupied and (x+(row_width*2),y) in grid: #checks right
            cell.append("r")

        if (x-(row_width*2),y) not in occupied and (x-(row_width*2),y) in grid: #checks left
            cell.append("l")

        if (x,y-(col_height*2)) not in occupied and (x,y-(col_height*2)) in grid: #checks up
            cell.append("u")

        if (x,y+(col_height*2)) not in occupied and (x,y+(col_height*2)) in grid: #checks down
            cell.append("d")

        if len(cell)>0:
            direction = (random.choice(cell))

            if direction == "r":
                right(x,y)
                x = x+(row_width*2)
                stack.append((x,y))
                occupied.append((x,y))
                occupied.append((x-row_width,y))

            if direction == "l":
                left(x,y)
                x = x-(row_width*2)
                stack.append((x,y))
                occupied.append((x,y))
                occupied.append((x+row_width, y))

            if direction == "u":
                up(x,y)
                y = y-(col_height*2)
                stack.append((x,y))
                occupied.append((x,y))
                occupied.append((x, y+col_height))

            if direction == "d":
                down(x,y)
                y = y+(col_height*2)
                stack.append((x,y))
                occupied.append((x,y))
                occupied.append((x, y -col_height))
        else:
            x, y = stack.pop()


        firstcell(0, 0)

##################################################################

#solves maze
def solveMaze():
    for cell in occupied:

        unvisited_nodes.append(Node(cell[0], cell[1]))
        if cell[0] == endcoord[0] and cell[1] == endcoord[1]:
            end = unvisited_nodes[len(unvisited_nodes)-1]


    #unvisited_nodes = [Node(cell[0],cell[1]) for cell in occupied]
    start = unvisited_nodes[0]
    start.distance = 0
    for node in unvisited_nodes:
        if node is not start:
            node.distance = infinity

    current_node = start
    #print(unvisited_nodes[1].x)
    #print(unvisited_nodes[1].y)
    #print(end.x)
    #print(end.y)

    #print(unvisited_nodes[4])
    #print(get_neighbors(unvisited_nodes[4]))
    #print(occupied)

    while not end.visited:

        get = get_neighbors(current_node)
        #print(get)

        for neighbor in get:
            if unvisited_nodes[neighbor[2]].visited:
                continue
        
            new_distance = current_node.distance + 1
            if unvisited_nodes[neighbor[2]].distance>new_distance:
                unvisited_nodes[neighbor[2]].distance = new_distance

        current_node.visited = True



        smallest_distance = infinity
        for node in unvisited_nodes:
            if not node.visited and node.distance<smallest_distance:
                smallest_distance = node.distance
                current_node = node



#shows what nodes it visited
    #for node in unvisited_nodes:
        #if (node.distance < infinity):
            #pygame.draw.rect(screen, RED, (node.x, node.y, (row_width), (col_height)))
            #pygame.display.update()


#reverse traversal

    current_node = end
    while current_node is not start:

        get = get_neighbors(current_node)
        current_node.visited = False
        pygame.draw.rect(screen, BLUE, (current_node.x, current_node.y, (row_width), (col_height)))
        for neighbor in get:
            if not unvisited_nodes[neighbor[2]].visited:
                continue

            if unvisited_nodes[neighbor[2]].distance == current_node.distance-1:
                current_node = unvisited_nodes[neighbor[2]]

    pygame.display.update()

    lastcell(endcoord[0], endcoord[1])
    return 0


#########################################################################
draw_grid()
makeMaze(0,0)
solveMaze()

running = True
while running:

    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False