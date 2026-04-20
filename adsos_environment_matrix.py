from dataclasses import dataclass
from adsos.runners.search.environment_matrix_runner import EnvironmentMatrixRunner
import carla
from adsos.runners.search.end_conditions.num_searches_end_condition import NumSearchesEndCondition
from adsos.evaluation.ego_minimum_distance_evaluation_strategy import EgoMinimumDistanceEvaluationStrategy
from adsos.evaluation.scenario_evaluator import ScenarioEvaluator
import adsos.matrix_builder as matrix_builder
from adsos.adsos import ADSoSVehicleConfiguration
        

""" Sample showing spawning of multiple vehicles """
def main():

    HOST_IP: str = "localhost"
    client = carla.Client(HOST_IP, 2000)
    client.set_timeout(10.0)
    client.load_world("Town02")

    # Add some vehicles
    vehicles = [
        ADSoSVehicleConfiguration('model3', "carl_carl_0", spawn_point_id=31, end_point_id=11),
        ADSoSVehicleConfiguration('model3', "carl_carl_1", spawn_point_id=27, end_point_id=14)
    ]
    
    environment_parameters = {
        "cloudyness": range(0, 101, 50),
        "precipitation": range(0, 101, 50),
        "sun_altitude_angle": range(-90, 91, 180)
    }
    
    environment_matrix = matrix_builder.build_matrix(environment_parameters)
    print(environment_matrix)
    
    
    evaluation_strategy = EgoMinimumDistanceEvaluationStrategy()
    evaluator = ScenarioEvaluator(evaluation_strategy)

    runner = EnvironmentMatrixRunner(client=client, steps=150, evaluator=evaluator)
    runner.set_initial_vehicle_configuration(vehicles=vehicles)
    runner.set_environment_matrix(environment_matrix)
    runner.run()
    runner.write("env_search_results.json")
    

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('Done.')
