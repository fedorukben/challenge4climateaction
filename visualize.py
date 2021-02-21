import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np
import config as g

from utils import Debugger

class Plotter(object):
  def __init__(self):
    self.debug = Debugger()
    self._set_axes()
    self._set_labels()
    self.sketches = []
    self.filename = g.files['plot']
    self.debug.prn(self, 'Plotter object created.')
  def class_name(self):
    return 'Plotter'
  def _set_axes(self):
    plt.axhline(0, color=g.x_clr)
    plt.axvline(0, color=g.y_clr)
    self.debug.prn(self, 'Axes drawn.', 3)
  def set_x_axis_label(self, x_label):
    plt.xlabel(x_label)
  def set_y_axis_label(self, y_label):
    plt.ylabel(y_label)
  def set_axis_labels(self, x_label, y_label):
    plt.xlabel(x_label)
    plt.ylabel(y_label)
  def _set_labels(self):
    plt.xlabel(g.x_lbl)
    plt.ylabel(g.y_lbl)
    self.debug.prn(self, 'Labels set.', 3)
  def set_output_filename(self, filename):
    self.filename = filename
    self.debug.prn(self, 'Filename set.')
  def set_title(self, title):
    plt.title(title)
    self.debug.prn(self, 'Title set.')
  def get_sketches(self):
    return self.sketches
  def load(self, sketches):
    if type(sketches) == list:
      for sketch in sketches:
        self.sketches.append(sketch)
      self.debug.prn(self, 'Sketches loaded')
    elif issubclass(type(sketches), Sketch):
      self.sketches.append(sketches)
      self.debug.prn(self, 'Sketch loaded.')
    else:
      self.debug.prn(self, 'load() takes either a Sketch or a list', 1)
  def _plot(self):
    for sketch in self.sketches:
      sketch.plot()
  def show(self):
    self._plot()
    plt.show()
  def save(self):
    self._plot()
    plt.savefig(self.filename)
  def close(self):
    plt.close()
    self.debug.prn(self, 'Plot closed.')

class Sketch(object):
  def __init__(self):
    self.debug = Debugger()
    self.x = []
    self.y = []
  def class_name(self):
    return 'Sketch'
  def add_x(self, x):
    if type(x) == list:
      for v in x:
        self.x.append(v)
      self.debug.prn(self, 'Added x-vals.')
    elif type(x) == int or type(x) == np.float64:
      self.x.append(x)
      self.debug.prn(self, 'Added x-val.')
    else:
      self.debug.prn(self, 'Incorrect type passed to add_x()', 1)
      print(type(x))
  def get_x(self):
    return self.x
  def add_y(self, y):
    for v in y:
      self.y.append(v)
    self.debug.prn(self, 'Added y-vals.')
  def get_y(self):
    return self.y
  def add(self, c):
    for x,y in c:
      self.x.append(x)
      self.y.append(y)
    self.debug.prn(self, 'Added coords.')
  def plot(self):
    self.debug.prn(self, 'Cannot call plot() on abstract Sketch.', 1)

class ScatterSketch(Sketch):
  def __init__(self):
    super().__init__()
  def class_name(self):
    return 'ScatterSketch'
  def plot(self):
    if len(self.x) == len(self.y):
      plt.scatter(self.x, self.y)
      self.debug.prn(self, 'Sketch drawn.')
    else:
      self.debug.prn(self, f'x({len(self.x)}) and y({len(self.y)}) must be of same length.', 1)

class SmoothSketch(Sketch):
  def __init__(self):
    super().__init__()
  def class_name(self):
    return 'SmoothSketch'
  def plot(self):
    if len(self.x) == len(self.y):
      plt.plot(self.x, self.y)
      self.debug.prn(self, 'Sketch drawn.')
    else:
      self.debug.prn(self, f'x({len(self.x)}) and y({len(self.y)}) must be of same length.', 1)

class HistogramSketch(Sketch):
  def __init__(self):
    super().__init__()
    self.bins = math.ceil(math.sqrt(len(self.x)))
  def class_name(self):
    return 'HistogramSketch'
  def add_y(self, y):
    self.debug.prn(self, 'Histograms do not need y.', 1)
  def add(self, c):
    self.debug.prn(self, 'Histograms do not need y.', 1)
  def set_bins(self, bins=None):
    if bins == None:
      self.bins = math.ceil(math.sqrt(len(self.x)))
    else:
      self.bins = bins
    self.debug.prn(self, 'Bins set.')
  def get_bins(self):
    return self.bins
  def plot(self):
    plt.hist(self.x, self.bins)
    self.debug.prn(self, 'Sketch drawn.')

class HorizontalLineSketch(Sketch):
  def __init__(self):
    super().__init__()
    self.x_max = None
    self.x_min = None
  def class_name(self):
    return 'HorizontalLineSketch'
  def add_y(self, y):
    self.debug.prn(self, 'Use set_y() for HorizontalLineSketch.', 1)
  def set_y(self, y):
    self.y = y
    self.debug.prn(self, 'Y set.')
  def add_x(self):
    self.debug.prn(self, 'Use set_x_max() and set_x_min() for HorizontalLineSketch.', 1)
  def set_x_max(self, x_max):
    self.x_max = x_max
    self.debug.prn(self, 'Maximum x set.')
  def set_x_min(self, x_min):
    self.x_min = x_min
    self.debug.prn(self, 'Minimum x set.')
  def get_x(self):
    self.debug.prn(self, 'Use get_x_max() and get_x_min() for HorizontalLineSketch.', 1)
  def get_x_max(self):
    return self.x_max
  def get_x_min(self):
    return self.x_min
  def plot(self):
    if not (self.y == [] or self.x_max == None or self.x_min == None):
      plt.hlines(self.y, self.x_max, self.x_min)
      self.debug.prn(self, 'Sketch drawn.')
    else:
      self.debug.prn(self, 'Y, x_max, or x_min not defined.', 1)

class VerticalLineSketch(Sketch):
  def __init__(self):
    super().__init__()
    self.y_max = None
    self.y_min = None
  def class_name(self):
    return 'VerticalLineSketch'
  def add_x(self, x):
    self.debug.prn(self, 'Use set_x() for VerticalLineSketch.', 1)
  def set_x(self, x):
    self.x = x
    self.debug.prn(self, 'X set.')
  def add_y(self):
    self.debug.prn(self, 'Use set_y_max() and set_y_min() for VerticalLineSketch.', 1)
  def set_y_max(self, y_max):
    self.y_max = y_max
    self.debug.prn(self, 'Maximum y set.')
  def set_y_min(self, y_min):
    self.y_min = y_min
    self.debug.prn(self, 'Minimum y set.')
  def get_y(self):
    self.debug.prn(self, 'Use get_y_max() and get_y_min() for VerticalLineSketch.', 1)
  def get_y_max(self):
    return self.y_max
  def get_y_min(self):
    return self.y_min
  def plot(self):
    if not (self.x == [] or self.y_max == None or self.y_min == None):
      plt.vlines(self.x, self.y_max, self.y_min)
      self.debug.prn(self, 'Sketch drawn.')
    else:
      self.debug.prn(self, 'X, y_max, or y_min not defined.', 1)