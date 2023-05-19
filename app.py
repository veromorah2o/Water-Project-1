#!/usr/bin/env python
# coding: utf-8

print('1D Contamination Spread in Groundwater')
# -pollution 
# -spread,movement, transport,distribution
# -define porosity & absorption(interaction,association w/ soil or rock), chemical interaction with the aquifer 
# -story telling! 
# -explain the model and plot and what we would see in the plot 
# Problem:<br>
# On a hot summer day, lab assistant Sally was given a task to disposal a bottle of chemical. Without much thinking, she pours the chemical right down the drain! It was later found that the chemical being poured is benzene and spills directly into the groundwater! In order to prevent the local residents using the contaminated water, use the following contamination model to check the spread of the benzene. 
# 
# Model Application:<br> 
# The spill occured at location where distance is 0 meter. The following program shows the concentration vs location curves at three different times after the spill occurance: 5, 10, and 20 days. (The groundwater in the aquifer has a flow speed of 1.667 meter/day in the positive horizontal direction.) You can adjust the mass of the spill, the porosity, and absorption of the aquifer in order to check concentrations at different locations under various spill mass and geological features. Try to change all three varibales built into the program and see their effects on the concentrations at different locations.
# -explain what the users will see in the plot
# -line vs area
# -visual aids 
# -choices for porosity 
# -delete absorption (R=1)
# Questions: <br>
# 1) What is the effect on the maximum concentration when porosity increases? <br>
# 2) If the pollution mass, porosity, and absorption all stay constant, what happens to the concentration as time goes on?<br>
# 3) Don't change the pollution mass and porosity, observe and describe the changes to the curves as absoption changes?<br>
# Advanced Questions:<br>
# 1) A spill occured into an aquifer near UC Davis! The spill mass is known to have a mass of 800 kg, and soil test shows that the porosity of the aquifer is 0.36 and the absorption is 2.5. How far away horizontally can we expect the maximum concentration to occure after 5 days? and 20 days? <br>
# 2) The city policy of Davis allows 20 kg/m of concentration for this contaminant. Knowing the porosity and absorption is 0.34 and 4.35 respectively. What is the maximum spill mass allowed in the aquifer) before violating the local environemtnal policy? 

# In[1]:


import math
import bokeh.plotting.figure as bk_figure
from bokeh.io import curdoc, show
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, Select
from bokeh.models.widgets import Slider, TextInput
import numpy as np
from bokeh.layouts import column, row

"""
Initialize global variables and functions
"""
M = 500
n = 0.375
R = 1
time1 = 5
time2 = 10
time3 = 20


def calculate_z(M, n):
    """
    Calculates z values for use in Bokeh plot curves
    :param M: mass (kg)
    :param n: porosity
    :return: x (range of curves), y/yy/y2 (concentration at different times)
    """
    x = np.arange(1.1, 400, 0.5)
    y = np.zeros([len(x)])
    yy = np.zeros([len(x)])
    y2 = np.zeros([len(x)])
    q = 1.667  # flow speed of groundwater in aquifer
    v = q / n
    D = v * 0.83 * (np.log10(x)) ** 2.414
    y = (M / (4 * math.pi * time1 * np.sqrt(D / R))) * np.exp(
        -((x - (((1.667 / n) * time1) / R)) ** 2) / (4 * D * time1 / R))
    yy = (M / (4 * math.pi * time2 * np.sqrt(D / R))) * np.exp(
        -((x - (((1.667 / n) * time2) / R)) ** 2) / (4 * D * time2 / R))
    y2 = (M / (4 * math.pi * time3 * np.sqrt(D / R))) * np.exp(
        -((x - (((1.667 / n) * time3) / R)) ** 2) / (4 * D * time3 / R))
    return x, y, yy, y2


x, y, yy, y2 = calculate_z(M, n)
source = ColumnDataSource(data=dict(x=x, y=y))
source1 = ColumnDataSource(data=dict(x=x, y=yy))
source2 = ColumnDataSource(data=dict(x=x, y=y2))

# Set up plotting function 
# set up the Bokeh figure first
plot = bk_figure(plot_height=400, plot_width=400, title="Concentration Signals (1 Dimension)",
                 tools="crosshair,pan,reset,save,wheel_zoom",
                 x_range=[-10, 350], y_range=[0, 15])
plot.xaxis.axis_label = 'Horizontal Distance (m)'
plot.yaxis.axis_label = 'Concentration (kg/m)'

# input three functions with 1, 5, 10 days
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6, color='magenta', legend_label='5 days')
plot.line('x', 'y', source=source1, line_width=3, line_alpha=0.6, color='blue', legend_label='10 days')
plot.line('x', 'y', source=source2, line_width=3, line_alpha=0.6, color='green', legend_label='20 days')

# Set up widgets aka. sliders and text box
text = TextInput(title="title", value='Concentration Signals (1 Dimension)')
Mass = Slider(title="Pollution Mass (kg)", value=500, start=300, end=1000, step=5)
menu = Select(options=['Well Sorted Sand', 'Glacial Till', 'Silt'], value='Well Sorted Sand', title='Soil Type')

"""
Define Bokeh event handler callback functions
"""
def update_title(attrname, old, new):
    """
    Bokeh event handler callback that changes the title of the plot
    :param attrname: 'value' attribute of TextInput widget
    :param old: previous title value
    :param new: updated title value
    :return:
    """
    plot.title.text = text.value


def update_data(attrname, old, new):
    """
    Bokeh event handler callback that redraws the plot when the mass or menu are changed
    :param attrname: 'value' attribute of Mass and menu widgets
    :param old: previous values of mass and menu
    :param new: updated values of mass and menu
    """
    # Get the current slider values
    if menu.value == 'Well Sorted Sand':
        n = 0.375
    elif menu.value == 'Glacial Till':
        n = 0.15
    elif menu.value == 'Silt':
        n = 0.42
    M = Mass.value
    x, y, yy, y2 = calculate_z(M, n)
    # Generate the new curve
    source.data = dict(x=x, y=y)
    source1.data = dict(x=x, y=yy)
    source2.data = dict(x=x, y=y2)


# Trigger callback to change title
text.on_change('value', update_title)

for w in [Mass, menu]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(text, menu, Mass)
layout = row(plot, column(text, menu, Mass))

curdoc().add_root(layout)
curdoc().title = "Signals"


# In[ ]:




