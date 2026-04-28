from typing import Dict, List
import itertools
from PCLA.PCLA import PCLA
from evaluation.scenario_evaluation_strategy import ScenarioEvaluationStrategy
import carla
import json

class EgoVehicleLogger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.locations: Dict[int, List[carla.Location]] = {}
        self.serialized_locations: Dict[int, List[float]] = {}
        self.frame = 0

    def record_locations(self, ego_vehicles: List[PCLA]) -> None:
        self.locations[self.frame] = []
        for ego_vehicle in ego_vehicles:
            location = ego_vehicle.vehicle.get_location()
            self.locations[self.frame].append(location)
        self.frame += 1

    def serialize_locations(self) -> None:
        for k, v in self.locations.items():
            seralized_location = []
            for loc in v:
                seralized_location.append(loc.x)
                seralized_location.append(loc.y)
                seralized_location.append(loc.z)
            self.serialized_locations[k] = seralized_location


    def write(self) -> None:
        self.serialize_locations()
        with open(self.file_path, "w") as file:
            json.dump(self.serialized_locations, file)