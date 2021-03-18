

"""import tkinter
import functools

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height):
        root = tkinter.Tk()
        window = cls(root, width, height)
        root.mainloop()

    def __init__(self, master, width, height):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__build_buttons()
        self.grid()

    def __build_buttons(self):
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self)
                button.grid(column=x, row=y)
                button['text'] = ''
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __push(self, x, y):
        print('Column = {}\nRow = {}'.format(x, y))

if __name__ == '__main__':
    MineSweep.main(10, 10)
    MineSweep.__push(self,2,3)"""

from tkinter import *
import numpy as np
import random


# Makes the visual canvas for the grid
class showMaze():
  def __init__(self):
      DIM = 10
      # makes the window for the maze
      window = Tk()
      window.title("Fire Maze")

      # makes the grid all white
      for i in range(10):
        Canvas(window, width=30, height = 30, bg = color,).grid(row = i // DIM, column = i % DIM)

      width = 30*DIM*1.20
      height = 30*DIM*1.20
      screen_width = window.winfo_screenwidth()
      screen_height = window.winfo_screenheight()

      # calculate position x and y coordinates
      x = (screen_width/2) - (width/2)
      y = (screen_height/2) - (height/2)
      window.geometry('%dx%d+%d+%d' % (width, height, x, y))
      window.mainloop()

def makeGrid():
    global SIZE
    global PROB
    global GRID

    PROB = 0.3 
    start = 3
    end = 98
    DIM = 10
    SIZE = DIM**2

    GRID = np.ones(DIM**2)

    GRID[start] = -1
    GRID[end] = -2

    for i in range(SIZE):
        if  ( not i == start ) and (not i == end):
            if (random.random() <= PROB):
                GRID[i] =0

makeGrid()
showMaze()