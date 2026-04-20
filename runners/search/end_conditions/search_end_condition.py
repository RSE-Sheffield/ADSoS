from abc import ABC, abstractmethod

class SearchEndCondition(ABC):
    def __init__(self):
        self.runner = None
        
    def set_search_runner(self, runner):
        self.runner = runner
        
    @abstractmethod
    def is_condition_met(self) -> bool:
        pass