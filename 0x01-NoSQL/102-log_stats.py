#!/usr/bin/env python3
"""
display information in a collection
"""


from pymongo import MongoClient


def get_logs_count(mongo_collection):
    """
    Get number of documents in the collection
    """
    return mongo_collection.count_documents({})


def get_methods_count(mongo_collection):
    """
    get number of documents with each HTTP method in the collection
    """
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        method_counts[method] = count
    return method_counts


def get_status_check_count(mongo_collection):
    """
    Get number of documents with method=GET
    """
    count = mongo_collection.count_documents(
            {"method": "GET", "path": "/status"})
    return count


def get_top_ips(mongo_collection, limit=10):
    """
    Get the top IPs in the collection
    """
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": limit
        }
    ]
    result = mongo_collection.aggregate(pipeline)
    top_ips = {}
    for item in result:
        ip = item["_id"]
        count = item["count"]
        top_ips[ip] = count
    return top_ips


client = MongoClient('mongodb://127.0.0.1:27017')
db = client.logs
nginx_collection = db.nginx


logs_count = get_logs_count(nginx_collection)
print(f"{logs_count} logs")


method_counts = get_methods_count(nginx_collection)
print("Methods:")
for method, count in method_counts.items():
    print(f"\tmethod {method}: {count}")


status_check_count = get_status_check_count(nginx_collection)
print(f"\tmethod {status_check_count}")


top_ips = get_top_ips(nginx_collection, limit=10)
print("IPs:")
for ip, count in top_ips.items():
    print(f"\t{ip}: {count}")
