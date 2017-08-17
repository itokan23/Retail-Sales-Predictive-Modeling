# -*- coding: utf-8 -*-
"""
Created on Fri Aug 04 13:38:27 2017

@author: Kan Ito
itokan@berkeley.edu
"""
# ============ This is for proof of concept that numpy, pandas can be used as well

import pandas as pd
from pandas import datetime
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
import math
%matplotlib inline
def get_holiday_discount_data():
     holiday_discounts = pd.read_csv('2015_and_2016_Holiday_Discount_Sales.csv', sep=',')
     holiday_discounts['Holiday Period End'] = pd.to_datetime(holiday_discounts['Holiday Period End'])
     holiday_discounts['Holiday Period Start'] = pd.to_datetime(holiday_discounts['Holiday Period Start'])
     return holiday_discounts
def get_seasonal_discount_data():
     seasonal_discounts = pd.read_csv('2015_and_2016_Seasonal_Discount_Sales.csv',sep=',')
     seasonal_discounts.columns = ['First Day','Last Day','Bogota','South Face','Pangea']
     # convert to datetime
     seasonal_discounts['First Day'] = pd.to_datetime(seasonal_discounts['First Day'])
     seasonal_discounts['Last Day'] = pd.to_datetime(seasonal_discounts['Last Day'])
     #float percentages
     seasonal_discounts['Bogota'] = seasonal_discounts['Bogota'].replace('%','',regex=True).astype('float')/100
     seasonal_discounts['South Face'] = seasonal_discounts['South Face'].replace('%','',regex=True).astype('float')/100
     seasonal_discounts['Pangea'] = seasonal_discounts['Pangea'].replace('%','',regex=True).astype('float')/100
     return seasonal_discounts
def get_brand_prices_data_beta(): 
     daily_prices = pd.read_csv('Daily_Brand_Prices_by_Store_2015_2016.csv',sep = ',')
     daily_prices.columns = ['Store','Date','Bogota','Pangea','South Face']
     # convert to datetime
     daily_prices['Date'] = pd.to_datetime(daily_prices['Date'])
     return daily_prices
def get_transaction_extract_data():
     transactions = pd.read_csv('transaction_extract_2015_2016.csv',sep=',')
     transactions.columns = ['TransactionID','Date','Store','Brand','Qty']
     transactions['Date'] = pd.to_datetime(transactions['Date'])
     store_names = {1:'Jacksonville',2:'Albany',3:'Springfield',4:'Bend',5:'Eugene',6:'Tacoma'}
     brand_names = {1:'Bogota',2:'South Face',3:'Pangea'}
     transactions = transactions.replace({'Store':store_names})
     transactions = transactions.replace({'Brand':brand_names})
     return transactions
