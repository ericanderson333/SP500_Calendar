import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import shutil
import pandas as pd
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError
import pickle
import requests

#directories
#historic_stock_data
#month_percent_calc
#final_csv_files

#saves all tickers from sp500 wikipiedia
def save_sp500():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll('td') [0].text.replace('\n','')
        if "." in ticker:
            ticker = ticker.replace('.','-')
            print('ticker replaced to', ticker)
        tickers.append(ticker)

    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers, f)

    print(tickers)

    return tickers


#gets 10 years historic data from each ticker
def get_data(reload_sp500=False):

    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if os.path.exists('historic_stock_data'):
        shutil.rmtree('historic_stock_data')
    os.makedirs('historic_stock_data')

    end = dt.datetime.date(dt.datetime.now())
    start = dt.datetime.date(dt.datetime.now()) - dt.timedelta(days=10 * 370)
    for ticker in tickers:
        print(ticker)
        if os.path.exists('historic_stock_data/{}.csv'.format(ticker)):
            os.remove('{}.csv'.format(ticker), 'historic_stock_data')
        try:
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('historic_stock_data/{}.csv'.format(ticker))
        except RemoteDataError:
            continue

    return True


def percentage_calc():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f) # gets all tickers

    if os.path.exists('Month_Percent_Calc'):
        shutil.rmtree('Month_Percent_Calc')
    os.makedirs('Month_Percent_Calc') #holds all of the percent day files
    if not os.path.exists('Month_Percent_Calc'):
        print('ERROR')
        return False

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('historic_stock_data/{}.csv'.format(ticker)):
            continue
        calc_month(ticker)
    return True


#Calculate 1 month percent percent change from tickers data
def calc_month(ticker):
    df = pd.read_csv('historic_stock_data/{}.csv'.format(ticker))
    df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

    df.rename(columns={'Date': 'Start Date'}, inplace=True)
    df['Percent Change'] = df['Adj Close'].pct_change(periods=-21).mul(-1)
    df['End Date'] = df['Start Date'].shift(periods=-21)
    df = df.reindex(columns=['Start Date', 'End Date', 'Adj Close', 'Percent Change'])
    df.to_csv('Month_Percent_Calc/Percent_Change_{}.csv'.format(ticker))


"""
#wrapper for week percent (need test)
def percentage_calc_week():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f) # gets all tickers

    if os.path.exists('recent_Week_Percent_Calc'):
        shutil.rmtree('recent_Week_Percent_Calc')
    #if not os.path.exists('Month_Percent_Calc'):
    os.makedirs('recent_Week_Percent_Calc') #holds all of the percent day files
    if not os.path.exists('recent_Week_Percent_Calc'):
        print('Error')
        return False

    for ticker in tickers:
        print(ticker)
        calc_week(ticker)
    return True

#calculate 1 week percent change(need tested)
def calc_week(ticker):
    df = pd.read_csv('historic_stock_data/{}.csv'.format(ticker))
    df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

    df.rename(columns={'Date': 'Start Date'}, inplace=True)
    df['Percent Change'] = df['Adj Close'].pct_change(periods=-5).mul(-1)
    df['End Date'] = df['Start Date'].shift(periods=-5)
    df = df.reindex(columns=['Start Date', 'End Date', 'Adj Close', 'Percent Change'])
    #print(df)
    df.to_csv('recent_week_Percent_Calc/recent_day_week_percent_{}.csv'.format(ticker))
"""


#finds percent change correlating to timeframe that is 90%+ out of 10 years
def find_stock_list_wrapper():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f) # gets all tickers
    main_df = pd.DataFrame()
    for ticker in tickers:
        try:
            df = pd.read_csv('Month_Percent_Calc/Percent_Change_{}.csv'.format(ticker))
        except OSError:
            continue
        print(ticker)
        YEAR_index = pd.DatetimeIndex(df['Start Date']).year
        for i in range(252):
            YEAR = YEAR_index[i]
            if YEAR == 2010 or YEAR == 2011:
                temp_df = find_stock_list(df, ticker, i)
            else:
                break
            if temp_df.empty:
                continue
            if main_df.empty:
                main_df = temp_df
            else:
                main_df = main_df.append(temp_df)
    main_df.index = range(len(main_df))
    if not os.path.exists('final_csv_files'):
        os.makedirs('final_csv_files')
    if os.path.exists('final_csv_files/Shuffled_Final_Percents.csv'):
        os.remove('final_csv_files/Shuffled_Final_Percents.csv')
    main_df.to_csv('final_csv_files/Shuffled_Final_Percents.csv')
    return True


