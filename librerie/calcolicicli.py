#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime as dt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import ffn
import librerie.importazioni as imp


pd.options.display.max_rows = 99999


# In[ ]:


def swing_HILO(path,start,stop,soglia,nome,out):#file di input deve essere un output di mt5
    """
    path = nome o percorso file origine
    start = data inizio 'AAAA-MM-GG'
    start = data fine 'AAAA-MM-GG'
    soglia = differenza minima tra un max e minimo in pt
    nome = str-> nome file di output
    out = bool -> True crea un file di output .csv, false no
    """
    #definizione df
    df=imp.import_mt5(path)
    df=df[start:stop]
    df['midprice']=(df.high+df.low+df.open+df.close)/4
        
    #loop indice    
    indicenum=[]
    i = 0
    n = len(df)
    while i < n:
        indicenum.append(i)
        i += 1
       
    df['data2']=df.index     
    df['indice']=indicenum
    df.set_index('indice',inplace=True)
    df['indice2']=df.index
#pulizia df
    df.drop(['open','high','low','close'],axis=1,inplace=True)

#inizializzazione loop
    swing_hilo=[0]
    data_hilo=[0]
    i = 3
    n = len(df)
    if df[(df.index==1)].midprice.sum()<df[(df.index==2)].midprice.sum():
        minimo=df[(df.index==1)].midprice.sum()
        massimo=df[(df.index==2)].midprice.sum()
        pmax=df[(df.midprice==massimo)].indice2.sum()
        pmin=df[(df.midprice==minimo)].indice2.sum()
    elif df[(df.index==1)].midprice.sum()>df[(df.index==2)].midprice.sum():
        minimo=df[(df.index==2)].midprice.sum()
        massimo=df[(df.index==1)].midprice.sum()
        pmin=df[(df.midprice==massimo)].indice2.sum()
        pmax=df[(df.midprice==minimo)].indice2.sum()
    else:
        minimo=df[(df.index==1)].midprice.sum()
        massimo=df[(df.index==2)].midprice.sum()
        pmin=1
        pmax=2

