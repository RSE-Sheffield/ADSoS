from pynput.keyboard import Key, Listener
import carla

class WorldManager:
    def __init__(self, client):
        self.client = client
        self.world = None

    """ Connect to the world, traffic manager and configure synchronous mode """
    def setup_world(self):
        self.world = self.client.get_world()
        traffic_manager = self.client.get_trafficmanager(8000)

        settings = self.world.get_settings()
        asynch = False
        if not asynch:
            traffic_manager.set_synchronous_mode(True)
            if not settings.synchronous_mode:
                synchronous_master = True
                settings.synchronous_mode = True
                settings.fixed_delta_seconds = 0.05
            else:
                synchronous_master = False
        else:
            print("You are currently in asynchronous mode. If this is a traffic simulation, \
                    you could experience some issues. If it's not working correctly, switch to \
                    synchronous mode by using traffic_manager.set_synchronous_mode(True)")
        #settings.no_rendering_mode = True
        self.world.apply_settings(settings)
        return self.world

    """ Configure the spectator """
    def configure_spectator(self) -> None:
            # Retrieve the spectator object
            spectator = self.world.get_spectator()

            # Set the spectator with our transform
            spectator.set_transform(carla.Transform(carla.Location(x=-8, y=108, z=7), carla.Rotation(pitch=-19, yaw=0, roll=0)))

    def display_spawn_points(self) -> None:
        spawn_points = self.world.get_map().get_spawn_points()

        # Draw the spawn point locations as numbers in the map
        for i, spawn_point in enumerate(spawn_points):
            self.world.debug.draw_string(spawn_point.location, str(i), life_time=600)
        self.world.tick()

        def on_press(_key):
            pass

        def on_release(key):
            if key == Key.esc:
                # Stop listener
                return False

        # Collect events until released
        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            while listener.is_alive():
                self.world.tick()

