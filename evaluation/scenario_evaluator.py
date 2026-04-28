from typing import List
from evaluation.scenario_evaluation_strategy import ScenarioEvaluationStrategy
from PCLA.PCLA import PCLA

class ScenarioEvaluator:
    def __init__(self, evaluation_strategy: ScenarioEvaluationStrategy):
        self.evaluation_strategy: ScenarioEvaluationStrategy = evaluation_strategy

    def evaluate_frame(self, world, ego_vehicles: List[PCLA]):
        self.evaluation_strategy.evaluate_frame(world, ego_vehicles)

    # TODO: Supply aggregation strategy to constructor
    def get_score(self):
        scores: List[float] = self.evaluation_strategy.get_scores()

        if len(scores) == 0:
            return 0.0

        return max(scores)

    def reset(self):
        self.scores = []
        self.evaluation_strategy.reset()
