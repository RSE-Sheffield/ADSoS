from dataclasses import dataclass
from typing import List
import filecmp
import carla
import time
from evaluation.ego_vehicle_logger import EgoVehicleLogger
from adsos import ADSoS, ADSoSVehicleConfiguration
from world_manager import WorldManager

""" For a given configuration, performs a number of runs and checks the results are consistent """
class DeterminismRunner:
    def __init__(self, client, steps, repetitions):
        self.vehicles: List[ADSoSVehicleConfiguration] = []
        self.client = client
        self.steps = steps
        self.repetitions = repetitions

    def set_vehicle_configuration(self, vehicles: List[ADSoSVehicleConfiguration]) -> None:
        self.vehicles = vehicles
        
    def _run_scenarios(self):
        run = 0
        while run < self.repetitions:
            self._run_single_scenario(run)
            run += 1
            
    def _validate(self) -> bool:
        other_rep = 1
        while (other_rep < self.repetitions):
            if not filecmp.cmp(f'r{other_rep}.json', 'r0.json'):
                return False
            other_rep += 1
        
        return True

    def _run_single_scenario(self, run_number: int):
        print(f'Starting run {run_number}')
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
            
            # Create the logger
            logger = EgoVehicleLogger(f'r{run_number}.json')
            
            # Main loop
            frame = 0
            while frame < self.steps:
                adsos.next_action() 
                logger.record_locations(adsos.ego_vehicles)
                world.tick()
                frame += 1
    
        finally:
            logger.write()

            #settings.no_rendering_mode = False
            settings = world.get_settings()
            settings.synchronous_mode = False
            world.apply_settings(settings)

            # Destroy vehicles
            print('\nCleaning up the vehicles')
            adsos.cleanup()
            time.sleep(0.5)

    def run(self):
        print('Running scenarios')
        self._run_scenarios()
        print('Validating')
        deterministic = self._validate()
        if deterministic:
            print("Deterministic")
        else:
            print("Non-deterministic")
        print('Complete')