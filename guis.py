import PySimpleGUI as sg
from model import LinearModel
from maps import MillerCylindricalProjection
from maps import OrthographicProjection
from maps import PolarAzimuthalEquidistantProjection
import os
import config as g

class GUI(object):
  def __init__(self, plotter, analyzer, modeller):
    self.is_compiled = False
    self.title = None
    self.layout = [[]]
    self.row = 0
    self.theme = None
    g.debug.prn(self, 'GUI object created.')
    self.submit_func = None
    self.plot_shown = 'imgs/p.png'
    self.plotter = plotter
    self.analyzer = analyzer
    self.modeller = modeller
  def class_name(self):
    return 'GUI'
  def standard(self):
    if g.interactive_mode:
      self.set_title(g.gui_title)
      self.text('Interactive Mode')
      self.next()
      self.image(self.plot_shown)
      self.next()
      self.button('Display')
      self.button('Peek')
      self.button('Generate')
      self.button('Map')
      self.next()
      self.button('Exit Program')
      self.button('Exit Interactive Mode')
    else:
      self.set_title(g.gui_title)
      self.text('Prompt Mode')
      self.next()
      self.image(self.plot_shown)
      self.next()
      self.text('Show: ')
      self.input('Show')
      self.next()
      self.button('Exit')
      self.button('Submit')
  def compile(self):
    if not self.is_compiled:
      self.window = sg.Window(self.title, self.layout)
      self.is_compiled = True
      g.debug.prn(self, 'Compiled data.')
  def set_theme(self, theme):
    sg.theme(theme)
    self.is_compiled = False
  def next(self):
    self.layout.append([])
    self.row += 1
    self.is_compiled = False
    g.debug.prn(self, f'Added row {self.row}.')
  def text(self, text):
    self.layout[self.row].append(sg.Text(text))
    self.is_compiled = False
    g.debug.prn(self, f'Added text to row {self.row}.')
  def input(self, key):
    self.layout[self.row].append(sg.InputText('', key=key))
    self.is_compiled = False
    g.debug.prn(self, f'Added input box to row {self.row}.')
  def button(self, key):
    self.layout[self.row].append(sg.Button(key))
    self.is_compiled = False
    g.debug.prn(self, f'Added button to row {self.row}.')
  def image(self, addr):
    self.layout[self.row].append(sg.Image(addr))
    self.is_compiled = False
    g.debug.prn(self, f'Added image to row {self.row}.')
  def file_browser(self, init_folder, key):
    self.layout[self.row].append(sg.FileBrowse(initial_folder=init_folder, key=key))
    self.is_compiled = False
    g.debug.prn(self, f'Added file browser to {self.row}.')
  def set_title(self, title):
    self.title = title
    self.is_compiled = False
    g.debug.prn(self, 'Set title.')
  def loop(self):
    if self.is_compiled:
      while True:
        event, values = self.window.read()
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Exit Program':
          g.debug.prn(self, 'Exit triggered.')
          break
        elif event == 'Submit':
          for command in values['Show'].split('|'):
            g.console.read(command)
        if g.interactive_mode:
          if event == 'Exit Interactive Mode':
            g.console.read(':')
          elif event == 'Display':
            image_browser = FileBrowserPopUp('Image Selector')
            image_browser.set_text('Find file below:')
            image_browser.show()
            image_browser.loop()
            image_browser.close()
          elif event == 'Peek':
            peek_stats = SelectPopUp('Peek Statistics')
            peek_stats.set_text('Select peekable from below:')
            peek_stats.show()
            peek_stats.loop()
            peek_stats.close()
          elif event == 'Generate':
            popup = GenerateVisualPopUp('Generate Visual')
            popup.set_text('Select visual to generate:')
            popup.show()
            popup.loop()
            popup.close()
          elif event == 'Map':
            popup = MapConfigureGUI('Map Configuration')
            popup.show()
            popup.loop()
            popup.close()
    else:
      g.debug.prn(self, 'GUI not compiled.', 1)
  def clear(self):
    self.is_compiled = False
    self.title = None
    self.layout = [[]]
    self.row = 0
    self.theme = None
    g.debug.prn(self, 'GUI cleared.')
  def close(self):
    self.window.close()
    g.debug.prn(self, 'GUI closed.')

