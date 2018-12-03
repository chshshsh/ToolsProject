# Group 3 Project - Game of 2048

> -  Group members: 
> -  Shuhui Chen         (sc4368)
> -  Tian Lei            (tl2846)
> -  Edison Wang         (yw3102)                 

# Desciption
> - We created game of 2048 using OOP as our main tool to contruct main structure. We took advantage of the packages we learned such as time, random and etc.   


## Intro to the Game

2048 is a single-player sliding block puzzle game, played on a gray 4×4 grid, with numbered tiles that slide smoothly when a player moves them using the four arrow keys

> - Every turn, a new tile will randomly appear in an empty spot on the board with a value of either 2 or 4
> - Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid
> - If two tiles of the same number collide while moving, they will merge into a tile with the total value of the two tiles that collided
> - The resulting tile cannot merge with another tile again in the same move. Higher-scoring tiles emit a soft glow
> - The user's score is tracked and starts at zero, and is incremented whenever two tiles combine, by the value of the new tile


## How to Win

The game objective is:

> - Slide numbered tiles on a grid to combine them to create a tile with the number 2048, the name of the game :)
> - Reach as high as possible on the scores

## Run the File

> - Please download the .py file and run it on Terminal using command code: 'python3 Project/ 2048.py'
> - Packages required: random, curses, time, from itertools import chain
> - Enjoy the game!
