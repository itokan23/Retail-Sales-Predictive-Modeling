# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 12:36:12 2017

@author: Kan Ito
itokan@berkeley.edu
=======================
IES Data Science Challenge 
Clustering
"""
from draw_data import get_transaction_extract_data, get_brand_prices_data_alpha
from matplotlib import pyplot as plt
from draw_data import count_sales
import random
from cluster_class import KMeans,squared_clustering_errors,plot_squared_clustering_errors,recolor_image,is_leaf,get_children,get_values,cluster_distance,get_merge_order,bottom_up_cluster,generate_clusters
brands = ["Bogota", "South Face", "Pangea"]
stores = ["Jacksonville", "Albany", "Springfield", "Eugene","Bend", "Tacoma"]
jacket_prices = [75.0,85.0,105.0]
#%% Transaction Data File 4
trx_id, trx_date, store_id, brand_id, num_sold = get_transaction_extract_data()
#%% find total sold per day, takes ~10 mins    
count_by_city,list_of_dates = count_sales(trx_id, trx_date, store_id, brand_id, num_sold)      
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
plt.title('Jacksonville Bogota Sales')
plt.axis([0,0.5,0,50])
plt.legend()
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.show()


#%% zip and get training data
jack_zip = zip(discount_j,count_by_city[0][0])
random.seed(1)
jack_zip_ran = random.sample(jack_zip,183)
print len(jack_zip_ran)
random.seed(0) # so you get the same results as me
clusterer = KMeans(4)
clusterer.train(jack_zip_ran)
print "4-means:"
print clusterer.means
print
[A,B] = zip(*clusterer.means)
[C,D] = zip(*jack_zip)
plt.figure(22)
plt.scatter(C,D,color='m',s=30,label='training data')
plt.scatter(A,B,color='b',s=100,label='cluster mean')
plt.legend()
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.show()

#%%
[dis_j,count_j] = zip(*jack_zip_ran)
plt.figure(26)
plt.scatter(dis_j,count_j)
plt.title('Jacksonville Bogota Sales Training Data')
plt.axis([0,0.5,0,50])
plt.xlabel('Discount')
plt.ylabel('Sales')
plt.show()
#%%
recolor_image(jack_zip_ran,k=4)

#%%
print "errors as a function of k"
for k in range(1, len(jack_zip_ran) + 1):
     print k, squared_clustering_errors(jack_zip_ran, k)
print
#%%
plt.figure(30)
J = zip(*jack_zip_ran)
A = plt.scatter(J[0],J[1])
plot_squared_clustering_errors(A)
#%% plot squared clustering error
ks = range(1, 25)
errors = [squared_clustering_errors(jack_zip_ran, k) for k in ks]
plt.figure(31)
plt.plot(ks, errors)
plt.xticks(ks)
plt.title('Total Error vs # of clusters')
plt.xlabel("k")
plt.ylabel("total squared error")
plt.show()