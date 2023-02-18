import time
import rospy

import sys
sys.path.append("../catkin_ws/devel/lib/python3/dist-packages")

from angle_sensor import AngleSensor
from ros_loop import RosLoop
from myobrick import MyoBrick
from safety_observer import SafetyObserver
from control_listener import ControlListener
from tick_loop import TickLoop


TICK_LOOP_FREQ = 100

def run_bench_node():
    print("Starting bench node")

    # Init angle sensor
    print('Init angle sensor.')
    angle_sensor = AngleSensor('/dev/ttyACM0')
    angle_sensor.start()

    # Init ros loop thread
    print('Init ROS loop.')
    ros_loop = RosLoop()

    # Init myobricks
    print('Init MyoBricks.')
    myobrick_flex = MyoBrick(1)
    myobrick_extend = MyoBrick(3)

    # Init safety observer
    print('Init safet observer.')
    safety_observer = SafetyObserver(
        myobrick_flex,
        myobrick_extend,
        angle_sensor
    )
    print('Statring safety observer.')
    safety_observer.start()

    # Init control listener
    print('Init control listener.')
    control_listener = ControlListener(
        myobrick_flex,
        myobrick_extend,
        safety_observer
    )

    # Start ROS loop
    print('Starting ROS loop.')
    ros_loop.start()

    # Begin broadvasting bench state
    print('Init state broadcaster.')
    state_broadcaster = TickLoop(
        angle_sensor,
        myobrick_flex,
        myobrick_extend,
        safety_observer,
        control_listener,
        freq = TICK_LOOP_FREQ
    )
    print('Starting state broadcaster.')
    state_broadcaster.start()


    # Run until keyboard interrupt
    print('Press q then enter to quit.')
    while True:
        key = sys.stdin.read(1)

        # Check if the user pressed "q"
        if key == "q":
            print("q was pressed")
            break


    print("Stopping bench node")


    # Terminating state broadcaster
    print('Terminating state broadcaster')
    state_broadcaster.terminate()

    # Terminating ROS loop
    print('Terminating ROS loop.')
    ros_loop.stop()

    print('Terminating safety observer.')
    safety_observer.stop()

    print('Terminating MyoBrick communication.')
    myobrick_extend.terminate()
    myobrick_flex.terminate()

    print('Terminate angle sensor communicatoin.')
    angle_sensor.terminate()

    
    


if __name__ == "__main__":
    print("Starting bench node")

    run_bench_node()

    print("Stopping bench node")