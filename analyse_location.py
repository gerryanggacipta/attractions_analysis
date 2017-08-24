# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 01:37:48 2017

@author: bryan
"""

from pymongo import MongoClient
import matplotlib.pyplot as plt
import operator

URI = "mongodb://admin:LesterCoffee!@cluster0-shard-00-00-9tg3l.mongodb.net:27017,cluster0-shard-00-01-9tg3l.mongodb.net:27017,cluster0-shard-00-02-9tg3l.mongodb.net:27017/attraction?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&readPreference=primaryPreferred"
#URI = "localhost:27017"

client = MongoClient(URI)
db = client.attraction
reviews = db.review1
users = db.user_profile1

good_reviews_location = {}
avg_reviews_location = {}
bad_reviews_location = {}

for x in reviews.find({"rating": {"$lt": 3}, "location": {"$ne": "None"}}):
    try:
        good_reviews_location[x['location']] = good_reviews_location[x['location']]+1
    except:
        good_reviews_location[x['location']] = 1

for x in reviews.find({"rating": {"$eq": 3}, "location": {"$ne": "None"}}):
    try:
        avg_reviews_location[x['location']] = avg_reviews_location[x['location']]+1
    except:
        avg_reviews_location[x['location']] = 1

for x in reviews.find({"rating": {"$gt": 3}, "location": {"$ne": "None"}}):
    try:
        bad_reviews_location[x['location']] = bad_reviews_location[x['location']]+1
    except:
        bad_reviews_location[x['location']] = 1



#location good review
dataframe = dict(sorted(good_reviews_location.items(), key=operator.itemgetter(1), reverse=True)[:5])        
plt.bar(range(len(dataframe)), dataframe.values(), align='center')
plt.xticks(range(len(dataframe)), dataframe.keys(), rotation=90)
plt.xlabel('Country')
plt.ylabel('Good Reviews')
plt.title('Demographics')
plt.show()

#location average review
dataframe = dict(sorted(avg_reviews_location.items(), key=operator.itemgetter(1), reverse=True)[:5])        
plt.bar(range(len(dataframe)), dataframe.values(), align='center')
plt.xticks(range(len(dataframe)), dataframe.keys(), rotation=90)
plt.xlabel('Country')
plt.ylabel('Average Reviews')
plt.title('Demographics')
plt.show()

#location bad review
dataframe = dict(sorted(bad_reviews_location.items(), key=operator.itemgetter(1), reverse=True)[:5])        
plt.bar(range(len(dataframe)), dataframe.values(), align='center')
plt.xticks(range(len(dataframe)), dataframe.keys(), rotation=90)
plt.xlabel('Country')
plt.ylabel('Bad Reviews')
plt.title('Demographics')
plt.show()

client.close()
