from dataclasses import dataclass
import json
import random
from typing import List
import filecmp
import carla
import time
from adsos.evaluation.scenario_evaluator import ScenarioEvaluator
from adsos.evaluation.scenario_evaluation_strategy import ScenarioEvaluationStrategy
from adsos.evaluation.ego_minimum_distance_evaluation_strategy import EgoMinimumDistanceEvaluationStrategy
from adsos.evaluation.ego_vehicle_logger import EgoVehicleLogger
from adsos.adsos import ADSoS, ADSoSVehicleConfiguration
from adsos.world_manager import WorldManager

""" For a given configuration, performs a number of runs and searches for high-quality scenarios """
class RandomSearchRunner:
    def __init__(self, client, steps, evaluator):
        self.vehicles: List[ADSoSVehicleConfiguration] = []
        self.client = client
        self.steps = steps
        self.end_conditions = []
        self.evaluator = evaluator
        self.results: List[List[int]] = [] # Score, [start, end] TODO: Improve this
        
    def add_end_condition(self, condition):
        condition.set_search_runner(self)
        self.end_conditions.append(condition)

    def set_initial_vehicle_configuration(self, vehicles: List[ADSoSVehicleConfiguration]) -> None:
        self.vehicles = vehicles
        
    def any_end_conditions_met(self) -> bool:
        for end_condition in self.end_conditions:
            if end_condition.is_condition_met():
                return True
            
        return False
        
    def _run_scenarios(self):
        while not self.any_end_conditions_met():
            self._run_single_scenario()
            self._record_config_and_score()
            self.evaluator.reset()
            self._generate_next_configuration()
            
    def _generate_next_configuration(self):
        for i in range(len(self.vehicles)):
            self.vehicles[i].spawn_point_id = random.randint(0, 87)
            self.vehicles[i].end_point_id = random.randint(0, 87)
        
    def _record_config_and_score(self):
        score = self.evaluator.get_score()
        result = [score]
        for v in self.vehicles:
            result.append(v.spawn_point_id)
            result.append(v.end_point_id)
        print("Appending result")
        self.results.append(result)
        
    def _report(self):
        pass # TODO: print some summary statistics
    
    def write(self, file_path):
        with open(file_path, "w") as file:
            json.dump(self.results, file)

    def _run_single_scenario(self):
        try:
            # Configure the world
            world_manager = WorldManager(self.client)
            world = world_manager.setup_world()
            world_manager.configure_spectator()
            world.tick()

            # Create our ADS manager
            adsos = ADSoS(world, self.client)
            
            # Add the vehicles
            adsos.add_vehicles(self.vehicles)
            
            # Main loop
            frame = 0
            while frame < self.steps:
                adsos.next_action() 
                world.tick()
                self.evaluator.evaluate_frame(world, adsos.ego_vehicles)
                frame += 1
    
        finally:
            #settings.no_rendering_mode = False
            settings = world.get_settings()
            settings.synchronous_mode = False
            world.apply_settings(settings)

            # Destroy vehicles
            print('\nCleaning up the vehicles')
            adsos.cleanup()
            time.sleep(0.5)

    def run(self):
        print('Searching scenario configurations')
        self._run_scenarios()
        print('Search completed')
        self._report()
        print('Complete')