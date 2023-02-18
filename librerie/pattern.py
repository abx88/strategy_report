#!/usr/bin/env python
# coding: utf-8

# In[7]:


import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import ffn
import librerie.importazioni as imp
import librerie.calcolivari as clc



# In[19]:


def pattern(path):
    df=imp.import_mt5(path)
    df['candela']=df.index.time
    df['range']=df.high-df.low
    df['mese']=df.index.month
    df['anno']=df.index.year
    #selezione ampiezza dataframe  
    #dfpars=df.loc["20180101":"20210530"]
    dfpars=df.loc[:]#usare se si vuole utilizzare intero df
    df_d=pd.DataFrame(df['open'].resample('D').first())
    df_d['high']=df['high'].resample('D').max()
    df_d['low']=df['low'].resample('D').min()
    df_d['close']=df['close'].resample('D').last()
    df_d['volume']=df['volume'].resample('D').sum()
    df_d['DOW']=df_d.index.dayofweek
    df_d['body']=abs(df_d.close-df_d.open)
    df_d['range']=(df_d.high-df_d.low)
    df_d['mese']=df_d.index.month
    df_d['anno']=df_d.index.year
    df_d.dropna(axis=0, inplace=True)

    #calcolo delle differenza fra open e low e open e high
    df_d['CO'] = round(df_d.close - df_d.open,2)
    df_d['CO1'] = df_d.CO.shift(-1)
    df_d['CO2'] = df_d.CO.shift(-2)
    df_d['OL']=round(df_d.open-df_d.low,5)
    df_d['HO']=round(df_d.high-df_d.open,5)
    df_d['CL']=round(df_d.close-df_d.low,5)
    df_d['HC']=round(df_d.high-df_d.close,5)
    df_d['BodyRangePerc'] = round(df_d.body/df_d.range * 100,2)
    # Percentuale della barra (all'interno del range) dove si attesta il close
    df_d['ClosePerc'] = round((df_d.close - df_d.low) * 100 / df_d.range,2)
    df_d['Color'] = list(map(lambda x: "black" if x <= 0 else "white", df_d.CO))
    #ulteriori campi
    df_d['PCTClose']=df_d.close.pct_change().dropna()*100
    df_d['NextClose']=df_d.close.pct_change().dropna()*100
    df_d['NextClose']=df_d.NextClose.shift(-1)
    df_d['NextClose2']=df_d.NextClose.shift(-1)
    df_d['ATR_l']=clc.SMA(df_d.range, 20)
    df_d['CLperc']=(round(df_d.close-df_d.low,2)/df_d.range)*100
    df_d['HCperc']=(round(df_d.high-df_d.close,2)/df_d.range)*100
    df_d['OLperc']=(round(df_d.open-df_d.low,2)/df_d.range)*100
    df_d['HOperc']=(round(df_d.high-df_d.open,2)/df_d.range)*100
    df_d['ATR']=clc.SMA(df_d.range, 10)
    df_d['ATR_s']=clc.SMA(df_d.range,5)
    #candela1 ribassista
    df_d['pat1']=np.where(((df_d.ClosePerc<40)&
                           (df_d.BodyRangePerc<100)&
                           (df_d.range>df_d.ATR)),1,0)
    #candela2 rialzista
    df_d['pat2']=np.where(((df_d.ClosePerc>60)&
                           (df_d.BodyRangePerc<100)&
                           (df_d.range>df_d.ATR)),1,0)
    #candela3 indecisione con volatilità 
    df_d['pat3']=np.where(((df_d.BodyRangePerc<50)&
                           (df_d.range>df_d.ATR)),1,0)
    #candela4 indecisione senza volatilità
    df_d['pat4']=np.where(((df_d.BodyRangePerc<50)&
                           (df_d.range<df_d.ATR)),1,0)
    #candela non volatile
    df_d['pat5']=np.where((df_d.range<df_d.ATR),1,0)

    #creazione dataframe filtrati
    df_dpA1=df_d.loc[(df_d.pat1==1)]#pattern di continuazione ribassista
    df_dpA2=df_d.loc[(df_d.pat1==1)&(df_d.PCTClose<-1)]#pattern di continuazione ribassista
    df_dpB1=df_d.loc[(df_d.pat2==1)]#pattern di continuazione rialzista
    df_dpB2=df_d.loc[(df_d.pat2==1)&(df_d.PCTClose>1)]#pattern di continuazione rialzista
    df_dpA3=df_d.loc[(df_d.pat1==1)&(df_d.pat1.shift(1)==1)]#pattern di continuazione ribassista
    df_dpB3=df_d.loc[(df_d.pat2==1)&(df_d.pat2.shift(1)==1)]#pattern di continuazione rialzista
    df_dpC=df_d.loc[(df_d.pat1==1)&(df_d.pat3.shift(1)==1)]#pattern di indecisione+break ribassista
    df_dpD=df_d.loc[(df_d.pat2==1)&(df_d.pat3.shift(1)==1)]#pattern di indecisione+break rialzista
    df_dpE=df_d.loc[(df_d.pat4==1)&(df_d.pat1.shift(1)==1)]#pattern di consolidamento ribassista
    df_dpF=df_d.loc[(df_d.pat3==1)&(df_d.pat1.shift(1)==1)]#pattern di consolidamento ribassista-2
    df_dpG=df_d.loc[(df_d.pat4==1)&(df_d.pat2.shift(1)==1)]#pattern di consolidamento rialzista
    df_dpH=df_d.loc[(df_d.pat3==1)&(df_d.pat2.shift(1)==1)]#pattern di consolidamento rialzista-2
    df_dpI=df_d.loc[(df_d.pat3==1)]#pattern indecisione
    df_dpJ=df_d.loc[(df_d.pat4==1)]#pattern indecisione-2
    df_dpK=df_d.loc[(df_d.pat5==1)]#pattern no vola
    df_dpL1=df_d.loc[(df_d.pat1==1)&(df_d.pat2.shift(1)==1)]#pattern inversione ribassista
    df_dpM1=df_d.loc[(df_d.pat2==1)&(df_d.pat1.shift(1)==1)]#pattern inversione rialzista
    df_dpL2=df_d.loc[(df_d.pat1==1)&(df_d.pat2.shift(1)==1)&(df_d.open.shift(1)>df_d.close)]#pattern inversione ribassista2
    df_dpM2=df_d.loc[(df_d.pat2==1)&(df_d.pat1.shift(1)==1)&(df_d.open.shift(1)<df_d.close)]#pattern inversione rialzista2
    #creazione pattern nel database daily
    df_d['date']=df_d.index.date
    df_d['patA1']=np.where((df_d.pat1==1),1,0)
    df_d['patA2']=np.where(((df_d.pat1==1)&(df_d.PCTClose<-1)),1,0)
    df_d['patA3']=np.where(((df_d.pat1==1)&(df_d.pat1.shift(1)==1)),1,0)
    df_d['patB1']=np.where((df_d.pat2==1),1,0)
    df_d['patB2']=np.where(((df_d.pat2==1)&(df_d.PCTClose>1)),1,0)
    df_d['patB3']=np.where(((df_d.pat2==1)&(df_d.pat2.shift(1)==1)),1,0)
    df_d['patC']=np.where(((df_d.pat1==1)&(df_d.pat3.shift(1)==1)),1,0)
    df_d['patD']=np.where(((df_d.pat2==1)&(df_d.pat3.shift(1)==1)),1,0)
    df_d['patE']=np.where(((df_d.pat4==1)&(df_d.pat1.shift(1)==1)),1,0)
    df_d['patF']=np.where(((df_d.pat3==1)&(df_d.pat1.shift(1)==1)),1,0)
    df_d['patG']=np.where(((df_d.pat4==1)&(df_d.pat2.shift(1)==1)),1,0)
    df_d['patH']=np.where(((df_d.pat3==1)&(df_d.pat2.shift(1)==1)),1,0)
    df_d['patI']=np.where((df_d.pat3==1),1,0)
    df_d['patJ']=np.where((df_d.pat4==1),1,0)
    df_d['patK']=np.where((df_d.pat5==1),1,0)
    df_d['patL1']=np.where(((df_d.pat1==1)&(df_d.pat2.shift(1)==1)),1,0)
    df_d['patM1']=np.where(((df_d.pat2==1)&(df_d.pat1.shift(1)==1)),1,0)
    df_d['patL2']=np.where(((df_d.pat1==1)&(df_d.pat2.shift(1)==1)&(df_d.open.shift(1)>df_d.close)),1,0)
    df_d['patM2']=np.where(((df_d.pat2==1)&(df_d.pat1.shift(1)==1)&(df_d.open.shift(1)<df_d.close)),1,0)
    df_d['max1']=np.where((df_d.high>df_d.high.shift(1)),1,0)
    df_d['max2']=np.where(((df_d.high>df_d.high.shift(1))&(df_d.max1.shift(1)==1)),1,0)
    df_d['max3']=np.where(((df_d.high>df_d.high.shift(1))&(df_d.max2.shift(1)==1)),1,0)
    df_d['min1']=np.where((df_d.low<df_d.low.shift(1)),1,0)
    df_d['min2']=np.where(((df_d.low<df_d.low.shift(1))&(df_d.min1.shift(1)==1)),1,0)
    df_d['min3']=np.where(((df_d.low<df_d.low.shift(1))&(df_d.min2.shift(1)==1)),1,0)
    df_d['closeperc']=df_d.ClosePerc
    
    return df_d

