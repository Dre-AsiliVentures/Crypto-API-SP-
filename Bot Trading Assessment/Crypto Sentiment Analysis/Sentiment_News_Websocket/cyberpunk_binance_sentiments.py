import os
from binance import Client,ThreadedWebsocketManager
# Use testnet (change to True) or live (change to False)?
testnet = True

# get binance key and secret from environment variables for testnet and live
api_key_test = os.getenv('BINANCE_TEST_API')
api_secret_test = os.getenv('BINANCE_TEST_SECRET')

api_key_live = os.getenv('BINANCE_API')
api_secret_live = os.getenv('BINANCE_SECRET')

# Authenticate with the client
if testnet:
    client = Client(api_key_test, api_secret_test)
else:
    client = Client(api_key_live, api_secret_live)

# The API URL is manually changed in the library to work on the testnet
if testnet:
    client.API_URL = 'https://testnet.binance.vision/api'

def main():

    symbol = 'BNBBTC'

    twm = ThreadedWebsocketManager(api_key_test,api_secret_test)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        print(msg)

    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    # multiple sockets can be started
    twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    # or a multiplex socket can be started like this
    # see Binance docs for stream names
    streams = ['bnbbtc@miniTicker', 'bnbbtc@bookTicker']
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

    twm.join()


if __name__ == "__main__":
   main()