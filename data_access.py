from pymongo import MongoClient
import time
import pymongo

#We have 3 shards for scalability & high-availability, i.e. 1 primary and 2 secondary.
URI = "mongodb://admin:LesterCoffee!@cluster0-shard-00-00-9tg3l.mongodb.net:27017,cluster0-shard-00-01-9tg3l.mongodb.net:27017,cluster0-shard-00-02-9tg3l.mongodb.net:27017/attraction?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&readPreference=primaryPreferred"

client = MongoClient(URI)

#database=attraction, collection=review
db = client.attraction

"""-------------------------------------------------------
Insert list of documents
e.g. insert(review, [{"attraction":"Marina Bay Sands"},{"attraction":"Lau Pa Sat"},{"attraction" : "Jurong Bird Park"}])
----------------------------------------------------------"""
def insert(collection, docs):
    try:
        db[collection].insert_many(docs, ordered=False)
    except pymongo.errors.BulkWriteError:
        print("Duplicate(s) found !")
    db[collection].update_one({ "last_inserted_date": { "$exists" : "True"}}, {"$set": {"last_inserted_date":time.strftime("%d/%m/%Y")}}, upsert=True)

"""-------------------------------------------------------
Get the last date which reviews were inserted
----------------------------------------------------------"""
def get_last_inserted_date():
    doc = db.review.find_one({"last_inserted_date": { "$exists" : "True"}}, {"last_inserted_date" : 1, "_id" : 0})
    return doc["last_inserted_date"]

"""-------------------------------------------------------
General query 
e.g. find( { "Rating": { $lt: 3 } } )
----------------------------------------------------------"""
def find(query):
    return db.review.find(query)
