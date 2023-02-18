#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import ffn



#istogramma andamento medio all'interno del giorno di una serie storica
def plot_histHOD(array,titolo):
    """
    array= inserire la lista dei valori medi per ora   
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = 24

    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)

    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 1

    rects1 = ax.bar(index, 
                array, 
                bar_width,
                alpha=opacity,
                color='blue',
                label=titolo +' media oraria')


    ax.set_xlabel('ore')
    ax.set_ylabel('punti')
    ax.set_title('bias orario ' + titolo)
    ax.set_xticks(index)
    ax.set_xticklabels(np.arange(n_groups))
    #ax.set_xticklabels((['0','1','2','3','4','5','6','7','8','9','10','11','12',
      #               '13','14','15','16','17','18','19','20','21','22','23']))
    ax.legend()
    ax.grid(True)
    plt.show()
    return

#istogramma andamento medio all'interno del giorno di una serie storica
def plot_histHODx3(array1,array2,array3,titolo1,titolo2,titolo3,titolograf):
    
    """
    array1-2-3= inserire la lista dei valori medi per ora   
    titolo1-2-3= str -> nome del titolo a cui si riferisce la lista
    titolograf= str -> nome che si vuol dare al grafico
    nb - funzione implementabile con ulteriori liste
    """
    n_groups = 24
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1
    
    rects1 = plt.bar(index, 
                array1, 
                bar_width,
                alpha=opacity,
                color='red',
                label= titolo1 + ' media oraria')
    rects2 = plt.bar(index + bar_width,  
                array2, 
                bar_width,
                alpha=opacity,
                color='blue',
                label= titolo2 + ' media oraria')
    rects3 = plt.bar(index + 2* bar_width, 
                array3, 
                bar_width,
                alpha=opacity,
                color='green',
                label=titolo3 + ' media oraria')

    ax.set_xlabel('ore')
    ax.set_ylabel('punti')
    ax.set_title( titolograf )
    ax.set_xticks(index)
    ax.set_xticklabels((['0','1','2','3','4','5','6','7','8','9','10','11','12',
                     '13','14','15','16','17','18','19','20','21','22','23']))
    ax.legend()
    ax.grid(True)
    plt.show()
    return



#plot di una serie storiche confrontata su andamento medio all'interno del giorno
def plot_lineHOD(array,startDate,endDate,titolo):
    """
    array= inserire la lista dei valori medi per ora   
    startDate = data in formato str "AAAAMMGG"
    endDate = data in formato str "AAAAMMGG"
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = 24
    
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1

    label = titolo + ": from " + startDate + " to " + endDate
    
  
    rects1 = plt.plot(array, color='black', label=label)
    
    ax.set_xlabel('Trading Hours')
    ax.set_ylabel('Intraday Trend')
    ax.set_title('Trend intraday medio ' + titolo)
    ax.set_xticks(index)
    ax.set_xticklabels((['0','1','2','3','4','5','6','7','8','9','10','11','12',
                         '13','14','15','16','17','18','19','20','21','22','23']))
    ax.legend()
    ax.grid(True)
    plt.show()
    return



#plot di 3 serie storiche confrontate su andamento medio all'interno del giorno
def plot_lineHODx3(array1,array2,array3,startDate1,endDate1,startDate2,endDate2,startDate3,endDate3,titolo1,titolo2,titolo3,titolograf):
    """
    array1-2-3= inserire la lista dei valori medi per ora   
    startDate1-2-3 = data in formato str "AAAAMMGG"
    endDate1-2-3 = data in formato str "AAAAMMGG"
    titolo1-2-3= str -> nome del titolo a cui si riferisce la lista
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = 24
    fig, ax = plt.subplots(figsize=(14, 9), dpi=100)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1

    label_1 = titolo1 + ": from " + startDate1 + " to " + endDate1
    label_2 = titolo2 + ": from " + startDate2 + " to " + endDate2
    label_3 = titolo3 + ": from " + startDate3 + " to " + endDate3

  
    rects1 = plt.plot(array1, color='red', label=label_1)
    rects2 = plt.plot(array2, color='blue', label=label_2)
    rects3 = plt.plot(array3, color='lime', label=label_3)

    ax.set_xlabel('Trading Hours')
    ax.set_ylabel('Intraday Trend')
    ax.set_title('Trend intraday medio ' + titolograf)
    ax.set_xticks(index)
    ax.set_xticklabels((['0','1','2','3','4','5','6','7','8','9','10','11','12',
                         '13','14','15','16','17','18','19','20','21','22','23']))
    ax.legend()
    ax.grid(True)
    plt.show()
    return

#istogramma andamento medio all'interno della settimana di una serie storica
def plot_histDOW(array,titolo):
    """
    array= inserire la lista dei valori medi per giorno   
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = 5

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 1

    rects1 = ax.bar(index, 
                array, 
                bar_width,
                alpha=opacity,
                color='blue',
                label=titolo +' medio orario')


    ax.set_xlabel('giorni')
    ax.set_ylabel('punti')
    ax.set_title('bias giorno settimana ' + titolo)
    ax.set_xticks(index)
    ax.set_xticklabels((['monday','tuesday','wednesday','thursday','friday']))
    ax.legend()
    ax.grid(True)
    plt.show()
    return

