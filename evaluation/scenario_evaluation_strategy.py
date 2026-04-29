"""
Base class for evaluation of scenarios. Extend this class and
implement the evlauate_frame method.
"""
from abc import ABC, abstractmethod
from typing import List
from PCLA.PCLA import PCLA

class ScenarioEvaluationStrategy(ABC):
    """
    Base class for evaluation of scenarios. Extend this class and
    implement the evlauate_frame method.
    """

    def __init__(self):
        """ Initialises scores to empty list """
        self.scores: List[float] = []

    @abstractmethod
    def evaluate_frame(self, world, ego_vehicles: List[PCLA]) -> float:
        """ Override this method to return a score for the given frame """

    def get_scores(self) -> List[float]:
        """ Get the stored scores """
        return self.scores

    def reset(self) -> None:
        """ Reset the scores to empty list """
        self.scores = []
