#!/usr/bin/env python
# coding: utf-8

# In[1]:
import datetime
import numpy as np
import pandas as pd
#import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


def normalizeMinMax(array):
    """
    Funzione per normalizzare un array
    che porta a 0 il valore minimo
    e ad 1 il valore massimo
    (a[i] - min(a))/(max(a)-min(a)) 
    """
    normalized_array = []
    for elements in array:
        normalized_array.append((elements - min(array))/(max(array)-min(array)))
    return normalized_array

def normalizeMax(array):
    """
    Funzione per normalizzare un array
    che porta ad 1 il valore massimo
    a[i]/max(a)
    """
    normalized_array = []
    for elements in array:
        normalized_array.append(elements / max(array))
    return normalized_array

def normalizeMaxMin(array):
    """
    Funzione per normalizzare un array
    che porta ad 1 il valore massimo
    a[i]/max(a) e a -1 il valore minimo a[i]/min(a)
    Funzione che lascia lo zero invariato!
    """
    normalized_array = []
    
    for element in array:
        if element > 0:
            normalized_array.append(element / max(array))
        elif element<=0:
            normalized_array.append(-element / min(array))
        else:
            normalized_array.append(0)
    
    return normalized_array

def percPosNeg(array, soglia):
    """
    Funzione che restituisce le percentuali di valori 
    maggiori e minori di una soglia
    """
    if len(array) == 0:
        return 0,0
    contapos = 0
    contaneg = 0
    for el in array:
        if el > soglia:
            contapos+=1
        if el <= soglia:
            contaneg+=1
    return round(contapos/len(array)*100,2), round(contaneg/len(array)*100,2)


def occorrenzeorariecount(df_h, soglia):
    """
    funzione che raccoglie le occorrenze positive o negative bias orario 
    su intero df e la plotta su heatmap
    """
    ore = []
    for ora in range(0,24):
        ore.append(ora)
    
    body_statistics = [] 

    for ora in ore:
    
        if df_h[(df_h.HOD==ora)].body.count()!=0:
            if df_h[(df_h.HOD==ora)].body.mean() > 0:
                body_statistics.append(round(percPosNeg(df_h[(df_h.HOD==ora)]['body'],soglia)[0],2))
            if df_h[(df_h.HOD==ora)]['body'].mean() <= 0:
                body_statistics.append(round(percPosNeg(df_h[(df_h.HOD==ora)]['body'],-soglia)[1],2))
        else:
            body_statistics.append(0)
   
    return body_statistics

def occorrenzegiornocount(df_d, soglia):
    """
    funzione che raccoglie le occorrenze positive o negative bias orario 
    su intero df e la plotta su heatmap
    """
    giorni = []
    for giorno in range(0,4):
        giorni.append(giorno)
    
    body_statistics = [] 

    for giorno in giorni:
    
        if df_d[(df_d.DOW==giorno)].body.count()!=0:
            if df_d[(df_d.DOW==giorno)].body.mean() > 0:
                body_statistics.append(round(percPosNeg(df_d[(df_d.DOW==giorno)]['body'],soglia)[0],2))
            if df_d[(df_d.DOW==giorno)]['body'].mean() <= 0:
                body_statistics.append(round(percPosNeg(df_d[(df_d.DOW==giorno)]['body'],-soglia)[1],2))
        else:
            body_statistics.append(0)
   
    return body_statistics


def SMA(array, period):
    """
    Funzione che calcola la media mobile semplice di una serie
    """
    return array.rolling(period).mean()

def BollingerBand(array,period,k):
    """
    Funzione che calcola una Banda di Bollinger di una serie
    """
    BB = SMA(array,period) + k * array.rolling(period).std()
    return BB

def ExpandingMax(array):
    """
    Funzione che calcola il massimo assoluto in avanzamento della serie
    """
    return array.expanding().max()

def DonchianChannelUp(array,period):
    """
    Funzione che calcola il massimo dei massimi di una serie
    a finestra scorrevole
    """
    return array.rolling(period).max()

def DonchianChannelDown(array,period):
    """
    Funzione che calcola il massimo dei massimi di una serie
    a finestra scorrevole
    """
    return array.rolling(period).min()

# In[ ]: