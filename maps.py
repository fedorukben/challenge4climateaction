import config as g
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from visualize import Plotter
from utils import ImageManager

class Geo2(object):
  def __init__(self, lat, lon):
    self.lat = lat
    self.lon = lon
  def __str__(self):
    return f'({self.lat}, {self.lon})'
  def class_name(self):
    return 'Geo2'
  def get_lat(self):
    return self.lat
  def get_lon(self):
    return self.lon
  def set_lat(self, lat):
    self.lat = lat
  def set_lon(self, lon):
    self.lon = lon
  def get_pair(self):
    return self.lat, self.lon
  def set_pair(self, lat, lon):
    self.lat = lat
    self.lon = lon

class Projection(object):
  def __init__(self, projection, resolution='l'):
    self.res = 'l'
    self.proj = projection
  def class_name(self):
    return 'Projection'
  def get_resolution(self):
    return self.res
  def set_resolution(self, res):
    self.res = res
    g.debug.prn(self, 'Set resolution.', 3)
  def get_projection(self):
    return self.proj
  def generate(self):
    g.debug.prn(self, 'Cannot call generate() on abstract Projection.', 1)

class OrthographicProjection(Projection):
  def __init__(self, resolution='l', center=Geo2(0, 0)):
    super().__init__('ortho', resolution)
    self.center = center
    g.debug.prn(self, 'Projection initialized.')
  def class_name(self):
    return 'OrthographicProjection'
  def set_center(self, center):
    self.center = center
  def get_center(self):
    return self.center
  def generate(self):
    m = Basemap(projection=self.proj,
                lat_0 = self.center.get_lat(),
                lon_0 = self.center.get_lon(),
                resolution = self.res)
    return m

class MillerCylindricalProjection(Projection):
  def __init__(self, resolution='l', lower=Geo2(-90, -180), upper=Geo2(90, 180)):
    super().__init__('mill', resolution)
    self.lower = lower
    self.upper = upper
    g.debug.prn(self, 'Projection initialized.')
  def class_name(self):
    return 'MillerCylindricalProjection'
  def set_lower(self, lower):
    self.lower = lower
  def get_lower(self):
    return self.lower
  def set_upper(self, upper):
    self.upper = upper
  def get_upper(self):
    return self.upper
  def generate(self):
    m = Basemap(projection=self.proj,
                llcrnrlat = self.lower.get_lat(),
                urcrnrlat = self.upper.get_lat(),
                llcrnrlon = self.lower.get_lon(),
                urcrnrlon = self.upper.get_lon(),
                resolution = self.res)
    return m

class PolarAzimuthalEquidistantProjection(Projection):
  def __init__(self, resolution='l', six_o_clock=Geo2(10, 270), pole = 'n'):
    if not pole in 'ns':
      g.debug.prn(self, 'Invalid pole specified', 1)
    super().__init__(f'{pole}paeqd', resolution)
    self.six_o_clock = six_o_clock
    self.pole = pole
    g.debug.prn(self, 'Projection initialized.')
  def class_name(self):
    return 'MillerCylindricalProjection'
  def set_six_o_clock(self, six_o_clock):
    self.six_o_clock = six_o_clock
  def get_six_o_clock(self):
    return self.six_o_clock
  def get_pole(self):
    return self.pole
  def generate(self):
    m = Basemap(projection=self.proj,
                boundinglat = self.six_o_clock.get_lat(),
                lon_0 = self.six_o_clock.get_lon(),
                resolution = self.res)
    return m

class Mapper(Plotter):
  def __init__(self, proj=None):
    self.m = None
    self.proj = proj
    self.get_m_warning_enabled = True
    self.line_thickness = 0.25
    self.index = 0
    self.color = 'black'
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
  def default(self, proj):
    image_manager = ImageManager()
    self.load_proj(proj)
    self.generate_basemap()
    self.draw_coast()
    plt.savefig(f'imgs/map-{self.index}.png')
    image_manager.scale(f'imgs/map-{self.index}.png', f'imgs/map-{self.index}.png', 250)
    self.index += 1
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
  def set_color(self, color):
    self.color = color
    g.debug.prn(self, 'Set color.')
  def get_color(self):
    return self.color
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
