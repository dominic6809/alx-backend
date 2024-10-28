# 0x00-pagination

This project implements pagination functionalities in Python, focusing on efficient data retrieval, resilience to deletions, and hypermedia capabilities. The code parses and paginates a CSV dataset of popular baby names.

## Table of Contents
- [Overview](#overview)
- [Tasks](#tasks)
  - [Task 0: Basic Pagination](#task-0-basic-pagination)
  - [Task 1: Pagination in a Server Class](#task-1-pagination-in-a-server-class)
  - [Task 2: Hypermedia Pagination](#task-2-hypermedia-pagination)
  - [Task 3: Deletion-Resilient Pagination](#task-3-deletion-resilient-pagination)
- [Usage](#usage)

---

## Overview
This project provides a `Server` class that reads from a CSV file and serves paginated results. Key features include pagination with customizable page sizes, hypermedia-style responses, and resilience against row deletions during pagination.

---

## Tasks

### Task 0: Basic Pagination
**File:** `0-simple_helper_function.py`

- Implements a function `index_range(page: int, page_size: int) -> Tuple[int, int]` to calculate the start and end indexes for pagination.
- Returns a tuple `(start, end)` based on the page number (1-indexed) and page size.

### Task 1: Pagination in a Server Class
**File:** `1-simple_pagination.py`

- Introduces a `Server` class to paginate a CSV dataset.
- Implements `get_page(page: int, page_size: int) -> List[List]` method:
  - Validates `page` and `page_size` are positive integers.
  - Utilizes `index_range` to calculate and retrieve the correct page of results.
  - Returns an empty list if `page` or `page_size` exceeds dataset bounds.

### Task 2: Hypermedia Pagination
**File:** `2-hypermedia_pagination.py`

- Adds a `get_hyper(page: int, page_size: int) -> Dict` method in the `Server` class.
- Returns a dictionary with pagination metadata:
  - `page_size`: Number of items on the page.
  - `page`: Current page number.
  - `data`: List of items on the current page.
  - `next_page`: Number of the next page (if available).
  - `prev_page`: Number of the previous page (if available).
  - `total_pages`: Total number of pages in the dataset.

### Task 3: Deletion-Resilient Pagination
**File:** `3-hypermedia_del_pagination.py`

- Implements `get_hyper_index(index: int, page_size: int) -> Dict` for deletion-resilient pagination.
- Handles cases where rows may be removed from the dataset between queries.
- Returns a dictionary with:
  - `index`: Start index of the current page.
  - `next_index`: Index to use for the next query (adjusts for any deletions).
  - `page_size`: Current page size.
  - `data`: List of items on the page.
  
---

## Usage

Each task builds on the previous one, providing increased functionality and flexibility:
1. **Run `0-main.py`** for basic pagination verification.
2. **Run `1-main.py`** to test pagination in the `Server` class.
3. **Run `2-main.py`** to check hypermedia-style pagination.
4. **Run `3-main.py`** to validate deletion-resilient pagination.

--- 

This project showcases Python’s capabilities in managing and paginating large datasets effectively, with consideration for real-world challenges like data consistency amidst deletions.
