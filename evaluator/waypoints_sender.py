import rospy
import time
import threading
import pandas as pd

import sys
sys.path.append("../catkin_ws/devel/lib/python3/dist-packages")

from controller.msg import NextWaypoints, Waypoint

# Ros msg definition:
# NextWaypoints.msg
#     Waypoint[] waypoint_list
#
# Waypoint.msg
#     float32 angle
#     float32 time

# waypoints_df format:
#     timestamp   angle

class WaypointsSender:
    def __init__(self, waypoints_df):
        self.waypoints_df = waypoints_df

        # Empty dataframe to store waypoints of same format as waypoints_df
        self.sent_waypoints_df = pd.DataFrame(columns=waypoints_df.columns)


        self.pub = rospy.Publisher('/controller/NextWaypoints', NextWaypoints, queue_size=10)


        self.thread = threading.Thread(target=self._run)

        self.stop_event = threading.Event()


    def _run(self):
        while not self.stop_event.is_set():
            current_time = time.time()

            # Get waypoints for the next second
            self.upcomming_waypoints_df = self.waypoints_df[self.waypoints_df['timestamp'] <= current_time + 1]
            

            msg = NextWaypoints()

            for waypoint in self.upcomming_waypoints_df.values:
                msg.waypoint_list.append(Waypoint(waypoint[1], waypoint[0]))

            self.pub.publish(msg)

            # Remove waypoints that have been sent from the dataframe
            self.waypoints_df = self.waypoints_df[self.waypoints_df['timestamp'] > current_time + 1]

            # Add sent waypoints to the sent waypoints dataframe
            self.sent_waypoints_df = self.sent_waypoints_df.append(self.upcomming_waypoints_df, ignore_index=True)

            # If there are no more waypoints, stop the thread
            if self.waypoints_df.empty:
                print('No more waypoints, stopping thread')
                self.stop_event.set()

            
            time.sleep(1)

    def get_sent_waypoints(self):
        return self.sent_waypoints_df

    def start(self):
        self.start_time = time.time()

        self.waypoints_df['timestamp'] = self.waypoints_df['timestamp'] - self.waypoints_df['timestamp'][0] + self.start_time


        self.thread.start()

    def terminate(self):
        self.stop_event.set()
        self.thread.join()

    def join(self):
        self.thread.join()