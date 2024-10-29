#!/usr/bin/env python3
"""
LFUCache module - implements a Least Frequently Used caching system
with LRU as tie-breaker
"""
from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """
    LFUCache defines a LFU caching system
    Inherits from BaseCaching
    """

    def __init__(self):
        """
        Initialize the cache with the necessary tracking structures
        """
        super().__init__()
        self.cache_data = OrderedDict()
        self.frequencies = defaultdict(int)  # Tracks frequency of each key
        self.freq_lists = defaultdict(OrderedDict)  # Groups keys by frequency
        self.min_freq = 0  # Tracks the minimum frequency

    def update_frequency(self, key):
        """
        Update the frequency of a key and adjust related data structures
        Args:
            key: The key whose frequency should be updated
        """
        freq = self.frequencies[key]
        self.frequencies[key] = freq + 1

        # Remove from old frequency list
        del self.freq_lists[freq][key]

        # If the list for this frequency is empty and it's the min frequency,
        # increment min_freq
        if freq == self.min_freq and not self.freq_lists[freq]:
            self.min_freq += 1

        # Add to new frequency list
        self.freq_lists[freq + 1][key] = self.cache_data[key]

    def put(self, key, item):
        """
        Add an item to the cache using LFU algorithm
        Args:
            key: The key to store the item under
            item: The item to store
        """
        if key is None or item is None:
            return

        # If key exists, update its value and frequency
        if key in self.cache_data:
            self.cache_data[key] = item
            self.update_frequency(key)
            return

        # If cache is full, remove LFU item
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Get all items with minimum frequency
            lfu_items = self.freq_lists[self.min_freq]
            lfu_key, _ = lfu_items.popitem(last=False)  # LRU among LFU

            del self.cache_data[lfu_key]
            del self.frequencies[lfu_key]
            print(f"DISCARD: {lfu_key}")

        # Add new item
        self.cache_data[key] = item
        self.frequencies[key] = 0
        self.freq_lists[0][key] = item
        self.min_freq = 0

    def get(self, key):
        """
        Retrieve an item from the cache by key and update frequency
        Args:
            key: The key to look up
        Returns:
            The value associated with the key if it exists, None otherwise
        """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and return value
        self.update_frequency(key)
        return self.cache_data[key]
