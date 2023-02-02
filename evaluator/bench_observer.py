import rospy
import threading
import time
import pandas as pd

from bench.msg import BenchState, BenchMotorControl, BenchRecorderControl


class BenchObserver:
    def __init__(self):

        # Setup message event callback
        self.subscriber = rospy.Subscriber('/test_bench/BenchState', BenchState, self._on_bench_state_callback)

        self.bench_state_df = pd.DataFrame(columns=[
            'timestamp',
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


    def _on_bench_state_callback(self, msg):
        
        self.bench_state_df = self.bench_state_df.append({
            'timestamp': time.time(),
            'angle': msg.angle,
            'safety_switch_pressed': msg.safety_switch_pressed, 
            'flex_myobrick_pos_encoder': msg.flex_myobrick_pos_encoder, 
            'flex_myobrick_torque_encoder': msg.flex_myobrick_torque_encoder, 
            'flex_myobrick_current': msg.flex_myobrick_current, 
            'flex_myobrick_pwm': msg.flex_myobrick_pwm, 
            'flex_myobrick_in_running_state': msg.flex_myobrick_in_running_state, 
            'extend_myobrick_pos_encoder': msg.extend_myobrick_pos_encoder, 
            'extend_myobrick_torque_encoder': msg.extend_myobrick_torque_encoder, 
            'extend_myobrick_current': msg.extend_myobrick_current, 
            'extend_myobrick_pwm': msg.extend_myobrick_pwm, 
            'extend_myobrick_in_running_state': msg.extend_myobrick_in_running_state,
        }, ignore_index=True)


    def get_recorded_bench_state(self):
        return self.bench_state_df

    