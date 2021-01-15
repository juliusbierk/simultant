from bokeh.plotting import figure, show
from bokeh.embed import json_item

def make_simple_plot(x, y):
   p = figure(
      tools="pan,box_zoom,reset"
   )

   p.line(x, y, line_width=2)

   return json_item(p)

if __name__ == '__main__':
   p = figure()
   p.line([0, 1], [5, 6], line_width=2)
   show(p)
