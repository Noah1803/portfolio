import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')


def calculateEMA(df, n, columns):
    """
    returns an n period exponential moving average as a new column for each columns.

    pd.Dataframe     df: The original dataframe.
    int               n: The number of periods to consider in the calculus.
    String List columns: The columns which the EMA will be calculated

    Returns a dataframe with a new columns containing the EMA.
    """
    
    k  = 2 / (n+1)
    for column in columns:
        EMAcolumn = 'EMA_'+column

        df[EMAcolumn] = df[column]
        df[EMAcolumn].iloc[n-1] = df[column].iloc[0:n-2].mean()

        for i in range(n, len(df)):
            df[EMAcolumn].iloc[i] = (df[column].iloc[i] - df[EMAcolumn].iloc[i-1])*k + df[EMAcolumn].iloc[i-1]
            #MME = (Close[i] - MME[i-1])*k + MME[i-1] 
     
    #The following function makes all the hardwork. However I'll keep it commented, once I've already implemented the calculation
    #f['pandasEMA'] = df['close'].ewm(span=5, adjust=False).mean()
    
    return df

def calculateBB(df, n, columns):
    """
    Returns a n period bollinger bands for the Dataset.

    pd.Dataframe      df: The original dataframe.
    int                N: Period of observation for the Bollinger Bands.
    String List  columns: Columns that will have the Bollinger Bands calculated over.
    
    Returns a dataframe with a new set of columns UB_Col/LB_Col column containing the Upper Band and Lower Band.
    """
    
    for column in columns:
        ma = df[column].rolling(window=n).mean()
        std = df[column].rolling(window=n).std() 
        
        df['UB_'+column] = ma + (std * 2)
        df['LB_'+column] = ma - (std * 2)
    
    return df

def addPreviousDays(df, days, columns):
    """
    returns a new Dataframe with the Columns for the N previous Days 

    pd.Dataframe      df: The original dataframe.
    int             days: The amount of days that will be included.
    String List  columns: The columns that will be added for each previous days.
    
    returns a dataframe with a new set of columns UB_Col column containing the MME
    """
    
    auxDf = df
    for day in range(1,days+1):
        for column in columns:
            colName = 'd-'+str(day)+'_'+column
            df[colName] = auxDf[column].shift(day)
    return df


def removeColumns(df, columns):
    """
    Remove a specific subset of columns from the Dataframe.
    
    pd.Dataframe      df: The original dataframe.
    String List  columns: The columns that will be removed.

    returns a dataframe with the columns removed.
    """
    
    df = df.drop(columns, axis=1)
    return df

def getPeriod(df, begin, end, resetIndex = False):
    """
    Returns the df in the chosen interval
    
    Object begin: Start date forrmated as 'yyyy.mm.dd'.
    Object   end: End date 'yyyy.mm.dd'.

    returns a dataframe with the historic of the selected period
    """
    
    indexBegin = df[df['date']==begin].index[0]
    indexEnd = df[df['date']==end].index[0]
    
    if (resetIndex):
        return df[(df.index >= indexBegin) & (df.index <= indexEnd)].reset_index(drop=True)
    else: 
        return df[(df.index >= indexBegin) & (df.index <= indexEnd)]
    

def mape(actual, pred): 
    """
    Calculate the MAPE - Mean Average Percentual Error - between two Lists.
    
    actual: List of the real values
    pred  : List of the predicted values

    returns the MAPE between the two lists.
    """
    
    actual, pred = np.array(actual), np.array(pred)
    return np.mean(np.abs((actual - pred) / actual)) * 100, np.std(np.abs((actual - pred) / actual)) * 100

def mae(actual, pred):
    """
    Calculate the MAE - Mean Average Error - between two Lists.
    
    actual: List of the real values
    pred  : List of the predicted values

    returns the MAE between the two lists.
    """
    actual, pred = np.array(actual), np.array(pred)
    return np.mean(np.abs(actual - pred)), np.std(np.abs(actual - pred))

def createDate(day, month, year):
    """
    returns a 'year.month.day' formatted string.
    
    int day  : The day 1 - 31    
    int month: The month 1 - 12
    int year : The year 2016 - 2021
    
    returns a 'year.month.day' formatted string.
    """
    if(day >= 10):
        day = str(day)
    else:
        day = '0' + str(day)
    
    if(month < 10):
        month = '0' + str(month)
    else:
        month = str(month)
        
    year = str(year)
    date = year + '.' + month + '.' + day
    
    return date

def getDate(date):
    """
    Convert a 'yyyy.mm.dd' string into integer data.
    
    int day  : The day 1 - 31    
    int month: The month 1 - 12
    int year : The year 2016 - 2021
    
    returns a year, month, day set of data. 
    """
    
    split = date.split('.')
    
    year = int(split[0])
    month = int(split[1])
    day = int(split[2])
    
    return year, month, day
 
def printResult(error, column):
    """
    Print the error formatted. 
    
    tuple error   : (error, std)   
    Object column : Name of the column
    """
    print(column+': '+str(error[0].round(2))+' +- '+str(error[1].round(2)) + ' %')