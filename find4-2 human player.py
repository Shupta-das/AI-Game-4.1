# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 23:03:04 2022

@author: Lenovo
"""
#board game

import numpy as np
import pygame
import pygame.event
import math
import sys
blue=(23,180,255)
black=(0,0,0)
player1_color=(255,0,0)
player2_color=(255,255,0)
total_row = 6
total_column = 7
def create_grid():
    grid = np.zeros((6,7));
    return grid

def place_ball(grid,row,col,ball):
    grid[row][col]=ball
   

def is_valid_column(grid,col):
    if grid[5][col]==0:
        return 1

def available_row(grid,col):
     for i in range(total_row):
         if grid[i][col]==0:
             return i #je row faka oita return korbe.
def print_flip_grid(grid):
    print(np.flip(grid,0)) #x - axis borabor flip korbe karon numpy upor theke indexing kore.amader nich theke lagbe.
    draw_grid(grid)
def winning_condition(grid,ball):
    #checking for horizontal winning condition
    for i in range(total_row):
        for j in range(total_column):
            if j < total_column-3:
                if grid[i][j] == ball and grid[i][j+1] == ball and grid[i][j+2] == ball and grid[i][j+3] == ball:
                    return True
                
    #checking for vertical winning condition
    for i in range(total_column):
        for j in range(total_row):
            if j < total_row-3:
                if grid[j][i] == ball and grid[j+1][i] == ball and grid[j+2][i] == ball and grid[j+3][i] == ball:
                    return True
                
    #positive slope of diagonal
    for i in range(total_row-3):
        for j in range(total_column-3):
            if grid[i][j] == ball and grid[i+1][j+1] == ball and grid[i+2][j+2] == ball and grid[i+3][j+3] == ball:
                return True
    #negative slope of diagonal
    for i in range(3,total_row):
        for j in range(total_column-3):
            if grid[i][j] == ball and grid[i-1][j+1] == ball and grid[i-2][j+2] == ball and grid[i-3][j+3] == ball:
                return True

def draw_grid(grid):
    for c in range(total_column):
        for r in range(total_row):
            pygame.draw.rect(screen,blue,(c*square_size,r*square_size+square_size,square_size,square_size))
            pygame.draw.circle(screen, black, (int(c*square_size+square_size/2),int(r*square_size+square_size+square_size/2)),radius)
    for c in range(total_column):
         for r in range(total_row):	
             if grid[r][c] == 1:
                 pygame.draw.circle(screen, player1_color, (int(c*square_size+square_size/2), height-int(r*square_size+square_size/2)), radius)
             elif grid[r][c] == 2: 
                 pygame.draw.circle(screen, player2_color, (int(c*square_size+square_size/2), height-int(r*square_size+square_size/2)), radius)
    pygame.display.update()
grid=create_grid()
end_of_game=False
move = 0




pygame.init()

square_size=100
width=total_column*square_size
height=(total_row+1)*square_size
size=(width,height)
radius= int(square_size/2-10)
screen=pygame.display.set_mode(size)
draw_grid(grid)
pygame.display.update()

winningfont = pygame.font.SysFont("monospace", 40)

"""
run = True
while run:
    #pygame.time.delay()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()
           
        square_size=100
        width=total_column*square_size
        height=(total_row+1)*square_size
        size=(width,height)
        screen=pygame.display.set_mode(size)
        #pygame.event.wait()
        """


while not end_of_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.display.quit()
           pygame.quit()
           sys.exit()
           
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black ,(0,0,width,square_size))
            position_x = event.pos[0]
            if move % 2 == 0:
                 pygame.draw.circle(screen, player1_color, (position_x,int(square_size/2)), radius)
            else:
                pygame.draw.circle(screen, player2_color, (position_x,int(square_size/2)), radius)
        pygame.display.update()
        
        if event.type==pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black ,(0,0,width,square_size))
            #print(event.pos)
            
            #p1
            if move%2==0:
                position_x=event.pos[0]
                col=int(math.floor(position_x/square_size))
                #col = int(input("player 1 input (0-6) to choose column: "))
                if is_valid_column(grid, col):
                    row = available_row(grid, col)
                    place_ball(grid, row, col, 1)
                    
                    if winning_condition(grid, 1):
                       #print("Player 1 wins!!! Game Over")
                       caption = winningfont.render("Player 1 wins",1,player1_color)#1 for printing horizontally
                       screen.blit(caption,(40,10))
                       end_of_game = True
                       
                      
               
            #p2
            else:
                position_x=event.pos[0]
                col=int(math.floor(position_x/square_size))
                
                #col = int(input("player 2 input (0-6) to choose column: "))
                if is_valid_column(grid, col):
                    row = available_row(grid, col)
                    place_ball(grid, row, col, 2)
                    
                    if winning_condition(grid, 2):
                       #print("Player 2 wins!!! Game Over")
                       caption = winningfont.render("Player 2 wins",1,player2_color)#1 for printing horizontally
                       screen.blit(caption,(40,10))
                       end_of_game = True
                       
            print_flip_grid(grid) #console e index print 
            #draw_grid(grid)
            move=move+1
#pygame.wait(10)
if end_of_game:
    pygame.time.wait(3000)
    pygame.display.quit()
    pygame.quit()
    sys.exit()

    
