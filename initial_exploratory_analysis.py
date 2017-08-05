# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 18:21:44 2017

@author: Kan Ito
itokan@berkeley.edu
=======================
IES Data Science Challenge 
Exploratory Analysis
"""
from draw_data import get_holiday_discount_data
from draw_data import get_seasonal_discount_data
from draw_data import get_brand_prices_data, get_brand_prices_data_alpha
from draw_data import get_transaction_extract_data
from draw_data import get_price
from draw_data import daterange
from draw_data import count_sales
from matplotlib import pyplot as plt
import datetime as datetime
import matplotlib.dates as mdates
from collections import Counter
brands = ["Bogota", "South Face", "Pangea"]
stores = ["Jacksonville", "Albany", "Springfield", "Eugene","Bend", "Tacoma"]
jacket_prices = [75.0,85.0,105.0]
# Visualizing the Data

#%% Holiday Discount Data File 1
holiday_start, holiday_end, brand, discount_factor = get_holiday_discount_data()
plt.figure(1)
plt.scatter(holiday_start,discount_factor)
plt.title("Holiday Discounts")
plt.xlabel("Start Date")
plt.ylabel("Discount Factor")
plt.show()

#%% Seasonal Discount Data File 2
first_day_sale, last_day_sale, bogota_discount, south_face_discount, pangea_discount = get_seasonal_discount_data()

plt.figure(2)
plt.plot(last_day_sale, bogota_discount, color='g', label = 'Bogota',marker='o')
plt.plot(last_day_sale, south_face_discount, color='b', label = 'Southface') 
plt.plot(last_day_sale, pangea_discount, color='r',label = 'Pangea')
plt.legend(loc=4)
plt.title("Seasonal Discounts")
plt.xlabel("Start Date")
plt.ylabel("Discount %")
plt.show()
#%% Prices by Brand and Location File 3
store_name, price_date, bogota_price, pangea_price, south_face_price = get_brand_prices_data()
# Initialize
price_date_albany,price_date_bend,price_date_eugene,price_date_jacksonville,price_date_springfield,price_date_tacoma = ([] for i in range(6))
bogota_price_albany,bogota_price_bend,bogota_price_eugene,bogota_price_jacksonville,bogota_price_springfield,bogota_price_tacoma = ([] for i in range(6))
pangea_price_albany,pangea_price_bend,pangea_price_eugene,pangea_price_jacksonville,pangea_price_springfield,pangea_price_tacoma = ([] for i in range(6))
south_face_price_albany,south_face_price_bend,south_face_price_eugene,south_face_price_jacksonville,south_face_price_springfield,south_face_price_tacoma = ([] for i in range(6))
aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,kk,ll,mm,nn,oo,pp,qq,rr = ([] for i in range(18))
price_date_by_store = [price_date_albany,price_date_bend,price_date_eugene,price_date_jacksonville,price_date_springfield,price_date_tacoma]
bogota_price_by_store =[bogota_price_albany,bogota_price_bend,bogota_price_eugene,bogota_price_jacksonville,bogota_price_springfield,bogota_price_tacoma]
pangea_price_by_store = [pangea_price_albany,pangea_price_bend,pangea_price_eugene,pangea_price_jacksonville,pangea_price_springfield,pangea_price_tacoma]
south_face_price_by_store = [south_face_price_albany,south_face_price_bend,south_face_price_eugene,south_face_price_jacksonville,south_face_price_springfield,south_face_price_tacoma]
AA = [aa,bb,cc,dd,ee,ff]
BB = [gg,hh,ii,jj,kk,ll]
CC = [mm,nn,oo,pp,qq,rr]
discount_by_store = [AA,BB,CC]
dates = []
start_date = datetime.datetime(2015, 1, 1) 
end_date = datetime.datetime(2016, 12, 31)

for index,value in enumerate(store_name): # iterates through large data set,thrid file
     for i,j in enumerate(stores):
          if value == j:
               price_date_by_store[i-1].append(price_date[index])
               bogota_price_by_store[i-1].append(bogota_price[index])
               pangea_price_by_store[i-1].append(pangea_price[index])
               south_face_price_by_store[i-1].append(south_face_price[index])   
               discount_by_store[0][i-1].append(1.0 - bogota_price[index]/jacket_prices[0])
               discount_by_store[1][i-1].append(1.0 - south_face_price[index]/jacket_prices[1])
               discount_by_store[2][i-1].append(1.0 - pangea_price[index]/jacket_prices[2])

#%% Graphing for file 3
plt.figure(3)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
#plt.gca().xaxis.set_tick(np.arange(min(price_date_albany),max(price_date_albany),int((max_x-min_x)/len(labels))
#np.arange(min_x, max_x, int((max_x-min_x)/len(labels))))
plt.scatter(price_date_by_store[1], bogota_price_by_store[1], color='g', label = 'Bogota')
plt.scatter(price_date_by_store[1], south_face_price_by_store[1], color='b', label = 'Southface') 
plt.scatter(price_date_by_store[1], pangea_price_by_store[1], color='r',label = 'Pangea')
#plt.gcf().autofmt_xdate()
plt.legend(loc=4)
plt.title("Prices in Albany")
plt.xlabel("Date")
plt.ylabel("Price [$]")
plt.show()

#%% Transaction Data File 4
trx_id, trx_date, store_id, brand_id, num_sold = get_transaction_extract_data()

# count per brand and per store
Brand_ct = Counter(brand_id)
jack_count = 0
jack_date = []
albany_date = []
albany_count = 0
springfield_count = 0
eugene_count = 0
bend_count = 0
tacoma_count = 0
bogota_count = 0
south_face_count = 0
pangea_count = 0
for i,j in enumerate(trx_id): 
     if store_id[i] == 1: #Jacksonville
          jack_count += num_sold[i]
     elif store_id[i] == 2:
          albany_count += num_sold[i]

     elif store_id[i] == 3:
          springfield_count += num_sold[i]
     elif store_id[i] == 4:
          eugene_count += num_sold[i]
     elif store_id[i] == 5:
          bend_count += num_sold[i]
     elif store_id[i] == 6:
          tacoma_count += num_sold[i]
     else:
          print "something wrong with transaction", trx_id[i]
     if brand_id[i] == 1:
          bogota_count += num_sold[i]
     elif brand_id[i] == 2:
          south_face_count += num_sold[i]
     elif brand_id[i] == 3:
          pangea_count += num_sold[i]
     else:
          print "something wrong with transaction", trx_id[i]
store_count = [jack_count, albany_count, springfield_count, eugene_count, bend_count, tacoma_count]
brand_count = [bogota_count, south_face_count, pangea_count]
print "units sold per store: \n[jack,albany,spring,eug,bend,tac]"
print store_count
print "units sold per brand: \n[bogota,south,pang]"
print brand_count   
#%%
plt.figure(9)          
cities = ["Jacksonville", "Albany", "Springfield", "Eugene", "Bend","Tacoma"]
xs = [i+0.1 for i, _ in enumerate(cities)]
plt.bar(xs,store_count,color='g')
plt.ylabel("Jackets sold")
plt.title("Units Sold by City")
plt.xticks([i+0.1 for i, _ in enumerate(cities)],cities)
plt.show()  

plt.figure(10)
xs = [i+0.1 for i, _ in enumerate(brands)]
plt.bar(xs,brand_count, color='r')
plt.ylabel("Jackets sold")
plt.title("Units Sold by Brand")
plt.xticks([i+0.1 for i, _ in enumerate(brands)],brands)
plt.show()  

#%% Date vs Sales
count_by_city,list_of_dates = count_sales(trx_id, trx_date, store_id, brand_id, num_sold)
dates = []
start_date = datetime.datetime(2015, 1, 1) 
end_date = datetime.datetime(2017, 1, 1)
for single_date in daterange(start_date, end_date):
     dates.append(single_date)
xs = dates
#%%
plt.figure(11)
plt.scatter(xs, count_by_city[5][0], s=20,color='g', label = 'Bogota')
plt.scatter(xs, count_by_city[5][1], s=20,color='r', label = 'South Face')
plt.scatter(xs, count_by_city[5][2], s=20,color = 'b', label = 'Pangea')
plt.legend()
axes = plt.gca()
axes.set_ylim([0, 150])
plt.title('Tacoma Sales')
plt.xlabel('date')
plt.ylabel('units sold')
plt.show()
#%% discount level vs sales

price_date, bogota_prices, south_face_prices, pangea_prices = get_brand_prices_data_alpha() 
discount_j,discount_a,discount_s,discount_e,discount_b,discount_t = ([] for i in range(6))
for i in range(731):
     discount_j.append((75-bogota_prices[0][i])/75) #jacksonville
     discount_a.append((75-bogota_prices[1][i])/75)
     discount_s.append((75-bogota_prices[2][i])/75)
     discount_e.append((75-bogota_prices[3][i])/75)
     discount_b.append((75-bogota_prices[4][i])/75)
     discount_t.append((75-bogota_prices[5][i])/75)
plt.figure(24)
plt.scatter(discount_j,count_by_city[0][0],s=30,color='b',label='Winter')
plt.scatter(discount_j,count_by_city[0][1],s=30,color='b',label='Spring')
plt.scatter(discount_j,count_by_city[0][2],s=30,color='b',label='Summer')
plt.title("Effect of Discounts in Jacksonville")
plt.xlabel("Discount")
plt.ylabel("Sales")
plt.show()     
     #%%
plt.figure(25)
plt.scatter(discount_j[0:60],count_by_city[0][0][0:60],color='b',s=30,label='Winter')
plt.scatter(discount_j[60:151],count_by_city[0][0][60:151],color='g',s=30,label='Spring')
plt.scatter(discount_j[151:242],count_by_city[0][0][151:242],color='r',s=30,label='Summer')
plt.scatter(discount_j[242:333],count_by_city[0][0][242:333],color='m',s=30,label='Fall')
plt.scatter(discount_j[333:365],count_by_city[0][0][333:365],color='b',s=30)
plt.scatter(discount_j[365:425],count_by_city[0][0][365:425],color='b',s=30)
plt.scatter(discount_j[425:516],count_by_city[0][0][425:516],color='g',s=30)
plt.scatter(discount_j[516:607],count_by_city[0][0][516:607],color='r',s=30)
plt.scatter(discount_j[607:698],count_by_city[0][0][607:698],color='m',s=30)
plt.scatter(discount_j[698:731],count_by_city[0][0][698:731],color='b',s=30)
#plt.scatter(discount_a,bogota_a,color='b',s=10,label='Albany')
#plt.scatter(discount_s,bogota_s,color='m',s=10,label='Springfield')
#plt.scatter(discount_e,bogota_e,color='c',s=10,label='Eugene')
#plt.scatter(discount_b,bogota_b,color='g',s=10,label='Bend')
#plt.scatter(discount_t,bogota_t,color='y',s=10,label='Tacoma')
plt.title('Jacksonville Bogota Sales')
plt.axis([0,0.5,0,50])
plt.legend()
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.show()

#%% similar but for tacoma south face
for i in range(731):
     discount_j.append((105-south_face_prices[0][i])/105) #jacksonville
     discount_a.append((105-south_face_prices[1][i])/105)
     discount_s.append((105-south_face_prices[2][i])/105)
     discount_e.append((105-south_face_prices[3][i])/105)
     discount_b.append((105-south_face_prices[4][i])/105)
     discount_t.append((105-south_face_prices[5][i])/105)
     
plt.figure(26)
plt.scatter(discount_t[0:60],count_by_city[5][1][0:60],color='b',s=30,label='Winter')
plt.scatter(discount_t[60:151],count_by_city[5][1][60:151],color='g',s=30,label='Spring')
plt.scatter(discount_t[151:242],count_by_city[5][1][151:242],color='r',s=30,label='Summer')
plt.scatter(discount_t[242:333],count_by_city[5][1][242:333],color='m',s=30,label='Fall')
plt.scatter(discount_t[333:365],count_by_city[5][1][333:365],color='b',s=30)
plt.scatter(discount_t[365:425],count_by_city[5][1][365:425],color='b',s=30)
plt.scatter(discount_t[425:516],count_by_city[5][1][425:516],color='g',s=30)
plt.scatter(discount_t[516:607],count_by_city[5][1][516:607],color='r',s=30)
plt.scatter(discount_t[607:698],count_by_city[5][1][607:698],color='m',s=30)
plt.scatter(discount_t[698:731],count_by_city[5][1][698:731],color='b',s=30)
plt.title('Tacoma South Face Sales')
plt.axis([0,0.5,0,120])
plt.legend()
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.show()


#%%

# discount program vs date

print get_price(5,2, datetime.datetime(2016, 04, 25))

bogota,south_face,pangea = ([] for i in range(3))
jack_prices = [bogota, south_face, pangea]
bogota_dis,south_face_dis,pangea_dis = ([] for i in range(3))
prog_dis = [bogota_dis, south_face_dis, pangea_dis]
max_discount = []
dates = []
start_date = datetime.datetime(2015, 1, 1) 
end_date = datetime.datetime(2016, 12, 31)
for single_date in daterange(start_date, end_date):
     dates.append(single_date)
     for i,j in enumerate(brands):
          jack_prices[i].append(get_price(1,i+1,single_date)[0])

plt.figure(20)
plt.plot(dates, jack_prices[0],color = 'green', marker='.', label = 'Bogota')
plt.plot(dates, jack_prices[1],color = 'blue', marker = '.', label = 'South Face')
plt.plot(dates, jack_prices[2],color = 'red', marker = '.', label = 'Pangea')
plt.title("Jacksonville")
plt.legend()
plt.ylabel("$")
plt.show()

