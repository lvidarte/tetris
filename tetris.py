#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

left   : request to translate left  by one column
right  : request to translate right by one column
rotate : request to do a counterclockwise rotation
drop   : request to instantly drop the piece

"""

i = [((0,1,0,0),
      (0,1,0,0),
      (0,1,0,0),
      (0,1,0,0)),
     ((0,0,0,0),
      (1,1,1,1),
      (0,0,0,0),
      (0,0,0,0))]

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

s = [((1,1,0),
      (0,1,1),
      (0,0,0)),
     ((0,0,1),
      (0,1,1),
      (0,1,0))]

z = [((0,1,1),
      (1,1,0),
      (0,0,0)),
     ((1,0,0),
      (1,1,0),
      (0,1,0))]

tetrominos = {'i': i, # cyan
              'o': o, # yellow
              't': t, # magenta
              'j': j, # blue
              'l': l, # orange
              's': s, # green
              'z': z} # red

WIDTH = 10
HEIGHT = 20

board = [[0]*WIDTH for _ in xrange(HEIGHT)]
