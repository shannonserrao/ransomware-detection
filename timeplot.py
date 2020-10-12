import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
						  ColumnDataSource, Panel, 
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis,CustomJS, Select)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
								  Tabs, CheckboxButtonGroup, 
								  TableColumn, DataTable, Select, Dropdown, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_8

# Make plot with histogram and return tab
def timeplot_tab(grouplabels, lstlabels):

	# Function to make a dataset for histogram based on a list of carriers
	# a minimum delay, maximum delay, and histogram bin width
	def make_dataset(feature_to_plot):

		# Dataframe to hold information
		# groupaddr[groupaddr['label']!='white']['count'].plot.hist(bins=number_bins, alpha=0.5)
		# by_rware=[]
		xs = []
		ys = []
		colors = []
		labels = []
		print(feature_to_plot)

		for i, label in enumerate(lstlabels):
			subset=grouplabels[grouplabels['label']==label].sort_values(by=['date'])
		
			# Evenly space x values
			x = subset['date']
			# Evaluate pdf at every value of x
			y = subset[subset['label']==label][feature_to_plot]
			print(y)
			print(x)
			# Append the values to plot
			xs.append(list(x))
			ys.append(list(y))

			# Append the colors and label
			colors.append(rw_colors[i])
			labels.append(label)

		new_src = ColumnDataSource(data={'x': xs, 'y': ys, 
								   'color': colors, 'label': labels})

		return new_src		

	def style(p):
		# Title 
		p.title.align = 'center'
		p.title.text_font_size = '20pt'
		p.title.text_font = 'serif'

		# Axis titles
		p.xaxis.axis_label_text_font_size = '14pt'
		p.xaxis.axis_label_text_font_style = 'bold'
		p.yaxis.axis_label_text_font_size = '14pt'
		p.yaxis.axis_label_text_font_style = 'bold'

		# Tick labels
		p.xaxis.major_label_text_font_size = '12pt'
		p.yaxis.major_label_text_font_size = '12pt'

		return p
	
	def make_plot(src,feature_to_plot):
		p = figure(plot_width = 1000, plot_height = 700,
				   title = 'time series of Ransom ware',
				   x_axis_label = 'date', y_axis_label = 'Mean of ransomware %s ' % (feature_to_plot), x_axis_type="datetime")


		p.multi_line('x', 'y', color = 'color', legend = 'label', 
					 line_width = 3,
					 source = src)

		# Hover tool with next line policy
		hover = HoverTool(tooltips=[('ransomware', '@label'), 
									('Date', '$x'),
									('Ransomware family', '$y')],
						  line_policy = 'next')

		# Add the hover tool and styling
		p.add_tools(hover)

		p = style(p)

		return p
	
	
	
	def update(attr, old, new):
		feature_to_plot = feature_select.value
		
		new_src = make_dataset(feature_to_plot)
		src.data.update(new_src.data)
		
	
	# p = figure(plot_width=1800, plot_height=750, x_axis_type="datetime")
	# p.title.text = 'Click on legend entries to mute the corresponding lines'

	# for label, color in zip(lstlabels[1:],Spectral9):
	#	 df=grouplabels[grouplabels['label']==label].sort_values(by=['date'])
	#	 p.line(df['date'], df['length'], line_width=2, color=color, alpha=0.8,
	#		 muted_color=color, muted_alpha=0.2, legend_label=label)
	#	 p.legend.location = "top_left"
	#	 p.legend.click_policy="mute"

	#	 script, div= components(p)
	#	 # show(p)
	
	
	# Carriers and colors
	
	# available_rwlabels = ['not ransomware', 'ransomware']

    #grouplabels, lstlabels
	rw_colors = Category20_8
	# rw_colors.sort() #['blue', 'red']
	# airline_colors.sort()
		
	# histogram_selection = CheckboxGroup(labels=available_rwlabels, 
	# 								  active = [0, 1])
	# histogram_selection.on_change('active', update)
	
	# binwidth_select = Slider(start = 1, end = 50, 
	# 						 step = 1, value = 5,
	# 						 title = 'Number of bins (min)')
	# binwidth_select.on_change('value', update)

	# menu = [("length", "length"), ("counts", "count"), ("income", "income"), ("weight", "weight"), ('looped', 'looped')]
	# feature_select = Dropdown(label="Dropdown button", button_type="warning", menu=menu)
	# feature_select.on_change('value', update)

	feature_select = Select(title='feature select', value="count", options=["length", "count", "income", "weight", "looped"])
	feature_select.js_on_change("value", CustomJS(code="""console.log('multi_select: value=' + this.value, this.toString())"""))
	feature_to_plot = feature_select.value
	# feature_select = RangeSlider(start = -60, end = 180, value = (-60, 120),
	# 						   step = 5, title = 'Range of Delays (min)')
	# feature_select.on_change('value', update)
	# print(feature_to_plot)
	# Initial carriers and data source
	# feature_to_plot = feature_select.
	
	src = make_dataset(feature_to_plot)
	p = make_plot(src, feature_to_plot)
	
	# Put controls in a single element
	controls = WidgetBox(feature_select)
	
	# Create a row layout
	layout = row(controls, p)
	
	# Make a tab with the layout 
	tab = Panel(child=layout, title = 'time plot')

	return tab