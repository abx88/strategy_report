#!/usr/bin/env python
# coding: utf-8

# In[1]:



import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math


    
def crossover(array1, array2):
    return (array1 > array2) & (array1.shift(1) < array2.shift(1))

def crossunder(array1, array2):
    return (array1 < array2) & (array1.shift(1) > array2.shift(1))
    
def marketposition_generator(enter_rules,exit_rules,enter_level,NOME_STRUMENTO,NOME_STRATEGIA):
    """
    Funzione per calcolare il marketposition date due serie di enter_rules and exit_rules
    """
    service_dataframe = pd.DataFrame(index = enter_rules.index)
    service_dataframe['enter_rules'] = enter_rules
    service_dataframe['exit_rules'] = exit_rules
    service_dataframe['entry_price']= enter_level
    status = 0
    mp = []
    for (i, j) in zip(enter_rules, exit_rules):
        if status == 0:
            if i == 1 and j != -1:
                status = 1
        else:
            if j == -1:
                status = 0
        mp.append(status)
        
    service_dataframe['mp_new'] = mp
    service_dataframe.mp_new = service_dataframe.mp_new.shift(1)
    service_dataframe.mp_new.fillna(0)
    service_dataframe.to_csv("trading_system_check\\"+NOME_STRUMENTO+"_"+NOME_STRATEGIA+"_posgen.csv")
    return service_dataframe.mp_new
    
def apply_trading_system(ORDER_TYPE,INSTRUMENT,OPERATION_MONEY,COSTS,imported_dataframe, direction, enter_level, enter_rules, exit_rules,NOME_STRUMENTO,NOME_STRATEGIA):
    dataframe = imported_dataframe.copy()
    dataframe['enter_rules'] = enter_rules.apply(lambda x: 1 if x == True else 0)
    dataframe['exit_rules'] = exit_rules.apply(lambda x: -1 if x == True else 0)
    dataframe["mp"] = marketposition_generator(dataframe.enter_rules,dataframe.exit_rules,enter_level,NOME_STRUMENTO,NOME_STRATEGIA)
    
    if ORDER_TYPE == "market":
        dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & 
                                            (dataframe.mp == 1), dataframe.open, np.nan)
        if INSTRUMENT == 1:
            dataframe["number_of_stocks"] = np.where((dataframe.mp.shift(1) == 0) & 
                                            (dataframe.mp == 1), OPERATION_MONEY / dataframe.open, np.nan)
    dataframe["entry_price"] = dataframe["entry_price"].fillna(method='ffill')
    if INSTRUMENT == 1:
        dataframe["number_of_stocks"] = dataframe["number_of_stocks"]                                        .apply(lambda x: round(x,0)).fillna(method='ffill')
    dataframe["events_in"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(1) == 0), "entry", "")

    if direction == "long":
        if INSTRUMENT == 1:
            dataframe["open_operations"] = (dataframe.close - dataframe.entry_price) * dataframe.number_of_stocks
            dataframe["open_operations"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(-1) == 0), 
                    (dataframe.open.shift(-1) - dataframe.entry_price) * dataframe.number_of_stocks - 2 * COSTS,
                     dataframe.open_operations)
    else:
        if INSTRUMENT == 1:
            dataframe["open_operations"] = (dataframe.entry_price - dataframe.close) * dataframe.number_of_stocks
            dataframe["open_operations"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(-1) == 0), 
                    (dataframe.entry_price - dataframe.open.shift(-1)) * dataframe.number_of_stocks - 2 * COSTS,
                     dataframe.open_operations)
        
    dataframe["open_operations"] = np.where(dataframe.mp == 1, dataframe.open_operations, 0)
    dataframe["events_out"] = np.where((dataframe.mp == 1) & (dataframe.exit_rules == -1), "exit", "")      
    dataframe["operations"] = np.where((dataframe.exit_rules == -1) & 
                                       (dataframe.mp == 1), dataframe.open_operations, np.nan)
    dataframe["closed_equity"] = dataframe.operations.fillna(0).cumsum()
    dataframe["open_equity"] = dataframe.closed_equity +                                dataframe.open_operations - dataframe.operations.fillna(0)
    dataframe.to_csv("trading_system_check\\"+NOME_STRUMENTO+"_"+NOME_STRATEGIA+"_export.csv")
    return dataframe
    
def plot_equity(equity,color):
    """
    Funzione per stampare un'equity line
    """
    plt.figure(figsize=(14, 8), dpi=300)
    plt.plot(equity, color=color)
    plt.xlabel("Time")
    plt.ylabel("Profit/Loss")
    plt.title('Equity Line')
    plt.xticks(rotation='vertical')
    plt.grid(True)
    plt.show()
    return
    
def drawdown(equity):
    """
    Funzione che calcola il draw down data un'equity line
    """
    maxvalue = equity.expanding(0).max()
    drawdown = equity - maxvalue
    drawdown_series = pd.Series(drawdown, index = equity.index)
    return drawdown_series

def drawdownperc(equity):
    """
    Funzione che calcola il draw down data un'equity line
    """
    maxvalue = equity.expanding(0).max()
    drawdown = (equity - maxvalue)/equity
    drawdownperc_series = pd.Series(drawdownperc, index = equity.index)
    return drawdownperc_series

def plot_drawdown(equity,color):
    """
    Funzione per graficare la curva di draw down
    """
    dd = drawdown(equity)
    plt.figure(figsize = (12, 6), dpi = 300)
    plt.plot(dd, color = color)
    plt.fill_between(dd.index, 0, dd, color = color)
    plt.xlabel("Time")
    plt.ylabel("Profit/Loss")
    plt.title('Draw Down')
    plt.xticks(rotation='vertical')
    plt.grid(True)
    plt.show()
    return

def plot_drawdownperc(equity,color):
    """
    Funzione per graficare la curva di draw down
    """
    ddp = drawdownperc(equity)
    plt.figure(figsize = (12, 6), dpi = 300)
    plt.plot(ddp, color = color)
    plt.fill_between(ddp.index, 0, ddp, color = color)
    plt.xlabel("Time")
    plt.ylabel("Profit/Loss")
    plt.title('Draw Down %')
    plt.xticks(rotation='vertical')
    plt.grid(True)
    plt.show()
    return

