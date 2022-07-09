# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 23:03:04 2022

@author: Lenovo
"""

import numpy as np
import pygame
import pygame.event
import math
import sys
from pygame import mixer
import random
blue=(23,180,255)
black=(0,0,0)
player1_color=(255,0,0)
player2_color=(255,255,0)
total_row = 6
total_column = 7

human = 0
ai_player=1
human_piece=1
ai_piece=2
target_length=4
blank_place=0
def create_grid():
    grid = np.zeros((6,7));
    return grid

def place_ball(grid,row,col,ball):
    grid[row][col]=ball
   

def is_valid_column(grid,col):
    if grid[total_row-1][col]==0:
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
             if grid[r][c] == human_piece:
                 pygame.draw.circle(screen, player1_color, (int(c*square_size+square_size/2), height-int(r*square_size+square_size/2)), radius)
             elif grid[r][c] == ai_piece: 
                 pygame.draw.circle(screen, player2_color, (int(c*square_size+square_size/2), height-int(r*square_size+square_size/2)), radius)
    pygame.display.update()

def score_position(grid,ball):
    score = 0
    #center
    center_array=[int(i) for i in list(grid[:,total_column//2]) ]
    center_count=  center_array.count(ball)
    score+=center_count*3 #majhe dile tin dik theke jitar chance ache
    #horizontal
    for r in range(total_row):
        horizontal_array=[int(j) for j in list(grid[r,:])] #each row er jonno shob column
        for c in range(total_column-3):
            current_connected=horizontal_array[c:c+target_length]
            score+=evaluate_fn(current_connected,ball)
            
    ## Vertical
    for c in range(total_column):
        vertical_array=[int(i) for i in list(grid[:,c])] #each col er jonno shob row
        for r in range(total_row-3):
            current_connected = vertical_array[r:r+target_length]
            score+=evaluate_fn(current_connected,ball)
            
    #positive diagonal:
    for r in range(total_row-3):
        for c in range(total_column-3):
            current_connected=[grid[r+i][c+i] for i in range(target_length)]
            score+=evaluate_fn(current_connected,ball)
            
    #negative diagonal
    for r in range(total_row-3):
        for c in range(total_column-3):
            current_connected=[grid[r+3-i][c+i] for i in range(target_length)]
            score+=evaluate_fn(current_connected,ball)
    return score

def evaluate_fn(current_connected,ball):
    score=0
    opponent=human_piece
    if ball==human_piece:
        opponent=ai_piece 
    if current_connected.count(ball)==4: 
        score+=100
    elif current_connected.count(ball)==3 and current_connected.count(blank_place)==1:
        score+=5
    elif current_connected.count(ball)==2 and current_connected.count(blank_place)==2:
        score+=2
    if current_connected.count(opponent)==3 and current_connected.count(blank_place)==1:
        score -= 4
    return score

def is_termination(grid):
    if winning_condition(grid, human_piece) or winning_condition(grid, ai_piece) or len(valid_columns_ai(grid)) == 0:
        return True
    else:
        return False

def minimax(grid, depth, maximizing_ai):
    valid_columns = valid_columns_ai(grid) 
    if depth == 0 or is_termination(grid):
        if is_termination(grid):
            if winning_condition(grid, ai_piece):
                return (None, 1000000000000)
            elif winning_condition(grid, human_piece):
                return (None,-1000000000000)
            else:
                return (None,0)
        else:
            return (None,score_position(grid, ai_piece))
    if maximizing_ai:
        value = -math.inf
        column = random.choice(valid_columns)
        for c in valid_columns:
            r = available_row(grid, c)
            grid_copy = grid.copy()
            place_ball(grid_copy, r, c, ai_piece)
            update_score = minimax(grid_copy, depth-1, False)[1]
            '''
            update = minimax(grid_copy, depth-1, False)
            update_score=update[1]
            update_col=update[0]
            print("max score ={} and colnumber: {} , row={} ".format(update_score,update_col,r))
            '''
            if update_score > value:
                value = update_score
                column = c
        #print ("max score ={} and colnumber: {} ".format(value,column))
        return column,value
    else:
        value = math.inf
        column = random.choice(valid_columns)
        for c in valid_columns:
            r = available_row(grid, c)
            grid_copy = grid.copy()
            place_ball(grid_copy, r, c, human_piece)
            update_score = minimax(grid_copy, depth-1,True)[1]
            """
            update = minimax(grid_copy, depth-1, False)
            update_score=update[1]
            update_col=update[0]
            print("min score ={} and colnumber: {} , row= {} ".format(update_score,update_col,r))
            """
            if update_score < value:
                value = update_score
                column = c
            
        #print ("min score ={} and colnumber: {} ".format(value,column))
        return column,value
        
    
    
def valid_columns_ai(grid):
    valid_columns=[]
    for c in range(total_column):
        if is_valid_column(grid, c):
            valid_columns.append(c)
    return valid_columns

def choose_best_move(grid,ball):
    valid_columns=valid_columns_ai(grid)
    best_score = -10000
    best_column=random.choice(valid_columns)
    for c in valid_columns:
        r=available_row(grid, c)
        temporary_grid=grid.copy() #copy()for creating new memory location
        place_ball(temporary_grid, r, c, ball)
        score=score_position(temporary_grid, ball)
        if score > best_score:
            best_score=score 
            best_column=c
    return best_column

grid=create_grid()
end_of_game=False
move = random.randint(human, ai_player)




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
mixer.init()
mixer.music.load('brush.wav')
mixer.music.set_volume(0.30)

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
        pygame.display.update()#why
        
        if event.type==pygame.MOUSEBUTTONDOWN:
            
            sound = pygame.mixer.Sound('brush.wav')
            sound.play()
            
            pygame.draw.rect(screen, black ,(0,0,width,square_size))
            #print(event.pos)
            mixer.music.pause()	
            
            #human..........................................................................................#
            
            if move%2==human:
                position_x=event.pos[0]
                col=int(math.floor(position_x/square_size))
                #col = int(input("player 1 input (0-6) to choose column: "))
                if is_valid_column(grid, col):
                    row = available_row(grid, col)
                    place_ball(grid, row, col, human_piece)
                    
                    if winning_condition(grid, human_piece):
                       #print("Player 1 wins!!! Game Over")
                       caption = winningfont.render("Player 1 wins",1,player1_color)#1 for printing horizontally
                       screen.blit(caption,(40,10))
                       end_of_game = True
                move=move+1
                print_flip_grid(grid) #console print
                       
                      
               
    #ai...............................................................#
    
    if move%2==ai_player and not end_of_game:
        #col=random.randint(0,total_column-1)
        col,minimax_score =minimax(grid, 3,True)

        
        #col = int(input("player 2 input (0-6) to choose column: "))
        #if is_valid_column(grid, col):
        pygame.time.wait(500)
        row = available_row(grid, col)
        place_ball(grid, row, col, ai_piece)
        
        if winning_condition(grid, ai_piece):
           #print("Player 2 wins!!! Game Over")
           caption = winningfont.render("Player 2 wins",1,player2_color)#1 for printing horizontally
           screen.blit(caption,(40,10))
           end_of_game = True
        move=move+1
        print_flip_grid(grid)
                       
    #print_flip_grid(grid) #console e index print 
    #draw_grid(grid)
    
#pygame.wait(10)
if end_of_game:
    pygame.time.wait(3000)
    pygame.display.quit()
    pygame.quit()
    sys.exit()

    