def find_stock_list(df, ticker, curr_index):
    #1st case, check if there is 10 years of data
    empty_df = pd.DataFrame()
    YEAR_index = pd.DatetimeIndex(df['Start Date']).year
    MONTH_index = pd.DatetimeIndex(df['Start Date']).month
    YEAR = YEAR_index[0]
    MONTH = MONTH_index[0]

    time_frame = 252 #number of work days in a year
    sign_val = [] #1 for positive, 0 for negative
    perc = 'Percent Change'
    #Check first 3 values
    hold = curr_index # hold value of current index
    for c in range(3):
        if df[perc][curr_index] > 0:
            sign_val.append(1)
        elif df[perc][curr_index] <= 0:
            sign_val.append(0)
        curr_index += time_frame
    #values are in place
    sign = find_const_sign(sign_val)  #finds constant sign that has to meet criteria
    curr_index = hold # reset back to starting index

    #for positive sign
    percent_values = [] #should be 10 values (up to index 9)
    year_values = [] #ultamiley find outlier if there is one
    key_error = 0
    for i in range(10):
        try:
            percent_values.append(df[perc][curr_index])
        except KeyError:
            key_error = 1
            break
        year_values.append(YEAR_index[curr_index])
        curr_index += time_frame
    #exception will break loop and set key
    if key_error == 1: #For error if out of range in index
        return empty_df
    #now we have an array of values
    total_percent = 0
    counter = 0
    outlier = 0
    if sign == 1:
        for x in range(10):
           if percent_values[x] > 0:
                total_percent += percent_values[x]
                counter += 1
           else:
                outlier = year_values[x]
        if counter >= 9:#90 percent success rate
            #make data frame, remmeber 'hold' still has value of current index
            #we need to change end date since it is not the same every year
            #curr index has the last date on the list
            temp_df = pd.DataFrame(columns=['Ticker', 'Start Date', 'End Date', 'Avg Percent Change', 'Outlier Year'])
            if outlier == 0:
                temp_df.loc[0] = [ticker, df['Start Date'][hold], df['End Date'][hold], total_percent/counter, np.nan]
            else:
                temp_df.loc[0] = [ticker, df['Start Date'][hold], df['End Date'][hold], total_percent/counter, outlier]
            return temp_df
        else:
            return empty_df
    elif sign == 0:
        for x in range(10):
            if percent_values[x] <= 0:
                total_percent += percent_values[x]
                counter += 1
            else:
                outlier = year_values[x]
        if counter >= 9:#90 percent rate of success at least
            #make data frame
            temp_df = pd.DataFrame(columns=['Ticker', 'Start Date', 'End Date', 'Avg Percent Change', 'Outlier Year'])
            if outlier == 0:
                temp_df.loc[0] = [ticker, df['Start Date'][hold], df['End Date'][hold], total_percent/counter, np.nan]
            else:
                temp_df.loc[0] = [ticker, df['Start Date'][hold], df['End Date'][hold], total_percent/counter, outlier]
            return temp_df
        else:
            return empty_df
    else:
        return empty_df


def find_const_sign(sign_val):
    if sign_val[0] == 1:
        if sign_val[1] == 1:
            sign = 1
        elif sign_val[1] == 0:
            if sign_val[2] == 1:
                sign = 1
            elif sign_val[2] == 0:
                sign = 0
    elif sign_val[0] == 0:
        if sign_val[1] == 1:
            if sign_val[2] == 1:
                sign = 1
            elif sign_val[2] == 0:
                sign = 0
        elif sign_val[1] == 0:
            sign = 0
    return sign


#sorts all the data inorder by date
def inorder_percents():
    if not os.path.exists('final_csv_files/Shuffled_Final_Percents.csv'):
        print('Error')
        return False
    df = pd.read_csv('final_csv_files/Shuffled_Final_Percents.csv')
    df = df.sort_values(by='Start Date')
    df.reset_index(drop=True, inplace=True)
    df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    if os.path.exists('final_csv_files/Sorted_Percents.csv'):
        os.remove('final_csv_files/Sorted_Percents.csv')
    df.to_csv('final_csv_files/Sorted_Percents.csv')
    return True

#finds timeframe in which 10/10 years were the same
def hundred_percent():
    df1 = pd.read_csv('final_csv_files/Sorted_Percents.csv')
    df = df1[df1['Outlier Year'].isnull()]
    df.reset_index(drop=True, inplace=True)
    df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    if os.path.exists('final_csv_files/Hundred_Percents.csv'):
        os.remove('final_csv_files/Hundred_Percents.csv')
    df.to_csv('final_csv_files/Hundred_Percents.csv')
    return True

