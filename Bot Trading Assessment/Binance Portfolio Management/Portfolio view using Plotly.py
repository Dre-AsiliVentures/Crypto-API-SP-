import os

from binance.client import Client
#from binance.websockets import BinanceSocketManager
from binance import BinanceSocketManager
import time

api_key = os.environ.get('BINANCE_TEST_API')
api_secret = os.environ.get('BINANCE_TEST_SECRET')
client=client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'  # To change endpoint URL for test account


# Dashboard layout
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