class PopUp(object):
  def __init__(self, title):
    self.text = None
    self.title = title
  def class_name(self):
    return 'PopUp'
  def set_text(self, text):
    self.text = text
    g.debug.prn(self, 'Text set.')
  def get_text(self):
    return self.text
  def close(self):
    self.window.close()
    g.debug.prn(self, 'Message terminated.')
  def show(self):
    g.debug.prn(self, 'Cannot perform show() on abstract PopUp.', 1)
  def loop(self):
    g.debug.prn(self, 'Cannot perform loop() on abstract PopUp.', 1)

class YesNoPopUp(PopUp):
  def __init__(self, title):
    super().__init__(title)
  def class_name(self):
    return 'YesNoPopUp'
  def show(self):
    self.layout = [
      [sg.Text(self.text)],
      [sg.Button('Yes'), sg.button('No')]
    ]
    self.window = sg.Window(self.title, self.layout)
    g.debug.prn(self, 'Message shown.')
  def loop(self):
    g.debug.prn(self, 'Loop commenced.')
    while True:
        event, values = self.window.read()
        if event == 'No' or event == sg.WIN_CLOSED:
          self.close()
          g.debug.prn(self, 'No selected.')
          return False
        elif event == 'Yes':
          self.close()
          g.debug.prn(self, 'Yes selected.')
          return True

class InfoPopUp(PopUp):
  def __init__(self, title):
    super().__init__(title)
  def class_name(self):
    return 'InfoPopUp'
  def show(self):
    self.layout = [
      [sg.Text(self.text)],
      [sg.Button('OK')]
    ]
    self.window = sg.Window(self.title, self.layout)
    g.debug.prn(self, 'Message shown.')
  def loop(self):
    g.debug.prn(self, 'Loop commenced.')
    while True:
        event, values = self.window.read()
        if event == 'OK' or event == sg.WIN_CLOSED:
          self.close()
          break

class FileBrowserPopUp(PopUp):
  def __init__(self, title):
    super().__init__(title)
  def class_name(self):
    return 'FileBrowserPopUp'
  def show(self):
    self.layout = [
      [sg.Text(self.text)],
      [sg.FileBrowse(initial_folder='imgs/', key='Image Browse')],
      [sg.Button('Submit')]
    ]
    self.window = sg.Window(self.title, self.layout)
    g.debug.prn(self, 'Message shown.')
  def loop(self):
    g.debug.prn(self, 'Loop commenced.')
    while True:
      event, values = self.window.read()
      if event == sg.WIN_CLOSED:
        self.close()
        break
      elif event == 'Submit':
        if not values['Image Browse'] == None:
          file = values['Image Browse'].split('/')[-1][:-4]
          self.close()
          g.console.read(f'i:{file}')
          break
        else:
          g.debug.prn(self, 'No file selected.', 1)

class SelectPopUp(PopUp):
  def __init__(self, title):
    super().__init__(title)
  def class_name(self):
    return 'SelectPopUp'
  def show(self):
    self.layout = [
      [sg.Text(self.text)],
      [sg.Combo([*g.stats_to_codes], key='Combo')],
      [sg.Button('Submit')]
    ]
    self.window = sg.Window(self.title, self.layout)
    g.debug.prn(self, 'Message shown.')
  def loop(self):
    g.debug.prn(self, 'Loop commenced.')
    while True:
      event, values = self.window.read()
      if event == sg.WIN_CLOSED:
        self.close()
        break
      elif event == 'Submit':
        if not values['Combo'] == None:
          code = g.stats_to_codes[values['Combo']]
          self.close()
          g.console.read(f'v:{code}')
          break
        else:
          g.debug.prn(self, 'No statistic selected.', 1)

