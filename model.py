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
import numpy as np

class Modeller(object):
  def __init__(self, analyzer):
    self.debug = Debugger()
    self.randomizer = Randomizer()
    self.analyzer = analyzer
    self.data = None
    self.linear_models = []
    self.logistic_models = []
    self.ridge_models = []
    g.debug.prn(self, 'Modeller object created.')
  def class_name(self):
    return "Modeller"
  def linear(self, index):
    g.debug.prn(self, 'Returned linear model.')
    return self.linear_models[index]
  def logistic(self, index):
    g.debug.prn(self, 'Returned logistic model.')
    return self.logistic_models[index]
  def gen_linear(self, slope, yint, x, y):
    i = len(self.linear_models) + 1
    linear_model = LinearModel(lambda x : slope * x + yint, x, y, i)
    linear_model.plot()
    self.linear_models.append(linear_model)
    g.debug.prn(self, 'Generated linear model.')
  def get_ridge(self, x, y):
    i = len(self.ridge_models) + 1
    slope, yint = self.analyzer.least_squares_slope_yint_eqn(x,y)
    ridge_model = RidgeModel(lambda x : slope * x + yint, x, y, i)
    ridge_model.plot()
    self.ridge_models.append(ridge_model)
    g.debug.prn(self, 'Generated ridge model.')
  def get_logistic(self, x, y):
    i = len(self.logistic_models) + 1
    m, b = g.analyzer.least_squares_slope_yint_eqn(x, y)
    f = lambda x : (math.e ** ((m * x) + (-m * b))) / (1 + (math.e ** ((m * x) + (-m * b))))
    logistic_model = LogisticModel(f, x, y, i)
    logistic_model.plot()
    self.logistic_models.append(logistic_model)
    g.debug.prn(self, 'Generated logistic model.')
  def gen_least_squares(self, x, y):
    slope, yint = self.analyzer.least_squares_slope_yint_eqn(x, y)
    self.gen_linear(slope, yint, x, y)
    g.debug.prn(self, 'Generated least squares linear model.')

class Model(object):
  def __init__(self, f, training_x, training_y, index):
    self.f = f
    self.debug = Debugger()
    self.training_x = training_x
    self.training_y = training_y
    self.index = index
    g.debug.prn(self, 'Model created.')
  def __str__(self):
    return "Abstract Model -- No function definable."
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
  def at(self, x):
    g.debug.prn(self, f'Returning value at {x}')
    return self.f(x)
  def plot(self):
    g.debug.prn(self, 'Cannot plot abstract Model.', 1)

class LinearModel(Model):
  def __init__(self, f, training_x, training_y, index):
    super().__init__(f, training_x, training_y, index)
    self.math = Math()
    g.debug.prn(self, 'LinearModel created')
  def __str__(self):
    return f'{self.get_slope()}x + {self.get_yint()}'
  def class_name(self):
    return "LinearModel"
  def get_sum_of_squared_residuals(self):
    ss_residuals_av = 0
    for x,y in zip(self.training_x, self.training_y):
      ss_residuals_av += math.abs(y - self.f(x)) ** 2
    g.debug.prn(self, 'SS Residuals gotten.')
    return ss_residuals_av
  def get_slope(self):
    g.debug.prn(self, 'Got slope.', 3)
    return (self.f(self.training_x[0]) - self.f(self.training_x[1])) / (self.training_x[0] - self.training_x[1])
  def get_yint(self):
    g.debug.prn(self, 'Got yint.', 3)
    return (self.f(self.training_x[0]) - self.get_slope() * self.training_x[0])
  def plot(self):
    plotter = Plotter()
    image_manager = ImageManager()
    sketches = []
    plotter.set_output_filename(g.files['least-squares'])
    plotter.set_title('Least Squares Regression')
    g.debug.prn(self, 'Plot basics set.')

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
    g.debug.prn(self, 'Linear curve saved as SmoothSketch.')

    sketches.append(ScatterSketch())
    sketches[-1].add_x(list(self.training_x))
    sketches[-1].add_y(list(self.training_y))
    g.debug.prn(self, 'Points saved as ScatterSketch.')

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
      g.debug.prn(self, 'Vertical line appended.', 3)
    g.debug.prn(self, 'SSR lines drawn as VerticalLineSketch(s).')

    plotter.load(sketches)
    plotter.save()
    plotter.close()
    g.debug.prn(self, 'All sketches loaded and saved.')

    image_manager.scale(g.files['least-squares'], g.files['least-squares'], 250)

    del plotter
    del image_manager
    g.debug.prn(self, 'Plotter and ImageManager objects deleted', 3)

