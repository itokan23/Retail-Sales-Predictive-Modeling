# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 17:15:39 2017

@author: Kan Ito
itokan@berkeley.edu
=======================
IES Data Science Challenge 
Draw Data
"""
import csv
from datetime import datetime, timedelta
import datetime
## Get Data
# Extract Data

# convert store string to respective store ID
def conv_store(store):
     #store_list = []

     if store == 'Jacksonville':
          return 1
     elif store == 'Albany':
          return 2
     elif store == 'Springfield':
          return 3
     elif store == 'Eugene':
          return 4
     elif store == 'Bend':
          return 5
     elif store == 'Tacoma':
          return 6
 
# convert jacket brand string to their respective store ID
def conv_brand(brand):
     brandlist = []
     for i,j in enumerate(brand):
          if brand[i] == 'Bogota':
               brandlist.append(1)
          elif brand[i] == 'South Face':
               brandlist.append(2)
          elif brand[i] == 'Pangea':
               brandlist.append(3)
     return brandlist

# Holiday Discount data
def get_holiday_discount_data():
     with open('2015_and_2016_Holiday_Discount_Sales.csv','rb',) as f:
         reader = csv.reader(f, delimiter=',')
         #initialize
         holiday_start = [] # date
         holiday_end = []   # date
         brand = []         # string
         discount_factor = [] # decimal
         count = 0
         for row in reader: 
             if count > 0:   # don't need first row
                 holiday_start.append(datetime.datetime.strptime(row[0], '%m/%d/%Y'))
                 holiday_end.append(datetime.datetime.strptime(row[1], '%m/%d/%Y'))
                 brand.append(row[2])
                 discount_factor.append(float(row[3]))
             count += 1 # keep count of entries
         return holiday_start, holiday_end, brand, discount_factor
     print "rows of data: ", count-1
#print holiday_start, holiday_end, brand, discount_factor
# seasonal discount data
def get_seasonal_discount_data():
     with open('2015_and_2016_Seasonal_Discount_Sales.csv','rb',) as f:
         reader = csv.reader(f,delimiter=',')
         #initialize
         first_day_sale = [] # date
         last_day_sale = []  # date
         bogota_discount = [] # %
         south_face_discount = [] # %
         pangea_discount = [] # %
         count = 0
         for row in reader: 
             if count > 0:   # don't need first row
                 first_day_sale.append(datetime.datetime.strptime(row[0], '%m/%d/%Y'))
                 last_day_sale.append(datetime.datetime.strptime(row[1], '%m/%d/%Y'))
                 bogota_discount.append(float(row[2][:-1]))
                 south_face_discount.append(float(row[3][:-1]))
                 pangea_discount.append(float(row[4][:-1]))
             count += 1 # keep count of entries
         return first_day_sale, last_day_sale, bogota_discount, south_face_discount, pangea_discount
     print "rows of data: ", count-1
#print first_day_sale, last_day_sale, bogota_discount, south_face_discount, pangea_discount
# Daily Brand Prices by store 2015-2016, this is awful data
def get_brand_prices_data(): 
     with open('Daily_Brand_Prices_by_Store_2015_2016.csv','rb',) as f:
         reader = csv.reader(f,delimiter=',')
         #initialize
         store_name = [] # string
         price_date = []  # date
         bogota_price = [] # $
         pangea_price = [] # $
         south_face_price = [] # $
         count = 0
         for row in reader: 
             if count > 0:   # don't need first row
                 store_name.append(row[0])
                 price_date.append(datetime.datetime.strptime(row[1], '%m/%d/%Y'))
                 if row[2] == '':
                      bogota_price.append(-1.0)
                 else:
                      bogota_price.append(float(row[2]))
                 if row[3] == '':
                      pangea_price.append(-1.0)
                 else:
                      pangea_price.append(float(row[3]))
                 if row[4] == '':
                      south_face_price.append(-1.0)
                 else:
                      south_face_price.append(float(row[4]))
             count += 1 # keep count of entries
        #organize better into 731 rows 
         return store_name, price_date, bogota_price, pangea_price, south_face_price
         print "rows of data: ", count-1

#%% second attempt

def get_brand_prices_data_alpha(): 
     with open('Daily_Brand_Prices_by_Store_2015_2016.csv','rb',) as f:
         reader = csv.reader(f,delimiter=',')
         #initialize
         H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y= ([] for i in range(18)) 
         bogota_price = [H,I,J,K,L,M] # $
         south_face_price = [N,O,P,Q,R,S]
         pangea_price = [T,U,V,W,X,Y] # $
         for i in range(731):
              for j in range(6):
                   bogota_price[j].append(0.0)
                   south_face_price[j].append(0.0)
                   pangea_price[j].append(0.0)
         dates = []
         start_date = datetime.datetime(2015, 1, 1) 
         end_date = datetime.datetime(2017, 1, 1)
         for single_date in daterange(start_date, end_date): #initialize dates, size 731
              dates.append(single_date)    
         count = 0
         for row in reader: 
             if count > 0:
                
                 current_date = datetime.datetime.strptime(row[1], '%m/%d/%Y')
                 current_index = dates.index(current_date)
                 cur_store_id = conv_store(row[0])

                 if row[2] != '':
                      bogota_price[cur_store_id-1][current_index] = (float(row[2]))
                 if row[3] != '':
                      pangea_price[cur_store_id-1][current_index] = (float(row[3]))
                 if row[4] != '':
                      south_face_price[cur_store_id-1][current_index] = (float(row[4]))
                
             count += 1 # keep count of entries
        #organize better into 731 rows 
         for i in range(len(dates)):
              for j in range(6):
                   if (bogota_price[j][i] == '' or bogota_price[j][i] == 0.0):
                        bogota_price[j][i] = 75.0
                   if (south_face_price[j][i] == '' or south_face_price[j][i] == 0.0):
                        south_face_price[j][i] = 85.0
                   if (pangea_price[j][i] == '' or pangea_price[j][i] == 0.0):
                        pangea_price[j][i] = 105.0
                   
         return dates, bogota_price, south_face_price, pangea_price
         print "rows of data: ", count-1

#%%
# Transaction Extract 2015-2016
def get_transaction_extract_data():
     with open('transaction_extract_2015_2016.csv','rb',) as f:
         reader = csv.reader(f,delimiter=',')
         #initialize
         trx_id = [] # int
         trx_date = []  # date
         store_id = [] # int
         brand_id = [] # int
         num_sold = [] # int
         count = 0
         for row in reader: 
             if count > 0:   # don't need first row
                 trx_id.append(int(row[0]))
                 trx_date.append(datetime.datetime.strptime(row[1], '%m/%d/%Y'))
                 store_id.append(int(row[2]))
                 brand_id.append(int(row[3]))
                 num_sold.append(int(row[4]))
             count += 1 # keep count of entries
         return trx_id, trx_date, store_id, brand_id, num_sold
         print "rows of data: ", count-1

# Calculate Price of Jacket
# return price based on national discount program
def get_price(store_id, brand_id, date):
     holiday_start, holiday_end, brand, discount_factor = get_holiday_discount_data()
     first_day_sale, last_day_sale, bogota_discount, south_face_discount, pangea_discount = get_seasonal_discount_data()
     jacket_retail_price = [75, 85, 105] # bogota(1), south face(2) , pangea(3)
     brand_discount = [bogota_discount, south_face_discount, pangea_discount]
     brand_list = conv_brand(brand)
     for i,j in enumerate(first_day_sale):
          if (first_day_sale[i] <= date <= last_day_sale[i]):
               seasonal_discount = float(brand_discount[brand_id-1][i]/100)
               break
          else:
               seasonal_discount = 0.0
     for i,j in enumerate(holiday_start):
          if (holiday_start[i] <= date <= holiday_end[i] and brand_id == brand_list[i]):
               holiday_discount = discount_factor[i]
               break
          else:
               holiday_discount = 0.0
     if (holiday_discount > seasonal_discount):
          discount = holiday_discount
     elif (seasonal_discount > holiday_discount):
          discount = seasonal_discount
     else:
          discount = 0.0
     price = jacket_retail_price[brand_id-1] * (1 - discount)
     return price, discount
# for x ticks dates plotting
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
   
def count_sales(trx_id, trx_date, store_id, brand_id, num_sold):
     date_index = 0
     bogota_j,bogota_a,bogota_s,bogota_e,bogota_b,bogota_t = (([1] * 731) for i in range(6))
     south_face_j,south_face_a,south_face_s,south_face_e,south_face_b,south_face_t = (([1] * 731) for i in range(6))
     pangea_j,pangea_a,pangea_s,pangea_e,pangea_b,pangea_t = (([1] * 731) for i in range(6))
     jack = [bogota_j, south_face_j, pangea_j]
     albany = [bogota_a, south_face_a, pangea_a]
     spring = [bogota_s, south_face_s, pangea_s]
     eugene = [bogota_e, south_face_e, pangea_e]
     bend = [bogota_b, south_face_b, pangea_b]
     tacoma = [bogota_t, south_face_t, pangea_t]
     count_by_city = [jack, albany, spring, eugene, bend, tacoma]
     list_of_dates = ([datetime.datetime(2015,1,1)] * 731)
     for i,j in enumerate(trx_id): 
         # temp = count_by_city[store_id[i]-1][brand_id[i]-1][date_index]
          print store_id[i], trx_date[i], date_index
          count_by_city[store_id[i]-1][brand_id[i]-1][date_index] += num_sold[i] 
          if (i == (len(trx_date)-1)):
               break
          elif (trx_date[i+1] != trx_date[i]):
               date_index += 1 # next day
               list_of_dates[date_index] = trx_date[i]
     return count_by_city, list_of_dates

