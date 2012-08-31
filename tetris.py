#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Tetяis

    Keys
    --------------------------------------------------
    left   : request to translate left by one column
    right  : request to translate right by one column
    up     : request to do a counterclockwise rotation
    down   : request to translate down by one row

__author__ = 'Leonardo Vidarte'

"""

import time
import random
import copy

import Tkinter as tk
import tkMessageBox

from pprint import pprint as pp


# ===============================================
# OPTIONS
# ===============================================
DEBUG = True

# Board
WIDTH = 10
HEIGHT = 20
BG_COLOR = 'black'
FG_COLOR = 'white'
GRID_COLOR = '#333'

# Status
FONT_SIZE = 14

# Tetrominos
SIZE = 30 # square size in pixels
BORDER_COLOR = 'black'
BORDER_WIDTH = 2 # in pixels
I_COLOR = 'cyan'
O_COLOR = 'yellow'
T_COLOR = 'magenta'
J_COLOR = 'blue'
L_COLOR = 'orange'
S_COLOR = 'green'
Z_COLOR = 'red'
COMPLETE_ROW_BG_COLOR = None # None for inherit
COMPLETE_ROW_FG_COLOR = 'white'

# Levels
LEVEL_0_DELAY = 1000 # inital delay between steps
LEVEL_STEPS = 100 # total pieces by level
# ===============================================


# Tetrominos
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

    def __init__(self, width=WIDTH, height=HEIGHT, size=SIZE):
        tk.Frame.__init__(self, bg=BG_COLOR)
        self.grid()
        self.width = width
        self.height = height
        self.size = size
        self.create_widgets()
        self.draw_grid()
        self.create_events()
        self.tetrominos = self.get_tetrominos()
        self.game_init()

    def create_widgets(self):
        top = self.winfo_toplevel()
        top.config(bg=BG_COLOR)

        width = self.width * self.size
        height = self.height * self.size
        self.canvas = tk.Canvas(self, width=width, height=height, bg=BG_COLOR)
        self.canvas.grid(row=0, column=0, padx=20, pady=20)

        sidebar = self.sidebar = tk.Frame(self, bg=BG_COLOR)
        sidebar.grid(row=0, column=1, padx=(0, 20), pady=20, sticky=tk.N)

        self.lb_status = tk.Label(sidebar, bg=BG_COLOR, fg=FG_COLOR,
                                  font=('monospace', FONT_SIZE))
        self.lb_status.grid()

    def draw_grid(self):
        for i in xrange(self.width - 1):
            x = (self.size * i) + self.size
            y0 = 0
            y1 = self.size * self.height
            self.canvas.create_line(x, y0, x, y1, fill=GRID_COLOR)
        for i in xrange(self.height - 1):
            x0 = 0
            x1 = self.size * self.width
            y = (self.size * i) + self.size
            self.canvas.create_line(x0, y, x1, y, fill=GRID_COLOR)

    def create_events(self):
        self.canvas.bind_all('<KeyPress-Up>', self.rotate)
        self.canvas.bind_all('<KeyPress-Down>', self.move)
        self.canvas.bind_all('<KeyPress-Left>', self.move)
        self.canvas.bind_all('<KeyPress-Right>', self.move)

    def get_tetrominos(self):
        return [
            {'name': 'I', 'pieces': I, 'color': I_COLOR,
             'coords': self.get_init_coords(I),
             'actual': 0, 'ids': []},
            {'name': 'O', 'pieces': O, 'color': O_COLOR,
             'coords': self.get_init_coords(O),
             'actual': 0, 'ids': []},
            {'name': 'T', 'pieces': T, 'color': T_COLOR,
             'coords': self.get_init_coords(T),
             'actual': 0, 'ids': []},
            {'name': 'J', 'pieces': J, 'color': J_COLOR,
             'coords': self.get_init_coords(J),
             'actual': 0, 'ids': []},
            {'name': 'L', 'pieces': L, 'color': L_COLOR,
             'coords': self.get_init_coords(L),
             'actual': 0, 'ids': []},
            {'name': 'S', 'pieces': S, 'color': S_COLOR,
             'coords': self.get_init_coords(S),
             'actual': 0, 'ids': []},
            {'name': 'Z', 'pieces': Z, 'color': Z_COLOR,
             'coords': self.get_init_coords(Z),
             'actual': 0, 'ids': []},
            ]

    def get_init_coords(self, tetromino):
        return (int(self.width / 2.0 - len(tetromino[0]) / 2.0), 1)

    def game_init(self):
        self.board = self.get_init_board()
        self.next = copy.deepcopy(random.choice(self.tetrominos))
        self.tetromino = None
        self.status = self.get_init_status()
        self.delay = LEVEL_0_DELAY
        self.job_id = None
        self.step()

    def get_init_board(self):
        if getattr(self, 'board', None) is None:
            self.board = [[0] * self.width for _ in xrange(self.height)]
        else:
            for y in xrange(self.height):
                for x in xrange(self.width):
                    if self.board[y][x]:
                        self.canvas.delete(self.board[y][x])
                        self.board[y][x] = 0
        return self.board

    def get_init_status(self):
        return {'score': 0, 'last_points': 0, 'next': '',
                'O': 0, 'I': 0, 'S': 0, 'T': 0, 'Z': 0, 'L': 0, 'J': 0,
                'total': 0, 'rows': 0, 'level': 0,}

    def step(self):
        if self.tetromino and self.can_be_moved('Down'):
            x, y = self.tetromino['coords']
            self.tetromino['coords'] = (x, y + 1)
            self.draw_tetromino()
            self.job_id = self.canvas.after(self.delay, self.step)
        else:
            self.check_status()
            if self.is_gameover(self.next):
                self.canvas.after_cancel(self.job_id)
                title = 'Game Over'
                message = '%s\nYour score: %d' % (title, self.status['score'])
                tkMessageBox.showinfo(title, message)
                self.game_init()
            else:
                self.tetromino = self.next
                self.next = copy.deepcopy(random.choice(self.tetrominos))
                self.status[self.tetromino['name']] += 1
                self.status['total'] += 1
                if self.status['total'] % LEVEL_STEPS == 0:
                    self.status['level'] += 1
                    if self.delay:
                        self.delay -= 100
                self.status['next'] = self.next['name']
                self.update_label_status()
                self.draw_tetromino()
                self.job_id = self.canvas.after(self.delay, self.step)

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
                self.canvas.itemconfig(id, fill=COMPLETE_ROW_BG_COLOR,
                                       outline=COMPLETE_ROW_FG_COLOR)
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
        points = scores[len(rows) - 1]
        self.status['rows'] = len(rows)
        self.status['last_points'] = points
        self.status['score'] += points
        self.update_label_status()

    def update_label_status(self):
        lines = [
            'Score: %6s' % self.status['score'],
            '',
            'Level: %6s' % self.status['level'],
            'Rows : %6s' % self.status['rows'],
            '',
            'O    : %6s' % self.status['O'],
            'I    : %6s' % self.status['I'],
            'J    : %6s' % self.status['J'],
            'L    : %6s' % self.status['L'],
            'T    : %6s' % self.status['T'],
            'S    : %6s' % self.status['S'],
            'Z    : %6s' % self.status['Z'],
            'Total: %6s' % self.status['total'],
            '',
            'Next : %6s' % self.status['next'],
            ] 
        self.lb_status.config(text='\n'.join(lines))

    def is_gameover(self, next):
        piece = next['pieces'][0]
        x, y = next['coords']
        for y0 in xrange(len(piece)):
            for x0 in xrange(len(piece[0])):
                x1 = x0 + x
                y1 = y0 + y
                if self.board[y1][x1]:
                    return True
        return False

    def draw_tetromino(self):
        self.del_tetromino()
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
                            x1, y1, x2, y2, width=BORDER_WIDTH,
                            outline=BORDER_COLOR,
                            fill=self.tetromino['color'])
                    self.tetromino['ids'].append(id)
                    self.board[y0 + y][x0 + x] = id
        self.canvas.update()
        if DEBUG:
            pp(self.board)

    def del_tetromino(self):
        if self.tetromino['ids']:
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
                self.job_id = self.canvas.after(self.delay, self.step)

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


if __name__ == '__main__':

    prog = u'Tetяis'

    from optparse import OptionParser
    parser = OptionParser(description=prog)
    parser.add_option('-W', '--width', type=int, default=WIDTH,
                      help="board width")
    parser.add_option('-H', '--height', type=int, default=HEIGHT,
                      help="board height")
    parser.add_option('-s', '--size', type=int, default=SIZE,
                      help="square size")
    args, _ = parser.parse_args()

    app = Application(args.width, args.height, args.size)
    app.master.title(prog)
    app.mainloop()

