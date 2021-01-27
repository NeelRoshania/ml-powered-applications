# Script to launch a bokeh application

# dependencies
import pandas as pd
import numpy as np
import bokeh.models as bmo
import bokeh.plotting as bpl
import matplotlib.pyplot as plt

from functions.funcs import export_df, test
from functions.bokeh_callbacks import checkbox_categorical_filter
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.palettes import d3, all_palettes
from bokeh.layouts import row, layout
from bokeh.models import CheckboxGroup, Panel
from bokeh.models.tools import HoverTool
from bokeh.models.widgets import Tabs
# from bokeh.io import show, output_notebook

# intialization
PATH_data = r"C:\Users\nrosh\Desktop\Personal Coding Projects\Python\ml-powered-applications\neel\data"

# ingestion
df_orig = pd.read_csv(
    PATH_data + "\\labelling\questions_by_cluster.csv",
)

df = df_orig.iloc[:, 1::].copy()
df.info()

# Bokeh setup and sources

# Last mile conversions
df_bokeh                      = df.copy()
df_bokeh["question_answered"] = df_bokeh.question_answered.apply(lambda row: "answered" if row==True else "unanswered")
df_bokeh["cluster"]           = df_bokeh.cluster.apply(lambda row: str(row))

# define UI Tools
TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
LABELS = ["Cluster {}".format(cluster) for cluster in np.sort(df_bokeh.cluster.unique())]

# sources
df_ans   = df_bokeh.loc[df_bokeh.question_answered == 'answered', :]
df_nans  = df_bokeh.loc[df_bokeh.question_answered == 'unanswered', :]

src_ans  = bpl.ColumnDataSource(
    df_ans.to_dict('list')
)

src_nans = bpl.ColumnDataSource(
    df_nans.to_dict('list')
)

## Bokeh worflow

# output_notebook()

#
# Figures and colormaps
#

p_answered = figure(tools=TOOLS)
p_nanswered = figure(tools=TOOLS)

ans_cmap = bmo.CategoricalColorMapper(
    factors=df_ans.cluster.unique(),
    palette=all_palettes['Set1'][len(df_ans.cluster.unique())]
)

nans_cmap = bmo.CategoricalColorMapper(
    factors=df_nans.cluster.unique(),
    palette=all_palettes['Set1'][len(df_nans.cluster.unique())]
) # this changes the order with which the colors are applied

#
# Visualizations
#

p_answered.scatter(
    x='x', 
    y='y',
    source=src_ans,
    color={'field': 'cluster', 'transform': ans_cmap},
    fill_alpha=0.9,
    line_color=None,
    legend_group='cluster'
)

# using the color mapped define by answered questions - potential bug
p_nanswered.scatter(
    x='x', 
    y='y',
    source=src_nans,
    color={'field': 'cluster', 'transform': ans_cmap},
    fill_alpha=0.9,
    line_color=None,
    legend_group='cluster'
)

# Decorations
p_answered.title.text = 'Answered questions'
p_answered.legend.title = 'Cluster'
p_answered.xaxis.axis_label = 'Dimensional x'
p_answered.yaxis.axis_label = 'Dimensional y'


p_nanswered.title.text = 'Unanswered questions'
p_nanswered.legend.title = 'Cluster'
p_nanswered.xaxis.axis_label = 'Dimensional x'
p_nanswered.yaxis.axis_label = 'Dimensional y'

fig_dim = 550
p_answered.width = p_nanswered.width = fig_dim
p_answered.height = p_nanswered.height = fig_dim

# hover parameters
hover_answered = HoverTool()
hover_answered.tooltips=[
    ('Question ', '@question_answered'),
    ('Post Question Title', '@post_title'),
    ('Cluster', '@cluster'),
]

hover_nanswered = HoverTool()
hover_nanswered.tooltips=[
    ('Question ', '@question_answered'),
    ('Post Question Title', '@post_title'),
    ('Cluster', '@cluster')
]

p_answered.add_tools(hover_answered)
p_nanswered.add_tools(hover_answered)

#
# Widgets
#

filter_answered = checkbox_categorical_filter(src_ans)
checkbox_group = CheckboxGroup(labels=LABELS, active=[i for i in range(len(LABELS))])
checkbox_group.js_on_change('active', filter_answered)

# checkbox_group.on_change('active', update)

# output_file("color_scatter.html", title="color_scatter.py example")

# layout specificationns 
lay = layout(
        children = [
            [p_answered, p_nanswered],
            [checkbox_group],
        ]
)

tab = Panel(child=lay, title = 'Clusters')
tabs = Tabs(tabs=[tab])

curdoc().add_root(tabs)

# show(tabs)  # open a browser or notebook depending on configuration