#loop individuazione max e min relativi
    while i < n:
        if pmax>pmin:#massimi crescenti 
            if df[(df.index==i)].midprice.sum()>=massimo:
                swing_hilo.pop()
                data_hilo.pop()
                massimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(massimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmax=i
            elif df[(df.index==i)].midprice.sum()<massimo-soglia:
                minimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(minimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmin=i
        elif pmax<pmin:#minimi decrescenti
            if df[(df.index==i)].midprice.sum()<=minimo:
                minimoold=minimo
                swing_hilo.pop()
                data_hilo.pop()
                minimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(minimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmin=i
            elif df[(df.index==i)].midprice.sum()>minimo+soglia:
                massimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(massimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmax=i
        i += 1
#creazione df dei soli swing        
    swing_HILO=pd.DataFrame(swing_hilo)
    swing_HILO.columns=[('maxmin')]
    swing_HILO['data']=data_hilo
#calcolo delle differenze tra i punti di swing
    differenze=[0]
    i=1
    n=len(swing_HILO)
    while i < n:
        differenza=(swing_HILO[(swing_HILO.index==i)].maxmin.sum())-(swing_HILO[(swing_HILO.index==i-1)].maxmin.sum())
        differenze.append(differenza)
        i+=1
 
    swing_HILO['differenze']=differenze
    
#calcolo delle differenze tra i punti di swing in minuti 
    swing_HILO['data1']=swing_HILO.data.shift(-1)
    swing_HILO.data1=pd.to_datetime(swing_HILO.data1)
    swing_HILO.dropna(axis=0,inplace=True)
    durata=[]
    i=0
    n=len(swing_HILO)
    while i<n:
        a=str(swing_HILO[(swing_HILO.index==i)].data.min())
        b=str(swing_HILO[(swing_HILO.index==i)].data1.min())
        start = dt.datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
        end = dt.datetime.strptime(b, "%Y-%m-%d %H:%M:%S")
        differenzat=end-start
        minuti=int((differenzat.total_seconds() // 60))
        durata.append(minuti)
        i+=1
    swing_HILO['durata']=durata
    swing_HILO['durata']=swing_HILO.durata.shift(1)
    swing_HILO.drop(['data1'], axis=1,inplace=True)
    
    swing_HILO.set_index('data', inplace=True)
    swing_HILO.index = pd.to_datetime(swing_HILO.index)
#output
    outputfile=out
    if outputfile==True:
        swing_HILO.to_csv(nome+'.csv', index=True)
    return swing_HILO


##########


def swing_HILOperc(path,start,stop,sogliaperc,nome,out):#file di input deve essere un output di mt5
    """
    path = nome o percorso file origine
    start = data inizio 'AAAA-MM-GG'
    start = data fine 'AAAA-MM-GG'
    sogliaperc = differenza minima tra un max e minimo in perc (0.01 = 1%)
    nome = str-> nome file di output
    out = bool -> True crea un file di output .csv, false no
    """
    #definizione df
    df=imp.import_mt5(path)
    df=df[start:stop]
    df['midprice']=(df.high+df.low+df.open+df.close)/4
        
    #loop indice    
    indicenum=[]
    i = 0
    n = len(df)
    while i < n:
        indicenum.append(i)
        i += 1
       
    df['data2']=df.index     
    df['indice']=indicenum
    df.set_index('indice',inplace=True)
    df['indice2']=df.index
#pulizia df
    df.drop(['high','low','close'],axis=1,inplace=True)

#inizializzazione loop
    swing_hilo=[0]
    data_hilo=[0]
    i = 3
    n = len(df)
    if df[(df.index==1)].midprice.sum()<df[(df.index==2)].midprice.sum():
        minimo=df[(df.index==1)].midprice.sum()
        massimo=df[(df.index==2)].midprice.sum()
        pmax=df[(df.midprice==massimo)].indice2.sum()
        pmin=df[(df.midprice==minimo)].indice2.sum()
    elif df[(df.index==1)].midprice.sum()>df[(df.index==2)].midprice.sum():
        minimo=df[(df.index==2)].midprice.sum()
        massimo=df[(df.index==1)].midprice.sum()
        pmin=df[(df.midprice==massimo)].indice2.sum()
        pmax=df[(df.midprice==minimo)].indice2.sum()
    else:
        minimo=df[(df.index==1)].midprice.sum()
        massimo=df[(df.index==2)].midprice.sum()
        pmin=1
        pmax=2

#loop individuazione max e min relativi
    while i < n:
        valoreindice=df[(df.index==i)].open.sum()
        soglia=sogliaperc*valoreindice
        if pmax>pmin:#massimi crescenti 
            if df[(df.index==i)].midprice.sum()>=massimo:
                swing_hilo.pop()
                data_hilo.pop()
                massimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(massimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmax=i
            elif df[(df.index==i)].midprice.sum()<massimo-soglia:
                minimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(minimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmin=i
        elif pmax<pmin:#minimi decrescenti
            if df[(df.index==i)].midprice.sum()<=minimo:
                minimoold=minimo
                swing_hilo.pop()
                data_hilo.pop()
                minimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(minimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmin=i
            elif df[(df.index==i)].midprice.sum()>minimo+soglia:
                massimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(massimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmax=i
        i += 1
      

 #creazione df dei soli swing        
    swing_HILO=pd.DataFrame(swing_hilo)
    swing_HILO.columns=[('maxmin')]
    swing_HILO['data']=data_hilo
#calcolo delle differenze tra i punti di swing
    differenze=[0]
    i=1
    n=len(swing_HILO)
    while i < n:
        differenza=(swing_HILO[(swing_HILO.index==i)].maxmin.sum())-(swing_HILO[(swing_HILO.index==i-1)].maxmin.sum())
        differenze.append(differenza)
        i+=1
 
    swing_HILO['differenze']=differenze
    
#calcolo delle differenze tra i punti di swing in minuti 
    swing_HILO['data1']=swing_HILO.data.shift(-1)
    swing_HILO.data1=pd.to_datetime(swing_HILO.data1)
    swing_HILO.dropna(axis=0,inplace=True)
    durata=[]
    i=0
    n=len(swing_HILO)
    while i<n:
        a=str(swing_HILO[(swing_HILO.index==i)].data.min())
        b=str(swing_HILO[(swing_HILO.index==i)].data1.min())
        start = dt.datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
        end = dt.datetime.strptime(b, "%Y-%m-%d %H:%M:%S")
        differenzat=end-start
        minuti=int((differenzat.total_seconds() // 60))
        durata.append(minuti)
        i+=1
    swing_HILO['durata']=durata
    swing_HILO['durata']=swing_HILO.durata.shift(1)
    swing_HILO.drop(['data1'], axis=1,inplace=True)
    
    swing_HILO.set_index('data', inplace=True)
    swing_HILO.index = pd.to_datetime(swing_HILO.index)
#output
    outputfile=out
    if outputfile==True:
        swing_HILO.to_csv(nome+'.csv', index=True)
    return swing_HILO

################
def swing_HILOvol(path,start,stop,soglia,nome,out):#file di input deve essere un output di mt5
    """
    path = nome o percorso file origine
    start = data inizio 'AAAA-MM-GG'
    start = data fine 'AAAA-MM-GG'
    soglia = differenza minima tra un max e minimo in pt
    nome = str-> nome file di output
    out = bool -> True crea un file di output .csv, false no
    """
    #definizione df
    df=imp.import_mt5(path)
    df=df[start:stop]
    df['midprice']=(df.high+df.low+df.open+df.close)/4
        
    #loop indice    
    indicenum=[]
    i = 0
    n = len(df)
    while i < n:
        indicenum.append(i)
        i += 1
       
    df['data2']=df.index     
    df['indice']=indicenum
    df.set_index('indice',inplace=True)
    df['indice2']=df.index
    df['volume']=df.volume.cumsum()
#pulizia df
    df.drop(['open','high','low','close'],axis=1,inplace=True)

#inizializzazione loop
    swing_hilo=[0]
    data_hilo=[0]
    volume_hilo=[0]
    i = 3
    n = len(df)
    if df[(df.index==1)].midprice.sum()<df[(df.index==2)].midprice.sum():
        minimo=df[(df.index==1)].midprice.sum()
        massimo=df[(df.index==2)].midprice.sum()
        pmax=df[(df.midprice==massimo)].indice2.sum()
        pmin=df[(df.midprice==minimo)].indice2.sum()
    elif df[(df.index==1)].midprice.sum()>df[(df.index==2)].midprice.sum():
        minimo=df[(df.index==2)].midprice.sum()
        massimo=df[(df.index==1)].midprice.sum()
        pmin=df[(df.midprice==massimo)].indice2.sum()
        pmax=df[(df.midprice==minimo)].indice2.sum()
    else:
        minimo=df[(df.index==1)].midprice.sum()
        massimo=df[(df.index==2)].midprice.sum()
        pmin=1
        pmax=2

#loop individuazione max e min relativi
    while i < n:
        if pmax>pmin:#massimi crescenti 
            if df[(df.index==i)].midprice.sum()>=massimo:
                swing_hilo.pop()
                data_hilo.pop()
                volume_hilo.pop()
                massimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(massimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                volume_hilo.append(df[(df.index==i)].volume.min())
                pmax=i
            elif df[(df.index==i)].midprice.sum()<massimo-soglia:
                minimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(minimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                volume_hilo.append(df[(df.index==i)].volume.min())
                pmin=i
        elif pmax<pmin:#minimi decrescenti
            if df[(df.index==i)].midprice.sum()<=minimo:
                minimoold=minimo
                swing_hilo.pop()
                data_hilo.pop()
                volume_hilo.pop()
                minimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(minimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                volume_hilo.append(df[(df.index==i)].volume.sum())
                pmin=i
            elif df[(df.index==i)].midprice.sum()>minimo+soglia:
                massimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(massimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                volume_hilo.append(df[(df.index==i)].volume.sum())
                pmax=i
        i += 1
#creazione df dei soli swing        
    swing_HILO=pd.DataFrame(swing_hilo)
    swing_HILO.columns=[('maxmin')]
    swing_HILO['data']=data_hilo
    swing_HILO['volume']=volume_hilo
    
#calcolo delle differenze tra i punti di swing
    differenze=[0]
    i=1
    n=len(swing_HILO)
    while i < n:
        differenza=(swing_HILO[(swing_HILO.index==i)].maxmin.sum())-(swing_HILO[(swing_HILO.index==i-1)].maxmin.sum())
        differenze.append(differenza)
        i+=1
    swing_HILO['diff_pt']=differenze
    
#calcolo delle differenze tra i punti di swing in minuti 
    swing_HILO['data1']=swing_HILO.data.shift(-1)
    swing_HILO.data1=pd.to_datetime(swing_HILO.data1)
    swing_HILO.dropna(axis=0,inplace=True)
    durata=[]
    i=0
    n=len(swing_HILO)
    while i<n:
        a=str(swing_HILO[(swing_HILO.index==i)].data.min())
        b=str(swing_HILO[(swing_HILO.index==i)].data1.min())
        start = dt.datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
        end = dt.datetime.strptime(b, "%Y-%m-%d %H:%M:%S")
        differenzat=end-start
        minuti=int((differenzat.total_seconds() // 60))
        durata.append(minuti)
        i+=1
    swing_HILO['durata']=durata
    swing_HILO['durata']=swing_HILO.durata.shift(1)
    swing_HILO.drop(['data1'], axis=1,inplace=True)

#calcolo delle differenze tra i volumi
    differenzevol=[0]
    i=1
    n=len(swing_HILO)
    while i < n:
        differenzavol=(swing_HILO[(swing_HILO.index==i)].volume.sum())-(swing_HILO[(swing_HILO.index==i-1)].volume.sum())
        differenzevol.append(differenzavol)
        i+=1
    swing_HILO['volumiswing']=differenzevol
    #swing_HILO.drop(['volume'], axis=1,inplace=True)
    swing_HILO.set_index('data', inplace=True)
    swing_HILO.index = pd.to_datetime(swing_HILO.index)
#output
    outputfile=out
    if outputfile==True:
        swing_HILO.to_csv(nome+'.csv', index=True)
    return swing_HILO


##########
def swing_HILOpercvol(path,start,stop,sogliaperc,nome,out):#file di input deve essere un output di mt5
    """
    path = nome o percorso file origine
    start = data inizio 'AAAA-MM-GG'
    start = data fine 'AAAA-MM-GG'
    sogliaperc = differenza minima tra un max e minimo in pt
    nome = str-> nome file di output
    out = bool -> True crea un file di output .csv, false no
    """
    #definizione df
    df=imp.import_mt5(path)
    df=df[start:stop]
    df['midprice']=(df.high+df.low+df.open+df.close)/4
        
    #loop indice    
    indicenum=[]
    i = 0
    n = len(df)
    while i < n:
        indicenum.append(i)
        i += 1
       
    df['data2']=df.index     
    df['indice']=indicenum
    df.set_index('indice',inplace=True)
    df['indice2']=df.index
    df['volume']=df.volume.cumsum()
#pulizia df
    df.drop(['high','low','close'],axis=1,inplace=True)

#inizializzazione loop
    swing_hilo=[0]
    data_hilo=[0]
    volume_hilo=[0]
    i = 3
    n = len(df)
    if df[(df.index==1)].midprice.sum()<df[(df.index==2)].midprice.sum():
        minimo=df[(df.index==1)].midprice.sum()
        massimo=df[(df.index==2)].midprice.sum()
        pmax=df[(df.midprice==massimo)].indice2.sum()
        pmin=df[(df.midprice==minimo)].indice2.sum()
    elif df[(df.index==1)].midprice.sum()>df[(df.index==2)].midprice.sum():
        minimo=df[(df.index==2)].midprice.sum()
        massimo=df[(df.index==1)].midprice.sum()
        pmin=df[(df.midprice==massimo)].indice2.sum()
        pmax=df[(df.midprice==minimo)].indice2.sum()
    else:
        minimo=df[(df.index==1)].midprice.sum()
        massimo=df[(df.index==2)].midprice.sum()
        pmin=1
        pmax=2

#loop individuazione max e min relativi
    while i < n:
        valoreindice=df[(df.index==i)].open.sum()
        soglia=sogliaperc*valoreindice
        if pmax>pmin:#massimi crescenti 
            if df[(df.index==i)].midprice.sum()>=massimo:
                swing_hilo.pop()
                data_hilo.pop()
                volume_hilo.pop()
                massimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(massimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                volume_hilo.append(df[(df.index==i)].volume.min())
                pmax=i
            elif df[(df.index==i)].midprice.sum()<massimo-soglia:
                minimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(minimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                volume_hilo.append(df[(df.index==i)].volume.min())
                pmin=i
        elif pmax<pmin:#minimi decrescenti
            if df[(df.index==i)].midprice.sum()<=minimo:
                minimoold=minimo
                swing_hilo.pop()
                data_hilo.pop()
                volume_hilo.pop()
                minimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(minimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                volume_hilo.append(df[(df.index==i)].volume.sum())
                pmin=i
            elif df[(df.index==i)].midprice.sum()>minimo+soglia:
                massimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(massimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                volume_hilo.append(df[(df.index==i)].volume.sum())
                pmax=i
        i += 1
#creazione df dei soli swing        
    swing_HILO=pd.DataFrame(swing_hilo)
    swing_HILO.columns=[('maxmin')]
    swing_HILO['data']=data_hilo
    swing_HILO['volume']=volume_hilo
    
#calcolo delle differenze tra i punti di swing
    differenze=[0]
    i=1
    n=len(swing_HILO)
    while i < n:
        differenza=(swing_HILO[(swing_HILO.index==i)].maxmin.sum())-(swing_HILO[(swing_HILO.index==i-1)].maxmin.sum())
        differenze.append(differenza)
        i+=1
    swing_HILO['diff_pt']=differenze
    
#calcolo delle differenze tra i punti di swing in minuti 
    swing_HILO['data1']=swing_HILO.data.shift(-1)
    swing_HILO.data1=pd.to_datetime(swing_HILO.data1)
    swing_HILO.dropna(axis=0,inplace=True)
    durata=[]
    i=0
    n=len(swing_HILO)
    while i<n:
        a=str(swing_HILO[(swing_HILO.index==i)].data.min())
        b=str(swing_HILO[(swing_HILO.index==i)].data1.min())
        start = dt.datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
        end = dt.datetime.strptime(b, "%Y-%m-%d %H:%M:%S")
        differenzat=end-start
        minuti=int((differenzat.total_seconds() // 60))
        durata.append(minuti)
        i+=1
    swing_HILO['durata']=durata
    swing_HILO['durata']=swing_HILO.durata.shift(1)
    swing_HILO.drop(['data1'], axis=1,inplace=True)

#calcolo delle differenze tra i volumi
    differenzevol=[0]
    i=1
    n=len(swing_HILO)
    while i < n:
        differenzavol=(swing_HILO[(swing_HILO.index==i)].volume.sum())-(swing_HILO[(swing_HILO.index==i-1)].volume.sum())
        differenzevol.append(differenzavol)
        i+=1
    swing_HILO['volumiswing']=differenzevol
    #swing_HILO.drop(['volume'], axis=1,inplace=True)
    swing_HILO.set_index('data', inplace=True)
    swing_HILO.index = pd.to_datetime(swing_HILO.index)
#output
    outputfile=out
    if outputfile==True:
        swing_HILO.to_csv(nome+'.csv', index=True)
    return swing_HILO



def swing_HILOperc2(path,start,stop,sogliaperc,nome,out):#file di input deve essere un output di mt5
    """
    path = nome o percorso file origine
    start = data inizio 'AAAA-MM-GG'
    start = data fine 'AAAA-MM-GG'
    sogliaperc = differenza minima tra un max e minimo in perc (0.01 = 1%)
    nome = str-> nome file di output
    out = bool -> True crea un file di output .csv, false no
    """
    #definizione df
    df=imp.import_mt5(path)
    df=df[start:stop]
    df['midprice']=(df.high+df.low+df.open+df.close)/4
        
    #loop indice    
    indicenum=[]
    i = 0
    n = len(df)
    while i < n:
        indicenum.append(i)
        i += 1
       
    df['data2']=df.index     
    df['indice']=indicenum
    df.set_index('indice',inplace=True)
    df['indice2']=df.index
#pulizia df
    df.drop(['high','low','close'],axis=1,inplace=True)

#inizializzazione loop
    swing_hilo=[0]
    data_hilo=[0]
    i = 3
    n = len(df)
    if df[(df.index==1)].midprice.sum()<df[(df.index==2)].midprice.sum():
        minimo=df[(df.index==1)].midprice.sum()
        massimo=df[(df.index==2)].midprice.sum()
        pmax=df[(df.midprice==massimo)].indice2.sum()
        pmin=df[(df.midprice==minimo)].indice2.sum()
    elif df[(df.index==1)].midprice.sum()>df[(df.index==2)].midprice.sum():
        minimo=df[(df.index==2)].midprice.sum()
        massimo=df[(df.index==1)].midprice.sum()
        pmin=df[(df.midprice==massimo)].indice2.sum()
        pmax=df[(df.midprice==minimo)].indice2.sum()
    else:
        minimo=df[(df.index==1)].midprice.sum()
        massimo=df[(df.index==2)].midprice.sum()
        pmin=1
        pmax=2

#loop individuazione max e min relativi
    while i < n:
        valoreindice=df[(df.index==i)].open.sum()
        soglia=sogliaperc*valoreindice
        if pmax>pmin:#massimi crescenti 
            if df[(df.index==i)].midprice.sum()>=massimo:
                swing_hilo.pop()
                data_hilo.pop()
                massimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(massimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmax=i
            elif df[(df.index==i)].midprice.sum()<massimo-soglia:
                minimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(minimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmin=i
        elif pmax<pmin:#minimi decrescenti
            if df[(df.index==i)].midprice.sum()<=minimo:
                minimoold=minimo
                swing_hilo.pop()
                data_hilo.pop()
                minimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(minimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmin=i
            elif df[(df.index==i)].midprice.sum()>minimo+soglia:
                massimo=df[(df.index==i)].midprice.sum()
                swing_hilo.append(massimo)
                data_hilo.append(df[(df.index==i)].data2.min())
                pmax=i
        i += 1
      

 #creazione df dei soli swing        
    swing_HILO=pd.DataFrame(swing_hilo)
    swing_HILO.columns=[('maxmin')]
    swing_HILO['data']=data_hilo
#calcolo delle differenze tra i punti di swing
    differenze=[0]
    i=1
    n=len(swing_HILO)
    while i < n:
        differenza=(swing_HILO[(swing_HILO.index==i)].maxmin.sum())-(swing_HILO[(swing_HILO.index==i-1)].maxmin.sum())
        differenze.append(differenza)
        i+=1
 
    swing_HILO['differenze']=differenze

#output
    outputfile=out
    if outputfile==True:
        swing_HILO.to_csv(nome+'.csv', index=True)
    return swing_HILO

##########