def plot_double_equity(closed_equity,open_equity):
    """
    Funzione per stampare due equity sovrapposte
    """
    plt.figure(figsize=(14, 8), dpi=300)
    plt.plot(open_equity, color='red')
    plt.plot(closed_equity, color='green')
    plt.xlabel("Time")
    plt.ylabel("Profit/Loss")
    plt.title('Open & Closed Equity Line')
    plt.xticks(rotation='vertical')
    plt.grid(True)
    plt.show()
    return
    
def profit(equity):
    return round(equity[-1],2)
    
def operation_number(operations):
    return operations.count()
    
def avg_trade(operations):
    return round(operations.mean(),2)
    
def max_draw_down(equity):
    dd = drawdown(equity)
    return round(dd.min(),2)
    
def avgdrawdown_nozero(equity):
    """
    calcola la media del draw down storico
    non considerando i valori nulli (nuovi massimi di equity line)
    """
    dd = drawdown(equity)
    return round(dd[dd < 0].mean(),2)

def avg_loss(operations):
    return round(operations[operations < 0].mean(),2)
    
def max_loss(operations):
    return round(operations.min(),2)
    
def max_loss_date(operations):
    return operations.idxmin()
    
def avg_gain(operations):
    return round(operations[operations > 0].mean(),2)
    
def max_gain(operations):
    return round(operations.max(),2)
    
def max_gain_date(operations):
    return operations.idxmax()
    
def gross_profit(operations):
    return round(operations[operations > 0].sum(),2)
    
def gross_loss(operations):
    return round(operations[operations <= 0].sum(),2)
    
def profit_factor(operations):
    a = gross_profit(operations)
    b = gross_loss(operations)
    if b != 0:
        return round(abs(a / b), 2)
    else:
        return round(abs(a / 0.00000001), 2)
        
def percent_win(operations):
    return round((operations[operations > 0].count() / operations.count() * 100),2)
    
def reward_risk_ratio(operations):
    if operations[operations <= 0].mean() != 0:
        return round((operations[operations > 0].mean() / -operations[operations <= 0].mean()),2)
    else:
        return np.inf
        
def delay_between_peaks(equity):
    """
    Funzione per calcolare i ritardi istantanei in barre
    nel conseguire nuovi massimi di equity line
    Input: equity line
    """
    work_df = pd.DataFrame(equity, index = equity.index)
    work_df["drawdown"] = drawdown(equity)
    work_df["delay_elements"] = work_df["drawdown"].apply(lambda x: 1 if x < 0 else 0)
    work_df["resets"] = np.where(work_df["drawdown"] == 0, 1, 0)
    work_df['cumsum'] = work_df['resets'].cumsum()
    #print(work_df.iloc[-20:,:])
    a = pd.Series(work_df['delay_elements'].groupby(work_df['cumsum']).cumsum())
    return a

def max_delay_between_peaks(equity):
    """
    Funzione per calcolare il più lungo ritardo in barre dall'ultimo massimo
    Input: equity line
    """
    a = delay_between_peaks(equity)
    return a.max()
    
def avg_delay_between_peaks(equity):
    """
    Funzione per calcolare il ritardo medio in barre
    nel conseguire nuovi massimi di equity line
    Input: equity line
    """
    work_df = pd.DataFrame(equity, index = equity.index)
    work_df["drawdown"] = drawdown(equity)
    work_df["delay_elements"] = work_df["drawdown"].apply(lambda x: 1 if x < 0 else np.nan)
    work_df["resets"] = np.where(work_df["drawdown"] == 0, 1, 0)
    work_df['cumsum'] = work_df['resets'].cumsum()
    work_df.dropna(inplace = True)
    a = work_df['delay_elements'].groupby(work_df['cumsum']).sum()
    return round(a.mean(),2)
    
def plot_annual_histogram(operations):
    yearly = operations.resample('A').sum()
    colors = pd.Series()
    colors = yearly.apply(lambda x: "green" if x > 0 else "red")
    n_groups = len(yearly)
    plt.subplots(figsize=(10, 7), dpi=200)
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 1

    rects1 = plt.bar(index,
                     yearly,
                     bar_width,
                     alpha=opacity,
                     color=colors,
                     label='Yearly Statistics')

    plt.xlabel('Years')
    plt.ylabel('Profit - Loss')
    plt.title('Yearly Profit-Loss')
    plt.xticks(index, yearly.index.year, rotation=90)
    plt.grid(True)
    plt.show()
    return
    
def plot_monthly_bias_histogram(operations):
    monthly = pd.DataFrame(operations.fillna(0)).resample('M').sum()
    monthly['Month'] = monthly.index.month
    biasMonthly = []
    months = []

    for month in range(1, 13):
        months.append(month)
    for month in months:
        biasMonthly.append(monthly[(monthly['Month'] == month)].mean())

    biasMonthly = pd.DataFrame(biasMonthly)
    column = biasMonthly.columns[0]
    colors = pd.Series()
    colors = biasMonthly[column].apply(lambda x: "green" if x > 0 else "red")
    n_groups = len(biasMonthly)
    plt.subplots(figsize=(14, 6), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 1

    rects1 = plt.bar(index,
                     biasMonthly[column],
                     bar_width,
                     alpha=opacity,
                     color=colors,
                     label='Yearly Statistics')

    plt.xlabel('Months')
    plt.ylabel('Average Profit - Loss')
    plt.title('Average Monthly Profit-Loss')
    months_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                    "October", "November", "December"]
    plt.xticks(index, months_names, rotation=45)
    plt.grid(True)
    plt.show()
    return
    
