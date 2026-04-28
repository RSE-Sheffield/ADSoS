"""
Example showing how to test determinism using an XML route file
"""
import carla
from runners.verification.determinism_runner import DeterminismRunner
from adsos import ADSoSVehicleConfiguration

def main():

    host_ip: str = "localhost"
    client = carla.Client(host_ip, 2000)
    client.set_timeout(10.0)
    client.load_world("Town04")

    # Add some vehicles
    vehicles = [
        ADSoSVehicleConfiguration('model3',
                                  "carl_carl_0",
                                  route_file="routes_devtest_sliced.xml",
                                  route_id=61),
    ]

    runner = DeterminismRunner(client=client, steps=350, repetitions=15)
    runner.set_vehicle_configuration(vehicles=vehicles)
    runner.run()


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('Done.')
