"""
Returns the maximum score
"""
from typing import List
from evaluation.score_aggregator import ScoreAggregator

class MaxScoreAggregator(ScoreAggregator):
    """
    Returns the maximum score
    """
    def __init__(self):
        pass

    def get_aggregate_score(self, scores: List[float]) -> float:
        """ Returns the maximum score """
        if len(scores) == 0:
            return 0.0

        return max(scores)
