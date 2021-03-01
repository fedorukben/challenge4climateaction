x = []
y = []
sketch_sets = {}
debug_level = 2
x_clr = 'k'
y_clr = 'k'
x_lbl = 'X'
y_lbl = 'Y'
model_precision = 0.01
gui_title = "Title"
upper_x_bound = 100
upper_y_bound = 100
lower_x_bound = 0
lower_y_bound = 0
points_to_gen = 25
randomizer = None
debug = None
console = None
analyzer = None
modeller = None
gui = None
image_height = 250
gui_title = 'Shell UI'
interactive_mode = True
visuals = {
  'Main Graph': 'p',
  'Least Squares - Regression': 'ls-reg',
  'Least Squares - F-Distribution': 'ls-f',
  'Least Squares - Sum of Squared Residuals': 'ls-ssr'
}
graph_titles = {
  'main': 'Main Graph',
}
files = {
  'plot': 'imgs/p.png',
  'least-squares': 'imgs/ls-reg.png',
  'f-dist': 'imgs/ls-f.png',
  'ls-ssr': 'imgs/ls-ssr.png',
}
stats_to_codes = {
  'Least Squares Slope': 'ls-a',
  'Least Squares Y-Intercept': 'ls-b'
}