def plot_equity_heatmap(operations,annotations):
    monthly = operations.resample('M').sum()
    toHeatMap = pd.DataFrame(monthly)
    toHeatMap["Year"] = toHeatMap.index.year
    toHeatMap["Month"] = toHeatMap.index.month
    Show = toHeatMap.groupby(by=['Year','Month']).sum().unstack()
    Show.columns = ["January","February","March","April","May","June",
                    "July","August","September","October","November","December"]
    plt.figure(figsize=(8,6),dpi=120)
    sns.heatmap(Show, cmap="RdYlGn", linecolor="white", linewidth=0.1, annot=annotations, 
                vmin=-max(monthly.min(),monthly.max()), vmax=monthly.max())
    return
    
def performance_report(trading_system,operations,closed_equity,open_equity,nome_strumento,nome_strategia):
    print("Performance Report -",nome_strumento," ",nome_strategia)
    print("")
    print("Profit:                  ", profit(open_equity))
    print("Operations:              ", operation_number(operations))
    print("Average Trade:           ", avg_trade(operations))
    print("")
    print("Profit Factor:           ", profit_factor(operations))
    print("Gross Profit:            ", gross_profit(operations))
    print("Gross Loss:              ", gross_loss(operations))
    print("")
    print("Percent Winning Trades:  ", percent_win(operations))
    print("Percent Losing Trades:   ", 100 - percent_win(operations))
    print("Reward Risk Ratio:       ", reward_risk_ratio(operations))
    print("")
    print("Max Gain:                ", max_gain(operations), " in date ", max_gain_date(operations))
    print("Average Gain:            ", avg_gain(operations))
    print("Max Loss:                ", max_loss(operations), " in date ", max_loss_date(operations))
    print("Average Loss:            ", avg_loss(operations))
    print("")
    print("Avg Open Draw Down:      ", avgdrawdown_nozero(open_equity))
    print("Max Open Draw Down:      ", max_draw_down(open_equity))
    print("")
    print("Avg Closed Draw Down:    ", avgdrawdown_nozero(trading_system.closed_equity))
    print("Max Closed Draw Down:    ", max_draw_down(trading_system.closed_equity))
    print("")
    print("Avg Delay Between Peaks: ", avg_delay_between_peaks(trading_system.open_equity))
    print("Max Delay Between Peaks: ", max_delay_between_peaks(trading_system.open_equity))
    plot_equity(trading_system.open_equity,"green")
    plot_drawdown(trading_system.open_equity,"red")
    plot_annual_histogram(operations)
    plot_monthly_bias_histogram(operations)
    plot_equity_heatmap(operations,False)
    return


def stop_check(dataframe,rules,level,direction):
    """
    Funzione per validare una regola di ingresso o di uscita rispetto ad un setup stop
    """
    service_dataframe = pd.DataFrame(index = dataframe.index)
    service_dataframe['rules'] = rules
    service_dataframe['level'] = level
    service_dataframe['low'] = dataframe.low
    service_dataframe['high'] = dataframe.high

    if direction == "long":
        service_dataframe['new_rules'] = np.where((service_dataframe.rules == True) &\
                                         (service_dataframe.high.shift(-1) >= service_dataframe.level.shift(-1)), 
                                          True, False)
    if direction == "short":
        service_dataframe['new_rules'] = np.where((service_dataframe.rules == True) &\
                                         (service_dataframe.low.shift(-1) <= service_dataframe.level.shift(-1)), 
                                          True, False)
    return service_dataframe.new_rules

def limit_check(dataframe,rules,level,direction):
    """
    Funzione per validare una regola di ingresso o di uscita rispetto ad un setup limit
    """
    service_dataframe = pd.DataFrame()
    service_dataframe['rules'] = rules
    service_dataframe['level'] = level
    service_dataframe['low'] = dataframe.low
    service_dataframe['high'] = dataframe.high
    
    if direction == "long":
        service_dataframe['new_rules'] = np.where((service_dataframe.rules == True) & \
                                         (service_dataframe.low.shift(-1) <= service_dataframe.level.shift(-1)), 
                                          True, False)
    if direction == "short":
        service_dataframe['new_rules'] = np.where((service_dataframe.rules == True) &
                                         (service_dataframe.high.shift(-1) >= service_dataframe.level.shift(-1)), 
                                          True, False)
    return service_dataframe.new_rules

def tick_correction_up(level,tick):
    if level != level:
        level = 0
    multiplier = math.ceil(level/tick)
    return multiplier * tick

def tick_correction_down(level,tick):
    if level != level:
        level = 0
    multiplier = math.floor(level/tick)
    return multiplier * tick

