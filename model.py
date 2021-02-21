from utils import Debugger
from utils import Math
from utils import ImageManager
from utils import Randomizer

from visualize import Plotter
from visualize import ScatterSketch
from visualize import SmoothSketch
from visualize import HistogramSketch
from visualize import VerticalLineSketch
from visualize import HorizontalLineSketch

import math
import config as g

class Modeller(object):
  def __init__(self, analyzer):
    self.debug = Debugger()
    self.randomizer = Randomizer()
    self.analyzer = analyzer
    self.data = None
    self.linear_models = []
  def class_name(self):
    return "Modeller"
  def linear(self, index):
    return self.linear_models[index]
  def gen_linear(self, slope, yint, x, y):
    i = len(self.linear_models) + 1
    linear_model = LinearModel(lambda x : slope * x + yint, x, y, i)
    linear_model.plot()
    self.linear_models.append(linear_model)
  def gen_least_squares(self, x, y):
    slope, yint = self.analyzer.least_squares_slope_yint_eqn(x, y)
    self.gen_linear(slope, yint, x, y)
  
class Model(object):
  def __init__(self, f, training_x, training_y, index):
    self.f = f
    self.debug = Debugger()
    self.training_x = training_x
    self.training_y = training_y
    self.index = index
  def get_f(self):
    return self.f
  def get_training_x(self):
    return self.training_x
  def get_training_y(self):
    return self.training_y
  def set_f(self, f):
    self.f = f
  def get_index(self):
    return self.index

class LinearModel(Model):
  def __init__(self, f, training_x, training_y, index):
    super().__init__(f, training_x, training_y, index)
    self.math = Math()
  def class_name(self):
    return "LeastSquaresModel"
  def get_sum_of_squared_residuals(self):
    ss_residuals_av = 0
    for x,y in zip(self.training_x, self.training_y):
      ss_residuals_av += math.abs(y - self.f(x)) ** 2
  def get_slope(self):
    return (self.f(self.training_x[0]) - self.f(self.training_x[1])) / (self.training_x[0] - self.training_x[1])
  def get_yint(self):
    return (self.f(self.training_x[0]) - self.get_slope() * self.training_x[0])
  def plot(self):
    plotter = Plotter()
    image_manager = ImageManager()
    sketches = []
    plotter.set_output_filename(g.files['least-squares'])
    plotter.set_title('Least Squares')

    # min_x = min(self.training.get_output()[x_index])
    # max_x = max(self.training.get_output()[x_index])
    min_x = min(self.training_x)
    max_x = max(self.training_x)
    x_vals = []
    y_vals = []
    for x in range(min_x * 100, max_x * 100):
      x_vals.append([x / 100])
      y_vals.append([self.f(x / 100)])
    sketches.append(SmoothSketch())
    sketches[-1].add_x(x_vals)
    sketches[-1].add_y(y_vals)

    sketches.append(ScatterSketch())
    sketches[-1].add_x(list(self.training_x))
    sketches[-1].add_y(list(self.training_y))

    for i in range(len(self.training_x)):
      if self.f(self.training_x[i]) > self.training_y[i]:
        y_max = self.f(self.training_x[i])
        y_min = self.training_y[i]
      else:
        y_min = self.f(self.training_x[i])
        y_max = self.training_y[i]
      sketches.append(VerticalLineSketch())
      sketches[-1].set_y_max(y_max)
      sketches[-1].set_y_min(y_min)
      sketches[-1].set_x(self.training_x[i])
    
    plotter.load(sketches)
    plotter.save()
    plotter.close()

    image_manager.scale(g.files['least-squares'], g.files['least-squares'], 250)

    del plotter
    del image_manager

class LogisticModel(Model):
  pass