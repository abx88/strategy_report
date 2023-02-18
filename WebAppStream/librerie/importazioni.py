#!/usr/bin/env python
# coding: utf-8

# In[1]:
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import ffn



#acquisizione dati serie storica

def import_intradaymt5(path):
    """
    Funzione per il caricamento di uno storico intraday da MT5 
    Fonte dati: xxxx.csv
    """
    df = pd.read_csv(path, delimiter="\t")
    df['date_time']= df['<DATE>'] + ' ' + df['<TIME>']
    df.drop(['<DATE>','<TIME>','<TICKVOL>','<SPREAD>'], axis=1,inplace=True)
    df.set_index('date_time', inplace=True)
    df.index = pd.to_datetime(df.index)#occorre per convertire in datetime la data
    df.columns=['open','high','low','close','volume']
    df["dayofweek"] = df.index.dayofweek
    df["day"] = df.index.day
    df["month"] = df.index.month
    df["year"] = df.index.year
    df["dayofyear"] = df.index.dayofyear
    df["quarter"] = df.index.quarter
    df["hour"] = df.index.hour
    df["minute"] = df.index.minute
    df["daily_high1"] = df.high.resample("D").max().shift(1)
    df["daily_high1"] = df["daily_high1"].fillna(method = 'ffill')
    df["daily_low1"] = df.low.resample("D").min().shift(1)
    df["daily_low1"] = df["daily_low1"].fillna(method = 'ffill')
    df["daily_open1"] = df.open.resample("D").first().shift(1)
    df["daily_open1"] = df["daily_open1"].fillna(method = 'ffill')
    df["daily_close1"] = df.close.resample("D").last().shift(1)
    df["daily_close1"] = df["daily_close1"].fillna(method = 'ffill')
    return df

def import_daymt5(path):
    """
    Funzione per il caricamento di uno storico D/W/M da MT5 
    Fonte dati: xxxx.csv
    """
    df = pd.read_csv(path, delimiter="\t")
    df['date_time']= df['<DATE>']
    df.drop(['<DATE>','<TICKVOL>','<SPREAD>'], axis=1,inplace=True)
    df.set_index('date_time', inplace=True)
    df.index = pd.to_datetime(df.index)#occorre per convertire in datetime la data
    df.columns=['open','high','low','close','volume']
    df["dayofweek"] = df.index.dayofweek
    df["day"] = df.index.day
    df["month"] = df.index.month
    df["year"] = df.index.year
    df["dayofyear"] = df.index.dayofyear
    df["quarter"] = df.index.quarter
    return df

def import_mt5(path):
    """
    Funzione per il caricamento generico di uno storico intraday da MT5 restituisce solo i campi 'open','high','low','close','volume'
    Fonte dati: xxxx.csv
    """
    
    df = pd.read_csv(path, delimiter="\t")
    df['date_time']= df['<DATE>'] + ' ' + df['<TIME>']
    df.drop(['<DATE>','<TIME>','<TICKVOL>','<SPREAD>'], axis=1,inplace=True)
    df.set_index('date_time', inplace=True)
    df.index = pd.to_datetime(df.index)#occorre per convertire in datetime la data
    df.columns=['open','high','low','close','volume']
    return df


def import_mt4(path):
    """
    Funzione per il caricamento generico di uno storico intraday da MT4 restituisce solo i campi 'open','high','low','close','volume'
    Fonte dati: xxxx.csv
    Date,Time,Open,High,Low,Close,Volume
    """
    
    df = pd.read_csv(path, delimiter=",")
    df['date_time']= df['Date'] + ' ' + df['Time']
    df.drop(['Date','Time'], axis=1,inplace=True)
    df.set_index('date_time', inplace=True)
    df.index = pd.to_datetime(df.index)#occorre per convertire in datetime la data
    df.columns=['open','high','low','close','volume']
    return df



def import_internetfiles(path):
    """
    Funzione per il caricamento di uno storico da sito web EA studio
    """
    df = pd.read_csv(path, delimiter="\t", parse_dates=['Time'], index_col='Time')
    df.columns=['open','high','low','close','volume']
    return df


def import_data_dailyTS(filename):
    """
    Funzione per il caricamento di uno storico daily
    Fonte dati: Tradestation .txt
    """
    data = pd.read_csv(filename, parse_dates = ["Date","Time"])
    data.columns = ["date","time","open","high","low","close","volume","oi"]
    data.set_index("date", inplace = True)
    data.drop(["time","oi"], axis=1, inplace=True)
    data["dayofweek"] = data.index.dayofweek
    data["day"] = data.index.day
    data["month"] = data.index.month
    data["year"] = data.index.year
    data["dayofyear"] = data.index.dayofyear
    data["quarter"] = data.index.quarter
    return data

def import_data_intradayTS(filename):
    """
    Funzione per il parsing di una serie intraday 
    con estensione txt esportata da Tradestation
    """
    df = pd.read_csv(filename, 
                       usecols=['Date','Time','Open','High','Low','Close','Up','Down'], 
                       parse_dates=[['Date', 'Time']], )
    df.columns = ["date_time","open","high","low","close","up","down"]
    df.set_index('date_time', inplace = True)
    df['volume'] = df['up'] + df['down']
    df.drop(['up','down'],axis=1,inplace=True)
    df["dayofweek"] = df.index.dayofweek
    df["day"] = df.index.day
    df["month"] = df.index.month
    df["year"] = df.index.year
    df["dayofyear"] = df.index.dayofyear
    df["quarter"] = df.index.quarter
    df["hour"] = df.index.hour
    df["minute"] = df.index.minute
    df["daily_high1"] = df.high.resample("D").max().shift(1)
    df["daily_high1"] = df["daily_high1"].fillna(method = 'ffill')
    df["daily_low1"] = df.low.resample("D").min().shift(1)
    df["daily_low1"] = df["daily_low1"].fillna(method = 'ffill')
    df["daily_open1"] = df.open.resample("D").first().shift(1)
    df["daily_open1"] = df["daily_open1"].fillna(method = 'ffill')
    df["daily_close1"] = df.close.resample("D").last().shift(1)
    df["daily_close1"] = df["daily_close1"].fillna(method = 'ffill')
    return data
# In[ ]:

