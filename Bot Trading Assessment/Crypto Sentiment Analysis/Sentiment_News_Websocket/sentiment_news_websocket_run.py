# Importing the libraries
import os,time
import xml.etree.ElementTree as ET
import requests
from datetime import date, datetime, timedelta
import csv
import numpy as np
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Binance API
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
#from binance.websockets import BinanceSocketManager
from binance.streams  import ThreadedWebsocketManager # Threaded Websocket for 
from twisted.internet import reactor # For Binance Websocket

# Executing the code
from itertools import count
# API keys
api_key=os.environ.get('BINANCE_API')
api_test_key=os.environ.get('BINANCE_TEST_API')
api_secret=os.environ.get('BINANCE_SECRET')
api_test_secret=os.environ.get('BINANCE_TEST_SECRET')

# Testnet Parameters
testnet=True # True= Demo Mode, False= Live Mode

# Authenticating the client
if testnet:
    client=Client(api_key,api_secret)
else:
    client=Client(api_test_key,api_test_secret)

if testnet:
    client.API_URL='https://testnet.binance.vision/api'

# Creating USER-INPUT VARIABLES

keywords= { # Coin words the user wants to search for using the Bot
    'XRP':['ripple','xrp','XRP','Ripple','Ripple'],
    'LTC':['litecoin','ltc','Litecoin','Litecoin'],
    'ETH':['ethereum','eth','Ethereum','Ethereum'],
    'BTC':['bitcoin','btc','Bitcoin','Bitcoin'],
    'BCH':['bitcoin cash','bch','Bitcoin Cash','Bitcoin Cash'],
    'BNB':['binance coin','bnb','Binance Coin','Binance Coin'],
    'EOS':['eos','eos','EOS','EOS'],
    'TRX':['tron','trx','TRON','TRON'],
    'XLM':['stellar','xlm','Stellar','Stellar'],
    'ADA':['cardano','ada','Cardano','Cardano'],
    'XMR':['monero','xmr','Monero','Monero'],
    'NEO':['neo','neo','NEO','NEO'],
    'DASH':['dash','dash','Dash','Dash'],
    'XEM':['nem','xem','NEM','NEM'],
    'ETC':['ethereum classic','etc','Ethereum Classic','Ethereum Classic'],
    'ONT':['ontology','ont','Ontology','Ontology'],
    'ZEC':['zcash','zec','Zcash','Zcash'],
    'BTG':['bitcoin gold','btg','Bitcoin Gold','Bitcoin Gold'],
    'ICX':['icon','icx','ICON','ICON'],
    'VET':['vechain','vet','VeChain','VeChain'],
    'QTUM':['qtum','qtum','Qtum','Qtum'],
    'OMG':['omisego','omg','OmiseGo','OmiseGo'],
    'LSK':['lisk','lsk','Lisk','Lisk'],
    'ZIL':['zilliqa','zil','Zilliqa','Zilliqa'],
    'STEEM':['steem','steem','Steem','Steem'],
    'STRAT':['stratis','strat','Stratis','Stratis'],
    'PPT':['populous','ppt','Populous','Populous'],
    'SNT':['status','snt','Status','Status'],
    'REP':['augur','rep','Augur','Augur']
}
PAIRING=str(input('Enter the coin pairing you want to search for e.g,USDT: '))
SENTIMENT_THRESHOLD=0.5 # Threshold for sentiment analysis, hOW positive the news should be to be considered positive to place an order
MINIMUM_ARTICLES=10 # Minimum number of articles to be considered for sentiment analysis to qualify the trade signal
REPEAT_EVERY=10 # Number of seconds to wait before repeating the trade signal or a new place trade in minutes

##  CONNECTING THE WEBSOCKET
CURRENT_PRICE={}
def ticker_socket(msg):
    if msg['e'] != 'error':
        global CURRENT_PRICE
        CURRENT_PRICE['{0}'.format(msg['s'])]=msg['c'] 
    else:
        print('Error')


bsm=ThreadedWebsocketManager(client)
#bsm=BinanceSocketManager(client)
for coin in keywords:
    conn_key=bsm.start_symbol_ticker_socket(coin+PAIRING,ticker_socket)
bsm.start()

##  CALCULATING TRADING VOLUME
def calculate_volume():
    while CURRENT_PRICE=={}:
        print('-----Connecting to Socket-------')
        time.sleep(3)
    else:
        volume={}
        for coin in CURRENT_PRICE:
            volume[coin]=float(QUANTITY/float(CURRENT_PRICE[coin]))
            volume[coin]=float('{:.6f}'.format(volume[coin]))
        return volume

## Webscraping the Cryptonews from Blogs
with open('Crypto_News.csv','w') as csv_file:
    # OPEN THE FILE
    csv_reader=csv.reader(csv_file)
    # Remove any headers
    next(csv_reader,None)
    feeds=[]  # Create an empty list
    for row in csv_reader:
        feeds.append(row[0])
