#!/usr/bin/env python3
"""
A function that returns the list of school having a specific topic
"""


import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    function that get list of schools with specific topic
    """
    return list(mongo_collection.find({"topics": topic}))
