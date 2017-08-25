#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 17:04:29 2017

@author: sophie
"""

from pymongo import MongoClient
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
import nltk
nltk.download('stopwords')


def review_to_words( review_text ):
    # Function to convert a raw review to a string of words
    
    # Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    words = letters_only.lower().split()                             
    stops = set(stopwords.words("english"))                  
    # 
    # Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words ))   


def DrawWordCloud(text):
    text = review_to_words(text);

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

good_reviews_entry = ""
avg_reviews_entry = ""
bad_reviews_entry = ""
all_entry = ""

for x in reviews.find({"rating": {"$gt": 3}}):
    good_reviews_entry = good_reviews_entry + x['entry']

for x in reviews.find({"rating": {"$eq": 3}}):
    avg_reviews_entry = avg_reviews_entry + x['entry']

for x in reviews.find({"rating": {"$lt": 3}}):
    bad_reviews_entry = bad_reviews_entry + x['entry']
             
all_entry = good_reviews_entry + avg_reviews_entry + bad_reviews_entry

print("good_reviews_entry")
DrawWordCloud(good_reviews_entry)

print("avg_reviews_entry")
DrawWordCloud(avg_reviews_entry)

print("bad_reviews_entry")
DrawWordCloud(bad_reviews_entry)   

print("all_entry") 
DrawWordCloud(all_entry)
          
client.close()     
