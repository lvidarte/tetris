#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Tetяis

left   : request to translate left  by one column
right  : request to translate right by one column
rotate : request to do a counterclockwise rotation
drop   : request to instantly drop the piece

"""

import time
import random
import copy
import Tkinter as tk

from pprint import pprint as pp


I = (
     ((0,0,0,0),
      (1,1,1,1),
      (0,0,0,0),
      (0,0,0,0)),
     ((0,1,0,0),
      (0,1,0,0),
      (0,1,0,0),
      (0,1,0,0)),
     )

O = (
     ((1,1),
      (1,1)),
     )

T = (
     ((0,0,0),
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
      (0,1,0)),
     )

J = (
     ((0,1,0),
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
      (0,0,1)),
     )

L = (
     ((0,1,0),
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
      (0,0,0)),
     )

S = (
     ((0,0,0),
      (0,1,1),
      (1,1,0)),
     ((1,0,0),
      (1,1,0),
      (0,1,0)),
     )

Z = (
     ((0,0,0),
      (1,1,0),
      (0,1,1)),
     ((0,0,1),
      (0,1,1),
      (0,1,0)),
     )


class Application(tk.Frame):

    def __init__(self, width=10, height=20, size=30):
        tk.Frame.__init__(self)
        self.grid()
        self.width = width
        self.height = height
        self.size = size
        self.board = [[0] * width for _ in xrange(height)]
        self.tetrominos = self.get_tetrominos()
        self.next = copy.deepcopy(random.choice(self.tetrominos))
        self.tetromino = None
        self.score = 0
        self.delay = 1000
        self.job_id = None
        self.create_widgets()
        self.draw_grid()
        self.create_events()
        self.start()

    def get_tetrominos(self):
        tetrominos = [
            {'name': 'I', 'pieces': I, 'color':'cyan',
             'coords': self.get_init_coords(I),
             'actual': 0, 'ids': []},
            {'name': 'O', 'pieces': O, 'color':'yellow',
             'coords': self.get_init_coords(O),
             'actual': 0, 'ids': []},
            {'name': 'T', 'pieces': T, 'color':'magenta',
             'coords': self.get_init_coords(T),
             'actual': 0, 'ids': []},
            {'name': 'J', 'pieces': J, 'color':'blue',
             'coords': self.get_init_coords(J),
             'actual': 0, 'ids': []},
            {'name': 'L', 'pieces': L, 'color':'orange',
             'coords': self.get_init_coords(L),
             'actual': 0, 'ids': []},
            {'name': 'S', 'pieces': S, 'color':'green',
             'coords': self.get_init_coords(S),
             'actual': 0, 'ids': []},
            {'name': 'Z', 'pieces': Z, 'color':'red',
             'coords': self.get_init_coords(Z),
             'actual': 0, 'ids': []},
            ]
        return tetrominos

    def get_init_coords(self, tetromino):
        coords = (int(self.width / 2.0 - len(tetromino[0]) / 2.0), 1)
        return coords

    def start(self):
        if self.tetromino and self.can_be_moved('Down'):
            x, y = self.tetromino['coords']
            self.tetromino['coords'] = (x, y + 1)
        else:
            self.check_status()
            self.tetromino = self.next
            self.next = copy.deepcopy(random.choice(self.tetrominos))
            self.update_status()
        self.draw_tetromino()
        self.job_id = self.canvas.after(self.delay, self.start)

    def check_status(self):
        rows = []
        for row in xrange(self.height):
            if 0 not in self.board[row]:
                rows.append(row)
        if rows:
            self.del_rows(rows)
            self.set_score(rows)

    def del_rows(self, rows):
        for row in rows:
            for id in self.board[row]:
                self.canvas.itemconfig(id, fill='white')
        self.canvas.update()
        time.sleep(0.5)
        for row in rows:
            for id in self.board[row]:
                self.canvas.delete(id)
            del self.board[row]
            self.board.insert(0, [0] * self.width)
            for row0 in xrange(row + 1):
                for id0 in self.board[row0]:
                    self.canvas.move(id0, 0, self.size)
        self.canvas.update()

    def set_score(self, rows):
        scores = [40, 100, 300, 1200]
        self.score += scores[len(rows) - 1]
        self.update_status()

    def update_status(self):
        text = 'Score: %d, Next: %s' % (self.score, self.next['name'])
        self.status.config(text=text)

    def create_widgets(self):
        width = self.width * self.size
        height = self.height * self.size
        self.canvas = tk.Canvas(self, width=width, height=height, bg='black')
        self.canvas.grid(row=0, column=0)
        self.status = tk.Label(self)
        self.status.grid(row=1, column=0)

    def draw_grid(self):
        color = '#333'
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
        self.drop_pieces()
        piece = self.tetromino['pieces'][self.tetromino['actual']]
        x0, y0 = self.tetromino['coords']
        for y in xrange(len(piece)):
            for x in xrange(len(piece[0])):
                if piece[y][x] == 1:
                    x1 = (x0 + x) * self.size
                    y1 = (y0 + y) * self.size
                    x2 = x1 + self.size
                    y2 = y1 + self.size
                    id = self.canvas.create_rectangle(
                            x1, y1, x2, y2, width=2,
                            fill=self.tetromino['color'])
                    self.tetromino['ids'].append(id)
                    self.board[y0 + y][x0 + x] = id
        self.canvas.update()
        pp(self.board)

    def drop_pieces(self):
        for y in xrange(self.height):
            for x in xrange(self.width):
                if self.board[y][x] in self.tetromino['ids']:
                    self.board[y][x] = 0
        for id in self.tetromino['ids']:
            self.canvas.delete(id)
        self.tetromino['ids'] = []

    def rotate(self, event):
        if len(self.tetromino['pieces']) == 1:
            return
        if self.tetromino['actual'] < len(self.tetromino['pieces']) - 1:
            next = self.tetromino['actual'] + 1
        else:
            next = 0
        if self.can_be_rotated(next):
            self.tetromino['actual'] = next
            self.draw_tetromino()

    def can_be_rotated(self, next):
        piece = self.tetromino['pieces'][next]
        board = self.board
        x, y = self.tetromino['coords']
        for y0 in xrange(len(piece)):
            for x0 in xrange(len(piece[0])):
                if piece[y0][x0] == 1:
                    if x == -1 and x0 == 1:
                        return False
                    if x + x0 >= self.width:
                        return False
                    if y + y0 >= self.height:
                        return False
                    x1 = x + x0
                    y1 = y + y0
                    if board[y1][x1] and \
                       (board[y1][x1] not in self.tetromino['ids']):
                        return False
        return True

    def move(self, event):
        if event.keysym in ('Left', 'Right', 'Down') and \
           self.can_be_moved(event.keysym):
            x, y = self.tetromino['coords']
            if event.keysym == 'Left':
                self.tetromino['coords'] = (x - 1, y)
                self.draw_tetromino()
            if event.keysym == 'Right':
                self.tetromino['coords'] = (x + 1, y)
                self.draw_tetromino()
            if event.keysym == 'Down':
                self.tetromino['coords'] = (x, y + 1)
                self.canvas.after_cancel(self.job_id)
                self.draw_tetromino()
                self.job_id = self.canvas.after(self.delay, self.start)

    def can_be_moved(self, direction):
        piece = self.tetromino['pieces'][self.tetromino['actual']]
        board = self.board
        x, y = self.tetromino['coords']
        for y0 in xrange(len(piece)):
            for x0 in xrange(len(piece[0])):
                if piece[y0][x0] == 1:
                    if direction == 'Left':
                        x1 = x + x0 - 1
                        y1 = y + y0
                        if x1 < 0 or (board[y1][x1] and
                           board[y1][x1] not in self.tetromino['ids']):
                            return False
                    if direction == 'Right':
                        x1 = x + x0 + 1
                        y1 = y + y0
                        if x1 >= self.width or (board[y1][x1] and
                           board[y1][x1] not in self.tetromino['ids']):
                            return False
                    if direction == 'Down':
                        x1 = x + x0
                        y1 = y + y0 + 1
                        if y1 >= self.height or (board[y1][x1] and
                           board[y1][x1] not in self.tetromino['ids']):
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
