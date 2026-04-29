"""
Performs a fixed number of searches
"""
from runners.search.end_conditions.search_end_condition import SearchEndCondition

class NumSearchesEndCondition(SearchEndCondition):
    """
    Performs a fixed number of searches
    """
    def __init__(self, num_searches: int):
        super().__init__()
        self.num_searches = num_searches

    def is_condition_met(self):
        return len(self.runner.results) >= self.num_searches
