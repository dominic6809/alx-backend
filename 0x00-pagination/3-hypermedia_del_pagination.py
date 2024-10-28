#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Optional


class Server:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header row

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """
        Returns pagination details, adjusting for deletions in the dataset.

        Args:
            index (int): The starting index for the page.
            page_size (int): The number of items per page.

        Returns:
            Dict: A dictionary containing the page data
            and related pagination information.
        """
        # Verify index is within the dataset's range
        assert 0 <= index < len(self.indexed_dataset()), "Index out of range"

        # Gather data from indexed dataset and adjust for deletions
        indexed_data = self.indexed_dataset()
        data = []
        current_index = index
        items_retrieved = 0

        # Collect up to `page_size` items starting from `index`
        while (items_retrieved < page_size and
                current_index < len(indexed_data)):
            if current_index in indexed_data:
                data.append(indexed_data[current_index])
                items_retrieved += 1
            current_index += 1

        # Calculate next_index as the index after the last item on this page
        next_index = current_index
        if current_index < len(indexed_data) else None

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }
