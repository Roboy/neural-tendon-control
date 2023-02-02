
import rospy
import time
import threading

import sys
sys.path.append("../catkin_ws/devel/lib/python3/dist-packages")
from bench.msg import BenchState, BenchMotorControl, BenchRecorderControl

from bench_handler import ActivationVector

class ControllerCore:
    def __init__(self, waypoint_handler, bench_handler):
        self.waypoint_handler = waypoint_handler
        self.bench_handler = bench_handler


        self.thread = threading.Thread(target=self._run)

        self.stop_event = threading.Event()



    def _run(self):
        while not self.stop_event.is_set():
            # Get waypoints for next 0.05 seconds
            # waypoints_df format:
            #     timestamp   angle
            current_time = time.time()
            upcomming_waypoints_df = self.waypoint_handler.pop_waypoints_until(current_time + 0.05)

            # Get current bench state
            bench_state = self.bench_handler.get_last_state_vector()


            # Take the last waypoint in the list and calculate the direction from the current pv angle
            direction = 0
            if bench_state is not None and len(upcomming_waypoints_df) > 0:
                # Get the angle of the last waypoint
                last_waypoint_angle = upcomming_waypoints_df.iloc[-1]['angle']

                if bench_state.angle < last_waypoint_angle:
                    direction = 1
                else:
                    direction = -1


            # Apply direction to the bench
            actication_vector = ActivationVector(
                flex_myobrick_pwm=0,
                extend_myobrick_pwm=0,
            )
            if direction == 1:
                actication_vector.flex_myobrick_pwm = 7
                actication_vector.extend_myobrick_pwm = -2
            if direction == -1:
                actication_vector.flex_myobrick_pwm = -2
                actication_vector.extend_myobrick_pwm = 7

            self.bench_handler.apply_activation_vector(actication_vector)

            
            time.sleep(0.05)
    
    def start(self):

        self.thread.start()

    def terminate(self):
        self.stop_event.set()
        self.thread.join()

    def join(self):
        self.thread.join()