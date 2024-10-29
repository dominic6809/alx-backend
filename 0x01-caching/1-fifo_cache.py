#!/usr/bin/env python3
"""
FIFOCache module - implements a First-In-First-Out caching system.
"""
from base_caching import BaseCaching
from collections import OrderedDict


class FIFOCache(BaseCaching):
    """
    FIFOCache defines a FIFO caching system
    Inherits from BaseCaching
    """

    def __init__(self):
        """
        Initialize the cache using OrderedDict to maintain FIFO order
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Add an item to the cache using FIFO algorithm
        Args:
            key: The key to store the item under
            item: The item to store
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                if key not in self.cache_data:
                    # Get the first item (FIFO)
                    first_key, _ = self.cache_data.popitem(last=False)
                    print(f"DISCARD: {first_key}")

            # Add/Update the new item
            self.cache_data[key] = item
            if key in self.cache_data:
                # Move to end if key exists
                self.cache_data.move_to_end(key)

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
