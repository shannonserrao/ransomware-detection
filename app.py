#Load the packages
import pandas as pd
import numpy as np
from flask import Flask, render_template
from bokeh.embed import components 
from bokeh.models import HoverTool
#from bokeh.charts import Scatter
from bokeh.palettes import Spectral9
from bokeh.plotting import figure, show

from os.path import dirname, join

# Bokeh basics 
#from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.plotting import curdoc

from scripts.histogram import histogram_tab
from scripts.timeplot import timeplot_tab


# #Connect the app
# app = Flask(__name__)


# # def get_plot(df):
# #     #Make plot and customize
# #     p = Scatter(df, x='sepal_length', y='sepal_width', xlabel='Sepal Length [cm]', ylabel='Sepal Width [cm]', title='Sepal width vs. length')
# #     p.xaxis.axis_label_text_font_size = "14pt"
# #     p.xaxis.major_label_text_font_size = '10pt'
# #     p.yaxis.axis_label_text_font_size = "14pt"
# #     p.yaxis.major_label_text_font_size = '10pt'
# #     p.title.text_font_size = '16pt'
# #     p.add_tools(HoverTool()) #Need to configure tooltips

# #     #Return the plot
# #     return(p)

# @app.route('/')
# def homepage():

#Get the data, from somewhere
data = pd.read_csv('./data/BitcoinHeistData.csv')
data['date']=pd.to_datetime(data['year'] * 1000 + data['day'], format='%Y%j')
lstlabels=data['label'].value_counts().nlargest(n=9).index.tolist()
grouplabels=data.groupby(by=['label','date'],as_index=False).agg({'length': 'mean','count': 'mean','income': 'mean','weight':'mean', 'looped':'mean' }).sort_values(by='date')

groupaddr=data.groupby(by=['label','address'],as_index=False).agg({'length': 'mean','count': 'mean','income': 'mean','weight':'mean','looped':'mean' })
featlist=grouplabels.columns[2:]

#print(featlist)
# Create each of the tabs
# histogram plot of features
tab1 = histogram_tab(groupaddr, featlist)
#time plot
tab2 = timeplot_tab(grouplabels, lstlabels[1:])

# Put all the tabs into one application
#tabs = Tabs(tabs =tab1)
tabs = Tabs(tabs = [tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)


    
    
    # p = figure(plot_width=1800, plot_height=750, x_axis_type="datetime")
    # p.title.text = 'Click on legend entries to mute the corresponding lines'

    # for label, color in zip(lstlabels[1:],Spectral9):
    #     df=grouplabels[grouplabels['label']==label].sort_values(by=['date'])
    #     p.line(df['date'], df['length'], line_width=2, color=color, alpha=0.8,
    #         muted_color=color, muted_alpha=0.2, legend_label=label)
    #     p.legend.location = "top_left"
    #     p.legend.click_policy="mute"

    # script, div= components(tabs)
    #     # show(p)







    #Setup plot    
    # p = get_plot(df)
    # script, div = components(p)

    # #Give some text for the bottom of the page 
    # example_string = 'Bitcoin Heist web app built using python, Flask, and Bokeh.'
    #   script, div= components(p)
    #Render the page
    # return render_template('home.html', script=script, div=div, example_string=example_string)    

if __name__ == '__main__':
    app.run(debug=False)

# #Connect the app
# app = Flask(__name__)


# # def get_plot(df):
# #     #Make plot and customize
# #     p = Scatter(df, x='sepal_length', y='sepal_width', xlabel='Sepal Length [cm]', ylabel='Sepal Width [cm]', title='Sepal width vs. length')
# #     p.xaxis.axis_label_text_font_size = "14pt"
# #     p.xaxis.major_label_text_font_size = '10pt'
# #     p.yaxis.axis_label_text_font_size = "14pt"
# #     p.yaxis.major_label_text_font_size = '10pt'
# #     p.title.text_font_size = '16pt'
# #     p.add_tools(HoverTool()) #Need to configure tooltips

# #     #Return the plot
# #     return(p)

# @app.route('/')
# def homepage():

#     #Get the data, from somewhere
#     data = pd.read_csv('./data/BitcoinHeistData.csv')
#     data['date']=pd.to_datetime(data['year'] * 1000 + data['day'], format='%Y%j')
#     lstlabels=data['label'].value_counts().nlargest(n=9).index.tolist()
#     grouplabels=data.groupby(by=['label','date'],as_index=False).agg({'length': 'mean','count': 'mean','income': 'mean','weight':'mean', 'looped':'mean' }).sort_values(by='date')
    
#     groupaddr=data.groupby(by=['label','address'],as_index=False).agg({'length': 'sum','count': 'sum','income': 'sum','weight':'sum','looped':'sum' })
#     featlist=grouplabels.columns[2:]

#     #print(featlist)
#     # Create each of the tabs
#     # histogram plot of features
#     tab1 = histogram_tab(groupaddr, featlist)
#     #time plot
#     tab2 = timeplot_tab(grouplabels, lstlabels[1:])

#     # Put all the tabs into one application
#     #tabs = Tabs(tabs =tab1)
#     tabs = Tabs(tabs = [tab1, tab2])

#     # Put the tabs in the current document for display
#     curdoc().add_root(tabs)


    
    
#     # p = figure(plot_width=1800, plot_height=750, x_axis_type="datetime")
#     # p.title.text = 'Click on legend entries to mute the corresponding lines'

#     # for label, color in zip(lstlabels[1:],Spectral9):
#     #     df=grouplabels[grouplabels['label']==label].sort_values(by=['date'])
#     #     p.line(df['date'], df['length'], line_width=2, color=color, alpha=0.8,
#     #         muted_color=color, muted_alpha=0.2, legend_label=label)
#     #     p.legend.location = "top_left"
#     #     p.legend.click_policy="mute"

#     script, div= components(tabs)
#     #     # show(p)







#     #Setup plot    
#     # p = get_plot(df)
#     # script, div = components(p)

#     # #Give some text for the bottom of the page 
#     example_string = 'Bitcoin Heist web app built using python, Flask, and Bokeh.'
#     #   script, div= components(p)
#     #Render the page
#     return render_template('home.html', script=script, div=div, example_string=example_string)    

# if __name__ == '__main__':
#     app.run(debug=False)

