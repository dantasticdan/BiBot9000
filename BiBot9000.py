# -*- coding: utf-8 -*-
"""
BINANCE BOT 9000
This is an automated trading bot built for the Binance platform, which places automated Buy/Sell trades based on a simple RSI indicator from the taapi.io

-Utilizing Python-Binance Wrapper( https://github.com/sammchardy/python-binance )
-Expanded and inpired by trading bots developed by Joaquin Roibal
    (https://github.com/Roibal/Cryptocurrency-Trading-Bots-Python-Beginner-Advance)

v0.1 - Updated 7/25/2020 - BTC and ETH price and RSI tracking. Buy/Sell Automation from preset criteria. 

@author: dantastic_dan
"""

#import keys
import BinanceKeys
import time
import requests 
from time import sleep
from binance.client import Client

from BinanceKeys import BinanceKey1

#Binance API Definitions
api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']

#TAAPI API Definitions
# Define indicator
indicator = "rsi"
# Define endpoint 
endpoint = f"https://ta.taapi.io/rsi"
# Define a parameters dict for the parameters to be sent to the API 
parameters = {
    'secret': '[TAAPI API SECRET]',
    'exchange': 'binance',
    'symbol': 'XTZ/BTC',
    'interval': '5m'
    } 

client = Client(api_key, api_secret)

def run():
    inOrder= True
    watch_list = ['SYSBTC','GVTBTC','CDTBTC','TROYBTC','RUNEBTC','SKYBTC','SXPBTC','NULSBTC']
    micro_cap_coins = ['ICXBNB', 'BRDBNB', 'NAVBNB', 'RCNBNB','FUNETH','COTETH']
    eth_watch_list = ['BQXETH','EVXETH']
    
    bot_watch_list = []
    eth_bot_watch_list = []
    rsi_list = []
    
    last_active_symbol = ['ONEBTC']
    
     #time_horizon = "Short"
    #Risk = "High"
    print("\n---------------------------------------------------------\n")
    print("BINANCE BOT 9000: Crypto Trader Python Script")
    print("\n---------------------------------------------------------\n")
      
    #Define active symbol on first run
    symbol = last_active_symbol[0]
    
    #Main program Loop
    while 1:
        t = time.localtime()
        print("\nLocal Time: ",time.strftime("%H:%M:%S", t)) 
        
        #Update Auto Generated Watch List
        ## build_watch_list()
        print ("-------- Bot Watch List----------")
        prices = client.get_ticker()
        for price in prices:
           if price['symbol'].endswith('BTC') == True:
               #print(price)
               #print(price['symbol'], end ="  % Chg: ")
               #print(price['priceChangePercent'], end ="  Volume: ")
               #print(price['quoteVolume'])
               if float(price['priceChangePercent']) > 6 and float(price['quoteVolume']) > 600:
                   bot_watch_list.insert(0,price['symbol'])  
           if price['symbol'].endswith('ETH') == True:
               #print(price)
               #print(price['symbol'], end ="  % Chg: ")
               #print(price['priceChangePercent'], end ="  Volume: ")
               #print(price['quoteVolume'])
               if float(price['priceChangePercent']) > 5 and float(price['quoteVolume']) > 500:
                   eth_bot_watch_list.insert(0,price['symbol'])           
                   
        print(bot_watch_list) 
        print(eth_bot_watch_list)
    
        print ("######### WATCHLIST################")
        print ("Symbol=====Price=========RSI=======")
        
        #####################
        ##Use Bot Watch List
        watch_list=bot_watch_list
        
        ##Use ETH Watch List
        #watch_list=eth_watch_list
        ##Use ETH Bot Watch List
        #watch_list=eth_bot_watch_list
        
        #Query Watch List for Price and RSI
        for pair in watch_list:
            avg_price = client.get_avg_price(symbol=pair)
            #print(watch_list[pair])
            print(pair, end =":  ")
            print(avg_price['price'], end ="  ")
            rsi=(get_rsi(pair))
            #rsi_index = watch_list.index(pair)
            rsi_index = watch_list.index(pair)
            rsi_value = (rsi['value'])
            rsi_list.insert(rsi_index, rsi_value)  
            #print(rsi_list[rsi_index])
            print(rsi_value)     
        #print(rsi_list)      
        print("#######################################")
              
        #Find lowest RSI from watch list and index     
        min_rsi = min(rsi_list)
        min_rsi_index = rsi_list.index(min(rsi_list))
        min_rsi_symbol = watch_list[min_rsi_index]
        print("Min RSI Symbol: ", min_rsi_symbol)
        print("Min RSI: ", min_rsi)
        print("Min RSI Index: ",min_rsi_index)
        #min_rsi_index = rsi_list.index(min(rsi_list))
        #print(min_rsi)
        #print(watch_list[min_rsi_index])
        
        #Trading Logic     
        if inOrder == True: 
            #symbol = list_of_symbols[0] 
            print("\nActive Order", symbol)
            rsi=(get_rsi(symbol))
            rsi_value = (rsi['value'])
            print(rsi_value)
            #print(symbol)
            if rsi_value > 70:
                order_amount = int(check_balance(symbol))
                #print(order_amount)
                #market_sell(symbol, 1347)
                market_sell(symbol, order_amount)
                print("Sell Order Triggered!! (RSI > 70) ")
                print("Symbol: ",symbol)
                print("Amount: ",order_amount)       
                inOrder= False
            elif rsi_value < 30:
                print("RSI Buying Opportunity (RSI < 30), but we are already in Order")
            else: 
                print("RSI value under sell threshold (RSI < 70)")
            print("---------------------------------")    
        else:
            print("No Order. Looking for Buying Opportunity")
            #check is lowest RSI is under threshold. If so, create Buy Order
            if min_rsi < 30:
                symbol = watch_list[min_rsi_index]
                order_amount = calculate_order(symbol)
                #market_buy(symbol, 1513)
                market_buy(symbol, order_amount)
                print("Buy Order Triggered!! (RSI < 30)")
                print("Symbol: ",symbol)
                print("Amount: ",order_amount) 
                inOrder= True
            #elif rsi_value > 70:
            #    print("RSI Selling Opportunity (RSI < 70), but we don't have an Order yet")
            else: 
                print("RSI values over buy threshold (RSI > 30)")
            print("---------------------------------")   
        
        #clear list
        rsi_list.clear()
        bot_watch_list.clear()
        eth_bot_watch_list.clear()
        #Wait for 5 minutes
        sleep(300)   

                
