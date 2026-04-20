from dataclasses import dataclass
import xml.etree.ElementTree as ET
from typing import Dict, List
import carla
from PCLA import PCLA, route_maker, location_to_waypoint

""" Configuration for spawning an ADS-controlled vehicle """
class ADSoSVehicleConfiguration:

    def __init__(self, vehicle, agent, route_file="", route_id=-1, spawn_point_id=-1, end_point_id=-1):
        self.vehicle: str = vehicle
        self.agent: str = agent
        self.spawn_point_id: int = spawn_point_id
        self.end_point_id: int = end_point_id
        self.route_file: str = route_file
        self.route_id = route_id

""" Manages route creation for, spawning of, running and destruction of multiple ADS-controlled vehicles """
class ADSoS:
    def __init__(self, world, client, json_path=None):
        self.world = world
        self.client = client
        self.ego_vehicles: List[PCLA] = []
        
    """ Generates a XML route file between two spawn points given by id """
    def generate_route_from_points(self, spawn_point_id, end_point_id):
        vehicle_spawn_points = self.world.get_map().get_spawn_points()
        start_point = vehicle_spawn_points[spawn_point_id].location
        end_point = vehicle_spawn_points[end_point_id].location
        waypoints = location_to_waypoint(self.client, start_point, end_point) 
        
        route_name = "generated_route_" + str(spawn_point_id) + "_" + str(end_point_id) + ".xml"
        route_maker(waypoints, route_name)

        return route_name
    
    def generate_route_from_file(self, route_file, route_id):
        # Load the routes file
        tree = ET.parse(route_file)
        root = tree.getroot()
        route = None
        for r in root:
            if r.attrib["id"] == str(route_id):
                route = r
                break
        
        file_name = f'generated_route_{route.attrib["town"]}_{route.attrib["id"]}.xml'
        route.attrib["id"] = "_"
        route.attrib["town"] = "_"
        new_tree = ET.ElementTree(route)
        new_tree.write(file_name)
            
        if route == None:
            print(f'Route with id {route_id} was not found in route file {route_file}')
            
        return file_name
    
    def set_weather(self, conditions: Dict[str, float]) -> None:
        weather_params = self.world.get_weather()
        for condition, value in conditions.items():
            weather_params.__setattr__(condition, value)
            print(f'Setting {condition} to {value}')
        self.world.set_weather(weather_params)
        
    """ Add a vehicle to the ADSoS """
    def add_vehicle(self, configuration: ADSoSVehicleConfiguration):
        # Create the vehicle
        bpLibrary = self.world.get_blueprint_library()
        vehicleBP = bpLibrary.filter(configuration.vehicle)[0]
        vehicle_spawn_points = self.world.get_map().get_spawn_points()
        vehicle = self.world.spawn_actor(vehicleBP, vehicle_spawn_points[configuration.spawn_point_id])
        
        # Generate its route
        route_name = ""
        if not configuration.route_file:
            route_name = self.generate_route_from_points(configuration.spawn_point_id, configuration.end_point_id)
        else:
            route_name = self.generate_route_from_file(configuration.route_file, configuration.route_id)

        # Instantiate the agent
        pcla = PCLA(configuration.agent, vehicle, route_name, self.client)
        self.ego_vehicles.append(pcla)
        print('\nSpawned the vehicle with model =', configuration.agent,', press Ctrl+C to exit.\n')
        
    """ Add multiple vehicles using a list of ADSoSVehicleConfiguration objects """
    def add_vehicles(self, configurations: List[ADSoSVehicleConfiguration]):
        for configuration in configurations:
            print(configuration.route_file)
            self.add_vehicle(configuration)
        
    """ Get and apply the next control action for all vehicles. Used in main loop, world should be stepped externally """
    def next_action(self):
        for pcla in self.ego_vehicles:
            ego_action = pcla.get_action()
            pcla.vehicle.apply_control(ego_action)

    """ Clear up any vehicles added to this ADSoS """
    def cleanup(self):
        for pcla in self.ego_vehicles:
            pcla.cleanup()