#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
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
import streamlit as st
from plotly import __version__
print("Plotly version: ",__version__)
init_notebook_mode(connected=True)
import os

# In[6]:
strumento = st.sidebar.text_input('inserisci strumento')
strategia = st.sidebar.text_input('inserisci strategia')

url = "C:/Users/Utente/Desktop/report_strategie"
strumenti = os.listdir(url)
st.caption("STRUMENTI DISPONIBILI:")
st.text(strumenti)
strategie = os.listdir(url+"/"+strumento)
st.caption("STRATEGIE DISPONIBILI:")
st.text(strategie)



file = "/"+strumento+"/"+strategia+".htm"  
st.caption("URL CARTELLA:")
st.text(url+file)

def dfstrategy (url, file):
    tabella = pd.read_html(url+file, skiprows=range(20))
    dftabella=pd.DataFrame(tabella[0])
    df=dftabella.rename(columns={0: "n_op", 1: "date_time",
                      2: "type", 3: "n_ord",
                      4: "lots", 5: "entry_price",
                      6: "sl", 7: "tp",8: "result",
                      9: "cumulative"})
    df.set_index(df.date_time, inplace=True)
    df.dropna(axis=0, inplace=True)
    df['name']=file
    return df
if strategia == "":
    st.text("ATTENZIONE: inserire nome strumento e strategia")
else:
    df=dfstrategy(url,file)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        mode = "lines",
        y = df.cumulative,
        x = df.index,
        name=file,
        connectgaps=True))
    fig.update_xaxes(
                title_text = "report strategia",
                title_font = {"size": 15},
                title_standoff = 10)
    st.plotly_chart(fig,use_container_width=False )

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
dfriep=pd.DataFrame(columns=["n_op", "date_time","type","n_ord","lots","entry_price","sl","tp","result","cumulative","name"])
for uploaded_file in uploaded_files:
    #bytes_data = uploaded_file.read()
    #st.write("filename:", uploaded_file.name)
    tabella = pd.read_csv(uploaded_file, delimiter="\t", names=[0,1,2,3,4,5,6,7,8,9])
    df=tabella.rename(columns={0: "n_op", 1: "date_time",
                      2: "type", 3: "n_ord",
                      4: "lots", 5: "entry_price",
                      6: "sl", 7: "tp",8: "result",
                      9: "cumulative"})
    df.set_index(df.date_time, inplace=True)
    #df.drop("date_time", axis=1, inplace=True)
    df["cumreturn"]=df.result.cumsum()
    #df.drop("cumulative",axis=1,inplace=True)
    #df.dropna(axis=0, inplace=True)
    df['name']=uploaded_file.name
    dfriep=dfriep.append(df)


dfriep.set_index(dfriep.date_time, inplace=True)
dfriep.sort_index(inplace=True)
dfriep['cumulativeGLOB']=dfriep.result.cumsum()
fig = go.Figure()
fig.add_trace(go.Scatter(
    mode = "lines",
    y = dfriep.cumulativeGLOB,
    x = dfriep.index,
    name=file,
    connectgaps=True))
fig.update_xaxes(
        title_text = "report strategia",
        title_font = {"size": 15},
        title_standoff = 10)
st.plotly_chart(fig,use_container_width=False )



# In[ ]:




