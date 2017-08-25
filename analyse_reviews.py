#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 17:04:29 2017

@author: sophie
"""

from __future__ import generators    # needs to be at the top of your module
import data_access as da
import nltk
import re
from rake_nltk import RakeKeywordExtractor
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def find_neg_reviews(batch_size=100):
    total = 0
    while total < 400:
        results = da.find({"rating": {"$lt": 3}}).limit(batch_size).skip(total)
        if not results:
            break
        for result in results:
            total = total + 1
            yield result
            
def review_to_words(review_text):
    # Function to convert a raw review to a string of words
    
    # Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    words = letters_only.lower().split()                                             
    # 
    # Remove stop words
    english_words = set(nltk.corpus.words.words())
    meaningful_words = [w for w in words if w in english_words and len(w) > 1]   
    #
    # Join the words back into one string separated by space, 
    # and return the result.
    return(" ".join(meaningful_words))   
    
def DrawWordCloud(text):
    wordcloud = WordCloud(max_font_size=60).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
if __name__ == '__main__':
    #print(is_english("xa"))
    # import nltk
    # nltk.download('stopwords')
    rake = RakeKeywordExtractor()
    keywords = []
    results = da.find({"rating": {"$lt": 3}})
    for result in results:
        review = review_to_words(result["title"] + " " + result["entry"])
        
        all_keywords = rake.extract(review, incl_scores=True)
        if len(all_keywords) > 5:
            all_keywords = all_keywords[5]
        for key in all_keywords:
            if isinstance(key, str):
                keywords.append(key.replace(" ", "_"))
    print(keywords)
    DrawWordCloud(" ".join(keywords))
        
        