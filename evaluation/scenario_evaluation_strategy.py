from PCLA.PCLA import PCLA
from abc import ABC, abstractmethod
from typing import List

class ScenarioEvaluationStrategy(ABC):
    def __init__(self):
        self.scores: List[float] = []

    @abstractmethod
    def evaluate_frame(self, world, ego_vehicles: List[PCLA]) -> float:
        pass
        
    def get_scores(self) -> List[float]:
        return self.scores

    def reset(self) -> None:
        self.scores = []
        