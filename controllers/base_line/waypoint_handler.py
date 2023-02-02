import rospy
import time
import pandas as pd

import sys
sys.path.append("../../catkin_ws/devel/lib/python3/dist-packages")

from controller.msg import NextWaypoints, Waypoint

# Ros msg definition:
# NextWaypoints.msg
#     Waypoint[] waypoint_list
#
# Waypoint.msg
#     float32 angle
#     float32 time



class WaypointHandler:
    def __init__(self):

        # Empty dataframe to store waypoints
        self.waypoints_df = pd.DataFrame(columns=['time', 'angle'])


        # Setup message event callback
        self.subscriber = rospy.Subscriber('/controller/NextWaypoints', NextWaypoints, self._on_next_waypoints_callback)


    def _on_next_waypoints_callback(self, msg):
        print('Received new waypoints')
        
        new_waypoints_df = pd.DataFrame(columns=['time', 'angle'])

        for waypoint in msg.waypoint_list:
            new_waypoints_df = new_waypoints_df.append({'time': waypoint.time, 'angle': waypoint.angle}, ignore_index=True)

        # Short by time so that the first waypoint is the one with the lowest timestamp
        new_waypoints_df = new_waypoints_df.sort_values(by=['time'])

        # Add old waypoints that are older thatn the first new waypoint
        if not self.waypoints_df.empty:
            new_waypoints_df = self.waypoints_df[self.waypoints_df['time'] < new_waypoints_df.iloc[0]['time']].append(new_waypoints_df, ignore_index=True)

        # Update waypoints
        self.waypoints_df = new_waypoints_df


    def pop_n_waypoints(self, n):
        if n > len(self.waypoints_df):
            n = len(self.waypoints_df)

        waypoints = self.waypoints_df.iloc[:n].values

        self.waypoints_df = self.waypoints_df.iloc[n:]

        return waypoints

    def pop_waypoints_until(self, time):
        poped_waypoints_df = self.waypoints_df[self.waypoints_df['time'] <= time]

        self.waypoints_df = self.waypoints_df[self.waypoints_df['time'] > time]

        return poped_waypoints_df