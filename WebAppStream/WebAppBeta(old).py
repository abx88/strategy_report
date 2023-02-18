#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import yfinance as yf
import streamlit as st
import numpy as np
import datetime as dt
import librerie.importazioni as imp
import librerie.stagionalità as stg
import librerie.pattern as pt
import librerie.calcolivari as clc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
from zigzag import *
from plotly import __version__
print("Plotly version: ",__version__)
init_notebook_mode(connected=True)



# In[7]:


instruments = pd.read_csv("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/strumenti.csv")
#instruments = pd.read_csv("dati_input/strumenti.csv")
symbols = instruments['Symbol'].sort_values().tolist()  


# In[9]:

pagina = st.sidebar.radio(
     "pagina app",
     ('analisi Daily','statistiche descrittive', 'stagionalità', 'analisi swing','becktest'))
 
ticker = st.sidebar.selectbox('SCEGLI STRUMENTO', symbols) 

if pagina == 'analisi Daily':
    st.title('studio barre giornaliere')   
    #st.subheader('grafico '+ticker)
    df=imp.import_mt4("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
    df['HOD']=df.index.hour
    df['body']=df.close-df.open
    df['candela']=df.index.time
    df['range']=df.high-df.low
    df['rangeperc']=(df.range/df.close.shift(1))*100
    df['c1-c']=df.close-df.close.shift(1)
    df['body']=df.close-df.open
    df['bodyperc']=df.body/df.close.shift(1)
    df['HOD']=df.index.hour
    df['DOW']=df.index.dayofweek
    df['giorno']=df.index.day
    df['giornoanno']=df.index.dayofyear
    df['mese']=df.index.month
    df['anno']=df.index.year
    
    
    
    inizio_serie=str(df.index.min())
    inizio_serieY=int(df.index.min().year)
    inizio_serieM=int(df.index.min().month)
    inizio_serieD=int(df.index.min().day)
    fine_serie=str(df.index.max())
    fine_serieY=int(df.index.max().year)
    fine_serieM=int(df.index.max().month)
    fine_serieD=int(df.index.max().day)

    st.sidebar.text("INIZIO SERIE "+inizio_serie)
    st.sidebar.text("FINE SERIE "+fine_serie)
    
        
    
    start = st.sidebar.date_input(
         "data inizio",
         dt.date(inizio_serieY, inizio_serieM, inizio_serieD))


    stop = st.sidebar.date_input(
         "data fine",
         dt.date(fine_serieY, fine_serieM, fine_serieD))
    
    st.subheader('statistiche su barre Daily '+ticker)
    dfD=pd.DataFrame(df['open'].resample('D').first())
    dfD['high']=df['high'].resample('D').max()
    dfD['low']=df['low'].resample('D').min()
    dfD['close']=df['close'].resample('D').last()
    dfD['volume']=df['volume'].resample('D').sum()
    dfD['closeperc']=dfD.close.pct_change()*100
    dfD['body']=abs(dfD.close-dfD.open)
    dfD['range']=dfD.high-dfD.low
    dfD['rangeperc']=dfD.range.pct_change()

    dfDdescr=pd.DataFrame(dfD['body'].describe([0.01,0.05,0.25,0.5,0.75,0.95,0.99]))
    dfDdescr['closeperc']=dfD['closeperc'].describe([0.01,0.05,0.25,0.5,0.75,0.95,0.99])
    dfDdescr['range']=dfD['range'].describe([0.01,0.05,0.25,0.5,0.75,0.95,0.99])
    dfDdescr['rangeperc']=dfD['rangeperc'].describe([0.01,0.05,0.25,0.5,0.75,0.95,0.99])

    st.table(dfDdescr.iloc[1:3])
    st.table(dfDdescr.iloc[4:11])
    
    dist = px.histogram(dfD[start:stop], x=dfD[start:stop].close.pct_change()*100,nbins=50)
    dist.update_xaxes(
                title_text = "distribuzione chiusure giornaliere",
                title_font = {"size": 15},
                title_standoff = 10)
    st.plotly_chart(dist,use_container_width=False )
    conta=str(dfD.close.count())
    st.text('(totale barre in esame '+conta+')')
    
    dispersione = px.scatter(dfD[start:stop], x=dfD[start:stop].index, y=dfD[start:stop].close.pct_change())
    dispersione.update_xaxes(
                title_text = "dispersione chiusure giornaliere",
                title_font = {"size": 15},
                title_standoff = 10)
    st.plotly_chart(dispersione,use_container_width=False )
    
    dfD['ATRfast']=clc.SMA(dfD.range,5)*10
    #dfD['ATRslow']=clc.SMA(dfD.range,200)*10
    vola = go.Figure()
    vola.add_trace(go.Scatter(
        mode = "lines",
        y = dfD[start:stop].ATRfast,
        x = dfD[start:stop].index,
        name="volatilità di breve periodo",
        connectgaps=True))
    vola.add_trace(go.Scatter(
        mode = "lines",
        y = dfD[start:stop].close,
        x = dfD[start:stop].index,
        name="prezzo",
        connectgaps=True))
    vola.update_xaxes(
                title_text = "volatilità e prezzo",
                title_font = {"size": 15},
                title_standoff = 10)
    st.plotly_chart(vola,use_container_width=False )
                
    

    
    
elif pagina == 'statistiche descrittive':
    st.title('statistiche descrittive')   
    #st.subheader('grafico '+ticker)
    #df=imp.import_mt5("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
    
    df=imp.import_mt4("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
    df['HOD']=df.index.hour
    df['body']=df.close-df.open
    df['candela']=df.index.time
    df['range']=df.high-df.low
    df['c1-c']=df.close-df.close.shift(1)
    df['body']=df.close-df.open
    df['bodyperc']=df.body/df.close.shift(1)
    df['HOD']=df.index.hour
    df['DOW']=df.index.dayofweek
    df['giorno']=df.index.day
    df['giornoanno']=df.index.dayofyear
    df['mese']=df.index.month
    df['anno']=df.index.year
    
    
    
    inizio_serie=str(df.index.min())
    inizio_serieY=int(df.index.min().year)
    inizio_serieM=int(df.index.min().month)
    inizio_serieD=int(df.index.min().day)
    fine_serie=str(df.index.max())
    fine_serieY=int(df.index.max().year)
    fine_serieM=int(df.index.max().month)
    fine_serieD=int(df.index.max().day)

    st.sidebar.text("INIZIO SERIE "+inizio_serie)
    st.sidebar.text("FINE SERIE "+fine_serie)
    
        
    
    start = st.sidebar.date_input(
         "data inizio",
         dt.date(inizio_serieY, inizio_serieM, inizio_serieD))


    stop = st.sidebar.date_input(
         "data fine",
         dt.date(fine_serieY, fine_serieM, fine_serieD))
    
    options=st.sidebar.selectbox('applica statistiche a:',
                               ('range','close','volume'))
    
    if options==('range'):
        df=imp.import_mt4("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
        df['HOD']=df.index.hour
        df['body']=df.close-df.open
        df['candela']=df.index.time
        df['range']=df.high-df.low
        df['c1-c']=df.close-df.close.shift(1)
        df['body']=abs(df.close-df.open)
        df['bodyperc']=df.body/df.close.shift(1)
        df['rangeperc']=(df.range/df.close.shift(1))*100
        df['HOD']=df.index.hour
        df['DOW']=df.index.dayofweek
        df['giorno']=df.index.day
        df['giornoanno']=df.index.dayofyear
        df['mese']=df.index.month
        df['anno']=df.index.year
        df['sessione']=np.where((df.HOD<8),"asia", np.where(((df.HOD>7) & (df.HOD<16)),"europa", "usa"))
        df['nomegiorno']=np.where((df.DOW==0),"1-lunedì",
                          np.where((df.DOW==1),"2-martedì",
                                np.where((df.DOW==2),"3-mercoledì", 
                                         np.where((df.DOW==3),"4-giovedì", 
                                                  np.where((df.DOW==4),"5-venerdì",
                                                           np.where((df.DOW==5),"6-sabato","7-domenica"))))))
        
        
        #df1=df.loc[start:stop]
        pivotRANGE = pd.pivot_table(df[start:stop], values='range', index='candela', aggfunc=np.mean)
        pivotRANGEfilt=pivotRANGE.nlargest(20, "range")

        pivotRANGEtot = pd.pivot_table(df, values='range', index='candela', aggfunc=np.mean)
        pivotRANGEfilttot=pivotRANGEtot.nlargest(20, "range")
        
        range_bar = make_subplots(rows=1, cols=2)
        
        range_bar.add_trace(go.Bar(x=pivotRANGEfilt.index, y=pivotRANGEfilt.range, name="periodo"), 1, 1)

        range_bar.add_trace(go.Bar(x=pivotRANGEfilttot.index, y=pivotRANGEfilttot.range,name="totale"), 1, 2)

        range_bar.update_layout( title_text="range medio per candela "+ticker+"(prime 20)")
        
        st.plotly_chart(range_bar,use_container_width=False )
        pivotRANGEhod = pd.pivot_table(df[start:stop], values='range', index='anno',columns='sessione', aggfunc=np.mean)
        st.caption("range medi assuluti per sessione "+ticker)
        st.table(pivotRANGEhod)
        
        pivotRANGEhodperc = pd.pivot_table(df[start:stop], values='rangeperc', index='anno',columns='sessione', aggfunc=np.mean)
        st.caption("range medi percentuali per sessione "+ticker)
        st.table(pivotRANGEhodperc)
        
        pivotRANGEdow = pd.pivot_table(df[start:stop], values='range', index='anno',columns='nomegiorno', aggfunc=np.mean)
        st.caption("range medi assuluti per giorno della settimana "+ticker)
        st.table(pivotRANGEdow)
        
        pivotRANGEdowperc = pd.pivot_table(df[start:stop], values='rangeperc', index='anno',columns='nomegiorno', aggfunc=np.mean)
        st.caption("range medi percentuali per giorno della settimana "+ticker)
        st.table(pivotRANGEdowperc)
        
        
    elif options==('close'):
        df=imp.import_mt4("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
        df['HOD']=df.index.hour
        df['body']=df.close-df.open
        df['candela']=df.index.time
        df['range']=df.high-df.low
        df['c1-c']=df.close-df.close.shift(1)
        df['body']=abs(df.close-df.open)
        df['bodyperc']=df.body/df.close.shift(1)
        df['HOD']=df.index.hour
        df['DOW']=df.index.dayofweek
        df['giorno']=df.index.day
        df['giornoanno']=df.index.dayofyear
        df['mese']=df.index.month
        df['anno']=df.index.year
        df['cp']=df.close.pct_change()
        df['l']=np.where((df.cp>0),1,0)
        df['l1']=df.l.shift(-1)
        
        pivotBODY = pd.pivot_table(df[start:stop], values='body', index='candela', aggfunc=np.mean)
        pivotBODYfilt=pivotBODY.nlargest(20, "body")

        pivotBODYtot = pd.pivot_table(df, values='body', index='candela', aggfunc=np.mean)
        pivotBODYfilttot=pivotBODYtot.nlargest(20, "body")
        
        body_bar = make_subplots(rows=1, cols=2)
        
        body_bar.add_trace(go.Bar(x=pivotBODYfilt.index, y=pivotBODYfilt.body, name="periodo"), 1, 1)

        body_bar.add_trace(go.Bar(x=pivotBODYfilttot.index, y=pivotBODYfilttot.body,name="totale"), 1, 2)

        body_bar.update_layout( title_text="body per candela "+ticker+"(prime 20)")
        st.plotly_chart(body_bar,use_container_width=False )
        #calcolo rapporto range per vedere la distribuzione totale
        
        
        range_candela = st.slider('range candela', 0, 100, 25)
        
        df['rapporto_rangeDist']=(df.body/df.range)
        pivotRRdist = pd.pivot_table(df[start:stop], values='rapporto_rangeDist', index='candela', aggfunc=np.mean)
                
        df['rapporto_range']=np.where((df.range>range_candela),(df.body/df.range),np.nan)
                    
        pivotRR = pd.pivot_table(df[start:stop], values='rapporto_range', index='candela', aggfunc=np.mean)
        pivotRRfilt=pivotRR.nlargest(20, "rapporto_range")
        
        pivotRRtot = pd.pivot_table(df, values='rapporto_range', index='candela', aggfunc=np.mean)
        pivotRRtotfilt=pivotRRtot.nlargest(20, "rapporto_range")
        
        body_barRR = make_subplots(rows=1, cols=2)
        
        body_barRR.add_trace(go.Bar(x=pivotRRfilt.index, y=pivotRRfilt.rapporto_range, name="periodo"), 1, 1)

        body_barRR.add_trace(go.Bar(x=pivotRRtotfilt.index, y=pivotRRtotfilt.rapporto_range,name="totale"), 1, 2)

        body_barRR.update_layout( title_text=ticker+" candele con direzionalità con range superiore a valore slider")
        st.plotly_chart(body_barRR,use_container_width=False )
        
        rrdistr=px.histogram(pivotRRdist, x="rapporto_rangeDist")
        rrdistr.update_layout( title_text=ticker+" distribuzione candele con direzionalità")
        st.plotly_chart(rrdistr,use_container_width=False )

    else:
        df=imp.import_mt4("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
        df['HOD']=df.index.hour
        df['body']=df.close-df.open
        df['candela']=df.index.time
        df['range']=df.high-df.low
        df['c1-c']=df.close-df.close.shift(1)
        df['body']=abs(df.close-df.open)
        df['bodyperc']=df.body/df.close.shift(1)
        df['HOD']=df.index.hour
        df['DOW']=df.index.dayofweek
        df['giorno']=df.index.day
        df['giornoanno']=df.index.dayofyear
        df['mese']=df.index.month
        df['anno']=df.index.year
        
        
        #df1=df.loc[start:stop]
        pivotVOL = pd.pivot_table(df[start:stop], values='volume', index='candela', aggfunc=np.mean)
        pivotVOLfilt=pivotVOL.nlargest(20, "volume")

        pivotVOLtot = pd.pivot_table(df, values='volume', index='candela', aggfunc=np.mean)
        pivotVOLfilttot=pivotVOLtot.nlargest(20, "volume")
        
        vol_bar = make_subplots(rows=1, cols=2)
        
        vol_bar.add_trace(go.Bar(x=pivotVOLfilt.index, y=pivotVOLfilt.volume, name="periodo"), 1, 1)

        vol_bar.add_trace(go.Bar(x=pivotVOLfilttot.index, y=pivotVOLfilttot.volume,name="totale"), 1, 2)

        vol_bar.update_layout( title_text="volume per candela "+ticker)
        st.plotly_chart(vol_bar,use_container_width=False )
        
    

elif pagina == 'stagionalità':
    st.title('Stagionalità')
    df=imp.import_mt4("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
    inizio=str(df.index.min())
    fine=str(df.index.max())
    startDate=inizio[0:4]+inizio[5:7]+inizio[8:10]
    endDate=fine[0:4]+fine[5:7]+fine[8:10]
    year=str((df.index.max().year))
    month=str((df.index.max().month))
    #periodo completo (long)
    startDateLong = startDate
    endDateLong = endDate
    #ultimo anno 
    lastyear=str((df.index.max().year)-1)
    startDateLY =lastyear+fine[5:7]+fine[8:10]
    endDateLY = endDate
    #ultimi 3 mesi 
    if month=='1':
        last3month=lastyear+'10'
    elif month=='2':
        last3month=lastyear+'11'
    elif month=='3':
        last3month=lastyear+'12'
    elif month=='4':
        last3month=str((df.index.max().year))+'01'
    elif month=='5':
        last3month=str((df.index.max().year))+'02'
    elif month=='6':
        last3month=str((df.index.max().year))+'03'
    elif month=='7':
        last3month=str((df.index.max().year))+'04'
    elif month=='8':
        last3month=str((df.index.max().year))+'05'
    elif month=='9':
        last3month=str((df.index.max().year))+'06'
    elif month=='10':
        last3month=str((df.index.max().year))+'07'
    elif month=='11':
        last3month=str((df.index.max().year))+'08'
    else:    
        last3month=str((df.index.max().year))+'09'

    startDateL3M = last3month+fine[8:10]         
    endDateL3M = endDate
   
    #ultimo mese
    if month=='1':
        lastmonth=lastyear+'12'
    elif month=='2':
        lastmonth=str((df.index.max().year))+'01'
    elif month=='3':
        lastmonth=str((df.index.max().year))+'02'
    elif month=='4':
        lastmonth=str((df.index.max().year))+'03'
    elif month=='5':
        lastmonth=str((df.index.max().year))+'04'
    elif month=='6':
        lastmonth=str((df.index.max().year))+'05'
    elif month=='7':
        lastmonth=str((df.index.max().year))+'06'
    elif month=='8':
        lastmonth=str((df.index.max().year))+'07'
    elif month=='9':
        lastmonth=str((df.index.max().year))+'08'
    elif month=='10':
        lastmonth=str((df.index.max().year))+'09'
    elif month=='11':
        lastmonth=str((df.index.max().year))+'10'
    else:    
        lastmonth=str((df.index.max().year))+'11'

    startDateLM = lastmonth+fine[8:10]         
    endDateLM = endDate

    df_h=pd.DataFrame(df['open'].resample('H').first())
    df_h['high']=df['high'].resample('H').max()
    df_h['low']=df['low'].resample('H').min()
    df_h['close']=df['close'].resample('H').last()
    df_h['volume']=df['volume'].resample('H').sum()
    df_h['HOD']=df_h.index.hour
    df_h['body']=df_h.close-df_h.open
    df_h['candela']=df_h.index.time
    df_h['range']=df_h.high-df.low
    df_h['c1-c']=df_h.close-df_h.close.shift(1)
    df_h['body']=df_h.close-df.open
    df_h['bodyperc']=df_h.body/df_h.close.shift(1)
    df_h['HOD']=df_h.index.hour
    df_h['DOW']=df_h.index.dayofweek
    df_h['giorno']=df_h.index.day
    df_h['giornoanno']=df_h.index.dayofyear
    df_h['mese']=df_h.index.month
    df_h['anno']=df_h.index.year
    df_h.dropna(axis=0, inplace=True)
    df_hLY=df_h.loc[startDateLY:endDateLY]
    df_hL3M=df_h.loc[startDateL3M:endDateL3M]
    df_hLM=df_h.loc[startDateLM:endDateLM]
    tipo_stagionalità = st.sidebar.radio('tipo stagionalita', 
                                         ('intraday', 'intrasettimanale', 'intramensile'))
    if tipo_stagionalità == 'intraday':
        st.subheader('stagionalità su base giornaliera (valori NON normalizzati)', anchor=None)
        pivotHODmean = pd.pivot_table(df_h, values='bodyperc', index=['HOD'], aggfunc=np.mean,fill_value=0)
        pivotHODmeanLY = pd.pivot_table(df_hLY, values='bodyperc', index=['HOD'], aggfunc=np.mean,fill_value=0)
        pivotHODmeanL3M = pd.pivot_table(df_hL3M, values='bodyperc', index=['HOD'], aggfunc=np.mean,fill_value=0)
        pivotHODmeanLM = pd.pivot_table(df_hLM, values='bodyperc', index=['HOD'], aggfunc=np.mean,fill_value=0)
        pivotHODmean['total']=pivotHODmean.bodyperc
        pivotHODmean.drop(['bodyperc'], axis=1,inplace=True)
        pivotHODmean['LY']=pivotHODmeanLY.bodyperc
        pivotHODmean['L3M']=pivotHODmeanL3M.bodyperc
        pivotHODmean['LM']=pivotHODmeanLM.bodyperc
        pivotHODmean=pivotHODmean.replace(np.nan,0)
        #grafico stagionalità HOD non normaliz
        stagHOD = go.Figure()
        stagHOD.add_trace(go.Scatter(
            mode = "lines",
            y = pivotHODmean.total.cumsum(),
            x = pivotHODmean.index,
            name="total"))
        stagHOD.add_trace(go.Scatter(
            mode = "lines",
            y = pivotHODmean.LY.cumsum(),
            x = pivotHODmean.index,
            name="LY"))
        stagHOD.add_trace(go.Scatter(
            mode = "lines",
            y = pivotHODmean.L3M.cumsum(),
            x = pivotHODmean.index,
            name="L3M"))
        stagHOD.add_trace(go.Scatter(
            mode = "lines",
            y = pivotHODmean.LM.cumsum(),
            x = pivotHODmean.index,
            name="LM"))

        stagHOD.update_xaxes(
                tickangle = 90,
                title_text = "trend giornaliero",
                title_font = {"size": 20},
                title_standoff = 10)
        
        st.plotly_chart(stagHOD,use_container_width=True)
    
    
        st.subheader('stagionalità su base giornaliera (valori normalizzati)', anchor=None)
        pivotHODmeanNorm=pivotHODmean.copy()
        pivotHODmeanNorm.dropna(axis=0, inplace=True)
        pivotHODmeanNorm['totaln']=clc.normalizeMaxMin(pivotHODmeanNorm.total.cumsum())
        pivotHODmeanNorm['LYn']=clc.normalizeMaxMin(pivotHODmeanNorm.LY.cumsum())
        pivotHODmeanNorm['L3Mn']=clc.normalizeMaxMin(pivotHODmeanNorm.L3M.cumsum())
        pivotHODmeanNorm['LMn']=clc.normalizeMaxMin(pivotHODmeanNorm.LM.cumsum())
        pivotHODmeanNorm.drop(['total','LY','L3M','LM'], axis=1,inplace=True)
        #grafico stagionalità HOD normaliz
        stagHODn = go.Figure()
        stagHODn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotHODmeanNorm.totaln,
            x = pivotHODmeanNorm.index,
            name="total"))
        stagHODn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotHODmeanNorm.LYn,
            x = pivotHODmeanNorm.index,
            name="LY"))
        stagHODn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotHODmeanNorm.L3Mn,
            x = pivotHODmeanNorm.index,
            name="L3M"))
        stagHODn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotHODmeanNorm.LMn,
            x = pivotHODmeanNorm.index,
            name="LM"))

        stagHODn.update_xaxes(
                tickangle = 90,
                title_text = "trend giornaliero",
                title_font = {"size": 20},
                title_standoff = 10)
        
        st.plotly_chart(stagHODn,use_container_width=True)
        
        
        
        
        
        
    elif tipo_stagionalità == 'intrasettimanale':
        st.subheader('stagionalità su base settimanale', anchor=None)
                
        pivotDOWmean = pd.pivot_table(df_h, values='bodyperc', index=['DOW','HOD'], aggfunc=np.mean,fill_value=0)
        pivotDOWmeanLY = pd.pivot_table(df_hLY, values='bodyperc', index=['DOW','HOD'], aggfunc=np.mean,fill_value=0)
        pivotDOWmeanL3M = pd.pivot_table(df_hL3M, values='bodyperc', index=['DOW','HOD'], aggfunc=np.mean,fill_value=0)
        pivotDOWmeanLM = pd.pivot_table(df_hLM, values='bodyperc', index=['DOW','HOD'], aggfunc=np.mean,fill_value=0)
        pivotDOWmean['total']=pivotDOWmean.bodyperc
        pivotDOWmean['LY']=pivotDOWmeanLY.bodyperc
        pivotDOWmean['L3M']=pivotDOWmeanL3M.bodyperc
        pivotDOWmean['LM']=pivotDOWmeanLM.bodyperc
        pivotDOWmean=pivotDOWmean.replace(np.nan,0)
        
        indicenum=[]
        i = 0
        n = len(pivotDOWmean)
        while i < n:
            indicenum.append(i)
            i += 1
        pivotDOWmean['indice']=indicenum
        giorno=[]
        i = 0
        n = len(pivotDOWmean.indice)
        while i < n:
            if pivotDOWmean[pivotDOWmean.indice==i].indice.sum() < len(indicenum)/5:
                giorno.append(str(i)+'lunedì')
                i += 1
            elif ((pivotDOWmean[pivotDOWmean.indice==i].indice.sum() >= len(indicenum)/5) 
                  & (pivotDOWmean[pivotDOWmean.indice==i].indice.sum() < len(indicenum)/5*2)):
                giorno.append(str(i)+'martedì')
                i += 1
            elif ((pivotDOWmean[pivotDOWmean.indice==i].indice.sum() >= len(indicenum)/5*2) 
                  & (pivotDOWmean[pivotDOWmean.indice==i].indice.sum() < len(indicenum)/5*3)):
                  giorno.append(str(i)+'mercoledì')
                  i += 1
            elif ((pivotDOWmean[pivotDOWmean.indice==i].indice.sum() >= len(indicenum)/5*3) 
                  & (pivotDOWmean[pivotDOWmean.indice==i].indice.sum() < len(indicenum)/5*4)):
                  giorno.append(str(i)+'giovedì')
                  i += 1
            else:
                  giorno.append(str(i)+'venerdì')
                  i += 1



        pivotDOWmean['giorno']=giorno
        pivotDOWmean.drop(['bodyperc','indice'], axis=1,inplace=True)
        #grafico stagionalità DOW non normaliz
        stagDOW = go.Figure()
        stagDOW.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOWmean.total.cumsum(),
            x = pivotDOWmean.giorno,
            name="total"))
        stagDOW.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOWmean.LY.cumsum(),
            x = pivotDOWmean.giorno,
            name="LY"))
        stagDOW.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOWmean.L3M.cumsum(),
            x = pivotDOWmean.giorno,
            name="L3M"))
        stagDOW.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOWmean.LM.cumsum(),
            x = pivotDOWmean.giorno,
            name="LM"))

        stagDOW.update_xaxes(
                tickangle = 90,
                title_text = "trend settimanale",
                title_font = {"size": 20},
                title_standoff = 10)
        
        st.plotly_chart(stagDOW,use_container_width=True)
        
        st.subheader('stagionalità su base settimanale (valori normalizzati)', anchor=None)
        pivotDOWmeanNorm=pivotDOWmean.copy()
        pivotDOWmeanNorm=pivotDOWmeanNorm.replace(np.nan,0)
        pivotDOWmeanNorm['totaln']=clc.normalizeMaxMin(pivotDOWmeanNorm.total.cumsum())
        pivotDOWmeanNorm['LYn']=clc.normalizeMaxMin(pivotDOWmeanNorm.LY.cumsum())
        pivotDOWmeanNorm['L3Mn']=clc.normalizeMaxMin(pivotDOWmeanNorm.L3M.cumsum())
        pivotDOWmeanNorm['LMn']=clc.normalizeMaxMin(pivotDOWmeanNorm.LM.cumsum())
        pivotDOWmeanNorm.drop(['total','LY','L3M','LM'], axis=1,inplace=True)
        #grafico stagionalità DOW normaliz
        stagDOWn = go.Figure()
        stagDOWn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOWmeanNorm.totaln,
            x = pivotDOWmeanNorm.giorno,
            name="total"))
        stagDOWn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOWmeanNorm.LYn,
            x = pivotDOWmeanNorm.giorno,
            name="LY"))
        stagDOWn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOWmeanNorm.L3Mn,
            x = pivotDOWmeanNorm.giorno,
            name="L3M"))
        stagDOWn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOWmeanNorm.LMn,
            x = pivotDOWmeanNorm.giorno,
            name="LM"))

        stagDOWn.update_xaxes(
                tickangle = 90,
                title_text = "trend settimanale normalizzato",
                title_font = {"size": 20},
                title_standoff = 10)
        
        st.plotly_chart(stagDOWn,use_container_width=True)
        
    else:
        st.subheader('stagionalità su base mensile', anchor=None)
        pivotDOMmean = pd.pivot_table(df_h, values='bodyperc', index=['giorno'], aggfunc=np.mean,fill_value=0)
        pivotDOMmeanLY = pd.pivot_table(df_hLY, values='bodyperc', index=['giorno'], aggfunc=np.mean,fill_value=0)
        pivotDOMmeanL3M = pd.pivot_table(df_hL3M, values='bodyperc', index=['giorno'], aggfunc=np.mean,fill_value=0)
        pivotDOMmeanLM = pd.pivot_table(df_hLM, values='bodyperc', index=['giorno'], aggfunc=np.mean,fill_value=0)
        pivotDOMmean['total']=pivotDOMmean.bodyperc
        pivotDOMmean['LY']=pivotDOMmeanLY.bodyperc
        pivotDOMmean['L3M']=pivotDOMmeanL3M.bodyperc
        pivotDOMmean['LM']=pivotDOMmeanLM.bodyperc
        pivotDOMmean.drop(['bodyperc'], axis=1,inplace=True)
        pivotDOMmean=pivotDOMmean.replace(np.nan,0)
       #grafico stagionalità DOM non normaliz
        stagDOM = go.Figure()
        stagDOM.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOMmean.total.cumsum(),
            x = pivotDOMmean.index,
            name="total"))
        stagDOM.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOMmean.LY.cumsum(),
            x = pivotDOMmean.index,
            name="LY"))
        stagDOM.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOMmean.L3M.cumsum(),
            x = pivotDOMmean.index,
            name="L3M"))
        stagDOM.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOMmean.LM.cumsum(),
            x = pivotDOMmean.index,
            name="LM"))

        stagDOM.update_xaxes(
                tickangle = 90,
                title_text = "trend mensile",
                title_font = {"size": 20},
                title_standoff = 10)
        
        st.plotly_chart(stagDOM,use_container_width=True)
        #grafico stagionalità DOM normaliz
        st.subheader('stagionalità su base mensile (valori normalizzati)', anchor=None)
        pivotDOMmeanNorm=pivotDOMmean.copy()
        pivotDOMmeanNorm=pivotDOMmeanNorm.replace(np.nan,0)
        pivotDOMmeanNorm['totaln']=clc.normalizeMaxMin(pivotDOMmeanNorm.total.cumsum())
        pivotDOMmeanNorm['LYn']=clc.normalizeMaxMin(pivotDOMmeanNorm.LY.cumsum())
        pivotDOMmeanNorm['L3Mn']=clc.normalizeMaxMin(pivotDOMmeanNorm.L3M.cumsum())
        pivotDOMmeanNorm['LMn']=clc.normalizeMaxMin(pivotDOMmeanNorm.LM.cumsum())
        pivotDOMmeanNorm.drop(['total','LY','L3M','LM'], axis=1,inplace=True)
        
        stagDOMn = go.Figure()
        stagDOMn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOMmeanNorm.totaln,
            x = pivotDOMmeanNorm.index,
            name="totaln"))
        stagDOMn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOMmeanNorm.LYn,
            x = pivotDOMmeanNorm.index,
            name="LYn"))
        stagDOMn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOMmeanNorm.L3Mn,
            x = pivotDOMmeanNorm.index,
            name="L3Mn"))
        stagDOMn.add_trace(go.Scatter(
            mode = "lines",
            y = pivotDOMmeanNorm.LMn,
            x = pivotDOMmeanNorm.index,
            name="LMn"))

        stagDOMn.update_xaxes(
                tickangle = 90,
                title_text = "trend mensile",
                title_font = {"size": 20},
                title_standoff = 10)
        
        st.plotly_chart(stagDOMn,use_container_width=True)
