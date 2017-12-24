#!/usr/bin/env python
## data_source.py
## Copyright 2012 Mac Radigan
## All Rights Reserved

"""data_source.py

This module performs input file generation, with the probability of the next shape 
generated being a box (with probability p) or a point (with probability 1-p).  

The generator will apply the above specification to generate a sequence of N shapes.
If the number of shape records is not specified, the sequence will be infinite in 
length (continue forever).

Example:
  The main function provides an entry point for the 
  generation of input data.

   usage: data_source <args>
   
   optional arguments:
       -h, --help                          show this help message and exit
       -n,--total-records COUNT            total number of records [d:unlimited]
       -p,--box-probability P              Bernoulli probability of a record being a box [d:0.10]
       -r,--extent-rectangle x1 y1 x2 y2   extent rectangle, upper left and lower right corners
                                           of 2D extent from which bivariate uniform random
                                           points are drawn. [d:-100 -100 100 100]
       NOTE:
         This is designed to be a data source used with dd, and will continue printing
         forever if no record limit (--total-records) is specified.

"""

from abc import *
import argparse
from sys import argv, stderr, exit, version_info, version
from uuid import  uuid4
from random import random
from random import uniform
import errno
import signal

class Box():
  """Draws a random box from an urn, bounded by extent (x1, y1, x2, y2)."""
  def __init__(self, extent_rectangle):
    x1 = min(extent_rectangle[0], extent_rectangle[2])
    y1 = min(extent_rectangle[1], extent_rectangle[3])
    x2 = max(extent_rectangle[0], extent_rectangle[2])
    y2 = max(extent_rectangle[1], extent_rectangle[3])
    x_a = x1
    x_b = x2
    self.x_min = x_a + (x_b - x_a) * random() # x_min ~U[x1,x2]
    self.x_max = x_a + (x_b - x_a) * random() # x_max ~U[x1,x2]
    y_a = y1
    y_b = y2
    self.y_min = y_a + (y_b - y_a) * random() # y_min ~U[y1,y2]
    self.y_max = y_a + (y_b - y_a) * random() # y_max ~U[y1,y2]
  def __str__(self):
    return ('box %0.1f %0.1f %0.1f %0.1f' % (self.x_min, self.y_min, self.x_max, self.y_max))

class Point():
  """Draws a random point from an urn, bounded by extent (x1, y1, x2, y2)."""
  def __init__(self, extent_rectangle):
    x1 = min(extent_rectangle[0], extent_rectangle[2])
    y1 = min(extent_rectangle[1], extent_rectangle[3])
    x2 = max(extent_rectangle[0], extent_rectangle[2])
    y2 = max(extent_rectangle[1], extent_rectangle[3])
    self.uid = uuid4()
    x_a = x1
    x_b = x2
    self.px = x_a + (x_b - x_a) * random() # px ~U[x1,x2]
    y_a = y1
    y_b = y2
    self.py = y_a + (y_b - y_a) * random() # py ~U[y1,y2]
  def __str__(self):
    return ('point %0.1f %0.1f %s' % (self.px, self.py, self.uid))

def main(n_records, probability_box, extent_rectangle):
  """Generate a sequence of n_records.  Note that n_records may be infinity."""
  signal.signal(signal.SIGPIPE, signal.SIG_DFL)
  try:
    if n_records < float("inf"):
      for n in range(0, int(n_records)):
        xp = uniform(0.0, 1.0)    # draw a random number
        if(xp < probability_box): # a box is drawn from an urn
           box = Box(extent_rectangle)
           print(box)
        else:                     # a point is drawn from an urn
           point = Point(extent_rectangle)
           print(point)
    else:
      while True:
        xp = uniform(0.0, 1.0)    # draw a random number
        if(xp < probability_box): # a box is drawn from an urn
           box = Box(extent_rectangle)
           print(box)
        else:                     # a point is drawn from an urn
           point = Point(extent_rectangle)
           print(point)
  except IOError as ex:
    if ex.errno == errno.EPIPE:
      print('%s'%e, file=stderr)
      raise
    else:
      raise

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='input file generator')
  parser.add_argument('-n', '--nrecords', dest='n_records', default=float("inf"), required=False, type=float, help='number of points')
  parser.add_argument('-p', '--probability-box', dest='probability_box', required=False, default=0.05, type=float, help='probability of selecting a box')
  parser.add_argument('-r', '--extent-rectangle', dest='extent_rectangle', required=False, default=[-100,-100,100,100], nargs=4, metavar=('x1','y1','x2','y2'), type=float, help='extent of point distribution')
  args = parser.parse_args()
  main(args.n_records, args.probability_box, args.extent_rectangle)

## *EOF*