def plot_histDOWx3(array1,array2,array3,titolo1,titolo2,titolo3,titolograf):
    
    """
    array1-2-3= inserire la lista dei valori medi per giorno 
    titolo1-2-3= str -> nome del titolo a cui si riferisce la lista
    titolograf= str -> nome che si vuol dare al grafico
    nb - funzione implementabile con ulteriori liste
    """
    n_groups = 5
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1
    
    rects1 = plt.bar(index, 
                array1, 
                bar_width,
                alpha=opacity,
                color='red',
                label= titolo1 + ' medio orario')
    rects2 = plt.bar(index + bar_width,  
                array2, 
                bar_width,
                alpha=opacity,
                color='blue',
                label= titolo2 + ' medio orario')
    rects3 = plt.bar(index + 2* bar_width, 
                array3, 
                bar_width,
                alpha=opacity,
                color='green',
                label=titolo3 + ' medio orario')

    ax.set_xlabel('giorni')
    ax.set_ylabel('punti')
    ax.set_title('bias giorno settimana ' + titolograf )
    ax.set_xticks(index)
    ax.set_xticklabels((['monday','tuesday','wednesday','thursday','friday']))
    
    ax.legend()
    ax.grid(True)
    plt.show()
    return

#plot di una serie storiche confrontata su andamento medio all'intera settimana
def plot_lineDOW(array,startDate,endDate,titolo):
    """
    array= inserire la lista dei valori medi per giorno   
    startDate = data in formato str "AAAAMMGG"
    endDate = data in formato str "AAAAMMGG"
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = 5
    
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1

    label = titolo + ": from " + startDate + " to " + endDate
    
  
    rects1 = plt.plot(array, color='blue', label=label)
    
    ax.set_xlabel('giorni della settimana')
    ax.set_ylabel('Trend settimanale')
    ax.set_title('Trend settimanale medio ' + titolo)
    ax.set_xticks(index)
    #ax.set_xticklabels(index)
    ax.set_xticklabels((['monday','tuesday','wednesday','thursday','friday']))
    ax.legend()
    ax.grid(True)
    plt.show()
    return

def plot_lineDOWx3(array1,array2,array3,startDate1,endDate1,startDate2,endDate2,startDate3,endDate3,titolo1,titolo2,titolo3,titolograf):
    """
    array1-2-3= inserire la lista dei valori medi per giorno   
    startDate1-2-3 = data in formato str "AAAAMMGG"
    endDate1-2-3 = data in formato str "AAAAMMGG"
    titolo1-2-3= str -> nome del titolo a cui si riferisce la lista
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = 5
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1

    label_1 = titolo1 + ": from " + startDate1 + " to " + endDate1
    label_2 = titolo2 + ": from " + startDate2 + " to " + endDate2
    label_3 = titolo3 + ": from " + startDate3 + " to " + endDate3

  
    rects1 = plt.plot(array1, color='red', label=label_1)
    rects2 = plt.plot(array2, color='blue', label=label_2)
    rects3 = plt.plot(array3, color='lime', label=label_3)

    ax.set_xlabel('giorni della settimana')
    ax.set_ylabel('Trend settimanale')
    ax.set_title('Trend settimanale medio ' + titolograf)
    ax.set_xticks(index)
    ax.set_xticklabels((['monday','tuesday','wednesday','thursday','friday']))
    ax.legend()
    ax.grid(True)
    plt.show()
    return



#istogramma andamento medio all'interno del giorno di una serie storica
def plot_histHODx2(array1,array2,titolo1,titolo2,titolograf):
    
    """
    array1-2-3= inserire la lista dei valori medi per ora   
    titolo1-2-3= str -> nome del titolo a cui si riferisce la lista
    titolograf= str -> nome che si vuol dare al grafico
    nb - funzione implementabile con ulteriori liste
    """
    n_groups = 24
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1
    
    rects1 = plt.bar(index, 
                array1, 
                bar_width,
                alpha=opacity,
                color='red',
                label= titolo1 + ' medio orario')
    rects2 = plt.bar(index + bar_width,  
                array2, 
                bar_width,
                alpha=opacity,
                color='blue',
                label= titolo2 + ' medio orario')
    

    ax.set_xlabel('ore')
    ax.set_ylabel('punti')
    ax.set_title('bias orario ' + titolograf )
    ax.set_xticks(index)
    ax.set_xticklabels((['0','1','2','3','4','5','6','7','8','9','10','11','12',
                     '13','14','15','16','17','18','19','20','21','22','23']))
    ax.legend()
    ax.grid(True)
    plt.show()
    return


