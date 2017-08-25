# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 08:05:47 2017

@author: bryan
"""

from pymongo import MongoClient
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def DrawWordCloud(text):
    #wordcloud = WordCloud().generate(text)  
    #plt.imshow(wordcloud, interpolation='bilinear')
    #plt.axis("off")
    wordcloud = WordCloud(max_font_size=60).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

URI = "mongodb://admin:LesterCoffee!@cluster0-shard-00-00-9tg3l.mongodb.net:27017,cluster0-shard-00-01-9tg3l.mongodb.net:27017,cluster0-shard-00-02-9tg3l.mongodb.net:27017/attraction?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&readPreference=primaryPreferred"
#URI = "localhost:27017"

client = MongoClient(URI)
db = client.attraction
reviews = db.review1
users = db.user_profile1

good_reviews_styles = ""
avg_reviews_styles = ""
bad_reviews_styles = ""
all_styles = ""

for x in reviews.find({"rating": {"$gt": 3}}):
    for y in users.find({"_id": {"$eq": x['user_id']}}):
        for z in y['travel_styles']:
             good_reviews_styles = good_reviews_styles + z.replace(" ", "_") + " "

for x in reviews.find({"rating": {"$eq": 3}}):
    for y in users.find({"_id": {"$eq": x['user_id']}}):
        for z in y['travel_styles']:
             avg_reviews_styles = avg_reviews_styles + z.replace(" ", "_") + " "

for x in reviews.find({"rating": {"$lt": 3}}):
    for y in users.find({"_id": {"$eq": x['user_id']}}):
        for z in y['travel_styles']:
             bad_reviews_styles = bad_reviews_styles + z.replace(" ", "_") + " "
             
all_styles = good_reviews_styles + avg_reviews_styles + bad_reviews_styles

print("good_reviews_styles")
DrawWordCloud(good_reviews_styles)

print("avg_reviews_styles")
DrawWordCloud(avg_reviews_styles)

print("bad_reviews_styles")
DrawWordCloud(bad_reviews_styles)   

print("all_styles") 
DrawWordCloud(all_styles)
          
client.close()     
             
