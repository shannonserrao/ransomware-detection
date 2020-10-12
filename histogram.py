import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
						  ColumnDataSource, Panel, 
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis,Select,CustomJS, Dropdown)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
								  Tabs, CheckboxButtonGroup, 
								  TableColumn, DataTable, Select, Select,Dropdown)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16
from bokeh.io import show
# Make plot with histogram and return tab
def histogram_tab(groupaddr, featlist):

	# Function to make a dataset for histogram based on a list of carriers
	# a minimum delay, maximum delay, and histogram bin width
	def make_dataset(feature_select, number_bins = 25):

		# Dataframe to hold information
		# groupaddr[groupaddr['label']!='white']['count'].plot.hist(bins=number_bins, alpha=0.5)
		# by_rware=[]
		
		by_rware = pd.DataFrame(columns=['proportion', 'left', 'right', 
										   'f_proportion', 'f_interval',
										   'name', 'color'])
		
		
		
 		# by_carrier = pd.DataFrame(columns=['proportion', 'left', 'right', 
		# 								   'f_proportion', 'f_interval',
		# 								   'name', 'color'])
		
		# range_extent = range_end - range_start


		# Iterate through all the carriers
		# for i, carrier_name in enumerate(carrier_list):

			# Subset to the carrier
		subset = groupaddr[groupaddr['label']!='white'][feature_select]
		
		range_extent = np.max(groupaddr[groupaddr['label']!='white'][feature_select])
			# Create a histogram with 5 minute bins
		arr_hist, edges = np.histogram(subset, 
										bins = number_bins, 
										range = [0, range_extent])

			# Divide the counts by the total to get a proportion
		arr_df = pd.DataFrame({'proportion': arr_hist / np.sum(arr_hist), 'left': edges[:-1], 'right': edges[1:] })

			# Format the proportion 
		arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

			# Format the interval
		arr_df['f_interval'] = ['%d to %d minutes' % (left, right) for left, right in zip(arr_df['left'], arr_df['right'])]

		# Assign the carrier for labels
		arr_df['name'] = 'ransom ware'

			# Color each carrier differently
		arr_df['color'] = Category20_16[0]

			# Add to the overall dataframe
		by_rware = by_rware.append(arr_df)
#######################################################
		# Overall dataframe
		by_rware = by_rware.sort_values(['name', 'left'])
		subset = groupaddr[groupaddr['label']=='white'][feature_select]
		
		range_extent = np.max(groupaddr[groupaddr['label']!='white'][feature_select])
			# Create a histogram with 5 minute bins
		arr_hist, edges = np.histogram(subset, 
										bins = number_bins, 
										range = [0, range_extent])

			# Divide the counts by the total to get a proportion
		arr_df = pd.DataFrame({'proportion': arr_hist / np.sum(arr_hist), 'left': edges[:-1], 'right': edges[1:] })

			# Format the proportion 
		arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

			# Format the interval
		arr_df['f_interval'] = ['%d to %d minutes' % (left, right) for left, right in zip(arr_df['left'], arr_df['right'])]

		# Assign the carrier for labels
		arr_df['name'] = 'not ransom ware'

			# Color each carrier differently
		arr_df['color'] = Category20_16[6]

			# Add to the overall dataframe
		by_rware = by_rware.append(arr_df)

		# Overall dataframe
		by_rware = by_rware.sort_values(['name', 'left'])


		return ColumnDataSource(by_rware)

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
	
	def make_plot(src):
		# Blank plot with correct labels
		p = figure(plot_width = 700, plot_height = 700, 
				  title = 'Histogram of Ransomware features',
				  x_axis_label = 'Frequency', y_axis_label = 'Number of ransomware addresses')

		# Quad glyphs to create a histogram
		p.quad(source = src, bottom = 0, top = 'proportion', left = 'left', right = 'right',
			   color = 'color', fill_alpha = 0.7, hover_fill_color = 'color', legend = 'name',
			   hover_fill_alpha = 1.0, line_color = 'black')

		# Hover tool with vline mode
		hover = HoverTool(tooltips=[('Label', '@name'), 
									('Delay', '@f_interval'),
									('Proportion', '@f_proportion')],
						  mode='vline')

		p.add_tools(hover)

		# Styling
		p = style(p)

		return p
	
	
	
	def update(attr, old, new):
		feature_to_plot = feature_select.value
		
		new_src = make_dataset(feature_to_plot, number_bins = binnumber_select.value)
		src.data.update(new_src.data)
		
	def handler(event):
		print(event.item)
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
	
	available_rwlabels = ['not ransomware', 'ransomware']


	rw_colors = Category20_16 #['blue', 'red']
	# airline_colors.sort()
		
	# histogram_selection = CheckboxGroup(labels=available_rwlabels, 
	# 								  active = [0, 1])
	# histogram_selection.on_change('active', update)
	
	binnumber_select = Slider(start = 10, end = 100, 
							 step = 1, value = 5,
							 title = 'Number of bins (min)')
	binnumber_select.on_change('value', update)

	# menu = [("length", "length"), ("counts", "count"), ("income", "income"), ("weight", "weight"), ('looped', 'looped')]
	# feature_select = Dropdown(label="Dropdown button", button_type="warning", menu=menu)
	# feature_select.on_click(handler)
	#menu = [("1", "length"), ("2", "count"), ("3", "income"), ("4", "weight"), ('5', 'looped')]
	feature_select = Select(title='feature select', value="count", options=["length", "count", "income", "weight", "looped"])
	feature_select.js_on_change("value", CustomJS(code="""console.log('multi_select: value=' + this.value, this.toString())"""))
	feature_to_plot = feature_select.value
	# feature_select.on_click(handler)



	# OPTIONS = [("1", "foo"), ("2", "bar"), ("3", "baz"), ("4", "quux")]

	# multi_select = MultiSelect(value=["1", "2"], options=OPTIONS)
	
	# feature_select = RangeSlider(start = -60, end = 180, value = (-60, 120),
	# 						   step = 5, title = 'Range of Delays (min)')
	# feature_select.on_change('value', update)
	#d = Dropdown(label='Click me', menu=['a', 'b', 'c'])



	# Initial carriers and data source
	
	
	src = make_dataset(feature_to_plot,  number_bins = binnumber_select.value)
	p = make_plot(src)
	
	# Put controls in a single element
	controls = WidgetBox(binnumber_select, feature_select)
	
	# Create a row layout
	layout = row(controls, p)
	
	# Make a tab with the layout 
	tab = Panel(child=layout, title = 'Histogram')

	return tab