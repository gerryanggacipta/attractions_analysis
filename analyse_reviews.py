#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 17:04:29 2017

@author: sophie
"""

from __future__ import generators    # needs to be at the top of your module
import data_access as da
from nltk.corpus import stopwords
import re

def find_neg_reviews(arraysize=10):
    while True:
        results = da.find( { "rating": { "$lt": 3 } } ).limit(arraysize)
        if not results:
            break
        for result in results:
            yield result
            
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

if __name__ == '__main__':
    # import nltk
    # nltk.download('stopwords')
    for result in find_neg_reviews():
        print(review_to_words(result["entry"]))
    