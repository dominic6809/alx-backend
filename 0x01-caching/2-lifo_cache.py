#!/usr/bin/env python3
"""
LIFOCache module - implements a Last-In-First-Out caching system.
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache defines a LIFO caching system
    Inherits from BaseCaching
    """

    def __init__(self):
        """
        Initialize the cache and the order tracking
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item to the cache using LIFO algorithm
        Args:
            key: The key to store the item under
            item: The item to store
        """
        if key is not None and item is not None:
            if (len(self.cache_data) >= BaseCaching.MAX_ITEMS
                    and key not in self.cache_data):
                # Remove the last item added (LIFO)
                last_key = self.order.pop()
                del self.cache_data[last_key]
                print(f"DISCARD: {last_key}")

            # Add/Update the new item
            self.cache_data[key] = item

            # Update order tracking
            if key in self.order:
                self.order.remove(key)
            self.order.append(key)

    def get(self, key):
        """
        Retrieve an item from the cache by key
        Args:
            key: The key to look up
        Returns:
            The value associated with the key if it exists, None otherwise
        """
        if key is not None:
            return self.cache_data.get(key)
        return None
