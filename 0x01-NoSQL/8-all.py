#!/usr/bin/env python3
"""
A Python function that lists all documents in a collection
"""


import pymongo


def list_all(mongo_collection):
    """
    function to list documents in mongo
    """
    if mongo_collection.count_documents({}) == 0:
        return []
    return list(mongo_collection.find())
