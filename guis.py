import PySimpleGUI as sg
from model import LinearModel
import os
import config as g

'''

layout =
[
  [text("MatPlotLib Figure")],
  [image("plot.png")],
  [button("Exit"), button("Submit")]
]

event == "Exit"

input("Name")
if event == "Name":
  if values[0] == "Ben Fedoruk":
    print("This man is a god")
  else:
    print("This is a normal man")

'''

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
      self.next()
      self.button('Exit Program')
      self.button('Exit Interactive Mode')
    else:
      self.set_title(g.gui_title)
      self.text('Standard Mode')
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
            peek_stats.set_text('Select image from below:')
            peek_stats.show()
            peek_stats.loop()
            peek_stats.close()
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
      [sg.Input(do_not_clear=True, enable_events=True, key='In')],
      [sg.Listbox(values=g.stats_to_codes.keys(), key='Peek', size=(30,6), enable_events=True)],
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
        if not values['Peek'] == None:
          #self.close()
          print(values['Peek'])
          code = g.stats_to_codes[values['Peek']]
          g.console.read(f'v:{code}')
          break
        else:
          g.debug.prn(self, 'No statistic selected.', 1)

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
          g.debug.prn(self, 'Generated f-distribution.')
        elif body == 'ls':
          g.modeller.gen_least_squares(g.x,g.y)
          g.debug.prn(self, 'Generated least squares model.')
        else:
          g.debug.prn(self, 'File to generate not recognized.')
          return
        
      elif header == 'v':
        text = ''
        if body == 'ls-a':
          text = f'slope = {g.modeller.linear(0).get_slope()}'
        elif body == 'ls-b':
          text = f'yint = {g.modeller.linear(0).get_yint()}'
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
        elif body == 'var':
          text = f'variance = {g.analyzer.get_variance()}'
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