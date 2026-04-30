"""
Evaluator based on the minimum distance achieved between any two ego vehicles
"""
from typing import List
import itertools
import carla
from PCLA.PCLA import PCLA
from evaluation.scenario_evaluation_strategy import ScenarioEvaluationStrategy

class EgoMinimumDistanceEvaluationStrategy(ScenarioEvaluationStrategy):
    """
    Evaluator based on the minimum distance achieved between any two ego vehicles
    """
    def __init__(self):
        super().__init__()
        self.max_evaluation_score: float = 1e6

    def evaluate_frame(self, _world, ego_vehicles: List[PCLA]) -> float:
        """
        Computes a score according to the minimum distance between any two ego vehicles
        """
        # Compute the minimum distance between the ego vehicles
        min_dist: float = 10000000.0
        for pair in itertools.combinations(ego_vehicles, 2):
            dist: float = self.get_distance(*pair)
            min_dist = min(dist, min_dist)

        # Store it
        frame_score: float = min(1.0 / min_dist, self.max_evaluation_score)
        self.scores.append(frame_score)

    def get_distance(self, vehicle, other_vehicle) -> float:
        """
        Gets the distance between two carla vehicles
        """
        location: carla.Location = vehicle.vehicle.get_location()
        other_location: carla.Location = other_vehicle.vehicle.get_location()
        return location.distance(other_location)