def apply_trading_system_limstop(ORDER_TYPE,INSTRUMENT,OPERATION_MONEY,COSTS,imported_dataframe, tick, direction, enter_level, enter_rules, exit_rules,NOME_STRUMENTO,NOME_STRATEGIA):
    dataframe = imported_dataframe.copy()
    if ORDER_TYPE == "stop":
        enter_rules = stop_check(dataframe,enter_rules,enter_level,direction)
    if ORDER_TYPE == "limit":
        enter_rules = limit_check(dataframe,enter_rules,enter_level,direction)
        
    dataframe['enter_level'] = enter_level
    dataframe['enter_rules'] = enter_rules.apply(lambda x: 1 if x == True else 0)
    dataframe['exit_rules'] = exit_rules.apply(lambda x: -1 if x == True else 0)

    dataframe["mp"] = marketposition_generator(dataframe.enter_rules,dataframe.exit_rules,dataframe.enter_level,NOME_STRUMENTO,NOME_STRATEGIA)
 
    if ORDER_TYPE == "market":
        dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                             dataframe.open, np.nan)
        if INSTRUMENT == 1:
            dataframe["number_of_stocks"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                      OPERATION_MONEY / dataframe.open, np.nan)
    if ORDER_TYPE == "stop":
        if direction == "long":
            dataframe.enter_level = dataframe.enter_level.apply(lambda x: tick_correction_up(x,tick))
            real_entry = np.where(dataframe.open > dataframe.enter_level, dataframe.open, dataframe.enter_level)
            dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                real_entry, np.nan)
        if direction == "short":
            dataframe.enter_level = dataframe.enter_level.apply(lambda x: tick_correction_down(x,tick))
            real_entry = np.where(dataframe.open < dataframe.enter_level, dataframe.open, dataframe.enter_level)
            dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                real_entry, np.nan)
        if INSTRUMENT == 1:
            dataframe["number_of_stocks"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                      OPERATION_MONEY / real_entry, np.nan)   
    if ORDER_TYPE == "limit":
        if direction == "long":
            dataframe.enter_level = dataframe.enter_level.apply(lambda x: tick_correction_down(x,tick))
            real_entry = np.where(dataframe.open < dataframe.enter_level, dataframe.open, dataframe.enter_level)
            dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                real_entry, np.nan)
        if direction == "short":
            dataframe.enter_level = dataframe.enter_level.apply(lambda x: tick_correction_up(x,tick))
            real_entry = np.where(dataframe.open > dataframe.enter_level, dataframe.open, dataframe.enter_level)
            dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                real_entry, np.nan)
        if INSTRUMENT == 1:
            dataframe["number_of_stocks"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                      OPERATION_MONEY / real_entry, np.nan) 
            
    dataframe["entry_price"] = dataframe["entry_price"].fillna(method='ffill')
    dataframe["events_in"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(1) == 0), "entry", "")
    if INSTRUMENT == 1:
        dataframe["number_of_stocks"] = dataframe["number_of_stocks"].apply(lambda x: round(x,0))\
                                        .fillna(method='ffill')

    if direction == "long":
        if INSTRUMENT == 1:
            dataframe["open_operations"] = (dataframe.close - dataframe.entry_price) * dataframe.number_of_stocks
            dataframe["open_operations"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(-1) == 0), 
                                                    (dataframe.open.shift(-1) - dataframe.entry_price)
                                                    * dataframe.number_of_stocks - 2 * COSTS, 
                                                    dataframe.open_operations)
    else:
        if INSTRUMENT == 1:
            dataframe["open_operations"] = (dataframe.entry_price - dataframe.close) * dataframe.number_of_stocks
            dataframe["open_operations"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(-1) == 0), 
                                            (dataframe.entry_price - dataframe.open.shift(-1))\
                                            * dataframe.number_of_stocks - 2 * COSTS,
                                            dataframe.open_operations)
        
    dataframe["open_operations"] = np.where(dataframe.mp == 1, dataframe.open_operations, 0)
    dataframe["events_out"] = np.where((dataframe.mp == 1) & (dataframe.exit_rules == -1), "exit", "")      
    dataframe["operations"] = np.where((dataframe.exit_rules == -1) & (dataframe.mp == 1), 
                                        dataframe.open_operations, np.nan)
    dataframe["closed_equity"] = dataframe.operations.fillna(0).cumsum()
    dataframe["open_equity"] = dataframe.closed_equity + \
                               dataframe.open_operations - dataframe.operations.fillna(0)
    dataframe.to_csv("trading_system_check\\"+NOME_STRUMENTO+"_"+NOME_STRATEGIA+"_export.csv")
    return dataframe


def apply_trading_systemall(COSTS,INSTRUMENT, imported_dataframe, bigpointvalue, tick, direction, ORDER_TYPE, 
                         enter_level, enter_rules, exit_rules,NOME_STRUMENTO,NOME_STRATEGIA):
    dataframe = imported_dataframe.copy()
    if ORDER_TYPE == "stop":
        enter_rules = stop_check(dataframe,enter_rules,enter_level,direction)
    if ORDER_TYPE == "limit":
        enter_rules = limit_check(dataframe,enter_rules,enter_level,direction)
        
    dataframe['enter_level'] = enter_level
    dataframe['enter_rules'] = enter_rules.apply(lambda x: 1 if x == True else 0)
    dataframe['exit_rules'] = exit_rules.apply(lambda x: -1 if x == True else 0)
   
    dataframe["mp"] = marketposition_generator(dataframe.enter_rules,dataframe.exit_rules,dataframe.enter_level,NOME_STRUMENTO,NOME_STRATEGIA)
 
    if ORDER_TYPE == "market":
        dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                             dataframe.open, np.nan)
        if INSTRUMENT == 1:
            dataframe["number_of_stocks"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                      OPERATION_MONEY / dataframe.open, np.nan)
    if ORDER_TYPE == "stop":
        if direction == "long":
            dataframe.enter_level = dataframe.enter_level.apply(lambda x: tick_correction_up(x,tick))
            real_entry = np.where(dataframe.open > dataframe.enter_level, dataframe.open, dataframe.enter_level)
            dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                real_entry, np.nan)
        if direction == "short":
            dataframe.enter_level = dataframe.enter_level.apply(lambda x: tick_correction_down(x,tick))
            real_entry = np.where(dataframe.open < dataframe.enter_level, dataframe.open, dataframe.enter_level)
            dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                real_entry, np.nan)
        if INSTRUMENT == 1:
            dataframe["number_of_stocks"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                      OPERATION_MONEY / real_entry, np.nan)   
    if ORDER_TYPE == "limit":
        if direction == "long":
            dataframe.enter_level = dataframe.enter_level.apply(lambda x: tick_correction_down(x,tick))
            real_entry = np.where(dataframe.open < dataframe.enter_level, dataframe.open, dataframe.enter_level)
            dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                real_entry, np.nan)
        if direction == "short":
            dataframe.enter_level = dataframe.enter_level.apply(lambda x: tick_correction_up(x,tick))
            real_entry = np.where(dataframe.open > dataframe.enter_level, dataframe.open, dataframe.enter_level)
            dataframe["entry_price"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                real_entry, np.nan)
        if INSTRUMENT == 1:
            dataframe["number_of_stocks"] = np.where((dataframe.mp.shift(1) == 0) & (dataframe.mp == 1), 
                                                      OPERATION_MONEY / real_entry, np.nan)                                                      
        
    dataframe["entry_price"] = dataframe["entry_price"].fillna(method='ffill')
    dataframe["events_in"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(1) == 0), "entry", "")
    if INSTRUMENT == 1:
        dataframe["number_of_stocks"] = dataframe["number_of_stocks"].apply(lambda x: round(x,0))\
                                        .fillna(method='ffill')
        
    if direction == "long":
        if INSTRUMENT == 1:
            dataframe["open_operations"] = (dataframe.close - dataframe.entry_price) * dataframe.number_of_stocks
            dataframe["open_operations"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(-1) == 0), 
                                                    (dataframe.open.shift(-1) - dataframe.entry_price)
                                                    * dataframe.number_of_stocks - 2 * COSTS, 
                                                    dataframe.open_operations)
        if INSTRUMENT == 2:
            dataframe["open_operations"] = (dataframe.close - dataframe.entry_price) * bigpointvalue
            dataframe["open_operations"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(-1) == 0), 
                     (dataframe.open.shift(-1) - dataframe.entry_price) * bigpointvalue - 2 * COSTS,
                      dataframe.open_operations)
            
    if direction == "short":
        if INSTRUMENT == 1:
            dataframe["open_operations"] = (dataframe.entry_price - dataframe.close) * dataframe.number_of_stocks
            dataframe["open_operations"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(-1) == 0), 
                                            (dataframe.entry_price - dataframe.open.shift(-1))\
                                            * dataframe.number_of_stocks - 2 * COSTS,
                                            dataframe.open_operations)
        if INSTRUMENT == 2:
            dataframe["open_operations"] = (dataframe.entry_price - dataframe.close) * bigpointvalue
            dataframe["open_operations"] = np.where((dataframe.mp == 1) & (dataframe.mp.shift(-1) == 0), 
                     (dataframe.entry_price - dataframe.open.shift(-1)) * bigpointvalue - 2 * COSTS,
                      dataframe.open_operations)
        
    dataframe["open_operations"] = np.where(dataframe.mp == 1, dataframe.open_operations, 0)
    dataframe["events_out"] = np.where((dataframe.mp == 1) & (dataframe.exit_rules == -1), "exit", "")      
    dataframe["operations"] = np.where((dataframe.exit_rules == -1) & (dataframe.mp == 1), 
                                        dataframe.open_operations, np.nan)
    dataframe["closed_equity"] = dataframe.operations.fillna(0).cumsum()
    dataframe["open_equity"] = dataframe.closed_equity + \
                               dataframe.open_operations - dataframe.operations.fillna(0)
       
    dataframe.to_csv("trading_system_check\\"+NOME_STRUMENTO+"_"+NOME_STRATEGIA+"_export.csv")
    return dataframe


