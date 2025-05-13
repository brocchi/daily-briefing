# utils/db.py
from pymongo import MongoClient
import os
import datetime

# MongoDB connection configuration
MONGO_URI = "mongodb://admin:admin123@mongodb:27017/"
DB_NAME = "scrapper_db"
COLLECTION_NAME = "scrapped_urls"

def get_mongo_client():
    return MongoClient(MONGO_URI)

def should_scrape(url_target):
    client = get_mongo_client()
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Check if URL exists in database
    result = collection.find_one({"url": url_target})
    return result is None

def summarize(html_text):
    return html_text[:300]  # Reduz para 300 caracteres

def save_scrapped(url):
    client = get_mongo_client()
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Insert URL into database
    collection.insert_one({
        "url": url,
        "timestamp": datetime.datetime.utcnow()
    })