from CompanyTest import get_data, percentage_calc, find_stock_list_wrapper, inorder_percents
from main_functions import update, display_by_date, display_week, display_by_ticker, menu, display_hundred
import datetime as dt

# globals
today_date = dt.datetime.date(dt.datetime.now())

def main():
    print('STOCK CALENDAR')
    choice = 0
    while choice != 6:
        choice = menu()
        if choice == 1:
            #UPDATE DATA
            update()
        elif choice == 2:
            display_week()
        elif choice == 3:
            date_to_compare = input("\nEnter Date (Month-Day) (ex. 06-01): ")
            display_by_date(date_to_compare)
        elif choice == 4:
            ticker_to_compare = input("\nEnter Ticker Symb: ")
            ticker_to_compare = ticker_to_compare.upper()
            display_by_ticker(ticker_to_compare)
        elif choice == 5:
            display_hundred()

    print("Thank you")
if __name__ == '__main__':
    main()