def performancereport(trading_system,operations,closed_equity,open_equity,confronto,nome_strumento,nome_strategia):
    print("Performance Report -",nome_strumento," ",nome_strategia)
    print("")
    print("Profit:                  ", cumprofit(operations))
    print("Operations:              ", operation_number(operations))
    print("Average Trade:           ", avg_trade(operations))
    print("")
    print("Profit Factor:           ", profit_factor(operations))
    print("Gross Profit:            ", gross_profit(operations))
    print("Gross Loss:              ", gross_loss(operations))
    print("")
    print("Percent Winning Trades:  ", percent_win(operations))
    print("Percent Losing Trades:   ", 100 - percent_win(operations))
    print("Reward Risk Ratio:       ", reward_risk_ratio(operations))
    print("")
    print("Max Gain:                ", max_gain(operations), " in date ", max_gain_date(operations))
    print("Average Gain:            ", avg_gain(operations))
    print("Max Loss:                ", max_loss(operations), " in date ", max_loss_date(operations))
    print("Average Loss:            ", avg_loss(operations))
    print("")
    print("Avg Open Draw Down:      ", avgdrawdown_nozero(open_equity))
    print("Max Open Draw Down:      ", max_draw_down(open_equity))
    print("")
    print("Avg Closed Draw Down:    ", avgdrawdown_nozero(trading_system.closed_equity))
    print("Max Closed Draw Down:    ", max_draw_down(trading_system.closed_equity))
    print("")
    print("Avg Delay Between Peaks: ", avg_delay_between_peaks(trading_system.open_equity))
    print("Max Delay Between Peaks: ", max_delay_between_peaks(trading_system.open_equity))
    plot_double_equity(trading_system.closed_equity,trading_system.open_equity)
    plot_drawdown(trading_system.open_equity,"red")
    plot_annual_histogram(operations)
    plot_monthly_bias_histogram(operations)
    plot_equity_heatmap(operations,False)
    return

def cumprofit(operations):
    return round(operations.sum(),2)


def plot_confronto(open_equity,confronto):
    """
    Funzione per confronto fra 2 strategie
    """
    plt.figure(figsize=(14, 8), dpi=300)
    plt.plot(open_equity, color='red')
    plt.plot(confronto, color='green')
    plt.xlabel("Time")
    plt.ylabel("Profit/Loss")
    plt.title('confronto strategia')
    plt.xticks(rotation='vertical')
    plt.grid(True)
    plt.show()
    return

