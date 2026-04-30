"""
For a given configuration, performs a number of runs and searches
for high-quality scenarios
"""
import json
import random
from typing import List
import time
from world_manager import WorldManager
from ...adsos import ADSoS, ADSoSVehicleConfiguration

class RandomSearchRunner:
    """
    For a given configuration, performs a number of runs and searches
    for high-quality scenarios
    """

    def __init__(self, client, steps, evaluator):
        self.vehicles: List[ADSoSVehicleConfiguration] = []
        self.client = client
        self.steps = steps
        self.end_conditions = []
        self.evaluator = evaluator
        self.results: List[List[int]] = [] # Score, [start, end] TODO: Improve this

    def add_end_condition(self, condition):
        """ Adds an end condition to this runner """
        condition.set_search_runner(self)
        self.end_conditions.append(condition)

    def set_initial_vehicle_configuration(self, vehicles: List[ADSoSVehicleConfiguration]) -> None:
        """ Give a list of ADSoSVehicleConfiguration objects which will spawn ego vehicles """
        self.vehicles = vehicles

    def any_end_conditions_met(self) -> bool:
        """ Returns true if any end condition is met """
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
        for i, _v in enumerate(self.vehicles):
            self.vehicles[i].spawn_point_id = random.randint(0, 87)
            self.vehicles[i].end_point_id = random.randint(0, 87)

    def _record_config_and_score(self):
        score = self.evaluator.get_score()
        result = [score]
        for vehicle in self.vehicles:
            result.append(vehicle.spawn_point_id)
            result.append(vehicle.end_point_id)
        self.results.append(result)

    def _report(self):
        print("Search completed")

    def write(self, file_path):
        """ Writes the results to disk at the specified file path """
        with open(file_path, "w", encoding="utf-8") as file:
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
        """ Runs the search """
        print('Searching scenario configurations')
        self._run_scenarios()
        print('Search completed')
        self._report()
        print('Complete')
