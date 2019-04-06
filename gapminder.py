#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
from bokeh.io import output_file, show ,curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper, Slider, Select
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox , row , column


# In[30]:


data = pd.read_csv('datacamp_gapminder_tidy.csv' )
data.set_index("Year", inplace = True)
regions_list = data.region.unique().tolist()
data.head()


# In[31]:


def update_plot(attr, old, new):
    yr = slider.value
    x = x_select.value
    y = y_select.value
   
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
   
    new_data = {
        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
        'country' : data.loc[yr].Country,
        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region,
    }
   
    source.data = new_data

    
    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])

    
    plot.title.text = 'Gapminder data for %d' % yr


# In[32]:


color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)


# In[33]:


source = ColumnDataSource(data={
    'x'       : data.loc[1970].fertility,
    'y'       : data.loc[1970].life,
    'country' : data.loc[1970].Country,
    'pop'     : (data.loc[1970].population / 20000000) + 2,
    'region'  : data.loc[1970].region,
})


# In[34]:


x_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='fertility',
    title='x-axis data'
)
x_select.on_change('value', update_plot)
y_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='life',
    title='y-axis data'
)
y_select.on_change('value', update_plot)


# In[35]:


xmin, xmax = min(data.fertility), max(data.fertility)
ymin, ymax = min(data.life), max(data.life)


# In[36]:


plot = figure(title='Gapminder Data for 1970', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax) )


# In[37]:


plot.circle(x='x', y='y', fill_alpha=0.8, source=source,
            color=dict(field='region', transform=color_mapper), legend='region')


# In[38]:


slider = Slider(start=1970 , end =2010 , step=1 , value=1970 , title='Year')
slider.on_change('value', update_plot)
hover = HoverTool(tooltips=[('Country','@country')])
plot.add_tools(hover)


# In[39]:


plot.legend.location = 'top_right'
plot.xaxis.axis_label ='Fertility (children per woman)'
plot.yaxis.axis_label = 'Life is Expectancy '


# In[40]:


output_file("js_on.html")
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)


# In[ ]:




