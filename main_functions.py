from CompanyTest import get_data, percentage_calc, find_stock_list_wrapper, inorder_percents, hundred_percent
import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import shutil
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests

# globals
today_date = dt.datetime.date(dt.datetime.now())

def update():
    val = False
    if not os.path.exists('sp500tickers.pickle'):
        val = get_data(True)
    else:
        val = get_data()
    if val:
        val = percentage_calc()
        print("25%")
    if val:
        val = find_stock_list_wrapper()
        print("\n50%")
    if val:
        val = inorder_percents()
        print("\n75%")
    if val:
        hundred_percent()
        print("\n100%\nUP TO DATE!")
        return True

def display_by_date(to_compare):
    if not os.path.exists('final_csv_files/Sorted_Percents.csv'):
        print('Update Data')
        return
    if not isinstance(to_compare, str):
        to_compare_parsed = to_compare.strftime("%Y-%m-%d")
        to_compare_string = dt.datetime.strptime(to_compare_parsed, '%Y-%m-%d').strftime("%m-%d")
    else:
        to_compare_string = to_compare
    df = pd.read_csv('final_csv_files/Sorted_Percents.csv')
    num_lines = len(df.index)
    for i in range(num_lines):
        start_date = df['Start Date'][i]
        start_date_string = dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%m-%d")
        end_date = df['End Date'][i]
        end_date_string = dt.datetime.strptime(end_date, '%Y-%m-%d').strftime("%m-%d")
        if to_compare_string == start_date_string:
            #print(df.loc[i, 'Ticker':])
            print('Ticker: ', df['Ticker'][i], '\tStart ', start_date_string, '\tEnd ', end_date_string,
                 '\tAvg Percent Change: ', (df['Avg Percent Change'][i] * 100).round(1), '%', '\tOutlier Year: ',
                  df['Outlier Year'][i], '\n')
#display a week from today
def display_week():
    if not os.path.exists('final_csv_files/Sorted_Percents.csv'):
        print('Update Data')
        return
    current_day = dt.datetime.date(dt.datetime.now())
    for i in range(5):
        display_by_date(current_day)
        current_day = current_day + dt.timedelta(days=1)

def display_by_ticker(ticker_to_compare):
    if not os.path.exists('final_csv_files/Sorted_Percents.csv'):
        print('Update Data')
        return
    df = pd.read_csv('final_csv_files/Sorted_Percents.csv')
    num_lines = len(df.index)
    for i in range(num_lines):
        start_date = df['Start Date'][i]
        start_date_string = dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%m-%d")
        end_date = df['End Date'][i]
        end_date_string = dt.datetime.strptime(end_date, '%Y-%m-%d').strftime("%m-%d")
        if ticker_to_compare == df['Ticker'][i]:
            #print(df.loc[i, 'Ticker':])
            print('Ticker: ', df['Ticker'][i], '\tStart ', start_date_string, '\tEnd ', end_date_string,
                  '\tAvg Percent Change: ', (df['Avg Percent Change'][i] * 100).round(1), '%', '\tOutlier Year: ', df['Outlier Year'][i], '\n')

def display_hundred():
    if not os.path.exists('final_csv_files/Hundred_Percents.csv'):
        print('Update Data')
        return
    df = pd.read_csv('final_csv_files/Hundred_Percents.csv')
    num_lines = len(df.index)
    for i in range(num_lines):
        start_date = df['Start Date'][i]
        start_date_string = dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%m-%d")
        end_date = df['End Date'][i]
        end_date_string = dt.datetime.strptime(end_date, '%Y-%m-%d').strftime("%m-%d")
        print('Ticker: ', df['Ticker'][i], '\tStart ', start_date_string, '\tEnd ', end_date_string,
              '\tAvg Percent Change: ', (df['Avg Percent Change'][i] * 100).round(1), '%', '\n')

def menu():
    choice = 0
    print("Today's Date: ", today_date, 'Picks: ')
    display_by_date(today_date)
    while choice != 1 and choice != 2 and choice != 3 and choice != 4 and choice != 5 and choice != 6:
        print('\n1 --- UPDATE DATA')
        print('\n2 --- DISPLAY WEEKS PICKS')
        print('\n3 --- SEARCH BY DATE')
        print('\n4 --- SEARCH BY TICKER')
        print('\n5 --- DISPLAY OUTLIER FREE STOCKS')
        print('\n6 --- QUIT')
        choice = int(input('\nENTER CHOICE HERE: '))
        print(choice)
    return choice

#display_hundred()