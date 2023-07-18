#!/usr/bin/env python3
"""
A script that provides some stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient


def get_logs_count(mongo_collection):
    """
    get number of documents in the collection
    """
    return mongo_collection.count_documents({})


def get_methods_count(mongo_collection):
    """
    get number of documents with each http method
    in collection
    """
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        method_counts[method] = count
    return method_counts


def get_status_check_count(mongo_collection):
    """
    number of documents with method=GET
    """
    count = mongo_collection.count_documents(
            {"method": "GET", "path": "/status"})
    return count


client = MongoClient('mongodb://127.0.0.1:27017')
db = client.logs
nginx_collection = db.nginx


logs_count = get_logs_count(nginx_collection)
print("{} logs".format(logs_count))


method_counts = get_methods_count(nginx_collection)
print("Methods:")
for method, count in method_counts.items():
    print("\tmethod {}: {}".format(method, count))
