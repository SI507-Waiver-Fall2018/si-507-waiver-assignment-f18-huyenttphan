# Imports -- you may add others but do not need to
import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd
import numpy as np

# Code here should involve creation of the bar chart as specified in instructions
# And opening / using the CSV file you created earlier with noun data from tweets

py.sign_in('huyenttphan', 'wEv9dEArjHEIyUUSza55') # Replace the username, and API key with your credentials.

df = pd.read_csv('noun_data.csv')
df.head()

trace = go.Bar(
    x=df['Noun'], 
    y=df['Number'], 
    marker=dict(color='rgb(26, 118, 255)')
)
data = [trace]
layout = go.Layout(title='Most common nouns', width=800, height=640,
    yaxis=dict(
        title='Frequency',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        )
    ),
)
fig = go.Figure(data=data, layout=layout)

py.image.save_as(fig, filename='part4_viz_image.png')