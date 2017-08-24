# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 01:37:48 2017

@author: bryan
"""

from pymongo import MongoClient
import matplotlib.pyplot as plt

URI = "mongodb://admin:LesterCoffee!@cluster0-shard-00-00-9tg3l.mongodb.net:27017,cluster0-shard-00-01-9tg3l.mongodb.net:27017,cluster0-shard-00-02-9tg3l.mongodb.net:27017/attraction?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&readPreference=primaryPreferred"
#URI = "localhost:27017"

client = MongoClient(URI)
db = client.attraction
reviews = db.review1
users = db.user_profile1

good_reviews_monthly = {}
good_reviews_yearly = {}
avg_reviews_monthly = {}
avg_reviews_yearly = {}
bad_reviews_monthly = {}
bad_reviews_yearly = {}

for x in reviews.find({"rating": {"$gt": 3}}):
    try:
        good_reviews_monthly[x['rating_date'].month] = good_reviews_monthly[x['rating_date'].month]+1
    except:
        good_reviews_monthly[x['rating_date'].month] = 1
        
    try:
        good_reviews_yearly[x['rating_date'].year] = good_reviews_yearly[x['rating_date'].year]+1
    except:        
        good_reviews_yearly[x['rating_date'].year] = 1


for x in reviews.find({"rating": {"$eq": 3}}):
    try:
        avg_reviews_monthly[x['rating_date'].month] = avg_reviews_monthly[x['rating_date'].month]+1
    except:
        avg_reviews_monthly[x['rating_date'].month] = 1

    try:
        avg_reviews_yearly[x['rating_date'].year] = avg_reviews_yearly[x['rating_date'].year]+1
    except:        
        avg_reviews_yearly[x['rating_date'].year] = 1

for x in reviews.find({"rating": {"$lt": 3}}):
    try: 
        bad_reviews_monthly[x['rating_date'].month] = bad_reviews_monthly[x['rating_date'].month]+1
    except: 
        bad_reviews_monthly[x['rating_date'].month] = 1
        
    try: 
        bad_reviews_yearly[x['rating_date'].year] = bad_reviews_yearly[x['rating_date'].year]+1 
    except: 
        bad_reviews_yearly[x['rating_date'].year] = 1

#seaonal good review
plt.plot(*zip(*sorted(good_reviews_monthly.items())))
plt.xlabel('Month')
plt.ylabel('Good Reviews')
plt.title('Seasonality')
plt.grid(True)
plt.show()

#seaonal bad review
plt.plot(*zip(*sorted(avg_reviews_monthly.items())))
plt.xlabel('Month')
plt.ylabel('Average Reviews')
plt.title('Seasonality')
plt.grid(True)
plt.show()

#seaonal average review
plt.plot(*zip(*sorted(bad_reviews_monthly.items())))
plt.xlabel('Month')
plt.ylabel('Bad Reviews')
plt.title('Seasonality')
plt.grid(True)
plt.show()



#trend good review
plt.plot(*zip(*sorted(good_reviews_yearly.items())))
plt.xlabel('Year')
plt.ylabel('Good Reviews')
plt.title('Trend')
plt.grid(True)
plt.show()

#trend average review
plt.plot(*zip(*sorted(avg_reviews_yearly.items())))
plt.xlabel('Year')
plt.ylabel('Average Reviews')
plt.title('Trend')
plt.grid(True)
plt.show()

#trend bad review
plt.plot(*zip(*sorted(bad_reviews_yearly.items())))
plt.xlabel('Year')
plt.ylabel('Bad Reviews')
plt.title('Trend')
plt.grid(True)
plt.show()

client.close()
