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
    
    #turn user's input into game actions 
    input_letter = [ord(ch) for ch in 'WSADRQwsadrq']
    actions = [UP, DOWN, LEFT, RIGHT, RESTART, EXIT]
    actions_over = [UP, LEFT, DOWN, RIGHT]
    actions_dict = dict(zip(input_letter, actions * 2))
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
    
    #only do next movement until we get input in 'WASDRQwasdrq'
    def get_actions(self):
        i = 'N'
        if i not in self.actions_dict:
            i = self.stdscr.getch()
        return self.actions_dict[i]
                    
class Grid(object):
    def __init__(self, size, parent):
        self.size = size
        self.cells = None
        self.parent = parent
        self.reset()  
    
    def reset(self):
        self.cells = [[0 for i in range(self.size)] for j in range(self.size)]
        self.spawn()
        self.spawn()
    
    #spawn random number in empty cells                    
    def spawn(self):
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] == 0:
                    empty_cells.append((i, j))
        (i, j) = random.choice(empty_cells)
        self.cells[i][j] = random.choice([2,4]) #could try different probability to generate 2 or 4
    
    def transpose(self):
        new_cells = []
        for row in zip(*self.cells):
            new_cells.append(list(row))
        self.cells = new_cells
    
    def invert(self):
        new_cells = []
        for row in self.cells:
            new_cells.append(row[::-1])
        self.cells = new_cells  
                        
    def move_row_left(self, row):
        #move numbers to the most left nonempty cells and fill up right cells with 0  
        def tighten(row):
            new_row = []
            for i in row:
                if i != 0:
                    new_row.append(i)
            for i in range(len(row) - len(new_row)):
                new_row.append(0)
            return new_row
        
        #merge two same numbers in adjacent cells and cumulate score 
        def merge(row):
            pair = False
            new_row = []
            for i in range(len(row)):
                if pair:
                    new_row.append(row[i] + row[i])
                    self.parent.score += 2 * row[i]
                    pair = False
                else:
                    if i < len(row) - 1 and row[i] == row[i + 1]:
                        pair = True
                        new_row.append(0)
                    else:
                        new_row.append(row[i])
            return new_row
        return tighten(merge(tighten(row)))
    
    #base movement
    def move_left(self):
        new = []
        for row in self.cells:
            new.append(self.move_row_left(row))
        self.cells = new

    #transform other movements into base movement and then reverse back
    def move_right(self):
        self.invert()
        self.move_left()
        self.invert()

    def move_up(self):
        self.transpose()
        self.move_left()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.move_right()
        self.transpose()
    
    @staticmethod                   
    # check if it is possible to move left                    
    def row_can_move_left(row):
        #check one row 
        def change(i):
            if row[i] == 0 and row[i + 1] != 0:
                return True
            if row[i] != 0 and row[i + 1] == row[i]:
                return True
            return False
   
        #loop through and check all rows in range 
        check = False
        for i in range(len(row) - 1):
            if change(i):
                check = change(i)
                return check
        return check    
                        
    def can_move_right(self):
        self.invert()
        can = self.can_move_left()
        self.invert()
        return can

    def can_move_up(self):
        self.transpose()
        can = self.can_move_left()
        self.transpose()
        return can

    def can_move_down(self):
        self.transpose()
        can = self.can_move_right()
        self.transpose()
        return can                  


class Screen(object):
    menu1 = '(W)up (S)down (A)left (D)right'
    menu2 = '   (R)Restart (Q)Exit'
    win_string = 'Congratulations Paul, You Did It!'
    over_string = 'Sorry Paul, Please Try Again...'
    
    def __init__(self,screen=None, grid=None, score=0, best_score=0, over=False, win=False):
        self.grid = grid
        self.score = score
        self.over = over
        self.win = win
        self.screen = screen
        self.counter = 0
    
    #print out messages                    
    def cast(self, string):
        self.screen.addstr(string + '\n')
    
    #draw vertical line to seperate grids and fill numbers into grids
    def draw_row(self, row):
        self.cast(''.join('|{: ^4}'.format(num) if num > 0 else '|   ' for num in row) + '|')

    #horizontal line, show scores and integrate                    
    def draw(self):
        self.screen.clear()
        self.cast('SCORE:' + str(self.score))
        for row in self.grid.cells:
            self.cast('+----' * self.grid.size + '+')
            self.draw_row(row)
        self.cast('+----' * self.grid.size + '+')
                         
                      
class main(object):
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
    #make instance of Screen class for display
    def screen(self):
        return Screen(screen=self.stdscr, score=self.score, grid=self.grid, win=self.win, over=self.over)
    
    def move(self, direction):
        if self.can_move(direction):
            getattr(self.grid, 'move_' + direction,self)()
            self.grid.spawn()
            return True
        else:
            return False                 
    
    @property
    #find max number in all cells and compare it with win_num
    def is_win(self):
        self.win = max(chain(*self.grid.cells)) >= self.win_num
        return self.win                        
    
    @property
    def is_over(self):
        self.over = True
        for move in self.action.actions_over:
            if self.can_move(move):
                self.over = False
                return self.over
        return self.over        
    
    #check possible movement direction
    def can_move(self, direction):
        return getattr(self.grid, 'can_move_' + direction)()

    def state_init(self):
        self.reset()
        return 'game'
    
    #move to next state 
    def state_game(self):
        self.screen.draw()
        action = self.action.get()

        if action == Action.RESTART:
            return 'init'
        if action == Action.EXIT:
            return 'exit'
        if self.move(action):
            if self.is_win:
                return 'win'
            if self.is_over:
                return 'over'
        return 'game'

    def _restart_or_exit(self):
        self.screen.draw()
        return 'init' if self.action.get() == Action.RESTART else 'exit'

    def state_win(self):
        return self._restart_or_exit()

    def state_over(self):
        return self._restart_or_exit()
    
    def __call__(self, stdscr):
        curses.use_default_colors()
        self.stdscr = stdscr
        self.action = Action(stdscr)
        while self.state != 'exit':
            self.state = getattr(self, 'state_' + self.state)()
            
if __name__ == '__main__':
    curses.wrapper(main())                   