def pattern_dfts(path):
    df = imp.import_mt5(path)
    df.dropna(axis=0, inplace=True)
    df['date_time']=df.index
    df['date']=df.index.date
    #costruzione del dataframe daily con individuazione pattern
    df_d=pattern(path)
    df_d['ATR_l']=df_d.ATR_l.shift(1)
    df_d['ATR_S']=df_d.ATR_s.shift(1)
    df_d['ClosePerc']=df_d.ClosePerc.shift(1)
    df_d['high']=df_d.high.shift(1)
    df_d['low']=df_d.low.shift(1)
    df_d['close']=df_d.close.shift(1)
    df_d['close2']=df_d.close.shift(1)
    df_d['patA1']=df_d.patA1.shift(1)
    df_d['patA2']=df_d.patA2.shift(1)
    df_d['patA3']=df_d.patA3.shift(1)
    df_d['patB1']=df_d.patB1.shift(1)
    df_d['patB2']=df_d.patB2.shift(1)
    df_d['patB3']=df_d.patB3.shift(1)
    df_d['patC']=df_d.patC.shift(1)
    df_d['patD']=df_d.patD.shift(1)
    df_d['patE']=df_d.patE.shift(1)
    df_d['patF']=df_d.patF.shift(1)
    df_d['patG']=df_d.patG.shift(1)
    df_d['patH']=df_d.patH.shift(1)
    df_d['patI']=df_d.patI.shift(1)
    df_d['patJ']=df_d.patJ.shift(1)
    df_d['patK']=df_d.patK.shift(1)
    df_d['patL1']=df_d.patL1.shift(1)
    df_d['patM1']=df_d.patM1.shift(1)
    df_d['patL2']=df_d.patL2.shift(1)
    df_d['patM2']=df_d.patM2.shift(1)
    df_d['max1']=df_d.max1.shift(1)
    df_d['max2']=df_d.max2.shift(1)
    df_d['max3']=df_d.max3.shift(1)
    df_d['min1']=df_d.min1.shift(1)
    df_d['min2']=df_d.min2.shift(1)
    df_d['min3']=df_d.min3.shift(1)
    #costruzione databese unito per l'applicazione del trading system
    dfts=df.merge(df_d,how='left',on='date', left_index=True)
    dfts.set_index('date_time', inplace=True)
    dfts.drop([ 'volume_y', 'DOW', 'body', 'range',
           'mese', 'anno', 'CO', 'CO1', 'CO2', 'OL', 'HO', 'CL', 'HC',
           'BodyRangePerc', 'Color', 'PCTClose', 'NextClose',
           'NextClose2', 'CLperc', 'HCperc', 'OLperc', 'HOperc'],axis=1,inplace=True)
    dfts=dfts.rename(columns={"open_x": "open", "high_x": "high", "low_x": "low", "close_x": "close",
                            "volume_x": "volume","high_y":"yestHigh","low_y":"yestLow",
                            "close_y":"yestClose","close2_y":"yestClose2","open_y":"todayOpen","ClosePerc":"yest_closeperc"})
    #inserimento colonne aggiuntive suddivisioni temporali (qui potrebbero essere aggiunte
    #anche ulteriori colonne descrittive da utilizzare come test in condizioni boleane
    dfts['body']=df_d.close-df_d.open
    dfts["HOD"]=dfts.index.hour
    dfts["DOW"]=dfts.index.dayofweek
    dfts["DOY"]=dfts.index.day
    dfts["MOY"]=dfts.index.month
    dfts["YEAR"]=dfts.index.year
    dfts["DOWname"]=np.where((dfts.index.dayofweek==0),"lunedì",
                         np.where((dfts.index.dayofweek==1),"martedì",
                         np.where((dfts.index.dayofweek==2),"mercoledì",
                         np.where((dfts.index.dayofweek==3),"giovedì",
                         np.where((dfts.index.dayofweek==4),"venerdì",
                         np.where((dfts.index.dayofweek==5),"sabato",
                         np.where((dfts.index.dayofweek==6),"domenica",0)))))))
    dfts["MOYname"]=np.where((dfts.index.month==1),"gennaio",
                         np.where((dfts.index.month==2),"febbraio",
                         np.where((dfts.index.month==3),"marzo",
                         np.where((dfts.index.month==4),"aprile",
                         np.where((dfts.index.month==5),"maggio",
                         np.where((dfts.index.month==6),"giugno",
                         np.where((dfts.index.month==7),"luglio",
                         np.where((dfts.index.month==8),"agosto",
                         np.where((dfts.index.month==9),"settembre",
                         np.where((dfts.index.month==10),"ottobre",
                         np.where((dfts.index.month==11),"novembre",
                         np.where((dfts.index.month==12),"dicembre",
                         0))))))))))))
    
    return dfts
# In[ ]:




