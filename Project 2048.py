#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import curses
from itertools import chain

class Action(object):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    RESTART = 'restart'
    EXIT = 'exit'
    
    input_letter = [ord(ch) for ch in 'WSADRQwsadrq']
    actions = [UP, DOWN, LEFT, RIGHT, RESTART, EXIT]
    actions_dict = dict(zip(input_letter, actions * 2)
    
    def __init__(self,stdscr):
        self.stdscr = stdscr
    
    def get_actions(self):
        i = 'N'
        if i not in self.actions_dict:
            i = self.stdscr.getch()
        return self.actions_dict[i]
                    
class Interface(object):
    def __init__(self, width=4, height=4):
        self.width = width
        self.height = height
        self.score = 0
        self.highscore = 0
        self.reset()  
                                              
    def reset(self):
        self.score = 0                
        self.spawn()
        self.spawn()
                      
    def spawn(self):
        number = random.choice([2,4])     
        for i in range(self.width) and j in range(self.height)
        self.field[i][j] = number     

class Screen(object):
    manual1 = '(W)Up (A)Left (S)Down (D)Right'
    manual2 = '     (R)Restar (Q)Quit'
    win_ = 'You Win!'
    lose_ = 'Game Over!'
    
    def __init__(self, screen=None, grid=None, score=0, win=False, lose=False):
        self.screen = screen
        self.grid = grid
        self.score = score
        self.win = win
        self.lose = lose
        self.count = count
    
    def cast(self, string):
        self.screen.addstr(string + '\n')
    
    def draw_row(self, row):
        self.cast(''.join('|{: ^4}'.format(num) if num > 0 else '|   ' for num in row) + '|')

    def draw(self):
        self.screen.clear()
        self.cast('SCORE:' + str(self.score))
        for row in self.grid.cells:
            self.cast('+----' * self.grid.size + '+')
            self.draw_row(row)
        self.cast('+----' * self.grid.size + '+')
                         
                      
class main(stdscr):
    # could try different win number (such as 16 to win the game faster) 
    def __init__(self, size=4, win_num=2048):
        self.size = size
        self.win_num = win_num
        self.reset()
    
    #build the game reset function for game initialization
    def reset(self):
        self.state = 'init'
        self.win = False
        self.over = False
        self.score = 0
        #make instance of Grid class
        self.grid = Grid(self.size,self)
        self.grid.reset() 
                
    @property
    def win(self):
        if any(i >= self.win_value for i in row) for row in self.field
        return 'You Win!'
    
    def canmove(self, direction):
        
    def lose(self):
        #if not canmove
        return 'Game Over!'
    
    def stop(self):
        #if win or lose  
        #action restart or exit

                   
