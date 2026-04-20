from adsos.runners.search.end_conditions.search_end_condition import SearchEndCondition

class NumSearchesEndCondition(SearchEndCondition):
    def __init__(self, num_searches: int):
        super().__init__()
        self.num_searches = num_searches
        
    def is_condition_met(self):
        return len(self.runner.results) >= self.num_searches
        