
import threading
import subprocess
import collections
import rospy
import time


import sys
sys.path.append("../../catkin_ws/devel/lib/python3/dist-packages")

from bench.msg import BenchState, BenchMotorControl, BenchRecorderControl



class ActivationVector:
    def __init__(self, flex_myobrick_pwm, extend_myobrick_pwm):
        self.flex_myobrick_pwm = flex_myobrick_pwm
        self.extend_myobrick_pwm = extend_myobrick_pwm

class StateVector:
    def __init__(
            self, 
            timestamp,
            angle,
            safety_switch_pressed,
            flex_myobrick_pos_encoder,
            flex_myobrick_torque_encoder,
            flex_myobrick_current,
            flex_myobrick_pwm,
            flex_myobrick_in_running_state,
            extend_myobrick_pos_encoder,
            extend_myobrick_torque_encoder,
            extend_myobrick_current,
            extend_myobrick_pwm,
            extend_myobrick_in_running_state
        ):

        self.timestamp = timestamp
        self.angle = angle
        self.safety_switch_pressed = safety_switch_pressed
        self.flex_myobrick_pos_encoder = flex_myobrick_pos_encoder
        self.flex_myobrick_torque_encoder = flex_myobrick_torque_encoder
        self.flex_myobrick_current = flex_myobrick_current
        self.flex_myobrick_pwm = flex_myobrick_pwm
        self.flex_myobrick_in_running_state = flex_myobrick_in_running_state
        self.extend_myobrick_pos_encoder = extend_myobrick_pos_encoder
        self.extend_myobrick_torque_encoder = extend_myobrick_torque_encoder
        self.extend_myobrick_current = extend_myobrick_current
        self.extend_myobrick_pwm = extend_myobrick_pwm
        self.extend_myobrick_in_running_state = extend_myobrick_in_running_state


class BenchHandler:
    def __init__(self):

        # Setup message event callback
        self.subscriber = rospy.Subscriber('/test_bench/BenchState', BenchState, self._on_bench_state_callback)
        self.publisher = rospy.Publisher('/test_bench/BenchMotorControl', BenchMotorControl, queue_size=10)

        # Circular buffer for storing incoming messages
        self.state_buffer = collections.deque(maxlen=40)


    def _on_bench_state_callback(self, msg):
        state_vector = StateVector(
            time.time(),
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
            msg.extend_myobrick_in_running_state
        )

        self.state_buffer.append(state_vector)

    def get_n_last_state_vectors(self, n):
        return list(self.state_buffer)[-n:]
        
    def apply_activation_vector(self, activation_vector):

        msg = BenchMotorControl()
        msg.flex_myobrick_pwm = activation_vector.flex_myobrick_pwm
        msg.extend_myobrick_pwm = activation_vector.extend_myobrick_pwm
        self.publisher.publish(msg)
    
    def get_last_state_vector(self):
        return self.state_buffer[-1]

    