class GenerateVisualPopUp(PopUp):
  def __init__(self, title):
    super().__init__(title)
  def class_name(self):
    return 'GenerateVisualPopUp'
  def show(self):
    self.layout = [
      [sg.Text(self.text)],
      [sg.Combo([*g.visuals], key='Combo')],
      [sg.Button('Submit'), sg.Button('All')]
    ]
    self.window = sg.Window(self.title, self.layout)
    g.debug.prn(self, 'Message shown.')
  def loop(self):
    g.debug.prn(self, 'Loop commenced.')
    while True:
      event, values = self.window.read()
      if event == sg.WIN_CLOSED:
        self.close()
        break
      elif event == 'Submit':
        if not values['Combo'] == None:
          code = g.visuals[values['Combo']]
          self.close()
          g.console.read(f'g:{code}')
          break
        else:
          g.debug.prn(self, 'No visual selected.', 1)
      elif event == 'All':
        g.console.read(f'g:g')
        break

class MapTypePopUp(PopUp):
  def __init__(self):
    self.val = None
    self.i = 0
    g.debug.prn(self, 'MapTypePopUp created.')
  def class_name(self):
    return 'MapTypePopUp'
  def show(self):
    self.layout = [
      [sg.Text('Select map type:')]
    ]
    for proj_name in g.proj_names:
      self.i += 1
      self.layout.append([sg.Radio(proj_name, 'RADIO', default=False, key=f"In{self.i}")])
    self.layout.append([sg.Button('Submit')])
    self.window = sg.Window('Map Type Selector', self.layout)
    g.debug.prn(self, 'Map type selector popped up.')
  def loop(self):
    g.debug.prn(self, 'Loop commenced.')
    while True:
      event, values = self.window.read()
      if event == sg.WIN_CLOSED:
        self.close()
        break
      elif event == 'Submit' and (values['In1'] or values['In2'] or values['In3']):
        for j in range(self.i, 0, -1):
          if values[f'In{j}']:
            self.val = g.proj_names[j - 1]
        break
  def get_val(self):
    if self.val == None:
      g.debug.prn(self, 'The value has not been selected.')
      return
    return self.val
  def close(self):
    self.window.close()
    g.debug.prn(self, 'MapTypePopUp closed.')

class MapLinesPopUp(PopUp):
  def __init__(self):
    self.val = None
    self.i = 0
    g.debug.prn(self, 'MapLinesPopUp created.')
  def class_name(self):
    return 'MapLinesPopUp'
  def show(self):
    self.layout = [
      [sg.Text('Select lines to draw:')],
      [sg.Checkbox('Country Borders', default=False, key='Countries')],
      [sg.Checkbox('State Borders', default=False, key='States')],
      [sg.Checkbox('County Borders', default=False, key='Counties')],
      [sg.Checkbox('River Lines', default=False, key='Rivers')],
      [sg.Checkbox('Coast Lines', default=False, key='Coasts')],
      [sg.Button('Submit')]
    ]
    self.window = sg.Window('Map Type Selector', self.layout)
    g.debug.prn(self, 'Map lines selector popped up.')
  def loop(self):
    g.debug.prn(self, 'Loop commenced.')
    while True:
      event, values = self.window.read()
      if event == sg.WIN_CLOSED:
        self.close()
        break
      elif event == 'Submit':
        pass
  def get_val(self):
    if self.val == None:
      g.debug.prn(self, 'The value has not been selected.')
      return
    return self.val
  def close(self):
    self.window.close()
    g.debug.prn(self, 'MapTypePopUp closed.')



