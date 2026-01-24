from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
app = Dash(__name__)
app.layout = html.Div([
    dcc.Input(
        placeholder='Enter a valid number', 
        id='data',
        type='number'
    ),
    html.Button('Submit', id='numbers', n_clicks=0),
    html.H1(id='result')
])

@app.callback(
    Output('result', 'children'),
    Input('numbers', 'n_clicks'),
    Input('data', 'value')
)
def play_data(n,data):
    if n :
        return f"you entered {data}"
    return ""
    
app.run(debug=True)    