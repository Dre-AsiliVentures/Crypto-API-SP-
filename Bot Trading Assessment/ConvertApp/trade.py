from binance import Client
from binance.enums import *
from datafetch import Binance_DataFetch
class Trade:
    def __init__(self,tradesymbol1,tradesymbol2,tickerSymbol,targetProfit):
        self.tradesymbol1=tradesymbol1
        self.tradesymbol2=tradesymbol2
        self.targetProfit=targetProfit
        self.tickerSymbol=tickerSymbol #e.g., ETHUSDT
        self.tickerSymbol=None
        self.period_interval=Client.KLINE_INTERVAL_1DAY
        self.period=Client.KLINE_INTERVAL_1DAY
        self.lookback='2000 day ago UTC+3'
        self.data=Binance_DataFetch().client_dataFetch(ticker_symbol==self.tickerSymbol, period_interval=self.period, lookback_period=self.lookback)
        self.client=Binance_DataFetch().client_setup()
    def tickerID(self):
        return self.tickerSymbol
    def tickerPrice(self):
        self.tickerprice=self.client.get_symbol_ticker(symbol=self.tickerID())
        return self.tickerprice['price']
    def assetBalance(self):
        self.assetbalance1=self.client.get_asset_balance(asset=self.tradesymbol1)
        self.assetbalance2=self.client.get_asset_balance(asset=self.tradesymbol2)
        return [self.assetbalance1,self.assetbalance2]
    def buy(self,qty):
        if (testnet):
                    # create test order before pushing an actual order
            test_order = self.client.create_test_order(
                symbol=self.tickerSymbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                quantity=qty)
            try: # try to create a real order if the test orders did not raise an exception
                buy_limit = self.client.create_order(symbol=self.tickerSymbol,side='BUY',type='MARKET',quantity=qty)

            #error handling here in case position cannot be placed
            except Exception as e:
                print(e)

                    # run the else block if the position has been placed and return some info
        else:
            pass
    def sell(self,qty):
        if (testnet):
                    # create test order before pushing an actual order
            test_order = self.client.create_test_order(
                symbol=self.tickerSymbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                quantity=qty)
            try: # try to create a real order if the test orders did not raise an exception
                #buy_limit = self.client.create_order(symbol=self.tickerSymbol,side=SIDE_SELL,type='MARKET',quantity=qty)
                pass

            #error handling here in case position cannot be placed
            except Exception as e:
                print(e)

                    # run the else block if the position has been placed and return some info
        else:
            pass
    def convertStrategy(self,type):
        if type=='Base':
            # If trading is for base currency 
            buy_quantity=round(float(self.assetBalance()[0]))/float(self.tickerPrice())
        elif type=='Quote':
            # If trading is for Quote currency currency
            buy_quantity=round(float(self.assetBalance()[1]))/float(self.tickerPrice())
        else:
            pass
        while True:
            price_info=self.client.get_margin_price_index(symbol=self.tickerSymbol)
            order = self.client.get_all_orders(symbol=self.tickerSymbol, limit=1)
            if order:
                    # convert order timsestamp into UTC format
                    time = order[0]['time'] / 1000
                    utc_time = datetime.fromtimestamp(time)
                    # print order condirmation to the console
                    print(f"Order {order[0]['orderId']} has been placed on at {utc_time}")
            else:
                print('Could not get last order from Binance!')
