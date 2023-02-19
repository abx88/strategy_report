#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import librerie.backtest as bt
import librerie.calcolivari as clc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
import streamlit as st
from plotly import __version__
print("Plotly version: ",__version__)
import os

st.set_page_config(
    page_title="StrategyReportAB",
    layout="wide",
    initial_sidebar_state="expanded")


st.title('Report strategia')

initial_capital=st.number_input('capitale iniziale',value=10)

uploaded_files = st.file_uploader("inserire file CSV con i risultati di una strategia", accept_multiple_files=True)
dfriep=pd.DataFrame(columns=["n_op", "date_time","type","n_ord","lots","entry_price","sl","tp","result","cumulative","cumreturn","name"])
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
    st.header('Riepilogo equity')
    
    uploaded_instrument = st.file_uploader("Inserire strumento per confronto", accept_multiple_files=True)

    for uploaded_file in uploaded_instrument:
        instrument = str(uploaded_file.name)
       
    if len(uploaded_instrument) == 0:
        st.text("Nessun dato")
        
        equity = go.Figure()
        
        equity.add_trace(go.Scatter(
            mode = "lines",
            y = dfriep.cumulativeGLOB,
            x = dfriep.index,
            name="equity strategia",
            connectgaps=True))
        
        equity.update_xaxes(
            title_text = "report strategia",
            title_font = {"size": 15},
            title_standoff = 10)
        st.plotly_chart(equity,use_container_width=False )
        
        
    else:
     
        new_column_names = ["date","time", "open","high","low","close","volume"]
        dfinstrument = pd.read_csv(uploaded_instrument[0], delimiter=",", names=new_column_names)
        dfinstrument.set_index(dfinstrument.date, inplace=True)
        dfinstrument.index = pd.to_datetime(dfinstrument.index)
        dfinstrument.sort_index(inplace=True)
        
        
        inizio_serie=str(dfinstrument.index.min())
        inizio_serieY=int(dfinstrument.index.min().year)
        inizio_serieM=int(dfinstrument.index.min().month)
        inizio_serieD=int(dfinstrumentf.index.min().day)
        fine_serie=str(dfinstrument.index.max())
        fine_serieY=int(dfinstrument.index.max().year)
        fine_serieM=int(dfinstrument.index.max().month)
        fine_serieD=int(dfinstrument.index.max().day)

        st.sidebar.text("INIZIO SERIE "+inizio_serie)
        st.sidebar.text("FINE SERIE "+fine_serie)

        inizio=str(dfinstrument.index.min())
        fine=str(dfinstrument.index.max())
        startDate=inizio[0:4]+inizio[5:7]+inizio[8:10]
        endDate=fine[0:4]+fine[5:7]+fine[8:10]
        year=str((dfinstrument.index.max().year))
        month=str((dfinstrument.index.max().month))
        
        
        start = st.sidebar.date_input(
             "data inizio",
             dt.date(inizio_serieY, inizio_serieM, inizio_serieD))


        stop = st.sidebar.date_input(
             "data fine",
             dt.date(fine_serieY, fine_serieM, fine_serieD))
        
        
        
        
        equity = go.Figure()
        equity.add_trace(go.Scatter(
            mode = "lines",
            y = dfriep.cumulativeGLOB,
            x = dfriep.index,
            name="equity strategia",
            connectgaps=True))
        equity.add_trace(go.Scatter(
            mode = "lines",
            y = dfinstrument.close,
            x = dfinstrument.index,
            name = instrument,
            connectgaps=True,
            yaxis="y2"))
        equity.update_xaxes(
            title_text = "report strategia",
            title_font = {"size": 15},
            title_standoff = 10)
        equity.update_layout(
            yaxis2=dict(
                overlaying='y',
                side='right'))
          
        st.plotly_chart(equity,use_container_width=False)


  


    if len(uploaded_files) > 0:
        st.subheader("risultati per anno suddivisi per strategie")        
        reportAnno = px.histogram(dfriep, x="year", y="result",
                                  color='name', barmode='group',
                                  height=400)
        reportAnno.update_xaxes(
            title_text = "report per anno",
            title_font = {"size": 15},
            title_standoff = 10)
        st.plotly_chart(reportAnno,use_container_width=False )
        
        pivotAnno = pd.pivot_table(dfriep, values='result', index=['year'], columns=['name'], aggfunc=np.sum)
        st.dataframe(pivotAnno.style.highlight_max(axis=1))

    
    if len(uploaded_files) > 0:
        st.subheader("risultati cumulativi suddivisi per anno e mese")
        reportAnnoMese=px.density_heatmap(dfriep, x="month", y="year",z="result", nbinsx=12, nbinsy=20)

        reportAnnoMese.update_xaxes(
            title_text = "report per anno e mese",
            title_font = {"size": 15},
            title_standoff = 10)
        st.plotly_chart(reportAnnoMese,use_container_width=False )
        
        pivotAnnoMese = pd.pivot_table(dfriep, values='result', index=['year'], columns=['month'], aggfunc=np.sum)
        st.dataframe(pivotAnnoMese.style.highlight_max(axis=1))
    
           
    singole_strat = px.line(dfriep, x=dfriep.index, y='cumreturn', color='name')
    singole_strat.update_xaxes(
        title_text = "report strategie divise",
        title_font = {"size": 15},
        title_standoff = 10)
    st.plotly_chart(singole_strat,use_container_width=False )
    distrib_result = px.scatter(dfriep, y=dfriep.result, color='name')
    distrib_result.update_xaxes(
        title_text = "distribuzione ritorni",
        title_font = {"size": 15},
        title_standoff = 10)
    st.plotly_chart(distrib_result,use_container_width=False )
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
        st.text("Avg Draw Down (ad operazioni chiuse): "+ str(bt.avgdrawdown_nozero(dfriep.cumulativeGLOB)))
        st.text("Max Draw Down (ad operazioni chiuse): "+ str(bt.max_draw_down(dfriep.cumulativeGLOB)))
        st.text("Avg Delay Between Peaks(trade): "+ str(bt.avg_delay_between_peaks(dfriep.cumulativeGLOB)))
        st.text("Max Delay Between Peaks(trade): "+ str(bt.max_delay_between_peaks(dfriep.cumulativeGLOB)))
    
    
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
        #original_drawdown = bt.max_draw_down(original_operations)
        #original_max_drawdown = round(original_drawdown.min(),2)
        original_max_drawdown = bt.max_draw_down(dfriep.cumulativeGLOB)


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
            #new_drawdown = bt.max_draw_down(new_equity)
            matrix_of_equities["shuffle_" + str(i + 1)] = new_equity
            matrix_of_drawdowns["shuffle_" + str(i + 1)] = new_drawdown
            max_drawdown_list.append(new_drawdown.min())
            i += 1

        end = dt.datetime.now()
        timespent = end - start
        print("Shuffles executed in:", timespent)
        print("")

        #matrix_of_equities.to_csv('matrix_of_equities.csv', sep=',', decimal='.', index=False)
        #matrix_of_drawdowns.to_csv('matrix_of_drawdowns.csv', sep=',', decimal='.', index=False)

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
        #st.text("Worst Montecarlo Max Draw Down: "+str(round(min(max_drawdown_list),2)))
        st.text("Worst Montecarlo Max Draw Down: "+str(worst_drawdown))
        st.text("Montecarlo Risk Factor on Max Draw Down: "+str(riskfactor))


        montecarlo = px.line(matrix_of_equities)
        st.plotly_chart(montecarlo,use_container_width=False )

