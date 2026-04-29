""" Sample checking determinism with multiple vehicles """
import carla
from runners.verification.determinism_runner import DeterminismRunner
from .adsos import ADSoSVehicleConfiguration


def main():
    """ Sample checking determinism with multiple vehicles """

    host_ip: str = "localhost"
    client = carla.Client(host_ip, 2000)
    client.set_timeout(10.0)
    client.load_world("Town02")

    # Add some vehicles
    vehicles = [
        ADSoSVehicleConfiguration('model3', "carl_carl_0", spawn_point_id=31, end_point_id=11),
        ADSoSVehicleConfiguration('model3', "carl_carl_1", spawn_point_id=27, end_point_id=14)
    ]

    runner = DeterminismRunner(client=client, steps=150, repetitions=15)
    runner.set_vehicle_configuration(vehicles=vehicles)
    runner.run()


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('Done.')