def apply_event_ts(cost,df,direction,enter_rules,slpt,tppt,sl_level,tp_level,exit_rules,
                   initial_balance,point_value,nome_strumento,nome_strategia):
    dfts=df.copy()
    dfts['position'] = np.where((enter_rules==1),1,0)
    dfts['stoploss'] = np.where(((dfts.position==1)&(dfts.position.shift(1)==0)),(sl_level),0)
    dfts['takeprofit'] = np.where((dfts.position==1)&(dfts.position.shift(1)==0),(tp_level),0)
    dfts['exit']=np.where((exit_rules==1),1,0)

    indicenum=[]
    In_opID=0
    Out_opID=0
    i = 0
    n = len(dfts)
    while i < n:
        indicenum.append(i)
        i += 1
    dfts['indice']=indicenum


    inposition=0
    In_operazioneID=[]
    Out_operazioneID=[]
    entrate=[]
    uscite=[]
    check=[]


    i = 0
    n = len(dfts)

    while i<n:
        if inposition==0:
            if (dfts[(dfts.indice==i)].position.sum()>0):
                entrata=dfts[(dfts.indice==i+1)].open.sum()
                entrate.append(entrata)
                In_opID=i
                In_operazioneID.append(In_opID)
                inposition=1
            else:
                inposition=0
            check.append(inposition)
            Out_opID=0
            Out_operazioneID.append(Out_opID)


        elif inposition==1:
            if (dfts[(dfts.indice==i)].exit).sum()==1:#uscita su condizione logica
                uscita=dfts[(dfts.indice==i)].close.sum()
                uscite.append(uscita)
                Out_opID=i
                Out_operazioneID.append(Out_opID)
                inposition=0    
            else: #uscita su stop loss o take profit
                if direction=="long":
                    if (dfts[(dfts.indice==i)].close).sum()<(dfts[(dfts.indice==In_opID)].stoploss).sum():
                        uscita=dfts[(dfts.indice==i)].close.sum()
                        uscite.append(uscita)
                        Out_opID=i
                        Out_operazioneID.append(Out_opID)
                        inposition=0
                    elif (dfts[(dfts.indice==i)].close).sum()>(dfts[(dfts.indice==In_opID)].takeprofit).sum():
                        uscita=dfts[(dfts.indice==i)].close.sum()
                        uscite.append(uscita)
                        Out_opID=i
                        Out_operazioneID.append(Out_opID)
                        inposition=0
                    else:
                        inposition=1    
                        Out_opID=0
                        Out_operazioneID.append(Out_opID)
                else:
                    if (dfts[(dfts.indice==i)].close).sum()>(dfts[(dfts.indice==In_opID)].stoploss).sum():
                        uscita=dfts[(dfts.indice==i)].close.sum()
                        uscite.append(uscita)
                        Out_opID=i
                        Out_operazioneID.append(Out_opID)
                        inposition=0
                    elif (dfts[(dfts.indice==i)].close).sum()<(dfts[(dfts.indice==In_opID)].takeprofit).sum():
                        uscita=dfts[(dfts.indice==i)].close.sum()
                        uscite.append(uscita)
                        Out_opID=i
                        Out_operazioneID.append(Out_opID)
                        inposition=0
                    else:
                        inposition=1    
                        Out_opID=0
                        Out_operazioneID.append(Out_opID)

            check.append(inposition)


        elif i==n-1:
            if inposition==1:
                uscite=dfts.close


        i+=1

    if inposition==1:
        uscita=dfts[(dfts.indice==(len(dfts)-1))].close.sum()
        uscite.append(uscita)


    ultimauscita=uscite.pop()

    int(ultimauscita)
    if ultimauscita==0:
        uscita=dfts[(dfts.indice==(len(dfts))-1)].close.sum()
        uscite.append(uscita)



    else:
        uscite.append(ultimauscita)


    ultimaentrata=entrate.pop()
    int(ultimaentrata)
    if ultimaentrata==0:
        entrata=dfts[(dfts.indice==(len(dfts))-1)].close.sum()
        entrate.append(entrata)

    else:
        entrate.append(ultimaentrata)


    if direction=="long":
        l_s=1
    else:
        l_s=-1

    ts=pd.DataFrame(entrate)
    ts.columns=[('entrate')]
    #ts['entrate']=entrate
    ts['uscite']=uscite
    #ts['Out_operazioneID']=Out_operazioneID
    ts['In_operazioneID']=In_operazioneID
    #ts=ts.merge(dfts,left_on=['operazioneID'],right_on=['indice'])
    ts=dfts.merge(ts,how='left',left_on=['indice'],right_on=['In_operazioneID'])
    ts.set_index('date', inplace=True)
    ts.index = pd.to_datetime(ts.index)
    ts['entrate']=ts.entrate.fillna(method='ffill')
    ts['In_checkID']=np.where((ts.In_operazioneID>0),'Entry',np.nan)
    ts['Out_operazioneID']=Out_operazioneID
    ts['Out_checkID']=np.where((ts.Out_operazioneID>0),'Exit',np.nan)
    ts['mp']=check
    ts['mp']=ts.mp.shift(1)
    if direction=="long":
        ts['open_operation']=np.where((ts.mp==1),((ts.close-ts.entrate)*point_value),np.nan)
        ts['closed_operation']=np.where((ts.Out_checkID=='Exit'),(((ts.close-ts.entrate)*point_value)-cost),np.nan)
    else:
        ts['open_operation']=np.where((ts.mp==1),(-1*(ts.close-ts.entrate)*point_value),0)
        ts['closed_operation']=np.where((ts.Out_checkID=='Exit'),(-1*(((ts.close-ts.entrate)*point_value)-cost)),np.nan)

    ts['closed_equity']=initial_balance+(ts.closed_operation.cumsum().fillna(method='ffill'))

    ts['open_equity']=np.where((ts.mp==1),(ts.closed_equity.shift(1)+(((ts.close-ts.entrate)*point_value))),(ts.closed_equity))
    ts['open_equity']=np.where((ts.indice==0),initial_balance,ts.open_equity)
    ts['control']=np.where((ts.closed_operation>0),1,0)
    ts['diffpt']=ts.close-ts.close.shift(1)
    if direction=="long":
        ts['holdpos']=initial_balance+(ts.diffpt.cumsum())
    else:
        ts['holdpos']=initial_balance+((ts.diffpt*-1).cumsum())   
    
    ts.to_csv("trading_system_check\\"+nome_strumento+"_"+nome_strategia+"_EV_export.csv")
    
    return ts


