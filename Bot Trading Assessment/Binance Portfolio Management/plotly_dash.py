import dash
from dash import dcc
#import dash_core_components as dcc
#import dash_html_components as html
from dash import html
#from dash_dependencies import Input,Output
from dash.dependencies import Input,Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app=dash.Dash(__name__,external_stylesheets=[dbc.themes.FLATLY])
dcc.Slider(value=4,min=-50, max=50, step=0.5,
           label={-50:'-50 Degrees',0:'0',10:'10 Degrees'})
@dash_app.callback(Output('Graph-ID','figure'), # Decorator that binds/updates custom data analysis code to Dash UI
[Input('Slider-id','value')])
def data_analysis_function(new_slider_value):
    new_figure=your_computer_Figure(new_slider_value)
    return new_figure
"""Earlier code pasted as docstringsumary_line

app=dash.Dash(__name__,external_stylesheets=[dbc.themes.FLATLY])
app.layout=html.Div([
    html.Div([
        html.Div([
            dcc.Graph(
                id='figure-1',
                figure ={'data':[go.Indicator(
                    mode='number',
                    value=''
                )
                ],

                'layout':
                go.Layout(
                    title='Portfolio value (USDT)'
                )
                }

            )], 
            style={
                'width': '30%','height': '300px', 'display':'inline-block'
            })
    ])
])
"""
