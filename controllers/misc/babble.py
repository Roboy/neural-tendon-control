import sys
sys.path.append("../../catkin_ws/devel/lib/python3/dist-packages")

import rospy
from bench.msg import BenchState, BenchMotorControl, BenchRecorderControl
# Import the required modules
import csv
import time
import random
import numpy as np



TOP_ANGLE_VALUE = 2000.0
BOT_ANGLE_VALUE = 1250.0

FLEX_MYOBRICK_TORQUE_ENCODER_AT_REST = -900
FLEX_MYOBRICK_TORQUE_ENCODER_MAX = -3000

FLEX_MYOBRICK_TORQUE_ENCODER_DIRECTION = -1

EXTEND_MYOBRICK_TORQUE_ENCODER_AT_REST = -900
EXTEND_MYOBRICK_TORQUE_ENCODER_MAX = -3000
EXTEND_MYOBRICK_TORQUE_ENCODER_DIRECTION = 1

global_state = {
    'direction' : 1,
    'prev_random_float_1' : 0,
    'prev_random_float_2' : 0,
    'prev_flex_pwm' : 0,
    'prev_extend_pwm' : 0,
}

rospy.init_node('go_to_middle_controller')


bench_control_pub = rospy.Publisher('/test_bench/BenchMotorControl', BenchMotorControl, queue_size=10)

# Define the callback function that will be called
# whenever a message is received on the topic

def callback(bench_state, global_state):
    middle_pos = (TOP_ANGLE_VALUE + BOT_ANGLE_VALUE) / 2

    current_tick = bench_state.tick
    msg = BenchMotorControl()
    msg.tick = current_tick + 1

    if bench_state.angle > (TOP_ANGLE_VALUE - 100):
        global_state['direction'] = 0
        print('going down!')
    

    elif bench_state.angle < (BOT_ANGLE_VALUE + 100):
        global_state['direction'] = 1
        print('going up!')


    else:
        global_state['direction'] = -1
    

    if global_state['direction'] == 1:
        msg.flex_myobrick_pwm = 7
        msg.extend_myobrick_pwm = -2

    if global_state['direction'] == 0:
        msg.flex_myobrick_pwm = -2
        msg.extend_myobrick_pwm = 7
    

    if global_state['direction'] == -1:
        # Gaussian random variable with mean 0 and standard deviation 0.02
        random_float_1 = random.gauss(0, 0.5)
        random_float_2 = random.gauss(0, 0.5)

        new_flex_pwm = global_state['prev_flex_pwm'] + random_float_1
        new_extend_pwm = global_state['prev_extend_pwm'] + random_float_2

        # set interval to [15, -2]
        new_flex_pwm = max(min(new_flex_pwm, 15), -2)
        new_extend_pwm = max(min(new_extend_pwm, 15), -2)

        # Make sure tension is not low
        if bench_state.flex_myobrick_torque_encoder > FLEX_MYOBRICK_TORQUE_ENCODER_AT_REST:
            new_flex_pwm = new_flex_pwm + 0.01
        if bench_state.extend_myobrick_torque_encoder > EXTEND_MYOBRICK_TORQUE_ENCODER_AT_REST:
            new_extend_pwm = new_extend_pwm + 0.01

        # Make sure tension is not high
        if bench_state.flex_myobrick_torque_encoder < FLEX_MYOBRICK_TORQUE_ENCODER_MAX:
            new_flex_pwm = new_flex_pwm - 0.01
        if bench_state.extend_myobrick_torque_encoder < EXTEND_MYOBRICK_TORQUE_ENCODER_MAX:
            new_extend_pwm = new_extend_pwm - 0.01

        msg.flex_myobrick_pwm = new_flex_pwm
        msg.extend_myobrick_pwm = new_extend_pwm


    global_state['prev_flex_pwm'] = msg.flex_myobrick_pwm
    global_state['prev_extend_pwm'] = msg.extend_myobrick_pwm

    bench_control_pub.publish(msg)



    if bench_state.safety_switch_pressed == True:
        print('Kill switch is pressed, stopping.')
        rospy.signal_shutdown('')
        sys.exit()

    if bench_state.flex_myobrick_in_running_state == False:
        print('Flex MyoBrick is not in running state, stopping.')
        rospy.signal_shutdown('')
        sys.exit()

    if bench_state.extend_myobrick_in_running_state == False:
        print('Extend MyoBrick is not in running state, stopping.')
        rospy.signal_shutdown('')
        sys.exit()



bench_control_sub = rospy.Subscriber('/test_bench/BenchState', BenchState, callback, global_state)

rospy.spin()
