"""
Base class for end conditions for search-based runners
"""
from abc import ABC, abstractmethod

class SearchEndCondition(ABC):
    """
    Base class for end conditions for search-based runners.
    Override the is_condition_met method to return true when the
    search is completed.
    """
    def __init__(self):
        self.runner = None

    def set_search_runner(self, runner):
        """
        Give the end condition a reference to the runner it is attached to.
        Not intended to be called by users.
        """
        self.runner = runner

    @abstractmethod
    def is_condition_met(self) -> bool:
        """ Override this method. Returns true if the condition is met """
