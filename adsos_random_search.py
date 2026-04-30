""" Sample showing spawning of multiple vehicles """
import carla
from runners.search.end_conditions.num_searches_end_condition import NumSearchesEndCondition
from runners.search.random_search_runner import RandomSearchRunner
from evaluation.ego_minimum_distance_evaluation_strategy import EgoMinimumDistanceEvaluationStrategy
from evaluation.scenario_evaluator import ScenarioEvaluator
from evaluation.max_score_aggregator import MaxScoreAggregator
from .adsos import ADSoSVehicleConfiguration


def main():
    """ Sample showing spawning of multiple vehicles """

    host_ip: str = "localhost"
    client = carla.Client(host_ip, 2000)
    client.set_timeout(10.0)
    client.load_world("Town02")

    # Add some vehicles
    vehicles = [
        ADSoSVehicleConfiguration('model3', "carl_carl_0", 31, 11),
        ADSoSVehicleConfiguration('model3', "carl_carl_1", 27, 14)
    ]

    evaluation_strategy = EgoMinimumDistanceEvaluationStrategy()
    score_aggregator = MaxScoreAggregator()
    evaluator = ScenarioEvaluator(evaluation_strategy, score_aggregator)
    end_condition = NumSearchesEndCondition(3)
    runner = RandomSearchRunner(client=client, steps=150, evaluator=evaluator)
    runner.set_initial_vehicle_configuration(vehicles=vehicles)
    runner.add_end_condition(end_condition)
    runner.run()
    runner.write("search_results.json")



if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('Done.')
