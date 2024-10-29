#!/usr/bin/env python3
"""
BasicCache module
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache defines a basic caching system with no limit on size
    Inherits from BaseCaching
    """

    def put(self, key, item):
        """
        Add an item to the cache.
        Args:
            key: The key to store the item under
            item: The item to store
        Returns:
            None
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Retrieve an item from the cache by key.
        Args:
            key: The key to look up
        Returns:
            The value associated with the key if it exists, None otherwise
        """
        if key is not None:
            return self.cache_data.get(key)
        return None
