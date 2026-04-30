"""
Evaluates a given score based on user-supplied metrics
"""
from typing import List
from evaluation.scenario_evaluation_strategy import ScenarioEvaluationStrategy
from evaluation.score_aggregator import ScoreAggregator
from PCLA.PCLA import PCLA

class ScenarioEvaluator:
    """
    Evaluates a given score based on user-supplied metrics
    """
    def __init__(self,
                 evaluation_strategy: ScenarioEvaluationStrategy,
                 score_aggregator: ScoreAggregator):
        self.evaluation_strategy: ScenarioEvaluationStrategy = evaluation_strategy
        self.score_aggregator: ScoreAggregator = score_aggregator

    def evaluate_frame(self, world, ego_vehicles: List[PCLA]):
        """ Defers to the supplied evaluation strategy to evaluate the frame """
        self.evaluation_strategy.evaluate_frame(world, ego_vehicles)

    def get_score(self):
        """ Returns the aggregate score, determined by the aggregator supplied """
        scores: List[float] = self.evaluation_strategy.get_scores()
        return self.score_aggregator.get_aggregate_score(scores)

    def reset(self):
        """ Resets scores """
        self.evaluation_strategy.reset()