#%%
if __name__ == "__main__":
     #extract data
     hol_dis = get_holiday_discount_data()
     seas_dis = get_seasonal_discount_data()
     daily_prices = get_brand_prices_data_beta()
     # category essentials
     stores = ['Jacksonville','Albany','Springfield','Eugene','Bend','Tacoma']
     retail_prices = [75,85,105]
     brands = ['Bogota','South Face','Pangea']
     #%% This one takes a bit longer
     transactions = get_transaction_extract_data()
     #%% Create new data frame to organize better
     daily_prices = daily_prices.sort_values(by=['Store','Date'],ascending=[1,1])
     daily_prices_cp = daily_prices.copy()
     print daily_prices.isnull().any()
     prices = pd.DataFrame(daily_prices['Date'].unique())
     prices['Store'] = stores[0]
     prices['Bogota'] = 0.0
     prices['South Face'] = 0.0
     prices['Pangea'] = 0.0
     prices.columns = ['Date','Store','Bogota','South Face','Pangea']
     for i in range(len(stores)-1):
          prices1 = pd.DataFrame(daily_prices['Date'].unique())
          prices1['Store'] = stores[i+1]
          prices1['Bogota'] = 0.0
          prices1['South Face'] = 0.0
          prices1['Pangea'] = 0.0
          prices1.columns = ['Date','Store','Bogota','South Face','Pangea']
          prices = prices.append(prices1,ignore_index=True)     
     #%% Fill the new dataframe
     daily_prices = daily_prices.fillna(0.0) #set null entries to zero
     for index,row in prices.iterrows():
          alist = daily_prices[(daily_prices['Date']==row['Date']) & (daily_prices['Store']==row['Store'])].index.tolist()
          for i in range(len(alist)): 
               if daily_prices.loc[alist[i-1]]['Bogota'] != 0.0:
                    prices.set_value(index,'Bogota',daily_prices.loc[alist[i-1]]['Bogota'])
               if daily_prices.loc[alist[i-1]]['South Face'] != 0.0:
                    prices.set_value(index,'South Face',daily_prices.loc[alist[i-1]]['South Face'])
               if daily_prices.loc[alist[i-1]]['Pangea'] != 0.0:
                    prices.set_value(index,'Pangea',daily_prices.loc[alist[i-1]]['Pangea'])
     #%% Combine Holiday Discount and Seasonal Discount
     # Holiday Discounts
     discount_program1 = pd.DataFrame(hol_dis['Holiday Period Start'][0:14])
     discount_program1['Last Day'] = hol_dis['Holiday Period End'][0:14]
     discount_program1.columns = ['First Day','Last Day']
     for i in range(len(retail_prices)):
          discount_program1.insert(i+2,brands[i],retail_prices[i] * (1 - hol_dis['Discount Factor'][(0):(14)]),allow_duplicates=True)
          hol_dis = hol_dis[hol_dis.Brand != brands[i]]
          hol_dis = hol_dis.reset_index(drop=True)
     hol_dis = get_holiday_discount_data()
     # Seasonal Discounts
     discount_program2 = pd.DataFrame(seas_dis['First Day'])
     discount_program2['Last Day'] = seas_dis['Last Day']
     for i in range(len(retail_prices)):
          discount_program2[brands[i]] = retail_prices[i] * (1 - seas_dis[brands[i]])
     discount_program = discount_program1.append(discount_program2,ignore_index=True)
     print "National Discount Program"
     print
     print discount_program
     #%% Apply to Daily Prices
     discounted_prices = prices.copy()
     for index,row in discounted_prices.iterrows():
          for i,r in discount_program.iterrows():
               if (row['Date'] >= r['First Day'] and row['Date'] <= r['Last Day']):
                    for b in range(len(brands)):
                         if (row[brands[b]] > r[brands[b]] or row[brands[b]] == 0.0 ):
                              discounted_prices.set_value(index,brands[b],r[brands[b]])
               else:
                    for b in range(len(brands)):
                         if row[brands[b]] == 0.0:
                              discounted_prices.set_value(index,brands[b],retail_prices[b])
     #%% Exploratory Visuals
     for i in range(len(brands)):
          plt.figure(figsize=(10,5))
          plt.xlabel('Date')
          plt.ylabel('Price [$]')
          plt.title(brands[i])
          plt.scatter(discounted_prices['Date'].values,discounted_prices[brands[i]])
          plt.show()
     #%% Find where there are prices=0 USD
     zero_mask = discounted_prices[brands[0]] == 0.0
     print zero_mask
     zero_mask.describe()
     zero_mask.value_counts()
     #%% Accumulate Units sold by day
     # Very expensive
     sales = prices.copy()
     for i in range(len(brands)):
          sales[brands[i]] = sales[brands[i]].astype(int)
          sales[brands[i]] = sales[brands[i]] * 0
     for index,row in sales.iterrows(): #iterates through each day 6 times
          for j in range(len(brands)):
               sums = 0
               mask = (transactions['Date'] == row['Date'])
               temp = transactions[mask]
               mask2 = (temp['Brand'] == brands[j])
               temp2 = temp[mask2]
               mask3 = (temp2['Store'] == row['Store'])
               temp3 = temp2[mask3]
               sums = temp3['Qty'].sum()
               sales.set_value(index,brands[j],sums)
     #%% Exploratory Analysis of Sales
     # Let's look at sales per store
     %matplotlib auto
     for i in range(len(stores)):
          mask = sales['Store'] == stores[i]
          storewise = sales[mask]
          plt.figure()
          f, axarr = plt.subplots(3,sharex=True,figsize=(13,8))
          axarr[0].scatter(storewise['Date'].values,storewise[brands[0]],color='g')
          axarr[0].set_title(stores[i],fontsize=20)
          axarr[0].set_ylim([0,125])
          axarr[1].scatter(storewise['Date'].values,storewise[brands[1]],color='r')
          axarr[1].set_ylim([0,125])
          axarr[2].scatter(storewise['Date'].values,storewise[brands[2]],color='m')
          axarr[2].set_xlabel('Date',fontsize=15)
          axarr[2].set_ylabel('Units Sold',fontsize=15)
          axarr[2].set_ylim([0,125])
          plt.show()
     #%% Reorganize Dates into seasonality
     
          
          

     

          