def plot_lineDOWx3_new(array1,array2,array3,startDate1,endDate1,startDate2,
                       endDate2,startDate3,endDate3,titolo1,titolo2,titolo3,titolograf):
    """
    array1-2-3= inserire la lista dei valori medi per giorno   
    startDate1-2-3 = data in formato str "AAAAMMGG"
    endDate1-2-3 = data in formato str "AAAAMMGG"
    titolo1-2-3= str -> nome del titolo a cui si riferisce la lista
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = len(array1)
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1

    label_1 = titolo1 + ": from " + startDate1 + " to " + endDate1
    label_2 = titolo2 + ": from " + startDate2 + " to " + endDate2
    label_3 = titolo3 + ": from " + startDate3 + " to " + endDate3

    rects1 = plt.plot(array1, color='red', label=label_1)
    rects2 = plt.plot(array2, color='blue', label=label_2)
    rects3 = plt.plot(array3, color='lime', label=label_3)

    ax.set_xlabel('giorni della settimana')
    ax.set_ylabel('Trend settimanale')
    ax.set_title('Trend settimanale medio ' + titolograf)
    ax.set_xticks([0, len(array1)/5, (len(array1)/5)*2, (len(array1)/5)*3, (len(array1)/5)*4])
    ax.set_xticklabels((["lunedì","martedì","mercoledì","giovedì","venerdì"]))
    ax.legend()
    ax.grid(True)
    plt.show()

    return

def plot_lineDOW_new(array,startDate,endDate,titolo):
    """
    array= inserire la lista dei valori medi per giorno   
    startDate = data in formato str "AAAAMMGG"
    endDate = data in formato str "AAAAMMGG"
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = len(array)
    
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1

    label = titolo + ": from " + startDate + " to " + endDate
    
  
    rects1 = plt.plot(array, color='blue', label=label)
    
    ax.set_xlabel('giorni della settimana')
    ax.set_ylabel('Trend settimanale')
    ax.set_title('Trend settimanale medio ' + titolo)
    ax.set_xticks([0, len(array)/5, (len(array)/5)*2, (len(array)/5)*3, (len(array)/5)*4])
    ax.set_xticklabels((["lunedì","martedì","mercoledì","giovedì","venerdì"]))
    ax.legend()
    ax.grid(True)
    plt.show()
    return

def plot_lineDOMx3(array1,array2,array3,startDate1,endDate1,startDate2,
                       endDate2,startDate3,endDate3,titolo1,titolo2,titolo3,titolograf):
    """
    array1-2-3= inserire la lista dei valori medi per giorno   
    startDate1-2-3 = data in formato str "AAAAMMGG"
    endDate1-2-3 = data in formato str "AAAAMMGG"
    titolo1-2-3= str -> nome del titolo a cui si riferisce la lista
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = len(array1)
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1

    label_1 = titolo1 + ": from " + startDate1 + " to " + endDate1
    label_2 = titolo2 + ": from " + startDate2 + " to " + endDate2
    label_3 = titolo3 + ": from " + startDate3 + " to " + endDate3

    rects1 = plt.plot(array1, color='red', label=label_1)
    rects2 = plt.plot(array2, color='blue', label=label_2)
    rects3 = plt.plot(array3, color='lime', label=label_3)

    ax.set_xlabel('giorni del mese')
    ax.set_ylabel('Trend mensile')
    ax.set_title('Trend mensile medio ' + titolograf)
    ax.set_xticks(index)
    #ax.set_xticklabels((["gen","feb","mercoledì","giovedì","venerdì"]))
    ax.legend()
    ax.grid(True)
    plt.show()

    return
def plot_lineDOM(array,startDate,endDate,titolo):
    """
    array= inserire la lista dei valori medi per giorno   
    startDate = data in formato str "AAAAMMGG"
    endDate = data in formato str "AAAAMMGG"
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = len(array)
    
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1

    label = titolo + ": from " + startDate + " to " + endDate
    
  
    rects1 = plt.plot(array, color='blue', label=label)
    
    ax.set_xlabel('giorni del mese')
    ax.set_ylabel('Trend mensile')
    ax.set_title('Trend mensile medio ' + titolo)
    ax.set_xticks(index)
    #ax.set_xticklabels((["lunedì","martedì","mercoledì","giovedì","venerdì"]))
    ax.legend()
    ax.grid(True)
    plt.show()
    return

def plot_lineDOY(array,startDate,endDate,titolo):
    """
    array= inserire la lista dei valori medi per giorno   
    startDate = data in formato str "AAAAMMGG"
    endDate = data in formato str "AAAAMMGG"
    titolo= str -> nome del titolo a cui si riferisce la lista
    """
    n_groups = len(array)
    
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 1

    label = titolo + ": from " + startDate + " to " + endDate
    
  
    rects1 = plt.plot(array, color='blue', label=label)
    
    ax.set_xlabel('Trend annuo')
    ax.set_ylabel('')
    ax.set_title('Trend annuo medio ' + titolo)
    ax.set_xticks([len(array)/4, (len(array)/4)*2, (len(array)/4)*3, (len(array)/4)*4])
    ax.set_xticklabels((["1° trim","2° trim","3° trim","4° trim"]))
    ax.legend()
    ax.grid(True)
    plt.show()
    return


# In[ ]:


