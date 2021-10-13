from random import random
from bokeh.layouts import column, row
from bokeh.models import Button, Select, ColumnDataSource, Line, DataRange1d
from bokeh.palettes import Blues4
from bokeh.plotting import figure, curdoc
from bokeh.io import show
import pandas as pd
from os.path import join, dirname


# Load dataset
scriptdir = dirname(__file__)
data_path = join(scriptdir, '..', 'data', 'nyc_grouped.csv')
data = pd.read_csv(data_path, index_col=0)

def get_dataset(zipcode, zipcode2):
    source = ColumnDataSource(data[['month',zipcode, zipcode2]])
    return source

zipcode = '10000'
zipcode2 = '83'
source = get_dataset(zipcode, zipcode2)

plot = figure(x_range=source.data['month'],width=800, tools='', toolbar_location=None)
plot.line(x='month', y=zipcode, line_color='red', line_width=2, source=source, legend_label='First zipcode')
plot.line(x='month', y=zipcode2, line_color='blue', line_width=2, source=source, legend_label='Second zipcode')

plot.xaxis.axis_label = 'Month'
plot.yaxis.axis_label = 'Response time'
plot.grid.grid_line_alpha = 0.5

curdoc().add_root(plot)