# RETURN THE LATEST HEADLINE FOR EACH  NEWS SOURCE
def get_headlines():
    '''Bot Trading Assessment.code-workspace'''
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Windows; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'
    }
    headlines={'source':[],'title':[],'pubDate':[]}
    for feed in feeds:
        try:
            r=requests.get(feed,headers=headers,timeout=7) # get tXML for each feed
            root=ET.fromstring(r.text) # parse the XML, define the root for the parsing
            channel=root.find('channel/item/title').text
            pubDate=root.find('channel/item/pubDate').text # get the pubDate

            headlines['title'].append(channel.endcode('UTF-8').decode('UTF-8'))
            print(channel)
        except:
            print(f'Could not parse {feed}')

    return headlines

# Categorize the headlines
def categorise_headlines():
    '''Categorise the headlines'''
    headlines=get_headlines()
    categorised_headlines={}

    for keyword in keywords:
        categorised_headlines['{0}'.format(keyword)]=[] # Create an empty list for each keyword
    for keyword in keywords:
        for headline in headlines['title']:
            if any(key in headline for key in keywords[keyword]):
                categorised_headlines[keyword].append(headline)
    return categorised_headlines()

# Determine the sentiment
def analyse_headlines():
    sia=SentimentIntensityAnalyzer()
    categorised_headlines=categorise_headlines()
    sentiment={}
    for coin in categorised_headlines:
        if len(categorised_headlines[coin])>0:
            sentiment[{0}.format(coin)]=[] # Create an empty list for each coin
            for title in categorised_headlines[coin]:
                try:
                    #score=sia.polarity_scores(title)['compound']
                    score=sia.polarity_scores(title) # get the polarity score
                    sentiment[coin].append(score)

                except:
                    print(f'Could not parse {title}')
    return sentiment

def compile_sentiment():
    sentiment=analyse_headlines()
    compiled_sentiment={}
    for coin in sentiment:
        compiled_sentiment[coin]=[]
        for item in sentiment[coin]:
            compiled_sentiment[coin].append(sentiment[coin][sentiment[coin].index(item)]['compound']) # append the sentiment to compound score
    return compiled_sentiment
## Calculate the average compound sentiment

def compound_average():
    compiled_sentiment=compile_sentiment()
    headlines_analysed={}
    for coin in compiled_sentiment:
        headlines_analysed[coin]=len(compiled_sentiment[coin])
        compiled_sentiment[coin]=np.array(compiled_sentiment[coin])
        compiled_sentiment[coin]=np.mean(compiled_sentiment[coin])
        compiled_sentiment[coin]=compiled_sentiment[coin].item()
    return compiled_sentiment,headlines_analysed


## PLACE TRADE SIGNAL - BUY OR SELL
def buy():

    compiled_sentiment,headlines_analysed=compound_average()
    volume=calculate_volume()

    for coin in compiled_sentiment:
        if compiled_sentiment[coin]>SENTIMENT_THRESHOLD and headlines_analysed[coin]>=MINIMUM_ARTICLES:
            print(f'BUY {coin}')
            print(f'Preparing to buy {coin} with {volume} USDT at {CURRENT_PRICE[coin+PAIRING]}')
            if (testnet):
                # Create a test order
                test_order=client.creeate_test_order(symbol=coin+PAIRING,side='BUY',type='MARKET',quantity=volume[coin+PAIRING])

            # Place the actual order
            try:
                buy_limit=client.create_order(
                symbol=coin+PAIRING,
                side='BUY',
                type='MARKET',
                quantity=volume[coin+PAIRING],
            )
            except BinanceAPIException as e:
                print(e.message)
                print('Order failed')
                continue
            except BinanceOrderException as e:
                print(e.message)
                print('Order failed')
                continue
            else:
                # Retrieve the last order
                order=client.get_all_orders(symbol=coin+PAIRING,limit=1)
                # Convert order timestamp in UTC forma
                if order:
                    time=order[0]['time']/1000
                    #utc_time=datetime.datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
                    utc_time=datetime.fromtimestamp(time)
                    bought_at=CURRENT_PRICE[coin+PAIRING] # Grab the Crypto price the order was placed at 
                    print(f"order {order[0]['orderId']} has been placed on {coin} with {order[0]['origQty']} at {utc_time} and bought at {bought_at}")
                    #return bought_at,order
        else:
            print(f'Sentiment not positive enough for {coin}, or not enough headlines analysed: {compiled_sentiment[coin]}, {headlines_analysed[coin]}')
            print('\n')

if __name__ == '__main__':
    print('Press Ctrl-Q to stop the script')
    for i in count():
        buy()
        print(f'Iteration {i}')
        time.sleep(60 * REPEAT_EVERY)