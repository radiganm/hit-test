#!/usr/bin/env python
## visualize.py
## Copyright 2012 Mac Radigan
## All Rights Reserved

import argparse
from io import StringIO
from os.path import basename, splitext
from matplotlib.pyplot import plot, text, title, show, ioff, savefig, xlim, ylim, rc
from numpy import array
from abc import *

class AbstractShape(object):
  """Abstract shape"""
  __metaclass__ = ABCMeta
  @abstractmethod
  def foo(self):
    pass

class Box(AbstractShape):
  """Axis-aligned box in pixels"""
  def __init__(self, x1, y1, x2, y2):
    self.x1 = float(x1)
    self.y1 = float(y1)
    self.x2 = float(x2)
    self.y2 = float(y2)
    self.min_x = min(x1, x2)
    self.min_y = min(y1, y2)
    self.max_x = max(x1, x2)
    self.max_y = max(y1, y2)
    self.tiles = []
    self.ids = []
  def __str__(self):
    return("box {0:0.{1}f} {2:0.{3}f} {4:0.{5}f} {6:0.{7}f}".format(
      self.x1, 1 if int(self.x1 % 1 > 0) else 0, 
      self.y1, 1 if int(self.y1 % 1 > 0) else 0, 
      self.x2, 1 if int(self.x2 % 1 > 0) else 0, 
      self.y2, 1 if int(self.y2 % 1 > 0) else 0 ) )
  def get_shape(self):
    # CCW, starting with UL corner
    pts_x = [self.min_x, self.max_x, self.max_x, self.min_x, self.min_x]
    pts_y = [self.max_y, self.max_y, self.min_y, self.min_y, self.max_y]
    return (pts_x, pts_y)
  def get_label(self):
    return '%2.1f %2.1f %2.1f %2.1f' % (self.min_x, self.min_y, self.max_x, self.max_y)

class Point(AbstractShape):
  """uniquely identified 2D point in pixels"""
  def __init__(self, x, y, id):
    self.x = x
    self.y = y
    self.id = id
  def __str__(self):
    return "point %2.1f %2.1f %s"%(self.x, self.y, self.id)


def read_shapes(filename):
  'Parse shapes from file'
  shapes = []
  box_positions = []
  infile = open(filename, 'r')
  sfile = StringIO(infile.read())
  infile.close()
  line_index = 0
  for line in sfile:
    columns = line.strip().split()
    if columns: # skip blank lines
      type = columns[0]
      if 'box'==type:
        box_positions.append(line_index)
        x1 = float(columns[1])
        y1 = float(columns[2])
        x2 = float(columns[3])
        y2 = float(columns[4])
        box = Box(x1, y1, x2, y2)
        shapes.append(box)
        line_index += 1
      elif 'point'==type:
        x  = float(columns[1])
        y  = float(columns[2])
        id = columns[3]
        point = Point(x, y, id)
        shapes.append(point)
        line_index += 1
      elif type[0] in ['#','/',' ']:
        pass # comment or blank line
      else:
        raise ValueError('Unsupported shape: %s'%(type))
  sfile.close()
  return (shapes, box_positions)

def plot_shapes(points, boxes, filename, label, output, verbose):
  'Plot a list of boxes and points'
  DX = 0.25
  DY = 0.25
  (name, ext) = splitext(basename(filename))
  if not output:
    ioff()
  if verbose:
    for point in points:
      print(point)
    for box in boxes:
      print(box)
  pt_x = [pt.x for pt in points]
  pt_y = [pt.y for pt in points]
  plot(pt_x, pt_y, 'rx')
  if(label):
    for pt in points:
      text(pt.x+DX, pt.y+DY, pt.id[0:4])
  for box in boxes:
    (bx, by) = box.get_shape()
    plot(bx, by)
    #if(label):
    # text(box.xMin+DX, box.yMax+DY, pt.id[0:4])
    #  text(box.xMin+DX, box.yMax+DY, box.get_label())
  title(name)
  if output:
    savefig(output)
  else:
    show()


def main(filename, label, output, verbose):
  (shapes, box_positions) = read_shapes(filename)
  boxes = [shapes[n] for n in box_positions]
  points = [shapes[n] for n in set(range(0,len(shapes))) - set(box_positions)]
  plot_shapes(points, boxes, filename, label, output, verbose)
  exit(0)

if __name__ == '__main__':
 parser = argparse.ArgumentParser(description='plot intput files')
 parser.add_argument('-f', '--file', dest='filename', required=True, help='input file path')
 parser.add_argument('-o', '--output', dest='output', default=False, help='output file name')
 parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='verbose output to stdout')
 parser.add_argument('-l', '--label', action='store_true', dest='label', default=False, help='label points on plot')
 args = parser.parse_args()
 main(args.filename, args.label, args.output, args.verbose)

## *EOF*
