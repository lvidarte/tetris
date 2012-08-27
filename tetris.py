#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Tetяis

left   : request to translate left  by one column
right  : request to translate right by one column
rotate : request to do a counterclockwise rotation
drop   : request to instantly drop the piece

"""

import random
import Tkinter as tk


i = [((0,0,0,0),
      (1,1,1,1),
      (0,0,0,0),
      (0,0,0,0)),
     ((0,1,0,0),
      (0,1,0,0),
      (0,1,0,0),
      (0,1,0,0))]

o = [((1,1),
      (1,1))]

t = [((0,0,0),
      (1,1,1),
      (0,1,0)),
     ((0,1,0),
      (1,1,0),
      (0,1,0)),
     ((0,1,0),
      (1,1,1),
      (0,0,0)),
     ((0,1,0),
      (0,1,1),
      (0,1,0))]

j = [((0,1,0),
      (0,1,0),
      (1,1,0)),
     ((1,0,0),
      (1,1,1),
      (0,0,0)),
     ((0,1,1),
      (0,1,0),
      (0,1,0)),
     ((0,0,0),
      (1,1,1),
      (0,0,1))]

l = [((0,1,0),
      (0,1,0),
      (0,1,1)),
     ((0,0,0),
      (1,1,1),
      (1,0,0)),
     ((1,1,0),
      (0,1,0),
      (0,1,0)),
     ((0,0,1),
      (1,1,1),
      (0,0,0))]

s = [((0,0,0),
      (1,1,0),
      (0,1,1)),
     ((0,1,0),
      (1,1,0),
      (1,0,0))]

z = [((0,0,0),
      (0,1,1),
      (1,1,0)),
     ((0,1,0),
      (0,1,1),
      (0,0,1))]

tetrominos = {'i': (i, 'cyan'),
              'o': (o, 'yellow'),
              't': (t, 'magenta'),
              'j': (j, 'blue'),
              'l': (l, 'orange'),
              's': (s, 'green'),
              'z': (z, 'red')
              }

WIDTH = 10
HEIGHT = 20

board = [[0]*WIDTH for _ in xrange(HEIGHT)]


class Application(tk.Frame):

    def __init__(self, width=10, height=20, size=20):
        tk.Frame.__init__(self)
        self.grid()
        self.width = width
        self.height = height
        self.size = size
        self.create_widgets()
        self.draw_grid()
        self.create_events()
        self.draw_tetromino(random.choice(tetrominos.keys()))

    def create_widgets(self):
        width = self.width * self.size
        height = self.height * self.size
        self.canvas = tk.Canvas(self, width=width, height=height, bg='white')
        self.canvas.grid(row=0, column=0)

        #self.status = tk.Label(self, text="")
        #self.status.grid(row=1, column=0)

    def draw_grid(self):
        color = 'gray'
        for i in xrange(self.width - 1):
            x = (self.size * i) + self.size
            y0 = 0
            y1 = self.size * self.height
            self.canvas.create_line(x, y0, x, y1, fill=color)
        for i in xrange(self.height - 1):
            x0 = 0
            x1 = self.size * self.width
            y = (self.size * i) + self.size
            self.canvas.create_line(x0, y, x1, y, fill=color)

    def draw_tetromino(self, tetromino):
        piece, color = tetrominos[tetromino]
        piece = piece[0]
        x0, y0 = (3, 1)
        for x in xrange(len(piece[0])):
            for y in xrange(len(piece)):
                if piece[x][y] == 1:
                    x1 = (x0 + x) * self.size
                    y1 = (y0 + y) * self.size
                    x2 = x1 + self.size
                    y2 = y1 + self.size
                    id = self.canvas.create_rectangle(
                            x1, y1, x2, y2, width=2, fill=color)

    def create_events(self):
        pass
        #self.canvas.bind_all('<Button-1>', self.draw)


if __name__ == '__main__':

    app = Application()
    app.master.title('Tetяis')
    app.mainloop()
