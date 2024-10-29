#!/usr/bin/env python3
"""
LRUCache module - implements a Least Recently Used caching system.
"""
from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """
    LRUCache defines a LRU caching system
    Inherits from BaseCaching
    """

    def __init__(self):
        """
        Initialize the cache using OrderedDict to maintain usage order
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Add an item to the cache using LRU algorithm
        Args:
            key: The key to store the item under
            item: The item to store
        """
        if key is not None and item is not None:
            # If key exists, remove it to update its position
            if key in self.cache_data:
                self.cache_data.pop(key)
            else:
                # If cache is full, remove least recently used item
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    lru_key, _ = self.cache_data.popitem(last=False)
                    print(f"DISCARD: {lru_key}")

            # Add new item (most recently used)
            self.cache_data[key] = item

    def get(self, key):
        """
        Retrieve an item from the cache by key and update access order
        Args:
            key: The key to look up
        Returns:
            The value associated with the key if it exists, None otherwise
        """
        if key is not None and key in self.cache_data:
            # Move accessed item to the end (most recently used)
            value = self.cache_data.pop(key)
            self.cache_data[key] = value
            return value
        return None
