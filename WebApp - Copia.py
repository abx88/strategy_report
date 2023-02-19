
"""
#!/usr/bin/env python
# coding: utf-8
"""
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
import librerie.backtest as bt
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
from zigzag import *
from plotly import __version__
print("Plotly version: ",__version__)
init_notebook_mode(connected=True)



# In[7]:
path = "Documents/Python/Python_Analisi_Quantitativa/WebAppStream"

instruments = pd.read_csv(path+"/dati_input/strumenti.csv")

#instruments = pd.read_csv("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/strumenti.csv")
#instruments = pd.read_csv("dati_input/strumenti.csv")
symbols = instruments['Symbol'].sort_values().tolist()  

# In[9]:

pagina = st.sidebar.radio(
     "pagina app",
     ('analisi Daily','statistiche descrittive', 'stagionalità', 'analisi swing','backtest'))
if (pagina is not 'backtest'):
    ticker = st.sidebar.selectbox('scegli strumento', symbols)
    #df=imp.import_mt5(path+"/dati_input/"+ticker+".csv")
    df=imp.import_mt4(path+"/dati_input/"+ticker+".csv")
    #df=imp.import_mt4("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
    df['HOD']=df.index.hour
    df['minute']=df.index.minute
    df['body']=df.close-df.open
    df['candela']=df.index.time
    df['range']=df.high-df.low
    df['rangeperc']=(df.range/df.close.shift(1))*100
    df['c1-c']=df.close-df.close.shift(1)
    df['body']=df.close-df.open
    df['bodyabs']=abs(df.close-df.open)
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
#    df['sessione']=np.where((df.HOD<8),"asia", np.where(((df.HOD>7) & (df.HOD<15)),"europa", "usa"))
    df['sessione']=np.where((df.index.time<dt.time(7,0)),"asia",np.where(((df.index.time>dt.time(7,0))&(df.index.time<dt.time(15,30))),
                                 "europa",
                                 "usa"))
    df['nomegiorno']=np.where((df.DOW==0),"1-lunedì",
                      np.where((df.DOW==1),"2-martedì",
                            np.where((df.DOW==2),"3-mercoledì", 
                                     np.where((df.DOW==3),"4-giovedì", 
                                              np.where((df.DOW==4),"5-venerdì",
                                                       np.where((df.DOW==5),"6-sabato","7-domenica"))))))


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

    if pagina == 'analisi Daily':
        st.title('studio barre giornaliere')   
        #st.subheader('grafico '+ticker)

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

        start = st.sidebar.date_input(
             "data inizio",
             dt.date(inizio_serieY, inizio_serieM, inizio_serieD))


        stop = st.sidebar.date_input(
             "data fine",
             dt.date(fine_serieY, fine_serieM, fine_serieD))

        options=st.sidebar.selectbox('applica statistiche a:',
                                   ('range','close','volume'))

        if options==('range'):

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

            pivotRANGEsess = pd.pivot_table(df[start:stop], values='range', index='anno',columns='sessione', aggfunc=np.mean)
            st.caption("range medi assuluti per sessione "+ticker)
            st.table(pivotRANGEsess)

            pivotRANGEsessperc = pd.pivot_table(df[start:stop], values='rangeperc', index='anno',columns='sessione', aggfunc=np.mean)
            st.caption("range medi percentuali per sessione "+ticker)
            st.table(pivotRANGEsessperc)

            dfLY=df.loc[startDateLY:endDateLY]
            dfL3M=df.loc[startDateL3M:endDateL3M]
            dfLM=df.loc[startDateLM:endDateLM]
            rangeHODmean = pd.pivot_table(df, values='rangeperc', index=['HOD'], aggfunc=np.mean,fill_value=0)
            rangeHODmeanLY = pd.pivot_table(dfLY, values='rangeperc', index=['HOD'], aggfunc=np.mean,fill_value=0)
            rangeHODmeanL3M = pd.pivot_table(dfL3M, values='rangeperc', index=['HOD'], aggfunc=np.mean,fill_value=0)
            rangeHODmeanLM = pd.pivot_table(dfLM, values='rangeperc', index=['HOD'], aggfunc=np.mean,fill_value=0)
            rangeHODmean['total']=rangeHODmean.rangeperc
            rangeHODmean.drop(['rangeperc'], axis=1,inplace=True)
            rangeHODmean['LY']=rangeHODmeanLY.rangeperc
            rangeHODmean['L3M']=rangeHODmeanL3M.rangeperc
            rangeHODmean['LM']=rangeHODmeanLM.rangeperc
            rangeHODmean=rangeHODmean.replace(np.nan,0)
            #grafico stagionalità HOD non normaliz
            rangeHOD = go.Figure()
            rangeHOD.add_trace(go.Scatter(
                mode = "lines",
                y = rangeHODmean.total.cumsum(),
                x = rangeHODmean.index,
                name="total"))
            rangeHOD.add_trace(go.Scatter(
                mode = "lines",
                y = rangeHODmean.LY.cumsum(),
                x = rangeHODmean.index,
                name="LY"))
            rangeHOD.add_trace(go.Scatter(
                mode = "lines",
                y = rangeHODmean.L3M.cumsum(),
                x = rangeHODmean.index,
                name="L3M"))
            rangeHOD.add_trace(go.Scatter(
                mode = "lines",
                y = rangeHODmean.LM.cumsum(),
                x = rangeHODmean.index,
                name="LM"))

            rangeHOD.update_xaxes(
                    tickangle = 0,
                    title_text = "confronto range intraday storico "+ticker,
                    title_font = {"size": 20},
                    title_standoff = 10)

            st.plotly_chart(rangeHOD,use_container_width=True)



            pivotRANGEdow = pd.pivot_table(df[start:stop], values='range', index='anno',columns='nomegiorno', aggfunc=np.mean)
            st.caption("range medi assuluti per giorno della settimana "+ticker)
            st.table(pivotRANGEdow)

            pivotRANGEdowperc = pd.pivot_table(df[start:stop], values='rangeperc', index='anno',columns='nomegiorno', aggfunc=np.mean)
            st.caption("range medi percentuali per giorno della settimana "+ticker)
            st.table(pivotRANGEdowperc)


        elif options==('close'):

            pivotBODYabs = pd.pivot_table(df[start:stop], values='bodyabs', index='candela', aggfunc=np.mean)
            pivotBODYabsfilt=pivotBODYabs.nlargest(20, "bodyabs")

            pivotBODYabstot = pd.pivot_table(df, values='bodyabs', index='candela', aggfunc=np.mean)
            pivotBODYabsfilttot=pivotBODYabstot.nlargest(20, "bodyabs")

            body_barabs = make_subplots(rows=1, cols=2)

            body_barabs.add_trace(go.Bar(x=pivotBODYabsfilt.index, y=pivotBODYabsfilt.bodyabs, name="periodo"), 1, 1)

            body_barabs.add_trace(go.Bar(x=pivotBODYabsfilttot.index, y=pivotBODYabsfilttot.bodyabs,name="totale"), 1, 2)

            body_barabs.update_layout( title_text="body (valori assoluti) per candela "+ticker+"(prime 20)")
            st.plotly_chart(body_barabs,use_container_width=False )
            #calcolo rapporto range per vedere la distribuzione totale


            #range_candela = st.slider('range candela', 0.00, 100.00, 0.50)
            range_candela = st.number_input('range candela', value=0.0000)

            df['rapporto_rangeDist']=(df.bodyabs/df.range)
            pivotRRabsdist = pd.pivot_table(df[start:stop], values='rapporto_rangeDist', index='candela', aggfunc=np.mean)

            df['rapporto_range']=np.where((df.range>range_candela),(df.bodyabs/df.range),np.nan)

            pivotRRabs = pd.pivot_table(df[start:stop], values='rapporto_range', index='candela', aggfunc=np.mean)
            pivotRRabsfilt=pivotRRabs.nlargest(20, "rapporto_range")

            pivotRRabstot = pd.pivot_table(df, values='rapporto_range', index='candela', aggfunc=np.mean)
            pivotRRabstotfilt=pivotRRabstot.nlargest(20, "rapporto_range")

            body_barabsRR = make_subplots(rows=1, cols=2)

            body_barabsRR.add_trace(go.Bar(x=pivotRRabs.index, y=pivotRRabs.rapporto_range, name="periodo"), 1, 1)

            body_barabsRR.add_trace(go.Bar(x=pivotRRabstot.index, y=pivotRRabstot.rapporto_range,name="totale"), 1, 2)

            body_barabsRR.update_layout( title_text=ticker+" candele con direzionalità (valori assoluti) con range superiore a valore slider")
            st.plotly_chart(body_barabsRR,use_container_width=False )

            rrdistr=px.histogram(pivotRRabs, x="rapporto_range",histnorm='probability' )
            rrdistr.update_layout( title_text=ticker+" distribuzione candele con direzionalità (valori assoluti)")
            st.plotly_chart(rrdistr,use_container_width=False )
         
            pivotBODY = pd.pivot_table(df[start:stop], values='body', index='candela', aggfunc=np.mean)
            pivotBODYlongfilt=pivotBODY.nlargest(20, "body")

            pivotBODYshortfilt=pivotBODY.nsmallest(20, "body")

            body_bar = make_subplots(rows=1, cols=2)

            body_bar.add_trace(go.Bar(x=pivotBODYlongfilt.index, y=pivotBODYlongfilt.body, name="periodo"), 1, 1)

            body_bar.add_trace(go.Bar(x=pivotBODYshortfilt.index, y=pivotBODYshortfilt.body,name="totale"), 1, 2)

            body_bar.update_layout( title_text="body per candela "+ticker+"(20 direz. long e 20 direz. short)")
            st.plotly_chart(body_bar,use_container_width=False )
            #calcolo rapporto range per vedere la distribuzione totale
            



        else:
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
            
            pivotVOLcount = pd.pivot_table(df[start:stop], values='volume', index=['HOD','minute'], aggfunc=np.count_nonzero)
            pivotVOLcountfilt = pivotVOLcount.nsmallest(30, "volume")
            st.table(pivotVOLcountfilt)



    elif pagina == 'stagionalità':
        st.title('Stagionalità')


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
            pivotHODmeanNorm['totaln']=clc.normalizeMaxMin(pivotHODmeanNorm.total)
            pivotHODmeanNorm['LYn']=clc.normalizeMaxMin(pivotHODmeanNorm.LY)
            pivotHODmeanNorm['L3Mn']=clc.normalizeMaxMin(pivotHODmeanNorm.L3M)
            pivotHODmeanNorm['LMn']=clc.normalizeMaxMin(pivotHODmeanNorm.LM)
            pivotHODmeanNorm.drop(['total','LY','L3M','LM'], axis=1,inplace=True)
            #grafico stagionalità HOD normaliz
            stagHODn = go.Figure()
            stagHODn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotHODmeanNorm.totaln.cumsum(),
                x = pivotHODmeanNorm.index,
                name="total"))
            stagHODn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotHODmeanNorm.LYn.cumsum(),
                x = pivotHODmeanNorm.index,
                name="LY"))
            stagHODn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotHODmeanNorm.L3Mn.cumsum(),
                x = pivotHODmeanNorm.index,
                name="L3M"))
            stagHODn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotHODmeanNorm.LMn.cumsum(),
                x = pivotHODmeanNorm.index,
                name="LM"))

            stagHODn.update_xaxes(
                    tickangle = 90,
                    title_text = "trend giornaliero",
                    title_font = {"size": 20},
                    title_standoff = 10)

            st.plotly_chart(stagHODn,use_container_width=True)

            HODn = go.Figure()
            HODn.add_trace(go.Bar(
                    y = pivotHODmeanNorm.totaln,
                    x = pivotHODmeanNorm.index,
                    name="total"))
            HODn.add_trace(go.Bar(
                y = pivotHODmeanNorm.LYn,
                x = pivotHODmeanNorm.index,
                name="LY"))
            HODn.add_trace(go.Bar(
                y = pivotHODmeanNorm.L3Mn,
                x = pivotHODmeanNorm.index,
                name="L3M"))
            HODn.add_trace(go.Bar(
                y = pivotHODmeanNorm.LMn,
                x = pivotHODmeanNorm.index,
                name="LM"))

            HODn.update_xaxes(
                    tickangle = 90,
                    title_text = "dipendenza ore del giorno",
                    title_font = {"size": 20},
                    title_standoff = 10)

            st.plotly_chart(HODn,use_container_width=True)





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
            pivotDOWmeanNorm['totaln']=clc.normalizeMaxMin(pivotDOWmeanNorm.total)
            pivotDOWmeanNorm['LYn']=clc.normalizeMaxMin(pivotDOWmeanNorm.LY)
            pivotDOWmeanNorm['L3Mn']=clc.normalizeMaxMin(pivotDOWmeanNorm.L3M)
            pivotDOWmeanNorm['LMn']=clc.normalizeMaxMin(pivotDOWmeanNorm.LM)
            pivotDOWmeanNorm.drop(['total','LY','L3M','LM'], axis=1,inplace=True)
            #grafico stagionalità DOW normaliz
            stagDOWn = go.Figure()
            stagDOWn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotDOWmeanNorm.totaln.cumsum(),
                x = pivotDOWmeanNorm.giorno,
                name="total"))
            stagDOWn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotDOWmeanNorm.LYn.cumsum(),
                x = pivotDOWmeanNorm.giorno,
                name="LY"))
            stagDOWn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotDOWmeanNorm.L3Mn.cumsum(),
                x = pivotDOWmeanNorm.giorno,
                name="L3M"))
            stagDOWn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotDOWmeanNorm.LMn.cumsum(),
                x = pivotDOWmeanNorm.giorno,
                name="LM"))

            stagDOWn.update_xaxes(
                    tickangle = 90,
                    title_text = "trend settimanale normalizzato",
                    title_font = {"size": 20},
                    title_standoff = 10)

            st.plotly_chart(stagDOWn,use_container_width=True)
            
            DOWn = go.Figure()
            DOWn.add_trace(go.Bar(
                y = pivotDOWmeanNorm.totaln,
                x = pivotDOWmeanNorm.giorno,
                name="total"))
            DOWn.add_trace(go.Bar(
                y = pivotDOWmeanNorm.LYn,
                x = pivotDOWmeanNorm.giorno,
                name="LY"))
            DOWn.add_trace(go.Bar(
                y = pivotDOWmeanNorm.L3Mn,
                x = pivotDOWmeanNorm.giorno,
                name="L3M"))
            DOWn.add_trace(go.Bar(
                y = pivotDOWmeanNorm.LMn,
                x = pivotDOWmeanNorm.giorno,
                name="LM"))

            DOWn.update_xaxes(
                    tickangle = 90,
                    title_text = "dipendenza oraria settimanale",
                    title_font = {"size": 20},
                    title_standoff = 10)

            st.plotly_chart(DOWn,use_container_width=True)

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
            pivotDOMmeanNorm['totaln']=clc.normalizeMaxMin(pivotDOMmeanNorm.total)
            pivotDOMmeanNorm['LYn']=clc.normalizeMaxMin(pivotDOMmeanNorm.LY)
            pivotDOMmeanNorm['L3Mn']=clc.normalizeMaxMin(pivotDOMmeanNorm.L3M)
            pivotDOMmeanNorm['LMn']=clc.normalizeMaxMin(pivotDOMmeanNorm.LM)
            pivotDOMmeanNorm.drop(['total','LY','L3M','LM'], axis=1,inplace=True)

            stagDOMn = go.Figure()
            stagDOMn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotDOMmeanNorm.totaln.cumsum(),
                x = pivotDOMmeanNorm.index,
                name="totaln"))
            stagDOMn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotDOMmeanNorm.LYn.cumsum(),
                x = pivotDOMmeanNorm.index,
                name="LYn"))
            stagDOMn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotDOMmeanNorm.L3Mn.cumsum(),
                x = pivotDOMmeanNorm.index,
                name="L3Mn"))
            stagDOMn.add_trace(go.Scatter(
                mode = "lines",
                y = pivotDOMmeanNorm.LMn.cumsum(),
                x = pivotDOMmeanNorm.index,
                name="LMn"))

            stagDOMn.update_xaxes(
                    tickangle = 90,
                    title_text = "trend mensile",
                    title_font = {"size": 20},
                    title_standoff = 10)

            st.plotly_chart(stagDOMn,use_container_width=True)
            
            DOMn = go.Figure()
            DOMn.add_trace(go.Bar(
                y = pivotDOMmeanNorm.totaln,
                x = pivotDOMmeanNorm.index,
                name="totaln"))
            DOMn.add_trace(go.Bar(
                y = pivotDOMmeanNorm.LYn,
                x = pivotDOMmeanNorm.index,
                name="LYn"))
            DOMn.add_trace(go.Bar(
                y = pivotDOMmeanNorm.L3Mn,
                x = pivotDOMmeanNorm.index,
                name="L3Mn"))
            DOMn.add_trace(go.Bar(
                y = pivotDOMmeanNorm.LMn,
                x = pivotDOMmeanNorm.index,
                name="LMn"))

            DOMn.update_xaxes(
                    tickangle = 90,
                    title_text = "dipendenza giorni mensile",
                    title_font = {"size": 20},
                    title_standoff = 10)

            st.plotly_chart(DOMn,use_container_width=True)
            
            
    elif pagina == 'analisi swing':
        st.title('Analisi Swing')   

        #df=imp.import_mt5("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
        zig = st.slider('ampiezza swing', 0.000, 0.100, 0.010)
        X=df.close
        X=X.astype('double')
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
                    'text': 'swing '+ticker,
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})

        st.plotly_chart(swing,use_container_width=True)

        dfswing=pd.DataFrame(df[start:stop].zigzag)
        dfswing.dropna(axis=0,inplace=True)
        dfswing['abs']=abs(dfswing.zigzag.shift(1)-dfswing.zigzag) 
        dfswing.dropna(axis=0,inplace=True)
        #media=np.mean(dfswing.abs)
        
        #st.dataframe(swingdescr)
        st.subheader('andamento nel tempo swing maggiori di '+str(zig*100)+'% - '+ticker)
        swing = px.scatter(dfswing,x=dfswing.index, y='abs')
        swing.update_xaxes(
                    title_text = "ampiezza swing maggiori di "+str(zig*100)+'%',
                    title_font = {"size": 15},
                    title_standoff = 10)
        st.plotly_chart(swing,use_container_width=False )

        st.subheader('distribuzione swing maggiori di '+str(zig*100)+'% - '+ticker)
        swingdistr=px.histogram(dfswing, x="abs",histnorm='probability')
        swingdistr.update_xaxes(
                    title_text = "distribuzione swing maggiori di "+str(zig*100)+'%',
                    title_font = {"size": 15},
                    title_standoff = 10)
        st.plotly_chart(swingdistr,use_container_width=False )
        
        swingdescr=pd.DataFrame(dfswing['abs'].describe([0.01,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99]))
        st.subheader('valori statistici swing maggiori di '+str(zig*100)+'% - '+ticker)
        st.table(swingdescr.iloc[1:3])
        
        #swingdistr2=px.histogram(dfswing, x="abs",cumulative_enabled=True)
        swingdistrcum=go.Figure(data=[go.Histogram(x=dfswing['abs'],histnorm='probability density', cumulative_enabled=True)])

        swingdistrcum.update_xaxes(
                    title_text = "distribuzione cumulativa swing maggiori di "+str(zig*100)+'%',
                    title_font = {"size": 15},
                    title_standoff = 10)
        st.plotly_chart(swingdistrcum,use_container_width=False)
        
        st.subheader('percentili swing maggiori di '+str(zig*100)+'% - '+ticker)
        st.table(swingdescr.iloc[4:17])

        #go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True)])