elif pagina=='analisi swing':
    st.title('Analisi swing')   
    
    #df=imp.import_mt5("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
    zig = st.slider('ampiezza swing', 0.000, 0.100, 0.050)
    df=imp.import_mt4("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
    df['HOD']=df.index.hour
    df['body']=df.close-df.open
    df['candela']=df.index.time
    df['range']=df.high-df.low
    df['c1-c']=df.close-df.close.shift(1)
    df['body']=df.close-df.open
    df['bodyperc']=df.body/df.close.shift(1)
    df['HOD']=df.index.hour
    df['DOW']=df.index.dayofweek
    df['giorno']=df.index.day
    df['giornoanno']=df.index.dayofyear
    df['mese']=df.index.month
    df['anno']=df.index.year
    X=df.close
    pivots = peak_valley_pivots(X.values, zig, -zig)
    ts_pivots = pd.Series(X, index=X.index)
    ts_pivots = ts_pivots[pivots != 0]
    df['zigzag'] =  ts_pivots
    
    
    inizio_serie=str(df.index.min())
    inizio_serieY=int(df.index.min().year)
    inizio_serieM=int(df.index.min().month)
    inizio_serieD=int(df.index.min().day)
    fine_serie=str(df.index.max())
    fine_serieY=int(df.index.max().year)
    fine_serieM=int(df.index.max().month)
    fine_serieD=int(df.index.max().day)

    st.sidebar.text("INIZIO SERIE "+inizio_serie)
    st.sidebar.text("FINE SERIE "+fine_serie)
    
        
    
    start = st.sidebar.date_input(
         "data inizio",
         dt.date(inizio_serieY, inizio_serieM, inizio_serieD))


    stop = st.sidebar.date_input(
         "data fine",
         dt.date(fine_serieY, fine_serieM, fine_serieD))
    
    swing = go.Figure()
    swing.add_trace(go.Scatter(
        mode = "lines",
        y = df[start:stop].close,
        x = df[start:stop].index,
        name="indice"))
    swing.add_trace(go.Scatter(
        mode = "lines+markers",
        y = df[start:stop].zigzag,
        x = df[start:stop].index,
        name="zigzag",
        connectgaps=True))

    swing.update_layout(
            title={
                'text': ticker,
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

    st.plotly_chart(swing,use_container_width=True)
    
    dfswing=pd.DataFrame(df[start:stop].zigzag)
    dfswing.dropna(axis=0,inplace=True)
    dfswing['abs']=abs(dfswing.zigzag.shift(1)-dfswing.zigzag) 
    dfswing.dropna(axis=0,inplace=True)
    
    
    
    swingdescr=pd.DataFrame(dfswing['abs'].describe([0.01,0.05,0.25,0.5,0.75,0.95,0.99]))
    st.subheader('valori statistici swing '+ticker)
    st.table(swingdescr.iloc[1:3])
    st.table(swingdescr.iloc[4:10])
    
    #st.dataframe(swingdescr)
    st.subheader('andamento swing nel tempo '+ticker)
    swing = px.scatter(dfswing,x=dfswing.index, y='abs')
    swing.update_xaxes(
                title_text = "ampiezza swing maggiori di "+str(zig),
                title_font = {"size": 15},
                title_standoff = 10)
    st.plotly_chart(swing,use_container_width=False )
    
    st.subheader('distribuzione swing '+ticker)
    swingdistr=px.histogram(dfswing, x="abs",histnorm='probability')
    swingdistr.update_xaxes(
                title_text = "distribuzione swing maggiori di "+str(zig),
                title_font = {"size": 15},
                title_standoff = 10)
    st.plotly_chart(swingdistr,use_container_width=False )
    
    #swingdistr2=px.histogram(dfswing, x="abs",cumulative_enabled=True)
    swingdistr2=go.Figure(data=[go.Histogram(x=dfswing['abs'],histnorm='probability density', cumulative_enabled=True)])
    swingdistr2.update_xaxes(
                title_text = "distribuzione cumulativa swing maggiori di "+str(zig),
                title_font = {"size": 15},
                title_standoff = 10)
    st.plotly_chart(swingdistr2,use_container_width=False)
    
    #go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True)])
                            
                            
        
else:
    st.title('Backtest')
    
        
        
        
        
      
        
       



# In[ ]:




