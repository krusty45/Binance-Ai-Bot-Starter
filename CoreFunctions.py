"""
@author: Harnick Khera (Github.com/Hephyrius)

Use this class as your pipeline, use it for all of your data manipulation/feature creation functionality.

Functions here are used across the bot and training classes!

"""
from binance.client import Client
import pandas as pd 
import numpy as np

#Get the balance of a specified coin
def getCoinBalance(client, currency):
    balance = float(client.get_asset_balance(asset=currency)['free'])
    return balance

#Market buy
def executeBuy(client, market, qtyBuy):
    
    order = client.order_market_buy(symbol=market,quantity=qtyBuy)

#Market sell
def executeSell(client, market, qtySell):

    order = client.order_market_sell(symbol=market, quantity=qtySell)

#format the data correctly for later use
def CreateOpenHighLowCloseVolumeData(indata):
    
    out = pd.DataFrame()
    
    d = []
    o = []
    h = []
    l = []
    c = []
    v = []
    for i in indata:
        #print(i)
        d.append(float(i[0]))
        o.append(float(i[1]))
        h.append(float(i[2]))
        c.append(float(i[3]))
        l.append(float(i[4]))
        v.append(float(i[5]))

    out['date'] = d
    out['open'] = o
    out['high'] = h
    out['low'] = l
    out['close'] = c
    out['volume'] = v
    
    #print(out)
    
    return out

#Create targets for our machine learning model. This is done by predicting if the closing price of the next candle will 
#be higher or lower than the current one.
def CreateTargets(data, offset):
    
    y = []
    
    
    for i in range(0, len(data)-offset):
        current = float(data[i][3])
        comparison = float(data[i+offset][3])
        
        if current<comparison:
            y.append(1)

        elif current>=comparison:
            y.append(0)
            
    return y
    
#Calculate the change in the values of a column
def GetChangeData(x):

    cols = x.columns
    
    for i in cols:
        j = "c_" + i
        
        try:
            dif = x[i].diff()
            x[j] = dif
        except Exception as e:
            print(e)
        
#Calculate the percentage change between this bar and the previoud x bars
def ChangeTime(x, step):
    
    out = []
    
    for i in range(len(x)):
        try:
            a = x[i]
            b = x[i-step]
            
            change = (1 - b/a) 
            out.append(change)
        except Exception as e:
            out.append(0)
    
    return out

#Automate the creation of percentage changes for 48 candles.  
def StepData(x, data):
    
    for i in range(1,48):
        
        data[str(i)+"StepDifference"] = ChangeTime(x, i)


    
    