import pandas as pd
import numpy as np
from binance import Client
import os
class Binance_DataFetch():
    def __init___(self,ticker_symbol,period_interval,lookback_period):
        self.ticker_symbol=ticker_symbol
        self.period_interval=period_interval
        self.lookback_period=lookback_period
        self.client=None
        self.frame=None
        print("Done importing all libraries")
    def client_setup(self):
        api_key = os.environ.get('BINANCE_TEST_API')
        api_secret = os.environ.get('BINANCE_TEST_SECRET')
        self.client=Client(api_key, api_secret)
        return self.client
    def client_dataFetch(self):
        client=self.client_setup()
        if client!=None:
            print("Now fetching the client data")
            data=client.get_historical_klines(self.ticker_symbol,self.period_interval,self.lookback_period)
            self.frame=pd.DataFrame(data)
            self.frame=self.frame.iloc[:,:6] # All rows and column upto 6
            # Namig the columns
            self.frame.columns=['Time','Open','High','Low','Close','Volume']
            # Name the rows
            self.frame=self.frame.set_index('Time') # Note this is in ms
            # Convert this Time to readable form since this is time from 1970s
            self.frame.index=pd.to_datetime(self.frame.index,unit='ms')
            self.frame=self.frame.astype(float) # Convert values from strings to floatn
        else:
            print("There was an error defining the account")
        return self.frame

"""Example usage:
a=Binance_DataFetch()
data=a.client_dataFetch("BNBBUSD", Client.KLINE_INTERVAL_1DAY, "2000 day ago UTC+3")
# #https://python-binance.readthedocs.io/en/latest/market_data.html?highlight=kline%20limit#id6
"""