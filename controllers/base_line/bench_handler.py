
import threading
import subprocess
import collections
import rospy
import time
import random
import torch
import pandas as pd
import numpy as np


import sys

# Add folder to path
sys.path.append("../nn_1/dev/ctrl_model")
from ctrl_model import CtrlModel


sys.path.append("../../catkin_ws/devel/lib/python3/dist-packages")
from bench.msg import BenchState, BenchMotorControl, BenchRecorderControl

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

"""
        # Extract data
        past_inputs = df.iloc[:self.num_time_steps_before][[
            'flex_myobrick_pwm', 
            'extend_myobrick_pwm'
        ]].to_numpy().astype(np.float32)
        past_outputs = df.iloc[:self.num_time_steps_before][
            'angle'
        ].to_numpy().astype(np.float32)
        past_interals = df.iloc[:self.num_time_steps_before][[
            'flex_myobrick_torque_encoder',
            #'flex_myobrick_pos_encoder',
            'extend_myobrick_torque_encoder',
            #'extend_myobrick_pos_encoder'
        ]].to_numpy().astype(np.float32)

        # convert to tensors and fix dimensions
        past_inputs = torch.from_numpy(past_inputs).permute(1, 0)
        past_outputs = torch.from_numpy(past_outputs).unsqueeze(0)
        past_interals = torch.from_numpy(past_interals).permute(1, 0)

        for i in range(past_inputs.shape[0]):
            past_inputs[i] = (past_inputs[i] - self.input_channel_means[i]) / self.input_channel_stds[i]
        for i in range(past_outputs.shape[0]):
            past_outputs[i] = (past_outputs[i] - self.output_channel_means[i]) / self.output_channel_stds[i]
        for i in range(past_interals.shape[0]):
            past_interals[i] = (past_interals[i] - self.internal_channel_means[i]) / self.internal_channel_stds[i]

"""

