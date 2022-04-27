import os
from binance.client import Client

api_key=os.environ.get('binance_api')
api_secret=os.environ.get('binance_secret')

client=Client(api_key,api_secret,tld='com')
symbol=input("Enter the symbol e.g BNBBTC")

# Get Market Depth
depth=client.get_order_book(symbol)

## Create a test order
global quantity= input("Enter the ")
def test_order():
    return client.create_test_order(
    symbol,
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_MARKET,
    quantity)
)
print("All good")

#client.API_URL = 'https://api.binance.com/api/v3'
#client.API_URL = 'https://testnet.binance.vision/api' # testnet

