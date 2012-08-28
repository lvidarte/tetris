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
      (0,1,1),
      (1,1,0)),
     ((1,0,0),
      (1,1,0),
      (0,1,0))]

z = [((0,0,0),
      (1,1,0),
      (0,1,1)),
     ((0,0,1),
      (0,1,1),
      (0,1,0))]

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
        self._pieces = []
        self._tetromino_name = random.choice(tetrominos.keys())
        self._tetromino, self._color = tetrominos[self._tetromino_name]
        self._actual = 0
        self._coords = (3, 2)
        self.draw_tetromino()

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

    def draw_tetromino(self):
        for id in self._pieces:
            self.canvas.delete(id)
        piece = self._tetromino[self._actual]
        x0, y0 = self._coords
        for x in xrange(len(piece[0])):
            for y in xrange(len(piece)):
                if piece[y][x] == 1:
                    x1 = (x0 + x) * self.size
                    y1 = (y0 + y) * self.size
                    x2 = x1 + self.size
                    y2 = y1 + self.size
                    id = self.canvas.create_rectangle(
                            x1, y1, x2, y2, width=2, fill=self._color)
                    self._pieces.append(id)

    def rotate(self, event):
        if self._actual < len(self._tetromino) - 1:
            next = self._actual + 1
        else:
            next = 0
        if self.can_be_rotated(next):
            self._actual = next
            self.draw_tetromino()

    def can_be_rotated(self, next):
        piece = self._tetromino[next]
        x0, y0 = self._coords
        for x in xrange(len(piece[0])):
            for y in xrange(len(piece)):
                if piece[y][x] == 1:
                    if x0 == -1 and x == 1:
                        return False
                    if x0 + x > self.width - 1:
                        return False
        return True

    def move(self, event):
        coords = None
        x, y = self._coords
        if event.keysym == 'Left':
            coords = (x - 1, y)
        if event.keysym == 'Right':
            coords = (x + 1, y)
        if event.keysym == 'Down':
            coords = (x, y + 1)
        if coords and self.can_be_moved(event.keysym):
            self._coords = coords
            self.draw_tetromino()

    def can_be_moved(self, direction):
        piece = self._tetromino[self._actual]
        x, y = self._coords
        for x1 in xrange(len(piece[0])):
            for y1 in xrange(len(piece)):
                if piece[y1][x1] == 1:
                    if direction == 'Left' and x + x1 - 1 < 0:
                        return False
                    if direction == 'Right' and x + x1 > self.width - 2:
                        return False
        return True


    def create_events(self):
        self.canvas.bind_all('<KeyPress-Up>', self.rotate)
        self.canvas.bind_all('<KeyPress-Down>', self.move)
        self.canvas.bind_all('<KeyPress-Left>', self.move)
        self.canvas.bind_all('<KeyPress-Right>', self.move)


if __name__ == '__main__':

    app = Application()
    app.master.title('Tetяis')
    app.mainloop()