class BenchHandler:
    def __init__(self, waypoint_handler):

        self.waypoint_handler = waypoint_handler

        # Setup message event callback
        self.subscriber = rospy.Subscriber('/test_bench/BenchState', BenchState, self._on_bench_state_callback)
        self.publisher = rospy.Publisher('/test_bench/BenchMotorControl', BenchMotorControl, queue_size=10)

        # Circular buffer for storing incoming messages
        self.state_buffer = collections.deque(maxlen=40)

        self.ctrl_model = CtrlModel(
            num_past_time_steps=30,
            num_future_time_steps=30,
            num_input_vars=2,
            num_output_vars=1,
            num_internal_vars=2
        )
        self.ctrl_model.load_state_dict(torch.load('../nn_1/dev/ctrl_model/ctrl_model_2023-03-18_12-00-48.pt'))
        # send to cpu
        self.ctrl_model = self.ctrl_model.cpu()
        # set to eval mode
        self.ctrl_model.eval()

        # Setup data frame for storing incoming messages
        self.state_buffer_df = pd.DataFrame(columns=[
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

        self.input_channel_means = [5.867484, 5.720537]
        self.input_channel_stds = [4.866541,  4.8768854]
        self.output_channel_means = [1619.3425]
        self.output_channel_stds = [158.12558]
        self.internal_channel_means = [-2.0340237e+03, -2.1668540e+03]
        self.internal_channel_stds = [1.1323308e+03, 1.2715853e+03]

    def _on_bench_state_callback(self, bench_state):

        t_0 = time.time()

        self.state_buffer.append([
            bench_state.flex_myobrick_pwm,
            bench_state.extend_myobrick_pwm,
            bench_state.angle,
            bench_state.flex_myobrick_torque_encoder,
            bench_state.extend_myobrick_torque_encoder,
        ])


        # Create a new message object to send to the bench
        current_tick = bench_state.tick
        msg = BenchMotorControl()
        msg.tick = current_tick + 1


        # Check if there are enough data points for the model
        if len(self.state_buffer) >= 30:



            # Get 30 past data points
            past = list(self.state_buffer)[-30:]

            # Convert to numpy array
            past = np.array(past).astype(np.float32)

            # Get post inputs
            past_inputs = past[:, :2]
            # Get past outputs
            past_outputs = past[:, 2]
            # Get past internals
            past_interals = past[:, 3:]


            # convert to tensors and fix dimensions
            past_inputs = torch.from_numpy(past_inputs).permute(1, 0)
            past_outputs = torch.from_numpy(past_outputs).unsqueeze(0)
            past_interals = torch.from_numpy(past_interals).permute(1, 0)

            # Normalize data
            for i in range(past_inputs.shape[0]):
                past_inputs[i] = (past_inputs[i] - self.input_channel_means[i]) / self.input_channel_stds[i]
            for i in range(past_outputs.shape[0]):
                past_outputs[i] = (past_outputs[i] - self.output_channel_means[i]) / self.output_channel_stds[i]
            for i in range(past_interals.shape[0]):
                past_interals[i] = (past_interals[i] - self.internal_channel_means[i]) / self.internal_channel_stds[i]


            # Get desired future outputs
            desired_future_outputs = torch.ones(1, 30) * (TOP_ANGLE_VALUE + BOT_ANGLE_VALUE) / 2

            # Normalize desired future outputs
            for i in range(desired_future_outputs.shape[0]):
                desired_future_outputs[i] = (desired_future_outputs[i] - self.output_channel_means[i]) / self.output_channel_stds[i]


            # Reshape tensors
            past_inputs = past_inputs.unsqueeze(0)
            past_outputs = past_outputs.unsqueeze(0)
            past_interals = past_interals.unsqueeze(0)
            desired_future_outputs = desired_future_outputs.unsqueeze(0)


            # apply model
            activation_vector = self.ctrl_model(past_inputs, past_outputs, past_interals, desired_future_outputs)
            activation_vector = activation_vector.squeeze(0)

            # Denormalize activation vector 
            for i in range(activation_vector.shape[0]):
                activation_vector[i] = activation_vector[i] * self.input_channel_stds[i] + self.input_channel_means[i]

            # Set activation vector
            msg.flex_myobrick_pwm = activation_vector[0]
            msg.extend_myobrick_pwm = activation_vector[1]



        
        else:
            # Set zero pwm if not enough data points
            msg.flex_myobrick_pwm = 0
            msg.extend_myobrick_pwm = 0


        self.publisher.publish(msg)


        t_1 = time.time()
        # Print with centered decimal point
        print('Time to run controller: {0:.3f} ms'.format((t_1 - t_0) * 1000))




    def get_n_last_state_vectors(self, n):
        return list(self.state_buffer)[-n:]
        
    def apply_activation_vector(self, activation_vector):

        msg = BenchMotorControl()
        msg.flex_myobrick_pwm = activation_vector.flex_myobrick_pwm
        msg.extend_myobrick_pwm = activation_vector.extend_myobrick_pwm
        self.publisher.publish(msg)
    
    def get_last_state_vector(self):
        return self.state_buffer[-1]


# Create transform class
class SysModelTransform:
    def __init__(self):
        """
        From tick_based_100hz_23-02-19.csv we get:
            input_channel_means [5.867484 5.720537]
            input_channel_stds [4.866541  4.8768854]
            output_channel_means 1619.3425
            output_channel_stds 158.12558
            internal_channel_means [-2.0340237e+03  6.3358569e-01 -2.1668540e+03  1.4289156e+01]
            internal_channel_stds [1.1323308e+03 1.1938887e+00 1.2715853e+03 1.0630209e+00]
        """

        self.input_channel_means = [5.867484, 5.720537]
        self.input_channel_stds = [4.866541,  4.8768854]
        self.output_channel_means = [1619.3425]
        self.output_channel_stds = [158.12558]
        #self.internal_channel_means = [-2.0340237e+03,  6.3358569e-01, -2.1668540e+03,  1.4289156e+01]
        #self.internal_channel_stds = [1.1323308e+03, 1.1938887e+00, 1.2715853e+03, 1.0630209e+00]
        self.internal_channel_means = [-2.0340237e+03, -2.1668540e+03]
        self.internal_channel_stds = [1.1323308e+03, 1.2715853e+03]

    

    def __call__(self, past_inputs, past_outputs, past_interals, future_inputs, future_outputs, future_interals):
        for i in range(past_inputs.shape[0]):
            past_inputs[i] = (past_inputs[i] - self.input_channel_means[i]) / self.input_channel_stds[i]
        for i in range(past_outputs.shape[0]):
            past_outputs[i] = (past_outputs[i] - self.output_channel_means[i]) / self.output_channel_stds[i]
        for i in range(past_interals.shape[0]):
            past_interals[i] = (past_interals[i] - self.internal_channel_means[i]) / self.internal_channel_stds[i]

        for i in range(future_inputs.shape[0]):
            future_inputs[i] = (future_inputs[i] - self.input_channel_means[i]) / self.input_channel_stds[i]
        for i in range(future_outputs.shape[0]):
            future_outputs[i] = (future_outputs[i] - self.output_channel_means[i]) / self.output_channel_stds[i]
        for i in range(future_interals.shape[0]):
            future_interals[i] = (future_interals[i] - self.internal_channel_means[i]) / self.internal_channel_stds[i]

        return past_inputs, past_outputs, past_interals, future_inputs, future_outputs, future_interals
    
    def reverse(self, past_inputs, past_outputs, past_interals, future_inputs, future_outputs, future_interals):
        for i in range(past_inputs.shape[0]):
            past_inputs[i] = (past_inputs[i] * self.input_channel_stds[i]) + self.input_channel_means[i]
        for i in range(past_outputs.shape[0]):
            past_outputs[i] = (past_outputs[i] * self.output_channel_stds[i]) + self.output_channel_means[i]
        for i in range(past_interals.shape[0]):
            past_interals[i] = (past_interals[i] * self.internal_channel_stds[i]) + self.internal_channel_means[i]

        for i in range(future_inputs.shape[0]):
            future_inputs[i] = (future_inputs[i] * self.input_channel_stds[i]) + self.input_channel_means[i]
        for i in range(future_outputs.shape[0]):
            future_outputs[i] = (future_outputs[i] * self.output_channel_stds[i]) + self.output_channel_means[i]
        for i in range(future_interals.shape[0]):
            future_interals[i] = (future_interals[i] * self.internal_channel_stds[i]) + self.internal_channel_means[i]

        return past_inputs, past_outputs, past_interals, future_inputs, future_outputs, future_interals
    