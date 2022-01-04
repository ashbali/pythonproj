"""
Created on Fri Nov 19 17:06:15 2021

@author: Aashna Bali

"""
import pandas as pd
from descriptive import arima,raw_trend,linear_trend,sma,statistics,input_data
from predictive import predictor
import yfinance as yf
from datetime import datetime

def get_company_list():  #to fetch company data
    return pd.read_csv('companylist.csv')

def t_and_c(): #to read t&c file and print it
    """Display terms and conditions from 'terms.txt'"""
    for line in open("terms.txt"):
        print(line, end = "")

def display_welcome(): # displays welcome message for user
    print('\n =*=*=*=*=*=*=*Welcome to the Stock Predictor Application=*=*=*=*=*=*=*= ')

def display_menu(): # printing the main menu for user
    print("\n======Main Menu======\n1. Search Stocks\n2. Show Descriptives\n3. Show Stock Predictions\n4. Show Graphs\n5. Export Data\n6. Read T&C\n7. Quit")
    
def get_choice(): # to ask user for a choice
    return input("Please choose option: ")

def search_stocks(company_list): # to search the companies and return descriptive stats on the data
    try:
        symbol = input("Please choose ticker symbol: ")
        
        #filters data based on Symbol Name matching case-insensitively
        filtered = company_list[(company_list.Symbol.str.lower() == symbol.lower())]    
        
        if len(filtered) > 1:
            print('Multiple Ticker Symbols Found -- Please enter exact ticker symbol to get result')       
                
        elif len(filtered) == 1:  #for exact match
            print('\n',filtered) #printing company info
            
        elif len(filtered) == 0: #If ticker does not exist in csv file, hitting yfinance API to fetch data
            try:
                get_ticker_data = input_data(ticker=symbol)
                if len(get_ticker_data) > 0:
                    print(get_ticker_data)
                else:
                     print('Please Try another ticker symbol')  
            except:
                print('Internal Error Occured, Please Retry!')    
                
    except:
            print('Internal Error Occured, Please Retry!')           
        
        
def show_descriptives(): #To display descriptive statistical measures for each ticker
    try:
        symbol = input("Please choose ticker symbol: ")
        stat_output = statistics(symbol)
        if stat_output is None:
            print('Invalid ticker symbol, please try again!')
            
        else:
             print(stat_output)
    except: 
        print("Internal Error Occurred, please try again!")
    
def download_data():  # to export the stock data to user
    try:
            symbol = input("Please choose ticker symbol: ")
            start = input("Please choose start period: (YYYY-MM-DD)")
            end = input("Please choose end period: (YYYY-MM-DD)")
            format = "%Y-%m-%d"
            
            check_sdt = bool(datetime.strptime(start, format))
            check_edt = bool(datetime.strptime(end, format))
            
            if check_sdt == False or check_edt == False:
                print("Invalid Data, please try again!")
            else:    
                # Download stock data then export as CSV
                data_df = yf.download(symbol, start=start, end=end)
                #Creates the export csv file with ticker name in lowercase as the filename
                data_df.to_csv(symbol.lower() + '.csv')         
    except:
            print("Internal Error Occurred, please try again!")                        
            