class MapConfigureGUI(object):
  def __init__(self, title):
    self.title = title
    self.map_type = 'None'
    g.debug.prn(self, 'MapConfigureGUI created.')
  def class_name(self):
    return 'MapConfigurePopUp'
  def set_map_type(self, map_type):
    self.map_type = map_type
    g.debug.prn(self, 'Map type set.')
  def get_map_type(self):
    return self.map_type
  def show(self):
    self.layout = [
      [sg.Text("Map Configuration")],
      [sg.Text(f'Map Type: {self.map_type}')]
    ]
    if self.map_type == 'Orthographic':
      pass
    elif self.map_type == 'Miller Cylindrical':
      self.layout.append([sg.Button('Map Type'), sg.Button('Lines')])
    elif self.map_type == 'Polar Azimuthal Equidistant':
      pass
    else:
      self.layout.append([sg.Button('Map Type')])
    self.layout.append([sg.Button('Submit')])
    self.window = sg.Window(self.title, self.layout)
    g.debug.prn(self, 'GUI shown.')
  def loop(self):
    g.debug.prn(self, 'Loop commenced.')
    while True:
      event, values = self.window.read()
      if event == sg.WIN_CLOSED:
        self.close()
        break
      elif event == 'Map Type':
        popup = MapTypePopUp()
        popup.show()
        popup.loop()
        self.map_type = popup.get_val()
        popup.close()
        self.close()
        self.show()
      elif event == 'Submit':
        if self.map_type == 'None':
          g.debug.prn(self, 'Cannot create map of type \'None\'.', 1)
          continue
        g.map_config['map_type'] = self.map_type
        g.debug.prn(self, 'Submitted map configurations.')
        g.console.read('g:map')
        self.close()
        break
  def close(self):
    self.window.close()
    g.debug.prn(self, 'MapConfigureGUI closed.')