def apply_event_tsSTOP(cost,df,direction,entry_level,enter_rules,slpt,tppt,sl_level,tp_level,exit_rules,
                   initial_balance,point_value,nome_strumento,nome_strategia):
    dfts=df.copy()
    dfts['position'] = np.where((enter_rules==1),1,0)
    dfts['stoploss'] = np.where((dfts.position==1),(sl_level),0)
    dfts['takeprofit'] = np.where((dfts.position==1),(tp_level),0)
    dfts['entry_level']=np.where((dfts.position==1),entry_level,0)
    dfts['exit']=np.where((exit_rules==1),1,0)

    indicenum=[]
    In_opID=0
    Out_opID=0
    i = 0
    n = len(dfts)
    while i < n:
        indicenum.append(i)
        i += 1
    dfts['indice']=indicenum


    inposition=0
    In_operazioneID=[]
    Out_operazioneID=[]
    entrate=[]
    uscite=[]
    check=[]


    i = 0
    n = len(dfts)

    while i<n:
        if inposition==0:
            if (dfts[(dfts.indice==i)].position.sum()>0):
                entrata=dfts[(dfts.indice==i)].entry_level.sum()
                entrate.append(entrata)
                In_opID=i
                In_operazioneID.append(In_opID)
                inposition=1
            else:
                inposition=0
            check.append(inposition)
            Out_opID=0
            Out_operazioneID.append(Out_opID)
         


        elif inposition==1:
            if (dfts[(dfts.indice==i)].exit).sum()==1:#uscita su condizione logica
                uscita=dfts[(dfts.indice==i)].close.sum()
                uscite.append(uscita)
                Out_opID=i
                Out_operazioneID.append(Out_opID)
                inposition=0    
            else: #uscita su stop loss o take profit
                if direction=="long":
                    if (dfts[(dfts.indice==i)].low).sum()<(dfts[(dfts.indice==In_opID)].stoploss).sum():
                        uscita=dfts[(dfts.indice==In_opID)].stoploss.sum()
                        uscite.append(uscita)
                        Out_opID=i
                        Out_operazioneID.append(Out_opID)
                        inposition=0
                    elif (dfts[(dfts.indice==i)].high).sum()>(dfts[(dfts.indice==In_opID)].takeprofit).sum():
                        uscita=dfts[(dfts.indice==In_opID)].takeprofit.sum()
                        uscite.append(uscita)
                        Out_opID=i
                        Out_operazioneID.append(Out_opID)
                        inposition=0
                    else:
                        inposition=1    
                        Out_opID=0
                        Out_operazioneID.append(Out_opID)
                else:
                    if (dfts[(dfts.indice==i)].high).sum()>(dfts[(dfts.indice==In_opID)].stoploss).sum():
                        uscita=dfts[(dfts.indice==In_opID)].stoploss.sum()
                        uscite.append(uscita)
                        Out_opID=i
                        Out_operazioneID.append(Out_opID)
                        inposition=0
                    elif (dfts[(dfts.indice==i)].low).sum()<(dfts[(dfts.indice==In_opID)].takeprofit).sum():
                        uscita=dfts[(dfts.indice==In_opID)].takeprofit.sum()
                        uscite.append(uscita)
                        Out_opID=i
                        Out_operazioneID.append(Out_opID)
                        inposition=0
                    else:
                        inposition=1    
                        Out_opID=0
                        Out_operazioneID.append(Out_opID)
               

            check.append(inposition)


        elif i==n-1:
            if inposition==1:
                uscite=dfts.close


        i+=1

    if inposition==1:
        uscita=dfts[(dfts.indice==(len(dfts)-1))].close.sum()
        uscite.append(uscita)


    ultimauscita=uscite.pop()

    int(ultimauscita)
    if ultimauscita==0:
        uscita=dfts[(dfts.indice==(len(dfts))-1)].close.sum()
        uscite.append(uscita)



    else:
        uscite.append(ultimauscita)


    ultimaentrata=entrate.pop()
    int(ultimaentrata)
    if ultimaentrata==0:
        entrata=dfts[(dfts.indice==(len(dfts))-1)].close.sum()
        entrate.append(entrata)

    else:
        entrate.append(ultimaentrata)


    if direction=="long":
        l_s=1
    else:
        l_s=-1

    ts=pd.DataFrame(entrate)
    ts.columns=[('entrate')]
    #ts['entrate']=entrate
    ts['uscite']=uscite
    #ts['Out_operazioneID']=Out_operazioneID
    ts['In_operazioneID']=In_operazioneID
    #ts=ts.merge(dfts,left_on=['operazioneID'],right_on=['indice'])
    ts=dfts.merge(ts,how='left',left_on=['indice'],right_on=['In_operazioneID'])
    ts.set_index('date', inplace=True)
    ts.index = pd.to_datetime(ts.index)
    ts['entrate']=ts.entrate.fillna(method='ffill')
    ts['uscite']=ts.uscite.fillna(method='ffill')
    ts['In_checkID']=np.where((ts.In_operazioneID>0),'Entry',np.nan)
    ts['Out_operazioneID']=Out_operazioneID
    ts['Out_checkID']=np.where((ts.Out_operazioneID>0),'Exit',np.nan)
    ts['mp']=check
    #ts['mp']=ts.mp.shift(1)
    if direction=="long":
        ts['open_operation']=np.where((ts.mp==1),((ts.close-ts.entrate)*point_value),np.nan)
        ts['closed_operation']=np.where((ts.Out_checkID=='Exit'),(((ts.uscite-ts.entrate)*point_value)-cost),np.nan)
    else:
        ts['open_operation']=np.where((ts.mp==1),(-1*(ts.close-ts.entrate)*point_value),0)
        ts['closed_operation']=np.where((ts.Out_checkID=='Exit'),(-1*(((ts.uscite-ts.entrate)*point_value)-cost)),np.nan)

    ts['closed_equity']=initial_balance+(ts.closed_operation.cumsum().fillna(method='ffill'))

    ts['open_equity']=np.where((ts.mp==1),(ts.closed_equity.shift(1)+(((ts.close-ts.entrate)*point_value))),(ts.closed_equity))
    ts['open_equity']=np.where((ts.indice==0),initial_balance,ts.open_equity)
    ts['control']=np.where((ts.closed_operation>0),1,0)
    ts['diffpt']=ts.close-ts.close.shift(1)
    if direction=="long":
        ts['holdpos']=initial_balance+(ts.diffpt.cumsum())
    else:
        ts['holdpos']=initial_balance+((ts.diffpt*-1).cumsum())   
    
    ts.to_csv("trading_system_check\\"+nome_strumento+"_"+nome_strategia+"_EV_export.csv")
    
    return ts


