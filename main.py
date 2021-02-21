from utils import ImageManager
from utils import Randomizer
from utils import Debugger
from utils import OutputFileFormatter

from guis import GUI
from guis import Console

from model import Modeller
from model import LinearModel

from analyze import Analyzer

from visualize import Plotter
from visualize import ScatterSketch

import config as g

def init_globals():
  g.randomizer = Randomizer()
  g.debug = Debugger() 
  g.console = Console()
  g.analyzer = Analyzer()
  g.modeller = Modeller(g.analyzer)
  g.gui = GUI(plotter, g.analyzer, g.modeller)
  g.output_file_formatter = OutputFileFormatter()

def gen_plot():
  plotter.set_title(g.graph_titles['main'])

  g.x = g.randomizer.random_list(25, 0, 100)
  g.y = g.randomizer.random_list(25, 0, 100)

  # plotter.add_x_val(x) # [-2, -1, 0, 1, 2]
  # plotter.add_y_val(y) # [4,1,0,1,4]

  scatter = ScatterSketch()
  scatter.add_x(g.x)
  scatter.add_y(g.y)
  plotter.load(scatter)

  plotter.save()
  plotter.close()

  # g.modeller.gen_least_squares(x,y)
  # g.analyzer.f_dist(LinearModel, 100)

  image_manager.scale(g.files['plot'], g.files['plot'], g.image_height)

plotter = Plotter()
init_globals()
g.output_file_formatter.format_folder('imgs')
image_manager = ImageManager()

gen_plot()

#sg.theme('Dark Red 5')

g.gui.set_title(g.gui_title)
g.gui.text('MatPlotLib Figure')
g.gui.next()
g.gui.image(g.files['plot'])
g.gui.next()
g.gui.text('Show: ')
g.gui.input('Show')
g.gui.next()
g.gui.button('Exit')
g.gui.button('Submit')

g.gui.compile()
g.gui.loop()
g.gui.close()