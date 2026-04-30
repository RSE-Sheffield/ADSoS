"""
Stores locations of ego vehicles at each frame
"""

from typing import Dict, List
import json
import carla
from PCLA.PCLA import PCLA

class EgoVehicleLogger:
    """
    Stores locations of ego vehicles at each frame
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.locations: Dict[int, List[carla.Location]] = {}
        self.serialized_locations: Dict[int, List[float]] = {}
        self.frame = 0

    def record_locations(self, ego_vehicles: List[PCLA]) -> None:
        """ Stores the location of each ego vehicle at this frame """
        self.locations[self.frame] = []
        for ego_vehicle in ego_vehicles:
            location = ego_vehicle.vehicle.get_location()
            self.locations[self.frame].append(location)
        self.frame += 1

    def serialize_locations(self) -> None:
        """ Formats the stored locations into a list of floats """
        for key, value in self.locations.items():
            seralized_location = []
            for loc in value:
                seralized_location.append(loc.x)
                seralized_location.append(loc.y)
                seralized_location.append(loc.z)
            self.serialized_locations[key] = seralized_location

    def write(self) -> None:
        """ Writes the stored locations to disk """
        self.serialize_locations()
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.serialized_locations, file)
