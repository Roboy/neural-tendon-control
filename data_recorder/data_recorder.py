# Import the required modules

import sys
sys.path.append("../catkin_ws/devel/lib/python3/dist-packages")

import rospy
from bench.msg import BenchState, BenchMotorControl, BenchRecorderControl
# Import the required modules
import csv
import sys
import time

# Define the callback function that will be called
# whenever a message is received on the topic
def callback(msg, csv_file):
    # Create a CSV writer
    writer = csv.writer(csv_file)

    # Write the message data to the CSV file
    writer.writerow([
        msg.tick,
        msg.angle,
        msg.safety_switch_pressed, 
        msg.flex_myobrick_pos_encoder, 
        msg.flex_myobrick_torque_encoder, 
        msg.flex_myobrick_current, 
        msg.flex_myobrick_pwm, 
        msg.flex_myobrick_in_running_state, 
        msg.extend_myobrick_pos_encoder, 
        msg.extend_myobrick_torque_encoder, 
        msg.extend_myobrick_current, 
        msg.extend_myobrick_pwm, 
        msg.extend_myobrick_in_running_state, 
    ])

# Open the CSV file in append mode
with open(sys.argv[1], 'a') as csv_file:
    # Write header to CSV file if it is empty
    if csv_file.tell() == 0:
        csv.writer(csv_file).writerow([
            'tick',
            'angle',
            'safety_switch_pressed', 
            'flex_myobrick_pos_encoder', 
            'flex_myobrick_torque_encoder', 
            'flex_myobrick_current', 
            'flex_myobrick_pwm', 
            'flex_myobrick_in_running_state', 
            'extend_myobrick_pos_encoder', 
            'extend_myobrick_torque_encoder', 
            'extend_myobrick_current', 
            'extend_myobrick_pwm', 
            'extend_myobrick_in_running_state', 
        ])


    # Initialize the ROS node
    rospy.init_node('listener')

    # Create a ROS subscriber to listen on the topic
    sub = rospy.Subscriber('/test_bench/BenchState', BenchState, callback, csv_file)

    # Spin the node to keep it running
    print('Data recorder running.')
    print('Saving to file: ' + sys.argv[1])
    print('Press CTRL+C to terminate.')
    rospy.spin()
