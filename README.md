# BiBot9000 - Simple Crypto Trading Bot on the Binance Platform

 This python script works on a single basic strategy, which is to track the Relative Strength Indicator (RSI) of a list of BTC or ETH trading pairs.
 The script populates a list of trading pairs that meet predefined 24Hr price movement and volume requirements in a watchlist output to the terminal. 
 The script will automatically place buy and sell orders using all available BTC or ETH funds contained in the user's Spot Wallet.
 Trades are initiated based on trading pairs from the content of the dynamically populated watch list based on whether the RSI indicates an overbought (>70) or oversold (<30) condition. 
 
 CONSIDERATIONS
 In the current form, the script only hadles a single order at a time and will not place a second order if there is already one in progress.  
 
 NOTE: Since there is no easy way to pull the most recent order through teh Binance API, the script assumes that the is no existing order on first run. 
 If you are in an order and initiating the script, you must set 'inOrder' to True, and specify the active trading pair in 'last_active_symbol'
 
# Prerequisites

* Install Python 3.7 (Spyder, PyCharm IDE)
* Python-Binance Library
* Subscription to taapi.io for RSI technical indicators

# Acknowledgments

* **Samm Chardy** - *Initial work* - [Python-Binance](https://github.com/sammchardy/python-binance)
* **Blockchain Engineer** - *Trader Bot Examples & Functionality* - [Python-Binance](https://github.com/Roibal/python-binance)

# DISCLAIMER

THIS SCRIPT WILL TAKE WILL ISSUE TRADES AUTOMATICALLY FROM YOUR BINACNE ACCOUNT. PROCEED WITH CAUTION!
Be sure to test will small amounts and protect your assets before running for the first time.  