class Console(object):
  def __init__(self):
    pass
  def class_name(self):
    return 'Console'
  def clear(self):
    clear_console = lambda: os.system('cls')
    clear_console()
  def read(self, command):
    if command.count(':') == 1:
      header = command.split(':')[0]
      body = command.split(':')[1]
      if header == '' and body == '':
        g.interactive_mode = not g.interactive_mode
        g.debug.prn(self, f'Interactive mode set to {g.interactive_mode}.')
        g.gui.close()
        g.gui.clear()
        g.gui.standard()
        g.gui.compile()
        g.gui.loop()
        g.gui.close()
      elif header == 'i':
        if os.path.exists(f'imgs/{body}.png'):
          g.debug.prn(self, 'Updating visible file.')
          g.gui.close()
          g.gui.plot_shown = f'imgs/{body}.png'
          g.gui.clear()
          g.gui.standard()
          g.gui.compile()
          g.gui.loop()
          g.gui.close()
        else:
          g.debug.prn(self, 'File does not exist.', 1)
      elif header == 'g':
        if body == 'ls-f':
          g.analyzer.f_dist(LinearModel, 100)
          g.debug.prn(self, 'Generated least squares f-distribution.')
        elif body == 'ls-reg':
          g.modeller.gen_least_squares(g.x,g.y)
          g.debug.prn(self, 'Generated least squares regression.')
        elif body == 'ls-ssr':
          g.analyzer.ssr_curve(g.x, g.y)
          g.debug.prn(self, 'Generated least squares S.S. residuals.')
        elif body == 'lo-reg':
          g.modeller.get_logistic(g.x, g.y)
          g.debug.prn(self, 'Generated logistic regression.')
        elif body == 'ri-reg':
          g.modeller.get_ridge(g.x, g.y)
          g.debug.prn(self, 'Generated ridge regression.')
        elif body == 'map-mill':
          g.mapper.default(MillerCylindricalProjection())
          g.debug.prn(self, 'Generated Miller cylindrical map.')
        elif body == 'map-ortho':
          g.mapper.default(OrthographicProjection())
          g.debug.prn(self, 'Generated orthographic map.')
        elif body == 'map-npaeqd':
          g.mapper.default(PolarAzimuthalEquidistantProjection())
          g.debug.prn(self, 'Generated north polar azimuthal equidistant map.')
        elif body == 'map-spaeqd':
          g.mapper.default(PolarAzimuthalEquidistantProjection(pole='s'))
          g.debug.prn(self, 'Generated south polar azimuthal equidistant map.')
        elif body == 'map':
          if g.map_config['map_type'] == 'Orthographic':
            g.console.read('g:map-ortho')
          elif g.map_config['map_type'] == 'Miller Cylindrical':
            g.console.read('g:map-mill')
          elif g.map_config['map_type'] == 'Polar Azimuthal Equidistant':
            g.console.read('g:map-npaeqd')
          else:
            g.debug.prn(self, 'Map type not recognized.', 1)
        elif body == 'g':
          for v in g.visuals.values():
            if not v == 'p':
              self.read(f'g:{v}')
          g.debug.prn(self, 'All visuals generated.')
        else:
          g.debug.prn(self, 'File to generate not recognized.')
          return
      elif header == 'q':
          if body == 'q':
            g.debug.prn(self, "Exit triggered.")
            quit()
          else:
            g.debug.prn(self,'Command not recognized. Did you mean?: q:q', 1)
      elif header == 'v':
        text = ''
        if body == 'ls-a':
          if os.path.exists(g.files['least-squares']):
            text = f'slope = {g.modeller.linear(0).get_slope()}'
          else:
            g.debug.prn(self,'Least Squares model has not been generated.', 1)
            return
        elif body == 'ls-b':
          if os.path.exists(g.files['least-squares']):
            text = f'yint = {g.modeller.linear(0).get_yint()}'
          else:
            g.debug.prn(self, 'Least Squares model has not been generated.', 1)
            return
        elif body == 'ls-rsq':
          if os.path.exists(g.files['least-squares']):
            text = f'R^2 = {g.analyzer.get_r_sq(g.modeller.linear(0))}'
          else:
            g.debug.prn(self, 'Least Squares model has not been generated.', 1)
            return
        elif body == 'ls-var':
          if os.path.exists(g.files['least-squares']):
            text = f'variance = {g.analyzer.get_variance(g.modeller.linear(0))}'
          else:
            g.debug.prn(self, 'Least Squares model has not been generated.', 1)
            return
        elif body == 'lo-rsq':
          if os.path.exists(g.files['logistic-regression']):
            text = f'R^2 = {g.analyzer.get_r_sq(g.modeller.logistic(0))}'
          else:
            g.debug.prn(self, 'Logistic model has not been generated.', 1)
            return
        elif body == 'lo-var':
          if os.path.exists(g.files['logistic-regression']):
            text = f'variance = {g.analyzer.get_variance(g.modeller.logistic(0))}'
          else:
            g.debug.prn(self, 'Logistic model has not been generated.', 1)
            return
        elif body == 'specif':
          text = f'specificity = {g.analyzer.get_specificity()}'
        elif body == 'sensit':
          text = f'sensitivity = {g.analyzer.get_sensitivity()}'
        elif body == 'precis':
          text = f'precision = {g.analyzer.get_precision()}'
        elif body == 'acc':
          text = f'accuracy = {g.analyzer.get_accuracy()}'
        elif body == 'recall':
          text = f'recall = {g.analyzer.get_recall()}'
        elif body == 'fout':
          text = f'fallout = {g.analyzer.get_fallout()}'
        elif body == 'bias':
          text = f'bias = {g.analyzer.get_bias()}'
        elif body == 'cm':
          text = f'confusion matrix = {g.analyzer.get_confusion_matrix()}'
        elif body == 'auc':
          text = f'auc = {g.analyzer.get_auc()}'
        else:
          g.debug.prn(self, 'Variable could not be found.', 1)
          return
        g.debug.prn(self, f'Popping up {body} variable.')
        popup = InfoPopUp('Accessor')
        popup.set_text(text)
        popup.show()
        popup.loop()
        popup.close()
      else:
        g.debug.prn(self, 'Unknown header.', 1)
    else:
      g.debug.prn(self, 'Must use exactly 1 colon (:) per command.', 1)