class LogisticModel(Model):
  def __init__(self, f, training_x, training_y, index):
    super().__init__(f, training_x, training_y, index)
    self.math = Math()
  def class_name(self):
    return "LogisticModel"
  def plot(self):
    plotter = Plotter()
    image_manager = ImageManager()
    sketches = []
    plotter.set_output_filename(g.files['logistic-regression'])
    plotter.set_title('Logistic Regression')
    g.debug.prn(self, 'Plot basics set.')

    min_x = min(self.training_x)
    max_x = max(self.training_x)
    min_y = min(self.training_y)
    max_y = max(self.training_y)
    x_vals = []
    y_vals = []
    for x in range(min_x * 100, max_x * 100):
      y_adjust = self.f(x / 100) * (max_y - min_y) + min_y
      x_vals.append([x / 100])
      y_vals.append([y_adjust])
    sketches.append(SmoothSketch())
    sketches[-1].add_x(x_vals)
    sketches[-1].add_y(y_vals)
    g.debug.prn(self, 'Curve added to sketches list.')

    sketches.append(ScatterSketch())
    sketches[-1].add_x(list(self.training_x))
    sketches[-1].add_y(list(self.training_y))
    g.debug.prn(self, 'Scatter of points added to sketches list.')

    plotter.load(sketches)
    plotter.save()
    plotter.close()
    g.debug.prn(self, 'All sketches loaded and saved.')

    image_manager.scale(g.files['logistic-regression'], g.files['logistic-regression'], 250)

    del plotter
    del image_manager
    g.debug.prn(self, 'Plotter and ImageManager objects deleted', 3)


class RidgeModel(LinearModel):
  def __init__(self, f, training_x, training_y, index):
    super().__init__(f, training_x, training_y, index)
    self.math = Math()
    self.regularize()
    g.debug.prn(self, 'RidgeModel created')
  def class_name(self):
    return "RidgeModel"
  def regularize(self):
    y_av = np.mean(self.training_y)
    x_av = np.mean(self.training_x)
    while True:
      upper_m = self.get_slope() * 1.1
      lower_m = self.get_slope() * (1 - 2 * (1.1 - 1))
      upper_b = y_av - upper_m * x_av
      lower_b = y_av - lower_m * x_av
      upper_f = lambda x : upper_m * x + upper_b
      lower_f = lambda x : lower_m * x + lower_b
      upper_v = g.analyzer.get_variance_by_parts(upper_f, self.training_x)
      lower_v = g.analyzer.get_variance_by_parts(lower_f, self.training_x)
      var = g.analyzer.get_variance(self)
      print(upper_m)
      print(lower_m)
      if lower_m - self.get_slope() < 0.0001:
        if upper_m - self.get_slope() < 0.0001:
          break
      if var > upper_v and var > lower_v:
        break
      elif upper_v > lower_v:
        self.set_slope(upper_m)
        self.set_yint(upper_b)
      else:
        self.set_slope(lower_m)
        self.set_yint(lower_b)
  def set_slope(self, slope):
    yint = self.get_yint()
    self.f = lambda x : slope * x + yint
  def set_yint(self, yint):
    slope = self.get_slope()
    self.f = lambda x : slope * x + yint
  def plot(self):
    plotter = Plotter()
    image_manager = ImageManager()
    sketches = []
    plotter.set_output_filename(g.files['ridge-regression'])
    plotter.set_title('Ridge Regression')
    g.debug.prn(self, 'Plot basics set.')

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
    g.debug.prn(self, 'Linear curve saved as SmoothSketch.')

    sketches.append(ScatterSketch())
    sketches[-1].add_x(list(self.training_x))
    sketches[-1].add_y(list(self.training_y))
    g.debug.prn(self, 'Points saved as ScatterSketch.')

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
      g.debug.prn(self, 'Vertical line appended.', 3)
    g.debug.prn(self, 'SSR lines drawn as VerticalLineSketch(s).')

    plotter.load(sketches)
    plotter.save()
    plotter.close()
    g.debug.prn(self, 'All sketches loaded and saved.')

    image_manager.scale(g.files['ridge-regression'], g.files['ridge-regression'], 250)

    del plotter
    del image_manager
    g.debug.prn(self, 'Plotter and ImageManager objects deleted', 3)