def get_rsi(symbol):  
    #convert binance symbol to taapi.io format with forward slash,COIN/MARKET. ie. ETHBTC >> ETH/BTC
    if len(symbol)>6:
        taapi_symbol = symbol[:4]+'/'+symbol[4:]
    else:
        taapi_symbol = symbol[:3]+'/'+symbol[3:]   
    #print(taapi_symbol)
    #Send get request and save the response as response object 
    parameters['symbol'] = taapi_symbol
    response = requests.get(url = endpoint, params = parameters)
    # Extract data, convert into json format 
    result = response.json()
    return result

def calculate_order(order_symbol):
    #Check Available BTC Balance
    balance = client.get_asset_balance(asset='BTC')
    btc_available = balance['free']
    #print("$$$$$$$$$$$")
    print("BTC Balance: ",btc_available)
    #Get price for symbol to trade
    avg_price = client.get_avg_price(symbol=order_symbol)
    order_symbol_price = avg_price['price']
    order_amount = (float(btc_available) / float(order_symbol_price))
    order_amount = int(order_amount)
    #print(order_symbol,end =" Price: ")
    #print(order_symbol_price)
    #print(order_amount)
    #print("$$$$$$$$$$$")
    return order_amount

def check_balance(order_symbol):
    asset_symbol = order_symbol[:-3]
    balance = client.get_asset_balance(asset=asset_symbol)
    trade_balance = float(balance['free'])
    #balance = int(balance)
    return trade_balance

def convert_time_binance(gt):
    #Converts from Binance Time Format (milliseconds) to time-struct
    #From Binance-Trader Comment Section Code
    #gt = client.get_server_time()
    print("Binance Time: ", gt)
    print(time.localtime())
    aa = str(gt)
    bb = aa.replace("{'serverTime': ","")
    aa = bb.replace("}","")
    gg=int(aa)
    ff=gg-10799260
    uu=ff/1000
    yy=int(uu)
    tt=time.localtime(yy)
    #print(tt)
    return tt

def market_buy(pair, amount):
    order = client.order_market_buy(
        symbol=pair,
        quantity=amount)
    
def market_sell(pair, amount):
    order = client.order_market_sell(
        symbol=pair,
        quantity=amount)


if __name__ == "__main__":
    run()