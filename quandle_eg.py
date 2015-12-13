
# coding: utf-8

from __future__ import print_function
import requests
import simplejson as json
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

def parse_ticker(ticker):
  # the request is case insensitive
  r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json')
  
  # handle invalid tickers
  if not 'dataset' in r.json():
    return False, pd.DataFrame(), 'invalid'
  else:
    dict1 = r.json()['dataset']
    col_names = dict1['column_names']
    data = dict1['data']
    name = dict1['name'][:-45]
    df = pd.DataFrame(data,columns=col_names)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.loc[df['Date']>(df.loc[0,'Date']-np.timedelta64(31,'D'))]
    return True, df, name


def render_plot(df,name):
  # output to static HTML file
  output_file("lines.html", title="line plot example")

  TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

  # create a new plot with a title and axis labels
  p = figure(width=1000, height=750,
         title="simple line example", x_axis_type='datetime', 
         x_axis_label='x', y_axis_label='y',
         tools=TOOLS)

  # prepare some data
  x = df['Date']

  # add a line renderer with legend and line thickness
  p.line(x, df['Close'], legend="Close", line_width=1, color='gray')
  p.inverted_triangle(x, df['High'], legend="High", line_width=1, color='black',
                 size=10)
  p.triangle(x, df['Low'], legend="Low", line_width=1, color='red',
                 size=10)

  # NEW: customize by setting attributes
  p.title = name
  #p.legend.orientation = "top_left"
  p.grid.grid_line_alpha=0
  p.xaxis.axis_label = 'Date'
  p.xaxis.axis_label_text_font_size = '24pt'
  p.xaxis.major_label_text_font_size = '20pt'

  p.yaxis.major_label_text_font_size = '20pt'
  p.yaxis.axis_label = 'Price / $'

  p.yaxis.axis_label_text_font_size = '24pt'
  p.ygrid.band_fill_color="olive"
  p.ygrid.band_fill_alpha = 0.1

  # show the results
  return components(p)

def make_plot(ticker):
  good_ticker, df, name = parse_ticker(ticker)
  if good_ticker:
    script, div = render_plot(df,name)
    return True, script, div
  else:
    return False, '', ''

if __name__=='__main__':
  make_plot()

