#!/usr/bin/env python3
"""This script connects to MongoDB and retrieves log statistics."""

import pymongo
from pymongo import MongoClient
from collections import Counter

def connect_to_mongo():
    """Connect to MongoDB and return the client."""
    client = MongoClient("mongodb://localhost:27017/")
    return client

def get_log_stats(collection):
    """Retrieve log statistics from the specified collection."""
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Count HTTP methods
    methods = Counter()
    status_codes = Counter()
    ip_addresses = Counter()

    for log in collection.find():
        methods[log.get("method", "UNKNOWN")] += 1
        status_codes[log.get("status", "UNKNOWN")] += 1
        ip_addresses[log.get("ip", "UNKNOWN")] += 1

    # Print methods
    print("Methods:")
    for method, count in methods.items():
        print(f"\tmethod {method}: {count}")

    # Print status codes
    print(f"{sum(status_codes.values())} status check")
    print("IPs:")
    
    # Get the top 10 IPs
    top_ips = ip_addresses.most_common(10)
    for ip, count in top_ips:
        print(f"\t{ip}: {count}")

if __name__ == "__main__":
    client = connect_to_mongo()
    db = client.logs
    collection = db.nginx
    get_log_stats(collection)

