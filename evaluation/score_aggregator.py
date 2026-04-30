"""
Base class for score aggregators
"""
from abc import ABC, abstractmethod
from typing import List

class ScoreAggregator(ABC):
    """
    Base class for score aggregators
    Override the get_aggregate_score method
    """
    def __init__(self):
        pass

    @abstractmethod
    def get_aggregate_score(self, scores: List[float]) -> float:
        """ Override this method. Returns the aggregated score """