else:
    st.title('Backtest')

    initial_capital=st.number_input('capitale iniziale',value=10)
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    dfriep=pd.DataFrame(columns=["n_op", "date_time","type","n_ord","lots","entry_price",
                                 "sl","tp","result","cumulative","cumreturn","name"])
    for uploaded_file in uploaded_files:
        tabella = pd.read_csv(uploaded_file, delimiter="\t", names=[0,1,2,3,4,5,6,7,8,9])
        df=tabella.rename(columns={0: "n_op", 1: "date_time",
                          2: "type", 3: "n_ord",
                          4: "lots", 5: "entry_price",
                          6: "sl", 7: "tp",8: "result",
                          9: "cumulative"})
        df.set_index(df.date_time, inplace=True)
        df["cumreturn"]=df.result.cumsum()
        df['name']=uploaded_file.name
        dfriep=dfriep.append(df)

    dfriep.set_index(dfriep.date_time, inplace=True)
    dfriep.index = pd.to_datetime(dfriep.index)
    dfriep.sort_index(inplace=True)
    dfriep['cumulativeGLOB']=dfriep.result.cumsum()
    dfriep['year']=dfriep.index.year
    dfriep['month']=dfriep.index.month
    dfriep['pct']=dfriep.result/dfriep.cumulative.shift(1)

    pagina = st.sidebar.radio(
         "funzionalità",
         ('Riepilogo_equity', 'Montecarlo','Confronto'))
    if pagina=='Riepilogo_equity':
        st.header('Report strategia')
        equity = go.Figure()
        equity.add_trace(go.Scatter(
            mode = "lines",
            y = dfriep.cumulativeGLOB,
            x = dfriep.index,
            name="report",
            connectgaps=True))
        equity.update_xaxes(
            title_text = "report strategia",
            title_font = {"size": 15},
            title_standoff = 10)
        st.plotly_chart(equity,use_container_width=False )

        pivotAnno = pd.pivot_table(dfriep, values='result', index=['year'], aggfunc=np.sum)


        reportAnno = px.histogram(dfriep, x="year", y="result",
                                  color='name', barmode='group',
                                  height=400)

        reportAnno.update_xaxes(
            title_text = "report per anno",
            title_font = {"size": 15},
            title_standoff = 10)
        st.plotly_chart(reportAnno,use_container_width=False )

        distrib_result = px.scatter(dfriep, y=dfriep.result, color='name')
        distrib_result.update_xaxes(
            title_text = "distribuzione ritorni",
            title_font = {"size": 15},
            title_standoff = 10)
        st.plotly_chart(distrib_result,use_container_width=False ) 

        singole_strat = px.line(dfriep, x=dfriep.index, y='cumreturn', color='name')
        singole_strat.update_xaxes(
            title_text = "report strategie divise",
            title_font = {"size": 15},
            title_standoff = 10)
        st.plotly_chart(singole_strat,use_container_width=False )
 
        if len(uploaded_files) == 0:
            st.text("nessun dato")
        else:
            operazioni=sum(np.where(((dfriep.type=='buy')|(dfriep.type=='sell')),1,0))
            st.text("Profit: "+str(bt.profit(dfriep.cumulativeGLOB)))
            st.text("ROI: "+str(round((bt.profit(dfriep.cumulativeGLOB)/initial_capital*100),2))+'%')
            st.text("operations: " + str(operazioni))
            result=dfriep[dfriep.result!=0].result
            st.text("average trade: " + str(bt.avg_trade(result)))   
            st.text("Profit Factor: "+ str(bt.profit_factor(result)))
            st.text("Gross Profit: "+ str(bt.gross_profit(result)))
            st.text("Gross Loss: " + str(bt.gross_loss(result)))
            st.text("Percent Winning Trades: "+ str(bt.percent_win(result)))
            st.text("Percent Losing Trades: "+ str(100 - bt.percent_win(result)))
            st.text("Reward Risk Ratio: "+ str(bt.reward_risk_ratio(result)))
            st.text("Max Gain: "+ str(bt.max_gain(result))+ " in date "+ str(bt.max_gain_date(result)))
            st.text("Average Gain: "+ str(bt.avg_gain(result)))
            st.text("Max Loss: "+ str(bt.max_loss(result))+ " in date "+ str(bt.max_loss_date(result)))
            st.text("Average Loss: "+ str(bt.avg_loss(result)))
            st.text("Avg Closed Draw Down: "+ str(bt.avgdrawdown_nozero(dfriep.cumulativeGLOB)))
            st.text("Max Closed Draw Down: "+ str(bt.max_draw_down(dfriep.cumulativeGLOB)))
            st.text("Max Closed Draw Down %: "+ str(round((bt.max_draw_down(dfriep.cumulativeGLOB)/initial_capital*100),2))+'%')
            st.text("Avg Delay Between Peaks: "+ str(bt.avg_delay_between_peaks(dfriep.cumulativeGLOB)))
            st.text("Max Delay Between Peaks: "+ str(bt.max_delay_between_peaks(dfriep.cumulativeGLOB)))


    elif pagina=='Montecarlo':
        st.header("Montecarlo")
        if len(uploaded_files) == 0:
            st.text("nessun dato")
        else:
            Costs = 0
            PercentageNoiseAddiction = 0
            OperationsPercentage = 100
            NumberOfShuffles = 100
            operations=dfriep.result.copy()

            original_operations = operations

            if Costs != 0:
                original_operations = costs_adder(operations, Costs)

            if PercentageNoiseAddiction != 0:
                original_operations = noise_adder(operations, PercentageNoiseAddiction)

            original_equity = original_operations.cumsum()
            original_profit = round(original_operations.sum(),2)
            original_drawdown = bt.drawdown(original_operations)
            original_max_drawdown = round(original_drawdown.min(),2)

            if OperationsPercentage == 100:
                matrix_of_equities = pd.DataFrame(original_equity).reset_index()
                matrix_of_equities.drop(matrix_of_equities.columns[0], axis=1, inplace=True)
                matrix_of_equities.columns = ["original"]
                matrix_of_drawdowns = pd.DataFrame(original_drawdown).reset_index()
                matrix_of_drawdowns.drop(matrix_of_drawdowns.columns[0], axis=1, inplace=True)
                matrix_of_drawdowns.columns = ["original"]
            else:
                cutnumber = int(len(operations) * int(OperationsPercentage) / 100)
                matrix_of_equities = pd.DataFrame(original_equity[:cutnumber]).reset_index()
                matrix_of_equities.drop(matrix_of_equities.columns[0], axis=1, inplace=True)
                matrix_of_equities.columns = ["original"]
                matrix_of_drawdowns = pd.DataFrame(original_drawdown[:cutnumber]).reset_index()
                matrix_of_drawdowns.drop(matrix_of_drawdowns.columns[0], axis=1, inplace=True)
                matrix_of_drawdowns.columns = ["original"]

            max_drawdown_list = []
            fraction = OperationsPercentage / 100
            i = 0
            start = dt.datetime.now()
            while i < NumberOfShuffles:
                my_permutation = original_operations.sample(frac = fraction).reset_index(drop = True)
                my_permutation = pd.Series(my_permutation)
                new_equity = my_permutation.cumsum()
                new_drawdown = bt.drawdown(new_equity)
                matrix_of_equities["shuffle_" + str(i + 1)] = new_equity
                matrix_of_drawdowns["shuffle_" + str(i + 1)] = new_drawdown
                max_drawdown_list.append(new_drawdown.min())
                i += 1

            end = dt.datetime.now()
            timespent = end - start
            print("Shuffles executed in:", timespent)
            print("")

            matrix_of_equities.to_csv('matrix_of_equities.csv', sep=',', decimal='.', index=False)
            matrix_of_drawdowns.to_csv('matrix_of_drawdowns.csv', sep=',', decimal='.', index=False)

            worst_drawdown = round(matrix_of_drawdowns.min().min(),2)
            worst_drawdown_index = matrix_of_drawdowns.min().idxmin(axis=1)
            worst_drawdown_profit = round(matrix_of_equities[worst_drawdown_index]\
                                                            [matrix_of_equities[worst_drawdown_index].count()-1],2)

            best_drawdown = round(matrix_of_drawdowns.min().max(),2)
            best_drawdown_index = matrix_of_drawdowns.min().idxmax(axis=1)
            best_drawdown_profit = round(matrix_of_equities[best_drawdown_index]\
                                                           [matrix_of_equities[best_drawdown_index].count()-1],2)

            st.text("Original Profit/Loss: "+str(original_profit))
            st.text("Original Max Draw Down: "+ str(original_max_drawdown))
            st.text("Worst Equity Index: "+ str(worst_drawdown_index))
            st.text("Worst Equity Profit/Loss: "+ str(worst_drawdown_profit))
            st.text("Worst Equity Max Draw Down: "+ str(worst_drawdown))
            st.text("Best Equity Index: "+ str(best_drawdown_index))
            st.text("Best Equity Profit/Loss: "+ str(best_drawdown_profit))
            st.text("Best Equity Max Draw Down: "+ str(best_drawdown))

            MaxDrawDown95 = round(np.percentile(max_drawdown_list, 5),2)
            riskfactor95 = round(np.percentile(max_drawdown_list, 5) / original_max_drawdown, 2)
            riskfactor = round(min(max_drawdown_list) / original_max_drawdown, 2)

            st.text("95 Percentile Montecarlo Max Draw Down: "+ str(MaxDrawDown95))
            st.text("Montecarlo Risk Factor on 95 Percentile Probability: "+str(riskfactor95))
            st.text("Worst Montecarlo Max Draw Down: "+str(round(min(max_drawdown_list),2)))
            st.text("Montecarlo Risk Factor on Max Draw Down: "+str(riskfactor))


            montecarlo = px.line(matrix_of_equities)
            st.plotly_chart(montecarlo,use_container_width=False )

    else: 
        if len(uploaded_files) == 0:
            st.text("nessun dato")
        else:
            st.header("Confronto strategie")
            uploaded_files_corr = st.file_uploader("Choose a CSV file", accept_multiple_files=True, key="b")
            dfcorr=pd.DataFrame(columns=["n_op", "date_time","type","n_ord","lots","entry_price","sl",
                                         "tp","result","cumulative","cumreturn","name"])
            for uploaded_file_corr in uploaded_files_corr:
                tabella = pd.read_csv(uploaded_file_corr, delimiter="\t", names=[0,1,2,3,4,5,6,7,8,9])
                df=tabella.rename(columns={0: "n_op", 1: "date_time",
                                  2: "type", 3: "n_ord",
                                  4: "lots", 5: "entry_price",
                                  6: "sl", 7: "tp",8: "result",
                                  9: "cumulative"})
                df.set_index(df.date_time, inplace=True)
                df["cumreturn"]=df.result.cumsum()
                df['name']=uploaded_file.name
                dfcorr=dfcorr.append(df)
            
            dfcorr.set_index(dfcorr.date_time, inplace=True)
            dfcorr.index = pd.to_datetime(dfcorr.index)
            dfcorr.sort_index(inplace=True)
            dfcorr['cumulativeGLOB']=dfcorr.result.cumsum()
            dfcorr['year']=dfcorr.index.year
            dfcorr['month']=dfcorr.index.month
            dfcorr['pct']=dfcorr.result/dfriep.cumulative.shift(1)


            correlazione=dfriep['cumreturn'].corr(dfcorr['cumreturn'])
            st.text("correlazione strategie:  "+str(correlazione))
            st.subheader("strategia 1:")
            operazioni=sum(np.where(((dfriep.type=='buy')|(dfriep.type=='sell')),1,0))
            st.text("Profit: "+str(bt.profit(dfriep.cumulativeGLOB)))
            st.text("ROI: "+str(round((bt.profit(dfriep.cumulativeGLOB)/initial_capital*100),2))+'%')
            st.text("operations: " + str(operazioni))
            result=dfriep[dfriep.result!=0].result
            st.text("average trade: " + str(bt.avg_trade(result)))  
            st.text("Max Closed Draw Down: "+ str(bt.max_draw_down(dfriep.cumulativeGLOB)))
            st.text("Max Closed Draw Down %: "+ str(round((bt.max_draw_down(dfriep.cumulativeGLOB)/initial_capital*100),2))+'%')

            st.subheader("strategia 2:")
            if len(uploaded_files_corr) == 0:
                st.text("nessun dato")
            else:
                operazioni2=sum(np.where(((dfcorr.type=='buy')|(dfcorr.type=='sell')),1,0))
                st.text("Profit: "+str(bt.profit(dfcorr.cumulativeGLOB)))
                st.text("ROI: "+str(round((bt.profit(dfcorr.cumulativeGLOB)/initial_capital*100),2))+'%')
                st.text("operations: " + str(operazioni2))
                result2=dfcorr[dfcorr.result!=0].result
                st.text("average trade: " + str(bt.avg_trade(result2)))   
                st.text("Max Closed Draw Down: "+ str(bt.max_draw_down(dfcorr.cumulativeGLOB)))
                st.text("Max Closed Draw Down %: "+ str(round((bt.max_draw_down(dfcorr.cumulativeGLOB)/initial_capital*100),2))+'%')

    ticker = st.sidebar.selectbox('scegli strumento', symbols)
    #df=imp.import_mt5(path+"/dati_input/"+ticker+".csv")
    df=imp.import_mt4(path+"/dati_input/"+ticker+".csv")
    #df=imp.import_mt4("Documents/Python/Python_Analisi_Quantitativa/WebAppStream/dati_input/"+ticker+".csv")
    df['HOD']=df.index.hour
    df['minute']=df.index.minute
    df['body']=df.close-df.open
    df['candela']=df.index.time
    df['range']=df.high-df.low
    df['rangeperc']=(df.range/df.close.shift(1))*100
    df['c1-c']=df.close-df.close.shift(1)
    df['body']=df.close-df.open
    df['bodyabs']=abs(df.close-df.open)
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
#    df['sessione']=np.where((df.HOD<8),"asia", np.where(((df.HOD>7) & (df.HOD<15)),"europa", "usa"))
    

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

    inizio=str(df.index.min())
    fine=str(df.index.max())
    startDate=inizio[0:4]+inizio[5:7]+inizio[8:10]
    endDate=fine[0:4]+fine[5:7]+fine[8:10]
    year=str((df.index.max().year))
    month=str((df.index.max().month))
    
    start = st.sidebar.date_input(
         "data inizio",
         dt.date(inizio_serieY, inizio_serieM, inizio_serieD))


    stop = st.sidebar.date_input(
         "data fine",
         dt.date(fine_serieY, fine_serieM, fine_serieD))
    
    dfD=pd.DataFrame(df['open'].resample('D').first())
    dfD['high']=df['high'].resample('D').max()
    dfD['low']=df['low'].resample('D').min()
    dfD['close']=df['close'].resample('D').last()
    dfD['volume']=df['volume'].resample('D').sum()
    dfD['closeperc']=dfD.close.pct_change()*100
    dfD['body']=abs(dfD.close-dfD.open)
    dfD['range']=dfD.high-dfD.low
    dfD['rangeperc']=dfD.range.pct_change()
    dfD['ATRfast']=clc.SMA(dfD.range,5)*10
    #dfD['ATRslow']=clc.SMA(dfD.range,200)*10
    
    vola = go.Figure()
    vola.add_trace(go.Scatter(
        mode = "lines",
        y = dfD[start:stop].close,
        x = dfD[start:stop].index,
        #name="prezzo",
        connectgaps=True))
    
    vola.update_xaxes(
                title_text = "volatilità e prezzo",
                title_font = {"size": 15},
                title_standoff = 10)
    st.plotly_chart(vola,use_container_width=False )

  









    # In[ ]:



