import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib import style
import seaborn as sns

sns.set()
sns.set_style('dark')
sns.set_palette(sns.color_palette('muted'))
fig = plt.figure()
fig.patch.set_alpha(0.0)


# Basic styling
# style.use('seaborn-notebook')
pd.set_option('display.width', 200)

# load data
btc = pd.read_csv("E:\Intellectual Content\GMT\Gig-Econ\Strategic Programmer\Crypto API\Auto Investing DCA strategy\DCA scripts/Binance_QTUMUSDT_d.csv", skiprows=1, usecols=['date', 'close'])
# Index dataset by date
btc['date'] = pd.to_datetime(btc['date'])
btc = btc.set_index('date')
btc = btc.sort_index()

# ATTENTION - this is used so regenerating the data does not update notebook automatically
# Until I find a good way to inline numbers in markdown sections, this is the only solution
# I can think of to guarantee some consistency between generated outputs and written text
btc=btc.loc[:'2022-04-17']

# print results
print(btc.tail())

# CALCULATING THE VALUE OF DCA INVESTMENT
value_price = btc['close'][-1]
initial_investment = 2500.00

def doDCAmonthly(investment, start_date, periods, freq):
    investment_dates_all = pd.date_range(start_date,periods=periods,freq=freq)
    # Remove those dates beyond our known data range
    investment_dates = investment_dates_all[investment_dates_all < btc.index[-1]]

    # Get closest business dates with available data
    closest_investment_dates = btc.index.searchsorted(investment_dates)

    # How much to invest on each date
    portion = investment/periods

    # Get the total of all stocks purchased for each of those dates (on the Close)
    stocks_invested = sum(portion / btc['close'][closest_investment_dates])

    # Add uninvested amount back
    uninvested_dollars = portion * sum(investment_dates_all >= btc.index[-1])

    # value of stocks today
    total_value = value_price*stocks_invested + uninvested_dollars
    return total_value

# Generate DCA series for every possible date and investment strategy
dca_m = pd.Series(btc.index.map(lambda x: doDCAmonthly(initial_investment, x, 4, '30D')), index=btc.index, name='Monthly DCA')

dca_w = pd.Series(btc.index.map(lambda x: doDCAmonthly(initial_investment, x, 16, '7D')), index=btc.index, name='Weekly DCA')

dca_d = pd.Series(btc.index.map(lambda x: doDCAmonthly(initial_investment, x, 120, '1D')), index=btc.index, name='Daily DCA')

# Representing the strategies and plotting the data

dca = pd.concat([dca_d, dca_m, dca_w], axis=1)

ax = plt.subplot()
dca[1:].plot(ax=ax, figsize=(20,10), color=['b','r','g'], label="DCA")

ax.set_yscale('log')
plt.grid(linestyle='dotted')
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '${:,.0f}'.format(x)))

ax.axhline(initial_investment, alpha=0.5, linestyle="--", color="black")
ax.text(btc.index[20],initial_investment*1.3, "Initial Investment")
plt.title('Dollar Cost Averaging - Present value of $2,500 invested on a date')
plt.ylabel('Investment Value ($)')
plt.show()

# Comparing the results
winners = dca.idxmax(axis=1)
print(winners.value_counts())

# Monthly Investment and Statistical Significance

diff_mw = dca['Monthly DCA'] - dca['Weekly DCA']

print("Monthly DCA returns more than Weekly DCA %.1f%% of all the days" % (100*sum(diff_mw>0)/len(diff_mw)))
print("Weekly DCA returns more than Monthly DCA %.1f%% of all the days" % (100*sum(diff_mw<0)/len(diff_mw)))

print("Mean difference: Average dollar improvement Monthly DCA returns vs. Weekly DCA: ${:,.2f}".format(sum(diff_mw) / len(diff_mw)))
print("Mean difference when Monthly DCA > Weekly DCA: ${:,.2f}".format(sum(diff_mw[diff_mw>0]) / sum(diff_mw>0)))
print("Mean difference when Weekly DCA > Monthly DCA: ${:,.2f}".format(sum(-diff_mw[diff_mw<0]) / sum(diff_mw<0)))

# Calculation of Daily and Monthly Strategy
diff_md = dca['Monthly DCA'] - dca['Daily DCA']

print("Monthly DCA returns more than Daily DCA %.1f%% of all the days" % (100*sum(diff_md>0)/len(diff_md)))
print("Daily DCA returns more than Monthly DCA %.1f%% of all the days" % (100*sum(diff_md<0)/len(diff_md)))

print("Mean difference: Average dollar improvement Monthly DCA returns vs. Daily DCA: ${:,.2f}".format(sum(diff_md) / len(diff_md)))
print("Mean difference when Monthly DCA > Daily DCA: ${:,.2f}".format(sum(diff_md[diff_md>0]) / sum(diff_md>0)))
print("Mean difference when Daily DCA > Monthly DCA: ${:,.2f}".format(sum(-diff_md[diff_md<0]) / sum(diff_md<0)))

# Weekly versus Daily Strategies
diff_wd = dca['Weekly DCA'] - dca['Daily DCA']

print("Weekly DCA returns more than Daily DCA %.1f%% of all the days" % (100*sum(diff_wd>0)/len(diff_wd)))
print("Daily DCA returns more than Weekly DCA %.1f%% of all the days" % (100*sum(diff_wd<0)/len(diff_wd)))

print("Mean difference: Average dollar improvement Weekly DCA returns vs. Daily DCA: ${:,.2f}".format(sum(diff_wd) / len(diff_wd)))
print("Mean difference when Weekly DCA > Daily DCA: ${:,.2f}".format(sum(diff_wd[diff_wd>0]) / sum(diff_wd>0)))
print("Mean difference when Daily DCA > Weekly DCA: ${:,.2f}".format(sum(-diff_wd[diff_wd<0]) / sum(diff_wd<0)))
h