def show_predictions(): # method to show the stock predictions
    pred = None
    while pred is None:
        try:
            symbol = input("Please choose ticker symbol: ")
            period = input("Please enter modelling period [1mo,2mo,3mo,6mo,9mo,1y,2y,5y,10y,max]:  ")
            days = int(input("Please enter prediction days (1-365): "))
            check_period = [	period =='1mo'  , 
            					period =='2mo'  ,
                                period =='3mo'  , 
                                period =='6mo'  ,
                                period =='9mo'  ,
                                period =='1y'   , 
                                period =='2y'   , 
                                period =='5y'   , 
                                period =='10y'  ,
                                period =='max'
                            ]
            
            if any(check_period) and days in range(1,366): #check to ensure period and days are correctly entered by user
                    
                    try:
                        #to call predictor method defined in predictive.py
                        pred,r2,rmse,graph = predictor(ticker=symbol, period=period, flag=True, step = days)
                        
                        check_return = [    pred == 0,
                                            r2   == 0,
                                            rmse == 0
                                       ]
                        
                        if any(check_return) == False:
                            print ("Closing price at day {} would be around = {} ".format(days,pred))
                            print("The coefficient of determination (R^2) is {}.".format(round(r2,3)))
                            print("The root mean square error is {}.".format(round(rmse,3)))
                        
                    except KeyError:
                        print('Invalid Symbol - Please try again.')

            elif any(check_period) == False and days not in range(1,366):
                    print('## Invalid modelling period, please enter from given list [1mo,2mo,3mo,6mo,9mo,1y,2y,5y,10y,max]! ##')
                    print('## Invalid prediction days, please enter a number between 1 and 365 ##')
            
            elif any(check_period) == False:
                    print('## Invalid modelling period, please enter from given list [1mo,2mo,3mo,6mo,9mo,1y,2y,5y,10y,max]! ##')

            elif days not in range(1,366):
                    print('## Invalid prediction days, please enter a number between 1 and 365 ##')

        except:
            print('Internal Error in Predictions - Please try again.')
 
    
def display_graph_menu(): #to take input from user for plotting graphs
    print("\n====== GRAPH SELECTION MENU ======\nChoose the type of graph to display: \n1. Raw Time Series\n2. Linear Trend\n3. Simple Moving Average\n4. ARIMA\n5. Quit")    
   
def check_graph_inputs(period,price,arm_flag): #to validate graph method inputs

            check_period = [        period == '3d'   ,
                                    period == '5d'   ,
                                    period == '10d'  ,
                                    period == '15d'  ,
                                    period == '1mo'  ,
                                    period == '2mo'  ,
                                    period == '3mo'  ,
                                    period == '6mo'  ,
                                    period == '9mo'  ,
                                    period == '1y'   ,
                                    period == '2y'   ,
                                    period == '3y'   , 
                                    period == '5y'   , 
                                    period == '10y'  ,
                                    period == 'max'
                           ]
          
            check_price =  [
                                  price == 'Open'   ,
                                  price == 'Close'  ,
                                  price == 'Low'    ,
                                  price == 'High'   ,
                                  price == 'Volume' 
                            ] 
        
        				   
            check_period_arm =  [    period.lower()=='3y'  , 
                                     period.lower()=='5y'   ,  
                                     period.lower()=='10y'  , 
                                     period.lower()=='max'
        					
        				    ]
        
            check_price_arm =   [
                               
                                price.lower() == 'Open'   ,
                                price.lower() == 'Close'  ,
                                price.lower() == 'Low'    ,
                                price.lower() == 'High'   ,
            
                                ]
        
            if any(check_period_arm) == False and any(check_price_arm) == False and arm_flag == True:
                print("Invalid Time Period, please enter from given list [3y,5y,10y,max] ")
                print("Invalid type of stock price for ARIMA plot, please choose (Open/Close/High/Low) ")
                return 0
                
            elif any(check_period) == False and any(check_price) == False and arm_flag == False:
                  print("Invalid Time Period, please enter from given list [3d,5d,10d,15d,1mo,2mo,3mo,6mo,9mo,1y,2y,3y,4y,5y,10y,max] ")
                  print("Invalid Stock Price Type, please enter from given list [Open/Close/Low/High/Volume] ")
                  return 1
            elif any(check_period) == False and arm_flag == False : 
                  print("Invalid Time Period, please enter from given list [3d,5d,10d,15d,1mo,2mo,3mo,6mo,9mo,1y,2y,3y,4y,5y,10y,max] ")
                  return 2
              
            elif any(check_price) == False :
                   print("Invalid Stock Price Type, please enter from given list [Open/Close/Low/High/Volume] ")
                   return 3
           
   
