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
from binance.streams  import BinanceSocketManager # Binance Websocket
from twisted.internet import reactor # For Binance Websocket

# Executing the code
from itertools import count
# API keys
api_key=os.environ.get('BINANCE_TEST_API')
api_secret=os.environ.get('BINANCE_TEST_SECRET')

# Authenticating the client
client=Client(api_key,api_secret)

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
MINIMUM_ARTICLE=10 # Minimum number of articles to be considered for sentiment analysis to qualify the trade signal
REPEAT_EVERY=10 # Number of seconds to wait before repeating the trade signal or a new place trade in minutes

##  CONNECTING THE WEBSOCKET
CURRENT_PRICE={}
def ticker_socket(msg):
    if msg['e'] == 'error':
        global CURRENT_PRICE
        CURRENT_PRICE['{0}'.format(msg['s'])]=msg['c'] 
    else:
        print('Error')

bsm=BinanceSocketManager(client)
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