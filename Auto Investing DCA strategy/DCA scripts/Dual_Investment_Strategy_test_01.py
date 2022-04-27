import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib import style
import seaborn as sns
from datetime import date
from sklearn.tree import DecisionTreeRegressor

sns.set()
sns.set_style('dark')
sns.set_palette(sns.color_palette('muted'))
fig = plt.figure()
fig.patch.set_alpha(0.0)


# Basic styling
# style.use('seaborn-notebook')
pd.set_option('display.width', 200)

# load data
link="https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_d.csv"
btc = pd.read_csv(link, skiprows=1, usecols=['date', 'close','open'])
# Index dataset by date
btc['date'] = pd.to_datetime(btc['date'])
btc = btc.set_index('date')
btc = btc.sort_index()

# ATTENTION - this is used so regenerating the data does not update notebook automatically
# Until I find a good way to inline numbers in markdown sections, this is the only solution
# I can think of to guarantee some consistency between generated outputs and written text
today=date.today()
today_date=today.strftime("%Y-%m-%d")
btc=btc.loc[:today_date]
#btc=btc.reshape(-1,1)
# print results
#print(btc.tail())
data= btc.tail(n=25)
print(data)
btc_open_data=data.open.values.reshape(-1,1)
btc_close_data=data.close.values.reshape(-1,1)
data_model=DecisionTreeRegressor(max_depth=5).fit(btc_open_data,btc_close_data)
data_predict=data_model.predict(btc_close_data)
print(data_predict)


