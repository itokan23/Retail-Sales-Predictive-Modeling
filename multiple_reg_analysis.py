# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 23:13:31 2017

@author: Kan Ito
itokan@berkeley.edu
=======================
IES Data Science Challenge 
Multiple-Regression
"""

from draw_data import get_transaction_extract_data,get_brand_prices_data_alpha
from matplotlib import pyplot as plt
from draw_data import count_sales
from draw_data import daterange
import multiple_regression
from multiple_regression import estimate_beta, multiple_r_squared
import datetime as datetime
import random
#%% Transaction Data File 4
trx_id, trx_date, store_id, brand_id, num_sold = get_transaction_extract_data()

#%% find total sold per day, takes ~10 mins     
count_by_city, list_of_dates = count_sales(trx_id, trx_date, store_id, brand_id, num_sold)
#%% discount level vs sales4
# independent variables to use are the constant one, discount, and time of year
price_date, bogota_prices, south_face_prices, pangea_prices = get_brand_prices_data_alpha() 
discount_bog_j,discount_south_j,discount_pang_j = ([] for i in range(3))
discount_j = [discount_bog_j,discount_south_j,discount_pang_j]
discount_bog_a,discount_south_a,discount_pang_a = ([] for i in range(3))
discount_a = [discount_bog_a,discount_south_a,discount_pang_a]
discount_bog_s,discount_south_s,discount_pang_s = ([] for i in range(3))
discount_s = [discount_bog_s,discount_south_s,discount_pang_s]
discount_bog_e,discount_south_e,discount_pang_e = ([] for i in range(3))
discount_e = [discount_bog_e,discount_south_e,discount_pang_e]
discount_bog_b,discount_south_b,discount_pang_b = ([] for i in range(3))
discount_b = [discount_bog_b,discount_south_b,discount_pang_b]
discount_bog_t,discount_south_t,discount_pang_t = ([] for i in range(3))
discount_t = [discount_bog_t,discount_south_t,discount_pang_t]
discount = [discount_j,discount_a,discount_s,discount_e,discount_b,discount_t]

for j in range(6):
     for i in range(731):
          discount[j-1][0].append((75-bogota_prices[j-1][i])/75 *10) # jack,alb,spring,eug,bend,tac
          discount[j-1][1].append((85-south_face_prices[j-1][i])/85 *10)
          discount[j-1][2].append((105-pangea_prices[j-1][i])/105 *10)         
#%% 1. Multi Regression: Season, discounts
discount_jack = discount[0][0]
dates = list_of_dates
dates_ = ([1] * 731)
# Feb 4 is middle of winter, which is 34 days from Jan 1
multiplyer = -1
prev = 35/100.0
season = ([1] * 731)
print prev
for i,j in enumerate(list_of_dates):
     if (i == 34 or i == 217 or i == 399 or i == 582):
          multiplyer = multiplyer * -1

     season[i-1] = prev + (multiplyer / 100.0)
     prev = season[i-1] 
alpha = ([1] * 731)
random.seed(0)
x_y = zip(alpha, discount_jack, season, count_by_city[0][0])
training = random.sample(x_y,183) # 25% of the entire data
alpha_train, discount_train, season_train, count_j_train = zip(*training)
x = zip(alpha_train, discount_train, season_train)
y = count_j_train
print len(x)
random.seed(0)
beta1 = estimate_beta(x, y) 
print "beta", beta1
print "r-squared", multiple_r_squared(x, y, beta1)
print          
#%% 1. Plot
plot_set1 = zip(alpha_train, discount_train, season_train,y)
plot_set1.sort(key=lambda x:x[2])
alpha_train1,discount_train1, season_train1, y1 = zip(*plot_set1)
y_pred1 = []
for i in range(len(count_j_train)):
     y_pred1.append(beta1[0] + beta1[1] * discount_train1[i] + beta1[2] * float(season_train1[i]))
plt.figure(51)
plt.scatter(discount_train1, y1, color='g',label='Data')
plt.scatter(discount_train1, y_pred1,color='r',label='Regression',s=10)
plt.legend()
plt.title('1. Mult-Reg Jacksonville Bogota')
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.figure(52)
plt.scatter(season_train1, y1, color='g',label='Data')
plt.scatter(season_train1, y_pred1,color='r',label='Regression',s=10)
plt.legend()
plt.title('1. Mult-Reg Jacksonville Bogota')
plt.xlabel('Season')
plt.ylabel('Sales')
#%% 1. Try only winter season
alpha = ([1] * 731)
random.seed(0)
alpha_winter = alpha[0:91]+alpha[275:456]+alpha[639:731]
discount_jack_winter = discount_jack[0:91]+discount_jack[275:456]+discount_jack[639:731]
season_winter = season[0:91]+season[275:456]+season[639:731]
count_by_city_winter = count_by_city[0][0][0:91]+count_by_city[0][0][275:456]+count_by_city[0][0][639:731]
x_y = zip(alpha_winter, discount_jack_winter, season_winter, count_by_city_winter)
training = random.sample(x_y,183) # 50% of the entire data
alpha_train, discount_train, season_train, count_j_train = zip(*training)
x = zip(alpha_train, discount_train, season_train)
y = count_j_train
print len(x)
random.seed(1)
beta1 = estimate_beta(x, y) 
print "beta_winter", beta1
print "r-squared", multiple_r_squared(x, y, beta1)
print          
#%% 1. Try only summer season
alpha = ([1] * 731)
random.seed(1)
alpha_summer = alpha[91:275]+alpha[456:639]
discount_jack_summer = discount_jack[91:275]+discount_jack[456:639]
season_summer = season[91:275]+season[456:639]
count_by_city_summer = count_by_city[0][0][91:275]+count_by_city[0][0][456:639]
x_y = zip(alpha_summer, discount_jack_summer, season_summer, count_by_city_summer)
training = random.sample(x_y,183) # 50% of the entire data
alpha_train, discount_train, season_train, count_j_train = zip(*training)
x = zip(alpha_train, discount_train, season_train)
y = count_j_train
print len(x)
random.seed(1)
beta1 = estimate_beta(x, y) 
print "beta_summer", beta1
print "r-squared", multiple_r_squared(x, y, beta1)
print          
#%% 1. look at difference in coeff for discounts among diff brands
discount_jack = discount[0][2]+discount[1][2]+discount[2][2]+discount[3][2]+discount[4][2]+discount[5][2]
dates = list_of_dates
dates_ = ([1] * 731*6)
# Feb 4 is middle of winter, which is 34 days from Jan 1
multiplyer = -1
prev = 35/100.0
season = ([1] * 731)
print prev
for i,j in enumerate(list_of_dates):
     if (i == 34 or i == 217 or i == 399 or i == 582):
          multiplyer = multiplyer * -1

     season[i-1] = prev + (multiplyer / 100.0)
     prev = season[i-1] 
season_ = season + season + season+season+season+season
alpha = ([1] * 731*6)
random.seed(0)
x_y = zip(alpha, discount_jack, season_, count_by_city[0][2]+count_by_city[1][2]+count_by_city[2][2]+count_by_city[3][2]+count_by_city[4][2]+count_by_city[5][2])
training = random.sample(x_y,183) # 25% of the entire data
alpha_train, discount_train, season_train, count_j_train = zip(*training)
x = zip(alpha_train, discount_train, season_train)
y = count_j_train
print len(x)
random.seed(0)
beta1 = estimate_beta(x, y) 
print "beta", beta1
print "r-squared", multiple_r_squared(x, y, beta1)
print   

#%% 1. look at difference in coeff for discounts among diff locations
n = 5
discount_jack = discount[n][0]+discount[n][1]+discount[n][2]
dates = list_of_dates
dates_ = ([1] * 731*3)
# Feb 4 is middle of winter, which is 34 days from Jan 1
multiplyer = -1
prev = 35/100.0
season = ([1] * 731)
print prev
for i,j in enumerate(list_of_dates):
     if (i == 34 or i == 217 or i == 399 or i == 582):
          multiplyer = multiplyer * -1

     season[i-1] = prev + (multiplyer / 100.0)
     prev = season[i-1] 
season_ = season + season + season
alpha = ([1] * 731*3)
random.seed(0)
x_y = zip(alpha, discount_jack, season_, count_by_city[n][1]+count_by_city[n][1]+count_by_city[n][2])
training = random.sample(x_y,183) # 25% of the entire data
alpha_train, discount_train, season_train, count_j_train = zip(*training)
x = zip(alpha_train, discount_train, season_train)
y = count_j_train
print len(x)
random.seed(0)
beta1 = estimate_beta(x, y) 
print "beta", beta1
print "r-squared", multiple_r_squared(x, y, beta1)
print   
#%% 2. Multi Regress: Product of discounts and season term
dis_sea2 = []
for i in range(len(discount_train)):
     dis_sea2.append(discount_train[i] * season_train[i])
x2 = zip(alpha_train, discount_train, season_train, dis_sea2)
y2 = count_j_train
random.seed(0)
beta2 = estimate_beta(x2, y) 
print "beta", beta2
print "r-squared", multiple_r_squared(x2, y2, beta2)
print  

#%% 2. Plot 
plot_set2 = zip(alpha_train, discount_train, season_train, dis_sea2,y2)
plot_set2.sort(key=lambda x:x[1])
alpha_train2, discount_train2, season_train2, dis_sea2, y2 = zip(*plot_set2)
y_pred2 = []
for i in range(len(count_j_train)):
     y_pred2.append(beta2[0] + beta2[1] * discount_train2[i] + beta2[2] * float(season_train2[i]) + beta2[3] * float(dis_sea2[i]))

plt.figure(53)
plt.scatter(discount_train2, y2,color='g',label='Data')
plt.scatter(discount_train2, y_pred2,color='r',label='Regression',s=10)
plt.legend()
plt.title('2. Multiple Regression Jacksonville Bogota (Training Data)')
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.figure(54)
plt.scatter(season_train2, y2, color='g', label='Data')
plt.scatter(season_train2, y_pred2, color='r',label='Regression',s=10)
plt.legend()
plt.title('2. Multiple Regression Jacksonville Bogota (Training Data)')
plt.xlabel('Season')
plt.ylabel('Sales')
#%% 3. Multi-Regress: discounts and season and squared vars
dis_sea3 = []
dis_sq3 = []
sea_sq3 = []
for i in range(len(discount_train)):
     dis_sea3.append(discount_train[i] * season_train[i])
     dis_sq3.append(discount_train[i] * discount_train[i])
     sea_sq3.append(season_train[i] * season_train[i])
x3 = zip(alpha_train, discount_train, season_train, dis_sea3, dis_sq3, sea_sq3)
y3 = count_j_train
random.seed(0)
beta3 = estimate_beta(x3, y3) 
print "Alpha, Dis, season, season*discount, discount^2, seas^2"
print "beta", beta3
print "r-squared", multiple_r_squared(x3, y3, beta3)
print  
#%% 3. Plot
plot_set3 = zip(alpha_train, discount_train, season_train, dis_sea3, dis_sq3, sea_sq3 ,y3)
plot_set3.sort(key=lambda x:x[1])
alpha_train3, discount_train3, season_train3, dis_sea3, dis_sq3, sea_sq3, y3 = zip(*plot_set3)
y_pred3 = []
for i in range(len(count_j_train)):
     y_pred3.append(beta3[0] + beta3[1] * discount_train3[i] + beta3[2] * float(season_train3[i]) + beta3[3] * float(dis_sea3[i]) + beta3[4]*dis_sq3[i] + beta3[5]*sea_sq3[i])
plt.figure(55)
plt.scatter(discount_train3, y3,color='g',label='Data')
plt.scatter(discount_train3, y_pred3,color='r',label='Regression',s=10)
plt.legend()
plt.title('3. Multiple Regression Jacksonville Bogota (Training Data)')
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.figure(56)
plt.scatter(season_train3, y3,color='g',label='Data')
plt.scatter(season_train3, y_pred3,color='r',label='Regression',s=10)
plt.legend()
plt.title('3. Multiple Regression Jacksonville Bogota (Training Data)')
plt.xlabel('Season')
plt.ylabel('Sales')

#%% Test1. Predict on Test Set Jacksonville South Face
# Test Set
x_y = zip(alpha, discount_jack, season, count_by_city[0][1])
random.seed(4)
test_set = random.sample(x_y,183)
alpha_test, discount_test, season_test, y_test = zip(*test_set)
dis_sea_test = []
y_pred_test = []
dis_sq_test = []
sea_sq_test = []
for i in range(len(discount_test)):
     dis_sea_test.append(discount_test[i] * season_test[i])
     dis_sq_test.append(discount_test[i]*discount_test[i])
     sea_sq_test.append(season_test[i]*season_test[i])
     y_pred_test.append(beta3[0] + beta3[1] * discount_test[i] + beta3[2] * float(season_test[i]) + beta3[3] * dis_sea_test[i] + beta3[4] * dis_sq_test[i] +beta3[5] * sea_sq_test[i])
plt.figure(61)
plt.scatter(discount_test,y_test,color='b',label='Data')
plt.scatter(discount_test,y_pred_test,color='r',label='Regression',s=10)
plt.title('3. Multiple Regression Jacksonville South Face (Test Data)')
plt.legend()
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.figure(62)
plt.scatter(season_test,y_test,color='b',label='Data')
plt.scatter(season_test,y_pred_test,color='r',label='Regression',s=10)
plt.title('3. Multiple Regression Jacksonville South Face (Test Data)')
plt.legend()
plt.xlabel('Season')
plt.ylabel('Sales')
#%% 4. Model capturing city and brand
dis_sea4 = ([0] *(731*18))
dis_sq4 = ([0] *(731*18))
sea_sq4 = ([0] *(731*18))
all_bool = ([0] * 9)
for i in range(9):
     A = ([0] *(731*18))
     all_bool[i-1] = A
all_dates = []
all_discounts = []
k = 0 
all_seasons = []
all_counts = []
for i in range(6):
     for j in range(3):
          all_discounts = all_discounts + discount[i-1][j-1] 
          all_dates = all_dates + price_date
          all_seasons = all_seasons + season 
          all_counts = all_counts + count_by_city[i-1][j-1]
          for h in range(731):
               all_bool[i-1][k] = 1
               all_bool[j+5][k] = 1
               dis_sea4[k] = all_discounts[k] * all_seasons[k]
               dis_sq4[k] = all_discounts[k]*all_discounts[k]
               sea_sq4[k] = all_seasons[k]*all_seasons[k]
               k += 1
alpha = ([1] * (731*18))     
xy4 = zip(alpha,all_discounts,all_seasons,dis_sea4,dis_sq4,sea_sq4,all_bool[0],all_bool[1],all_bool[2],all_bool[3],all_bool[4],all_bool[5],all_bool[6],all_bool[7],all_bool[8],all_counts)
random.seed(2)
xy4_train = random.sample(xy4,3300)

alpha_train,all_discounts_train,all_seasons_train,dis_sea4_train,dis_sq4_train,sea_sq4_train,all_bool_train_jack,all_bool_train_alb,all_bool_train_spring,all_bool_train_eug,all_bool_train_bend,all_bool_train_tac,all_bool_train_bog,all_bool_train_south,all_bool_train_pang,all_counts_train = zip(*xy4_train)

x4 = zip(alpha_train, all_discounts_train, all_seasons_train, dis_sea4_train, dis_sq4_train, sea_sq4_train, all_bool_train_jack, all_bool_train_alb, all_bool_train_spring, all_bool_train_eug, all_bool_train_bend, all_bool_train_tac,all_bool_train_bog,all_bool_train_south,all_bool_train_pang)
y4 = all_counts_train
random.seed(4)
beta4 = estimate_beta(x4, y4) 
print "Alpha, Dis, season, season*discount, discount^2, seas^2, cities:jack->tacoma, brands:bog->pang "
print "beta", beta4
print "r-squared", multiple_r_squared(x4, y4, beta4)
print  
#%% 4. Plot
plot_set4 = zip(alpha_train,all_discounts_train,all_seasons_train,dis_sea4_train,dis_sq4_train,sea_sq4_train,all_bool_train_jack,all_bool_train_alb,all_bool_train_spring,all_bool_train_eug,all_bool_train_bend,all_bool_train_tac,all_bool_train_bog,all_bool_train_south,all_bool_train_pang,y4)
plot_set4.sort(key=lambda x:x[2])
alpha_train,all_discounts_train,all_seasons_train,dis_sea4_train,dis_sq4_train,sea_sq4_train,all_bool_train_jack,all_bool_train_alb,all_bool_train_spring,all_bool_train_eug,all_bool_train_bend,all_bool_train_tac,all_bool_train_bog,all_bool_train_south,all_bool_train_pang,y4 = zip(*plot_set4)
y_pred4 = []
for j in range(len(alpha_train)):
     i = j-1
     y_pred4.append(beta4[0]+beta4[1]*all_discounts_train[i]+beta4[2]*all_seasons_train[i]+beta4[3]*dis_sea4_train[i]+beta4[4]*dis_sq4_train[i]+beta4[5]*sea_sq4_train[i]+beta4[6]*all_bool_train_jack[i]+beta4[7]*all_bool_train_alb[i]+beta4[8]*all_bool_train_spring[i]+beta4[9]*all_bool_train_eug[i]+beta4[10]*all_bool_train_bend[i]+beta4[11]*all_bool_train_tac[i]+beta4[12]*all_bool_train_bog[i]+beta4[13]*all_bool_train_south[i]+beta4[14]*all_bool_train_pang[i])
plt.figure(63)
plt.scatter(all_discounts_train, y4, color='g',label='Data')
plt.scatter(all_discounts_train, y_pred4,color='r',label='Regression',s=10)
plt.legend()
plt.title('4. Mult-Reg Complete (Training Data)')
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.figure(64)
plt.scatter(all_seasons_train, y4, color='g',label='Data')
plt.scatter(all_seasons_train, y_pred4,color='r',label='Regression',s=10)
plt.legend()
plt.title('4. Mult-Reg Complete (Training Data)')
plt.xlabel('Season')
plt.ylabel('Sales')
#%% Test Set

xy4_test = random.sample(xy4,3300)
alpha_test,all_discounts_test,all_seasons_test,dis_sea4_test,dis_sq4_test,sea_sq4_test,all_bool_test_jack,all_bool_test_alb,all_bool_test_spring,all_bool_test_eug,all_bool_test_bend,all_bool_test_tac,all_bool_test_bog,all_bool_test_south,all_bool_test_pang,all_counts_test = zip(*xy4_test)
x4_test = zip(alpha_test,all_discounts_test,all_seasons_test,dis_sea4_test,dis_sq4_test,sea_sq4_test,all_bool_test_jack,all_bool_test_alb,all_bool_test_spring,all_bool_test_eug,all_bool_test_bend,all_bool_test_tac,all_bool_test_bog,all_bool_test_south,all_bool_test_pang)

y4_test = all_counts_test
plot_set4_test = zip(alpha_test,all_discounts_test,all_seasons_test,dis_sea4_test,dis_sq4_test,sea_sq4_test,all_bool_test_jack,all_bool_test_alb,all_bool_test_spring,all_bool_test_eug,all_bool_test_bend,all_bool_test_tac,all_bool_test_bog,all_bool_test_south,all_bool_test_pang,y4_test)
plot_set4_test.sort(key=lambda x:x[2])
alpha_test,all_discounts_test,all_seasons_test,dis_sea4_test,dis_sq4_test,sea_sq4_test,all_bool_test_jack,all_bool_test_alb,all_bool_test_spring,all_bool_test_eug,all_bool_test_bend,all_bool_test_tac,all_bool_test_bog,all_bool_test_south,all_bool_test_pang,y4_test = zip(*plot_set4)
y_pred4_test = []
for j in range(len(alpha_test)):
     i = j-1
     y_pred4_test.append(beta4[0]+beta4[1]*all_discounts_test[i]+beta4[2]*all_seasons_test[i]+beta4[3]*dis_sea4_test[i]+beta4[4]*dis_sq4_test[i]+beta4[5]*sea_sq4_test[i]+beta4[6]*all_bool_test_jack[i]+beta4[7]*all_bool_test_alb[i]+beta4[8]*all_bool_test_spring[i]+beta4[9]*all_bool_test_eug[i]+beta4[10]*all_bool_test_bend[i]+beta4[11]*all_bool_test_tac[i]+beta4[12]*all_bool_test_bog[i]+beta4[13]*all_bool_test_south[i]+beta4[14]*all_bool_test_pang[i])
plt.figure(65)
plt.scatter(all_discounts_test, y4_test,s=10, color='g',label='Data')
plt.scatter(all_discounts_test, y_pred4_test,s=10,color='r',label='Regression',)
plt.legend()
plt.title('4. Mult-Reg Complete')
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.figure(66)
plt.scatter(all_seasons_test, y4_test, s=10,color='g',label='Data')
plt.scatter(all_seasons_test, y_pred4_test,s=10,color='r',label='Regression')
plt.legend()
plt.title('4. Mult-Reg Complete')
plt.xlabel('Season')
plt.ylabel('Sales')
print "r-squared", multiple_r_squared(x4_test, y4_test, beta4)
#%% Color Coded by city and brand
plt.figure(71)
plt.scatter(discount[0][0],count_by_city[0][0],s=5,color='r',label='Jacksonville')
plt.scatter(discount[0][1],count_by_city[0][1],s=5,color='r')
plt.scatter(discount[0][2],count_by_city[0][2],s=5,color='r')
plt.scatter(discount[1][0],count_by_city[1][0],s=5,color='b',label='Albany')
plt.scatter(discount[1][1],count_by_city[1][1],s=5,color='b')
plt.scatter(discount[1][2],count_by_city[1][2],s=5,color='b')
plt.scatter(discount[2][0],count_by_city[2][0],s=5,color='g',label='Springfield')
plt.scatter(discount[2][1],count_by_city[2][1],s=5,color='g')
plt.scatter(discount[2][2],count_by_city[2][2],s=5,color='g')
plt.scatter(discount[3][0],count_by_city[3][0],s=5,color='m',label='Eugene')
plt.scatter(discount[3][1],count_by_city[3][1],s=5,color='m')
plt.scatter(discount[3][2],count_by_city[3][2],s=5,color='m')
plt.scatter(discount[4][0],count_by_city[4][0],s=5,color='y',label='Bend')
plt.scatter(discount[4][1],count_by_city[4][1],s=5,color='y')
plt.scatter(discount[4][2],count_by_city[4][2],s=5,color='y')
plt.scatter(discount[5][0],count_by_city[5][0],s=5,color='c',label='Tacoma')
plt.scatter(discount[5][1],count_by_city[5][1],s=5,color='c')
plt.scatter(discount[5][2],count_by_city[5][2],s=5,color='c')
plt.legend()
plt.title('The Data by City')
plt.xlabel('Discount')
plt.ylabel('Sales')
#%%
plt.figure(72)
plt.scatter(season,count_by_city[0][0],s=5,color='r',label='Jacksonville')
plt.scatter(season,count_by_city[0][1],s=5,color='r')
plt.scatter(season,count_by_city[0][2],s=5,color='r')
plt.scatter(season,count_by_city[1][0],s=5,color='b',label='Albany')
plt.scatter(season,count_by_city[1][1],s=5,color='b')
plt.scatter(season,count_by_city[1][2],s=5,color='b')
plt.scatter(season,count_by_city[2][0],s=5,color='g',label='Springfield')
plt.scatter(season,count_by_city[2][1],s=5,color='g')
plt.scatter(season,count_by_city[2][2],s=5,color='g')
plt.scatter(season,count_by_city[3][0],s=5,color='m',label='Eugene')
plt.scatter(season,count_by_city[3][1],s=5,color='m')
plt.scatter(season,count_by_city[3][2],s=5,color='m')
plt.scatter(season,count_by_city[4][0],s=5,color='y',label='Bend')
plt.scatter(season,count_by_city[4][1],s=5,color='y')
plt.scatter(season,count_by_city[4][2],s=5,color='y')
plt.scatter(season,count_by_city[5][0],s=5,color='c',label='Tacoma')
plt.scatter(season,count_by_city[5][1],s=5,color='c')
plt.scatter(season,count_by_city[5][2],s=5,color='c')
plt.legend()
plt.title('The Data by City')
plt.xlabel('Season')
plt.ylabel('Sales')
#%%
plt.figure(73)
plt.scatter(season,count_by_city[0][0],s=5,color='g',label='Bogota')
plt.scatter(season,count_by_city[2][0],s=5,color='g')
plt.scatter(season,count_by_city[2][0],s=5,color='g')
plt.scatter(season,count_by_city[3][0],s=5,color='g')
plt.scatter(season,count_by_city[4][0],s=5,color='g')
plt.scatter(season,count_by_city[5][0],s=5,color='g')
plt.scatter(season,count_by_city[0][1],s=5,color='m',label='South Face')
plt.scatter(season,count_by_city[2][1],s=5,color='m')
plt.scatter(season,count_by_city[2][1],s=5,color='m')
plt.scatter(season,count_by_city[3][1],s=5,color='m')
plt.scatter(season,count_by_city[4][1],s=5,color='m')
plt.scatter(season,count_by_city[5][1],s=5,color='m')
plt.scatter(season,count_by_city[0][2],s=5,color='y',label='Pangea')
plt.scatter(season,count_by_city[2][2],s=5,color='y')
plt.scatter(season,count_by_city[2][2],s=5,color='y')
plt.scatter(season,count_by_city[3][2],s=5,color='y')
plt.scatter(season,count_by_city[4][2],s=5,color='y')
plt.scatter(season,count_by_city[5][2],s=5,color='y')
plt.legend()
plt.title('The Data by Brand')
plt.xlabel('Season')
plt.ylabel('Sales')
#%%
plt.figure(74)
plt.scatter(discount[0][0],count_by_city[0][0],s=5,color='g',label='Bogota')
plt.scatter(discount[1][0],count_by_city[1][0],s=5,color='g')
plt.scatter(discount[2][0],count_by_city[2][0],s=5,color='g')
plt.scatter(discount[3][0],count_by_city[3][0],s=5,color='g')
plt.scatter(discount[4][0],count_by_city[4][0],s=5,color='g')
plt.scatter(discount[5][0],count_by_city[5][0],s=5,color='g')
plt.scatter(discount[0][1],count_by_city[0][1],s=5,color='m',label='South Face')
plt.scatter(discount[1][1],count_by_city[1][1],s=5,color='m')
plt.scatter(discount[2][1],count_by_city[2][1],s=5,color='m')
plt.scatter(discount[3][1],count_by_city[3][1],s=5,color='m')
plt.scatter(discount[4][1],count_by_city[4][1],s=5,color='m')
plt.scatter(discount[5][1],count_by_city[5][1],s=5,color='m')
plt.scatter(discount[0][2],count_by_city[0][2],s=5,color='y',label='Pangea')
plt.scatter(discount[1][2],count_by_city[1][2],s=5,color='y')
plt.scatter(discount[2][2],count_by_city[2][2],s=5,color='y')
plt.scatter(discount[3][2],count_by_city[3][2],s=5,color='y')
plt.scatter(discount[4][2],count_by_city[4][2],s=5,color='y')
plt.scatter(discount[5][2],count_by_city[5][2],s=5,color='y')

plt.legend()
plt.title('The Data by Brand')
plt.xlabel('Discount')
plt.ylabel('Sales')

