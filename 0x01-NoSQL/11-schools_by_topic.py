#!/usr/bin/env python3
"""
Module to return the list of schools having a specific topic.
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.
    
    Args:
        mongo_collection: The pymongo collection object.
        topic (str): The topic to search for in the schools' topics.
    
    Returns:
        A list of dictionaries representing the schools that have the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))