def costs_adder(operations, costs):
    """
    Per ogni operazione sottraiamo il doppio dei costi fissi (round turn)
    """
    new_operations = operations.apply(lambda x: x - 2 * costs)
    return new_operations

def noise_adder(operations, percentage_noise_addiction):
    """
    Funzione che modifica ciascun elemento dell'array di ingresso mediante la formula:
    new_array[i] = array[i] + factor * percentage * range[i]
    Di fatto si aggiunge una componente di rumore positiva o negativa 
    proporzionale all'estensione monetaria del trade
    """
    new_operations = []
    for el in operations:
        factor = np.random.uniform(-1, 1)
        new_operations.append(round(el + factor * (percentage_noise_addiction / 100) * abs(el),2))
    new_operations_series = pd.Series(new_operations, index=operations.index, name="operations")
    return new_operations_series

def evolved_montecarlo_analysis(operations,Costs,PercentageNoiseAddiction,OperationsPercentage,NumberOfShuffles):

        original_operations = operations

        if Costs != 0:
            original_operations = costs_adder(operations, Costs)

        if PercentageNoiseAddiction != 0:
            original_operations = noise_adder(operations, PercentageNoiseAddiction)

        original_equity = original_operations.cumsum()
        original_profit = round(original_operations.sum(),2)
        original_drawdown = drawdown(original_operations)
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
        start = datetime.datetime.now()
        while i < NumberOfShuffles:
            my_permutation = original_operations.sample(frac = fraction).reset_index(drop = True)
            my_permutation = pd.Series(my_permutation)
            new_equity = my_permutation.cumsum()
            new_drawdown = drawdown(new_equity)
            matrix_of_equities["shuffle_" + str(i + 1)] = new_equity
            matrix_of_drawdowns["shuffle_" + str(i + 1)] = new_drawdown
            max_drawdown_list.append(new_drawdown.min())
            i += 1

        end = datetime.datetime.now()
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

        print("Original Profit/Loss: ", original_profit)
        print("Original Max Draw Down: ", original_max_drawdown)
        print("")
        print("Worst Equity Index: ", worst_drawdown_index)
        print("Worst Equity Profit/Loss: ", worst_drawdown_profit)
        print("Worst Equity Max Draw Down: ", worst_drawdown)
        print("")
        print("Best Equity Index: ", best_drawdown_index)
        print("Best Equity Profit/Loss: ", best_drawdown_profit)
        print("Best Equity Max Draw Down: ", best_drawdown)
        print("")

        MaxDrawDown95 = round(np.percentile(max_drawdown_list, 5),2)
        riskfactor95 = round(np.percentile(max_drawdown_list, 5) / original_max_drawdown, 2)
        riskfactor = round(min(max_drawdown_list) / original_max_drawdown, 2)

        print("95 Percentile Montecarlo Max Draw Down: ", MaxDrawDown95)
        print("Montecarlo Risk Factor on 95 Percentile Probability: ", riskfactor95)
        print("Worst Montecarlo Max Draw Down: ", round(min(max_drawdown_list),2))
        print("Montecarlo Risk Factor on Max Draw Down: ", riskfactor)
        print("")
        # GRAPH 1
        plt.subplots(figsize=(14, 8), dpi=100)
        plt.plot(matrix_of_equities.iloc[:,1:], color="grey", linewidth=1, linestyle="-")
        plt.plot(matrix_of_equities[worst_drawdown_index], color="red", linewidth=2, linestyle="-", 
                 label="Worst Equity Line")
        plt.plot(matrix_of_equities[best_drawdown_index], color="green", linewidth=2, linestyle="-", 
                 label="Best Equity Line")

        if OperationsPercentage == 100:
            plt.plot(original_equity.reset_index(drop=True), color="blue", linewidth=2, linestyle="-", 
                     label="Original Equity Line")
        else:
            plt.plot(original_equity.reset_index(drop=True)[:cutnumber], color="blue", linewidth=2, linestyle="-")

        plt.grid(True)
        plt.legend()
        plt.savefig("Shuffle_1.png")
        plt.show()

        # GRAPH 2
        output = []
        output = sorted(max_drawdown_list)
        n_groups = NumberOfShuffles
        plt.figure(figsize=(14, 8), dpi=100)
        index = np.arange(n_groups)
        bar_width = 0.5
        opacity = 1
        error_config = {'ecolor': '0.3'}

        rects1 = plt.bar(index, output, bar_width,
                          alpha=opacity,
                          color='red',
                          error_kw=error_config,
                          label='DrawDowns Distribution')

        plt.xlabel('Shuffle Number')
        plt.ylabel('Monetary DrawDown')
        plt.title('Montecarlo Analysis on ' + str(NumberOfShuffles) + ' Shuffles - by Gandalf Project R&D')
        plt.legend()
        plt.grid(True)
        plt.savefig("Shuffle_2.png")
        plt.show()

        # GRAPH 3
        Percentiles = np.zeros(100)
        i = 0
        while i < 100:
            Percentiles[i] = np.percentile(max_drawdown_list, int(i))
            i += 1

        plt.figure(figsize=(14, 8), dpi=100)
        plt.xlabel('Percentile Values')
        plt.ylabel('Monetary Draw Down')
        plt.title('Montecarlo Analysis on ' + str(NumberOfShuffles) + ' Shuffles - by Gandalf Project R&D')
        plt.axhline(y=int(original_max_drawdown), xmin=0, xmax=100, linewidth=2, color='green')
        plt.axhline(y=int(MaxDrawDown95), xmin=0, xmax=100, linewidth=2, color='blue')
        plt.plot(Percentiles, color="red", linewidth=2, linestyle="-")
        plt.xticks(np.arange(0, 99, 5.0))
        plt.grid(True)
        plt.legend()
        plt.savefig("Shuffle_3.png")
        plt.show()
        return

        
# In[ ]:





# In[ ]:




