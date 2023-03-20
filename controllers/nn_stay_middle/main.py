import time
import rospy
import sys


from ros_loop import RosLoop

from bench_handler import BenchHandler
from waypoint_handler import WaypointHandler



def run_controller_node():
    print("Starting controller node.")


    # Init ros loop thread
    print('Init ROS loop.')
    ros_loop = RosLoop()


    # Init waypoint listener
    print('Init waypoint handler.')
    waypoint_handler = WaypointHandler()


    # Init communication with bench node
    print('Init communication with bench node.')
    bench_handler = BenchHandler(waypoint_handler)




    # Start ROS loop
    print('Starting ROS loop.')
    ros_loop.start()




    # Run until keyboard interrupt
    print('Press q then enter to quit.')
    while True:
        key = sys.stdin.read(1)

        # Check if the user pressed "q"
        if key == "q":
            print("q was pressed")
            break


    print("Stopping bench node")




    # Terminating ROS loop
    print('Terminating controller ROS loop.')
    ros_loop.stop()

    
    


if __name__ == "__main__":
    print("Starting controller node.")

    run_controller_node()

    print("Controler node exited.")