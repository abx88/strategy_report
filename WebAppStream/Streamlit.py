# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 19:48:19 2022

@author: assav
"""

import streamlit as st
import os
import pandas as pd
import numpy as np
import datetime 
from datetime import time
import streamlit as st
import plotly.graph_objects as go
import altair as alt
from vega_datasets import data

#st.set_page_config(layout="wide")

#CACHE
@st.cache
def expensive_computation(a, b):
   # time.sleep(1)  # 👈 This makes the function take 2s to run
    return a * b
a = 2
b = 21
res = expensive_computation(a, b)
st.sidebar.write("Result:", res)

#TITLE
st.sidebar.title('Seasonals app')

#LAYOUT
col1,col2 = st.columns((0.7,4.3))

#UPLOAD FILE CSV
#uploaded_file = col1.file_uploader("Upload your input CSV file", type=["csv"])
#if not uploaded_file:
    #st.stop()
#df = pd.read_csv(uploaded_file)

#path = "Documents/Python/Python_Analisi_Quantitativa/WebAppStream"

#instruments = pd.read_csv(path+"/dati_input/strumenti.csv")
#ticker = st.sidebar.selectbox('scegli strumento', symbols)
#df=imp.import_mt5(path+"/dati_input/"+ticker+".csv")
#df=imp.import_mt4(path+"/dati_input/"+ticker+".csv")
    
def file_selector(folder_path='Documents/Python/Python_Analisi_Quantitativa/WebAppStream/Streamlit data'):
    #modificato il path per la mia importazione
    filenames = os.listdir(folder_path)
    selected_filename = st.sidebar.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


filename = file_selector()
st.sidebar.write('You selected `%s`' % filename)

#DATA WRANGLING 
#(modificate righe per la mia importazione)
df = pd.read_csv(filename, delimiter=",")
df['date_time']= df['Date'] + ' ' + df['Time']
df.drop(['Date','Time'], axis=1,inplace=True)
df.set_index('date_time', inplace=True)
df.index = pd.to_datetime(df.index)#occorre per convertire in datetime la data
df.columns=['Open','High','Low','Close','Volume']
#df.set_axis(['Date', 'Open', 'High', 'Low', 'Close', 'Volume'], axis=1, inplace=True)
#df = df.set_index(pd.to_datetime(df['Date']))
#df.index = pd.to_datetime(df.index, format='%Y%m%d %H%M%S',  utc=True)
#df.index = df.index.tz_localize(None)
#df.index.rename('date', inplace=True)
#df.drop(['Date'], axis=1, inplace=True)
#df = df.set_index("Date") 
#df.index = pd.to_datetime(df.index, format='%Y%m%d %H%M%S',  utc=True)
#df['time'] = pd.to_datetime(df.index, format=r'%Y-%m-%d_%H%M%S').time

df['Returns'] = df['Close'].pct_change()
df['Close - Close[-1]'] = df['Close'] - df['Close'].shift()
df['Close - Open'] = df['Close'] - df['Open']
df['High - Low'] = df['High'] - df['Low']

#number input tick e valore tick
tick = col1.number_input("importo tick")
tickvalue = col1.number_input("valore tick")
#colonne di calcolo per valore tick
df['$Close-Close[-1]']= ((df['Close - Close[-1]']/tick)* tickvalue)
df['$Close-Open']= ((df['Close - Open']/tick)* tickvalue)
df['$High-Low']= ((df['High - Low']//tick)* tickvalue)

df['Date'] = df.index.date
df['HH:MM'] = df.index.time
df['Dayofweek'] = df.index.dayofweek
df['Day'] = df.index.day
df['Month'] = df.index.month
df['Year'] = df.index.year
df['Dayofyear'] = df.index.dayofyear



#METRICS
stats = col1.selectbox(
     'Metrics',
     ('Returns', 'Close - Close[-1]', 
      '$Close-Close[-1]', 'Close - Open', 
      '$Close-Open','High - Low',
      '$High-Low', 
      'High', 'Low', 'Volume'))

#if (stats == 'Returns'):
    #df['Returns'] = df['Close'].pct_change()

#if (stats == 'Close - Close[-1]'):
    #df['Close - Close[-1]'] = df['Close'] - df['Close'].shift()
    
#if (stats == 'Close - Open'):
    #df['Close - Open'] = df['Close'] - df['Open']
    
#if (stats == 'High - Low'):
    #df['High - Low'] = df['High'] - df['Low']
    

#STATS
statistics = col1.selectbox(
     'Stats',
     ('mean','sum','SD'))


df['Date'] = df.index.date
df['HH:MM'] = df.index.time
df['Dayofweek'] = df.index.dayofweek
df['Day'] = df.index.day
df['Month'] = df.index.month
df['Year'] = df.index.year
df['Dayofyear'] = df.index.dayofyear

#SLIDER YEARS
start = df.index.min()
end = df.index.max()
slider = st.sidebar.select_slider("Years range:", options=df.index.date, value=(start, end))
startyear, endyear = list(slider)[0], list(slider)[1]
df2 = df[((df.index.date >= startyear) & (df.index.date <= endyear))]



#SLIDER HOURS
start_time = datetime.time(00,0,0)
end_time = datetime.time(23,59,0)
#slider2 = col1.slider("Hours range:", min_value = start_time, max_value = end_time, value=(start_time, end_time))
slider2 = st.sidebar.slider("Hours range:", min_value = start_time, max_value = end_time, step = pd.Timedelta(minutes=1), value=(time(00, 00), time(23, 59)))
#startday, endday = list(slider2)[0], list(slider2)[1]
startday, endday = slider2[0], slider2[1]
df2 =  df2.between_time(startday,endday) 

#MESI DELL'ANNO
st.sidebar.text('Months of year')

gennaio = st.sidebar.checkbox("January", value=True)
febbraio = st.sidebar.checkbox("February", value=True)
marzo = st.sidebar.checkbox("March", value=True)
aprile = st.sidebar.checkbox("April", value=True)
maggio = st.sidebar.checkbox("May", value=True)
giugno = st.sidebar.checkbox("June", value=True)
luglio = st.sidebar.checkbox("July", value=True)
agosto = st.sidebar.checkbox("August", value=True)
settembre = st.sidebar.checkbox("September", value=True)
ottobre = st.sidebar.checkbox("October", value=True)
novembre = st.sidebar.checkbox("November", value=True)
dicembre = st.sidebar.checkbox("December", value=True)

if not gennaio:
    df2 = df2.drop(df2.loc[df2.index.month==1].index)
    
if not febbraio:
    df2 = df2.drop(df2.loc[df2.index.month==2].index)

if not marzo:
    df2 = df2.drop(df2.loc[df2.index.month==3].index)
    
if not aprile:
    df2 = df2.drop(df2.loc[df2.index.month==4].index)
    
if not maggio:
    df2 = df2.drop(df2.loc[df2.index.month==5].index)
    
if not giugno:
    df2 = df2.drop(df2.loc[df2.index.month==6].index)
    
if not luglio:
    df2 = df2.drop(df2.loc[df2.index.month==7].index)

if not agosto:
    df2 = df2.drop(df2.loc[df2.index.month==8].index)
    
if not settembre:
    df2 = df2.drop(df2.loc[df2.index.month==9].index)
    
if not ottobre:
    df2 = df2.drop(df2.loc[df2.index.month==10].index)
  
if not novembre:
    df2 = df2.drop(df2.loc[df2.index.month==11].index)
    
if not dicembre:
    df2 = df2.drop(df2.loc[df2.index.month==12].index)
    
#GIORNI DEL MESE
st.sidebar.text('Days of month')
day1 = st.sidebar.checkbox("1", value=True)
day2 = st.sidebar.checkbox("2", value=True)
day3 = st.sidebar.checkbox("3", value=True)
day4 = st.sidebar.checkbox("4", value=True)
day5 = st.sidebar.checkbox("5", value=True)
day6 = st.sidebar.checkbox("6", value=True)
day7 = st.sidebar.checkbox("7", value=True)
day8 = st.sidebar.checkbox("8", value=True)
day9 = st.sidebar.checkbox("9", value=True)
day10 = st.sidebar.checkbox("10", value=True)
day11 = st.sidebar.checkbox("11", value=True)
day12 = st.sidebar.checkbox("12", value=True)
day13 = st.sidebar.checkbox("13", value=True)
day14 = st.sidebar.checkbox("14", value=True)
day15 = st.sidebar.checkbox("15", value=True)
day16 = st.sidebar.checkbox("16", value=True)
day17 = st.sidebar.checkbox("17", value=True)
day18 = st.sidebar.checkbox("18", value=True)
day19 = st.sidebar.checkbox("19", value=True)
day20 = st.sidebar.checkbox("20", value=True)
day21 = st.sidebar.checkbox("21", value=True)
day22 = st.sidebar.checkbox("22", value=True)
day23 = st.sidebar.checkbox("23", value=True)
day24 = st.sidebar.checkbox("24", value=True)
day25 = st.sidebar.checkbox("25", value=True)
day26 = st.sidebar.checkbox("26", value=True)
day27 = st.sidebar.checkbox("27", value=True)
day28 = st.sidebar.checkbox("28", value=True)
day29 = st.sidebar.checkbox("29", value=True)
day30 = st.sidebar.checkbox("30", value=True)
day31 = st.sidebar.checkbox("31", value=True)

if not day1:
    df2 = df2.drop(df2.loc[df2.index.day==1].index)
    
if not day2:
    df2 = df2.drop(df2.loc[df2.index.day==2].index)

if not day3:
    df2 = df2.drop(df2.loc[df2.index.day==3].index)
    
if not day4:
    df2 = df2.drop(df2.loc[df2.index.day==4].index)

if not day5:
    df2 = df2.drop(df2.loc[df2.index.day==5].index)
    
if not day6:
    df2 = df2.drop(df2.loc[df2.index.day==6].index)

if not day7:
    df2 = df2.drop(df2.loc[df2.index.day==7].index)
    
if not day8:
    df2 = df2.drop(df2.loc[df2.index.day==8].index)

if not day9:
    df2 = df2.drop(df2.loc[df2.index.day==9].index)
    
if not day10:
    df2 = df2.drop(df2.loc[df2.index.day==10].index)

if not day11:
    df2 = df2.drop(df2.loc[df2.index.day==11].index)
    
if not day12:
    df2 = df2.drop(df2.loc[df2.index.day==12].index)

if not day13:
    df2 = df2.drop(df2.loc[df2.index.day==13].index)
    
if not day14:
    df2 = df2.drop(df2.loc[df2.index.day==14].index)

if not day15:
    df2 = df2.drop(df2.loc[df2.index.day==15].index)
    
if not day16:
    df2 = df2.drop(df2.loc[df2.index.day==16].index)

if not day17:
    df2 = df2.drop(df2.loc[df2.index.day==17].index)
    
if not day18:
    df2 = df2.drop(df2.loc[df2.index.day==18].index)

if not day19:
    df2 = df2.drop(df2.loc[df2.index.day==19].index)
    
if not day20:
    df2 = df2.drop(df2.loc[df2.index.day==20].index)

if not day21:
    df2 = df2.drop(df2.loc[df2.index.day==21].index)
    
if not day22:
    df2 = df2.drop(df2.loc[df2.index.day==22].index)

if not day23:
    df2 = df2.drop(df2.loc[df2.index.day==23].index)
    
if not day24:
    df2 = df2.drop(df2.loc[df2.index.day==24].index)

if not day25:
    df2 = df2.drop(df2.loc[df2.index.day==25].index)
    
if not day26:
    df2 = df2.drop(df2.loc[df2.index.day==26].index)

if not day27:
    df2 = df2.drop(df2.loc[df2.index.day==27].index)
    
if not day28:
    df2 = df2.drop(df2.loc[df2.index.day==28].index)

if not day29:
    df2 = df2.drop(df2.loc[df2.index.day==29].index)
    
if not day30:
    df2 = df2.drop(df2.loc[df2.index.day==30].index)

if not day31:
    df2 = df2.drop(df2.loc[df2.index.day==31].index)
    

#GIORNI DELLA SETTIMANA
st.sidebar.text('Days of week')
monday = st.sidebar.checkbox("Monday", value=True)
tuesday = st.sidebar.checkbox("Tuesday", value=True)
wednesday = st.sidebar.checkbox("Wednesday", value=True)
thursday = st.sidebar.checkbox("Thursday", value=True)
friday = st.sidebar.checkbox("Friday", value=True)
saturday = st.sidebar.checkbox("Saturday", value=True)
sunday = st.sidebar.checkbox("Sunday", value=True)

if not monday:
    df2 = df2.drop(df2.loc[df2.index.dayofweek==0].index)
    
if not tuesday:
    df2 = df2.drop(df2.loc[df2.index.dayofweek==1].index)
    
if not wednesday:
    df2 = df2.drop(df2.loc[df2.index.dayofweek==2].index)
    
if not thursday:
    df2 = df2.drop(df2.loc[df2.index.dayofweek==3].index)
    
if not friday:
    df2 = df2.drop(df2.loc[df2.index.dayofweek==4].index)
    
if not saturday:
    df2 = df2.drop(df2.loc[df2.index.dayofweek==5].index)
 
if not sunday:
    df2 = df2.drop(df2.loc[df2.index.dayofweek==6].index)


    
#GROUP BY
group = col1.selectbox(
     'Group by',
     ('HH:MM','HH:MM Day of week','HH:MM Day of month','HH:MM Month of year','HH:MM Year','Day','Day, Day of week','Day, Day of month','Day, Month of year','Day of week','Day of year'))

#hh:mm
if (group == 'HH:MM'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=df2.index.time).mean() 
    if (statistics == 'sum'):
       df2 = df2.groupby(by=df2.index.time).sum()
    if (statistics == 'SD'):
       df2 = df2.groupby(by=df2.index.time).std()
       
if (group == 'HH:MM Day of week'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=['HH:MM','Dayofweek']).mean() 
    if (statistics == 'sum'):
       df2 = df2.groupby(by=['HH:MM','Dayofweek']).sum()
    if (statistics == 'SD'):
       df2 = df2.groupby(by=['HH:MM','Dayofweek']).std()
    df2 = df2.unstack(level=-1) 
    df2 = df2[stats]
    column_names = list(df2.columns)
    #column_names[0:8] = ['monday','tuesday','wednesday','Thursday','Friday','Saturday','Sunday']
    df2.columns = column_names
    #df2.columns = df2.columns.droplevel(-1)

if (group == 'HH:MM Day of month'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=['HH:MM','Day']).mean() 
    if (statistics == 'sum'):
       df2 = df2.groupby(by=['HH:MM','Day']).sum()
    if (statistics == 'SD'):
       df2 = df2.groupby(by=['HH:MM','Day']).std()
    df2 = df2.unstack(level=-1) 
    df2 = df2[stats]
    column_names = list(df2.columns)
    df2.columns = column_names

if (group == 'HH:MM Month of year'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=['HH:MM','Month']).mean() 
    if (statistics == 'sum'):
       df2 = df2.groupby(by=['HH:MM','Month']).sum()
    if (statistics == 'SD'):
       df2 = df2.groupby(by=['HH:MM','Month']).std()
    df2 = df2.unstack(level=-1) 
    df2 = df2[stats]
    column_names = list(df2.columns)
    df2.columns = column_names

if (group == 'HH:MM Year'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=['HH:MM','Year']).mean() 
    if (statistics == 'sum'):
       df2 = df2.groupby(by=['HH:MM','Year']).sum()
    if (statistics == 'SD'):
       df2 = df2.groupby(by=['HH:MM','Year']).std()
    df2 = df2.unstack(level=-1) 
    df2 = df2[stats]
    column_names = list(df2.columns)
    df2.columns = column_names

#day
if (group == 'Day'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=df2.index.date).mean()
    if (statistics == 'sum'):
       df2 = df2.groupby(by=df2.index.date).sum()
    if (statistics == 'SD'):
       df2 = df2.groupby(by=df2.index.date).std()

if (group == 'Day, Day of week'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=['Date','Dayofweek']).mean() 
    if (statistics == 'sum'):
       df2 = df2.groupby(by=['Date','Dayofweek']).sum()
    if (statistics == 'SD'):
       df2 = df2.groupby(by=['Date','Dayofweek']).std()
    df2 = df2.unstack(level=-1)
    df2 = df2.interpolate()
    df2 = df2[stats]
    column_names = list(df2.columns)
    df2.columns = column_names

if (group == 'Day, Day of month'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=['Date','Day']).mean() 
    if (statistics == 'sum'):
       df2 = df2.groupby(by=['Date','Day']).sum()
    if (statistics == 'SD'):
       df2 = df2.groupby(by=['Date','Day']).std()
    df2 = df2.unstack(level=-1) 
    df2 = df2.interpolate()
    df2 = df2[stats]
    column_names = list(df2.columns)
    df2.columns = column_names

if (group == 'Day, Month of year'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=['Date','Month']).mean() 
    if (statistics == 'sum'):
       df2 = df2.groupby(by=['Date','Month']).sum()
    if (statistics == 'SD'):
       df2 = df2.groupby(by=['Date','Month']).std()
    df2 = df2.unstack(level=-1) 
    df2 = df2.interpolate()
    df2 = df2[stats]
    column_names = list(df2.columns)
    df2.columns = column_names

if (group == 'Day of week'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=df2.index.dayofweek).mean()
       df2.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if (statistics == 'sum'):
       df2 = df2.groupby(by=df2.index.dayofweek).sum()
       df2.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if (statistics == 'SD'):
       df2 = df2.groupby(by=df2.index.dayofweek).std()
       df2.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

if (group == 'Day of year'):
    if (statistics == 'mean'):
       df2 = df2.groupby(by=df2.index.dayofyear).mean()
    if (statistics == 'sum'):
       df2 = df2.groupby(by=df2.index.dayofyear).sum()
    if (statistics == 'SD'):
       df2 = df2.groupby(by=df2.index.dayofyear).std()

#CUMSUM
cumsum = col1.checkbox("Cumsum", value=False)    
if cumsum:
     df2 = df2.cumsum() 



#PLOT
plot = col1.radio("Chart type", ('Bar','Line'),index=1)

if (plot == 'Bar'):
 if (group == 'HH:MM Day of week') or (group == 'Day, Day of week'):
  import plotly.express as px
  fig = px.bar(df2, x=df2.index, y=df2.columns)
  newnames = {'0':'Monday', '1':'Tuesday', '2':'Wednesday', '3':'Thursday', '4':'Friday', '5':'Saturday', '6':'Sunday'}
  fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                   legendgroup = newnames[t.name],
                                   hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

 elif (group == 'HH:MM Day of month') or (group == 'Day, Day of month'):
  import plotly.express as px
  fig = px.bar(df2, x=df2.index, y=df2.columns)


 elif (group == 'HH:MM Month of year') or (group == 'Day, Month of year'):
  import plotly.express as px
  fig = px.bar(df2, x=df2.index, y=df2.columns)
  newnames = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June', '7':'July', '8':'August', '9':'September', '10':'October', '11':'November', '12':'December'}
  fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                   legendgroup = newnames[t.name],
                                   hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

 elif (group == 'HH:MM Year'):
  import plotly.express as px
  fig = px.bar(df2, x=df2.index, y=df2.columns)
  

 else:
  import plotly.express as px
  fig = px.bar(df2, x=df2.index, y=df2[stats])



if (plot == 'Line'):
 if (group == 'HH:MM Day of week') or (group == 'Day, Day of week'):
  import plotly.express as px
  fig = px.line(df2, x=df2.index, y=df2.columns)
  newnames = {'0':'Monday', '1':'Tuesday', '2':'Wednesday', '3':'Thursday', '4':'Friday', '5':'Saturday', '6':'Sunday'}
  fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                   legendgroup = newnames[t.name],
                                   hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

 elif (group == 'HH:MM Day of month') or (group == 'Day, Day of month'):
  import plotly.express as px
  fig = px.line(df2, x=df2.index, y=df2.columns)


 elif (group == 'HH:MM Month of year') or (group == 'Day, Month of year'):
  import plotly.express as px
  fig = px.line(df2, x=df2.index, y=df2.columns)
  newnames = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June', '7':'July', '8':'August', '9':'September', '10':'October', '11':'November', '12':'December'}
  fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                   legendgroup = newnames[t.name],
                                   hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

 elif (group == 'HH:MM Year'):
  import plotly.express as px
  fig = px.line(df2, x=df2.index, y=df2.columns)
 
 else:
  fig = go.Figure([go.Scatter(x=df2.index, y=df2[stats])])
  
  
fig.layout.template = 'ggplot2'
fig.update_xaxes(showgrid=False, rangeslider_visible=True)
fig.update_yaxes(showgrid=False)
fig.update_layout(yaxis_tickprefix = '$', yaxis_tickformat = ',.')
fig.update_layout(height=800)

plot1 = col2.plotly_chart(fig, height=800, use_container_width=True)


#st.sidebar.line_chart(df2)
#col2.write(df2)
