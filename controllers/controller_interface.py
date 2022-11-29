
class Waypoint:
    def __init__(self) -> None:
        self.id = 0 # Always incremented
        self.angle = 0
        self.speed = 0


class ProcessVariables:
    def __init__(self) -> None:
        self.waypoint = Waypoint()
        self.current_angle = 0
        self.current_speed = 0


class ControllerInterface:
    def init(self) -> bool:
        """
        Initiate controller by for example reading NN weights. 
        Return True if successful.
        """
        pass

    def add_waypoint(self, waypoint: Waypoint):
        """Add waypoint the the queue."""
        pass

    def get_current_waypoint_id(self) -> int:
        """Get the current waypoint id."""
        pass

    def clear_waypoints(self):
        """Clear all waypoints."""
        pass

    
    def feed_process_variables(self, process_variables: ProcessVariables):
        """Feed the controller with current process variables."""
        pass

    def get_set_point(self) -> SetPoint:
        """Get the current set point."""
        pass

    
    def start(self):
        """Start the controller."""
        pass

    def stop(self):
        """Stop the controller."""
        pass