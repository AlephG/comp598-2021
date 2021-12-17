from random import random
from bokeh.layouts import column, row
from bokeh.models import Button, Select, ColumnDataSource, Line, Div
from bokeh.palettes import Blues4
from bokeh.plotting import figure, curdoc
from bokeh.io import show
import pandas as pd
from os.path import join, dirname


# Load dataset
scriptdir = dirname(__file__)
data_path = join(scriptdir, '..', 'data', 'nyc_grouped.csv')
data = pd.read_csv(data_path, index_col=0)
data = data.set_index('month')

def get_dataset(zipcode):
    global data
    return data[zipcode].to_list()

def make_plot(source):
    # Create plot
    plot = figure(x_range=source.data['month'], width=800, tools="", toolbar_location=None)
    plot.title.text = 'Average monthly response time for incidents in the NYC area'
    plot.line(x='month', y='All', line_color='blue', line_width=2, source=source, legend_label='NYC')
    plot.line(x='month', y='zip1', line_color='red', line_width=2, source=source, legend_label='First zipcode')
    plot.line(x='month', y='zip2', line_color='orange', line_width=2, source=source, legend_label='Second zipcode')

    # fixed attributes
    plot.legend.location = 'top_left'
    plot.xaxis.axis_label = 'Month'
    plot.yaxis.axis_label = 'Response time (h)'
    plot.axis.axis_label_text_font_style = "bold"
    plot.grid.grid_line_alpha = 0.4
    
    return plot

def update_plot(attr, old, new):
    # If this works add if statements to make more efficient
    zip1 = zip_select1.value
    zip2 = zip_select2.value
    source.data['zip1'] =  get_dataset(zip1)
    source.data['zip2'] = get_dataset(zip2)

# Random initial zipcodes
zipcode1 = '11210'
zipcode2 = '10000'

# Create dropdown zipcode select
zip_select1 = Select(value=zipcode1, title='First zipcode', options=sorted(open(join(scriptdir, 'zipcodes.txt')).read().split()))

zip_select2 = Select(value=zipcode2, title='Second zipcode', options=sorted(open(join(scriptdir, 'zipcodes.txt')).read().split()))

# Add description
desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

# Create source
source = {'month': [], 'All': [], 'zip1': [], 'zip2': []}
source['month'] = data.index.to_list()
source['All'] = data['All'].to_list()
source['zip1'] = data[zipcode1].to_list()
source['zip2'] = data[zipcode2].to_list()
source = ColumnDataSource(source)

plot = make_plot(source)
zip_select1.on_change('value', update_plot)
zip_select2.on_change('value', update_plot)

controls = column(zip_select1, zip_select2)
curdoc().add_root(column(desc, row(plot, controls), sizing_mode='scale_both'))
curdoc().title = "Response times for incidents in NYC"