else: 
    st.header("Confronto strategie")
    uploaded_files_corr = st.file_uploader("Choose a CSV file", accept_multiple_files=True, key="b")
    dfcorr=pd.DataFrame(columns=["n_op", "date_time","type","n_ord","lots","entry_price","sl",
                                 "tp","result","cumulative","cumreturn","name"])
    for uploaded_file_corr in uploaded_files_corr:
        #bytes_data = uploaded_file.read()
        #st.write("filename:", uploaded_file.name)
        tabella = pd.read_csv(uploaded_file_corr, delimiter="\t", names=[0,1,2,3,4,5,6,7,8,9])
        df=tabella.rename(columns={0: "n_op", 1: "date_time",
                          2: "type", 3: "n_ord",
                          4: "lots", 5: "entry_price",
                          6: "sl", 7: "tp",8: "result",
                          9: "cumulative"})
        df.set_index(df.date_time, inplace=True)
        #df.drop("date_time", axis=1, inplace=True)
        df["cumreturn"]=df.result.cumsum()
        #df["net_cumulative"]=
        #df.drop("cumulative",axis=1,inplace=True)
        #df.dropna(axis=0, inplace=True)
        df['name']=uploaded_file.name
        dfcorr=dfcorr.append(df)
    dfcorr.set_index(dfcorr.date_time, inplace=True)
    dfcorr.index = pd.to_datetime(dfcorr.index)
    dfcorr.sort_index(inplace=True)
    dfcorr['cumulativeGLOB']=dfcorr.result.cumsum()
    dfcorr['year']=dfcorr.index.year
    dfcorr['month']=dfcorr.index.month
    dfcorr['pct']=dfcorr.result/dfcorr.cumulative.shift(1)
    
    if len(uploaded_files) == 0:
        st.text("nessun dato")
    else: 
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
        #st.text("Max Closed Draw Down % su capitale iniziale: "+ str(round((bt.max_draw_down(dfriep.cumulativeGLOB)/initial_capital*100),2))+'%')

    if len(uploaded_files_corr) == 0:
        st.text("nessun dato")
    else:
        st.subheader("strategia 2:")
        operazioni2=sum(np.where(((dfcorr.type=='buy')|(dfcorr.type=='sell')),1,0))
        st.text("Profit: "+str(bt.profit(dfcorr.cumulativeGLOB)))
        st.text("ROI: "+str(round((bt.profit(dfcorr.cumulativeGLOB)/initial_capital*100),2))+'%')
        st.text("operations: " + str(operazioni2))
        result2=dfcorr[dfcorr.result!=0].result
        st.text("average trade: " + str(bt.avg_trade(result2)))   
        st.text("Max Closed Draw Down: "+ str(bt.max_draw_down(dfcorr.cumulativeGLOB)))
        #st.text("Max Closed Draw Down % su capitale iniziale: "+ str(round((bt.max_draw_down(dfcorr.cumulativeGLOB)/initial_capital*100),2))+'%')
        


    

    

    
    
    # In[ ]:




