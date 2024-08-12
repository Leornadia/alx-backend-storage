#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient

def log_stats():
    """ Function that fetches and prints log statistics """
    # Connect to the MongoDB server
    client = MongoClient('mongodb://127.0.0.1:27017')
    
    # Select the database and collection
    db = client.logs
    nginx_collection = db.nginx
    
    # Count the total number of logs
    total_logs = nginx_collection.count_documents({})
    
    # Print the total number of logs
    print(f"{total_logs} logs")
    
    # Print the number of logs for each HTTP method
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    
    # Count the number of logs with method GET and path /status
    status_check_count = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    log_stats()

