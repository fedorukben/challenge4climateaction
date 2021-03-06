import config as g
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from visualize import Plotter

class Projection(object):
  def __init__(self, projection, resolution='l'):
    self.res = 'l'
    self.proj = projection
  def class_name(self):
    return 'Projection'
  def get_resolution(self):
    return self.res
  def get_projection(self):
    return self.proj
  def generate(self):
    g.debug.prn(self, 'Cannot call generate() on abstract Projection.', 1)

class OrthographicProjection(Projection):
  def __init__(self, resolution='l'):
    super().__init__('ortho', resolution)
    g.debug.prn(self, 'Projection initialized.')
  def class_name(self):
    return 'OrthographicProjection'

class MillerCylindricalProjection(Projection):
  def __init__(self, resolution='l', corners=[-90, 90, -180, 180]):
    super().__init__('mill', resolution)
    self.corners = corners
    g.debug.prn(self, 'Projection initialized.')
  def class_name(self):
    return 'MillerCylindricalProjection'
  def set_resolution(self, resolution):
    self.resolution = resolution
    g.debug.prn(self, 'Set resolution.', 3)
  def set_corners(self, corners):
    self.corners = corners
    g.debug.prn(self, 'Set corners.', 3)
  def generate(self):
    m = Basemap(projection=self.proj,
                llcrnrlat = self.corners[0],
                urcrnrlat = self.corners[1],
                llcrnrlon = self.corners[2],
                urcrnrlon = self.corners[3],
                resolution = self.res)
    g.debug.prn(self, 'Generated projection.')
    return m

class Mapper(Plotter):
  def __init__(self, proj=None):
    self.m = None
    self.proj = proj
    self.get_m_warning_enabled = True
    self.line_thickness = 0.25
    g.debug.prn(self, 'Mapper object created.')
  def class_name(self):
    return 'Mapper'
  def load_proj(self, projection):
    self.proj = projection
  def generate_basemap(self):
    if self.proj == None:
      g.debug.prn(self, 'You must load a Projection object.', 1)
      return
    self.m = self.proj.generate()
    g.debug.prn(self, 'Basemap generated.')
  def default(self):
    self.load_proj(MillerCylindricalProjection())
    self.generate_basemap()
    self.draw_coast()
    plt.savefig('imgs/map.png')
    plt.close()
  def draw_coast(self):
    self.m.drawcoastlines(linewidth = self.line_thickness)
    g.debug.prn(self, 'Coastline drawn.')
  def draw_countries(self):
    self.m.drawcountries(linewidth = self.line_thickness)
    g.debug.prn(self, 'Country borders drawn.')
  def draw_states(self):
    self.m.drawstates(linewidth = self.line_thickness)
    g.debug.prn(self, 'State borders drawn.')
  def draw_counties(self):
    self.m.drawcounties(linewidth = self.line_thickness)
    g.debug.prn(self, 'County borders drawn.')
  def draw_rivers(self):
    self.m.drawrivers(linewidth = self.line_thickness)
    g.debug.prn(self, 'Rivers drawn.')
  def set_line_thickness(self, line_thickness):
    self.line_thickness = line_thickness
    g.debug.prn(self, 'Line thickness set.')
  def get_line_thickness(self):
    return self.line_thickness
  def get_projection(self):
    if self.proj == None:
      g.debug.prn(self, 'Projection object has not been loaded.', 3)
      return
    return self.proj
  def get_m(self):
    if self.get_m_warning_enabled:
      g.debug.prn(self, 'Basemap object gotten. This is highly advised against. To hide, run set_m_warning().', 1)
    else:
      g.debug.prn(self, 'Basemap object gotten.')
    return self.m
  def set_m_warning(self):
    self.get_m_warning_enabled = not self.get_m_warning_enabled
    g.debug.prn(self, 'get_m() warning toggled.')
  def is_m_warning(self):
    return self.get_m_warning_enabled