def show_graphs(): #method to let user decide which graphs he wants to plot
    display_graph_menu()
    choice = get_choice()
    while choice != "5":
          
          ticker = input("Please choose ticker symbol: ")
          
          if choice == "4": #for ARIMA
              period = input("Please enter the time-period for the graph [3y,5y,10y,max]:  ")
              price = input("Please enter type of stock price (Open/Close/Low/High) : ") 
              check = check_graph_inputs(period, price, True) #method to validate graph inputs

          else: #for other graph types, below code to be executed
              period = input("Please enter the time-period for the graph [3d,5d,10d,15d,1mo,2mo,3mo,6mo,9mo,1y,2y,3y,4y,5y,10y,max]:  ")
              price = input("Please enter type of stock price (Open/Close/Low/High/Volume) : ") 
              check = check_graph_inputs(period, price, False) #method to validate graph inputs
                  
          #if input validation fails, this condition is executed    
          if (check == 0 or check == 1 or check == 2 or check == 3): 
              display_graph_menu()
              choice = get_choice()
         
              if choice == "5": #To exit from graph-menu, go back to main menu after a validation failure occurs
                  break
              
              elif choice == "4": #for ARIMA, after coming back from invalid input check method
                  ticker = input("Please choose ticker symbol: ")
                  period = input("Please enter the time-period for the graph [3y,5y,10y,max]:  ")
                  price = input("Please enter type of stock price (Open/Close/Low/High) : ") 
              
              else:
                  ticker = input("Please choose ticker symbol: ")
                  period = input("Please enter the time-period for the graph [3d,5d,10d,15d,1mo,2mo,3mo,6mo,9mo,1y,2y,3y,5y,10y,max]:  ")
                  price = input("Please enter type of stock price (Open/Close/Low/High/Volume) : ") 
          
          if choice == "1": #for Raw trend plot
              try:
                  raw = raw_trend(ticker, period, price)  #calls raw trend method from descriptive.py
                  if raw == 0:
                      print("Invalid ticker symbol, please try again!")
                  
              except:
                  print("Error occured while loading Raw trend! please try again!")
                
          elif choice == "2": #For Linear Trend Plot
              
                try:
                  linear = linear_trend(ticker, period, price, False) #calls linear trend method from descriptive.py
                  if linear == 0:
                      print("Invalid ticker symbol, please try again!")
                                            
                except:   
                   print("Error occured while loading Linear Trend! please try again!")
                    
          elif choice == "3": #For Simple Moving Averages Plot
              try:
                  sm_avg = sma(ticker, period, price) #calls sma trend method from descriptive.py
                  if sm_avg == 0:
                      print("Invalid ticker symbol, please try again!")
              
              except:
                   print("Error occured while loading Simple Moving Averages Trend! please try again!")

              
          elif choice == "4" : #For ARIMA Plot
               if price.lower() == "Volume" or price == "":
                   print("Invalid type of stock price for ARIMA plot, please choose (Open/Close/High/Low) ")
                   
               else :    
                   try:
                       arm = arima(ticker, period, price)
                       if arm == 0 : 
                           print("Invalid ticker symbol, please try again!")
                           
                       if arm == -1:
                           print("There is not enough data available for ARIMA. Please try again.")

                   except:
                       print("Error occured while loading ARIMA Trend! please try again!")
                       
          elif choice == "5":  # For Quit Option 
              break
            
          else:
               print("Wrong choice, please try again.")
                     
          display_graph_menu()
          choice = get_choice()
          

def process_choice(choice, company_list): # to display the main menu to the user and take the user inputs
    
    while choice != "7":
        if choice == "1":
            search_stocks(company_list)
            
        elif choice == "2":
            show_descriptives()
            
        elif choice == "3":
            show_predictions()
            
        elif choice == "4":
            show_graphs()

        elif choice == "5":
            download_data()
            
        elif choice == "6":
            t_and_c()
            
        elif choice == "7":
            break
            
        else:
            print("Wrong choice, please try again.")
            
        display_menu()
        choice = get_choice()

def main(): # the main function
    company_list = get_company_list()
    display_welcome()
    display_menu()
    choice = get_choice()
    process_choice(choice, company_list)


if __name__ == '__main__':
    main()    

    