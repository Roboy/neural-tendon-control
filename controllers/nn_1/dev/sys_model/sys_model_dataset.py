# Create dataset class
import numpy as np
import torch

class SysModelDataset:
    def __init__(self, df, num_time_steps_before, num_time_steps_after):
        self.df = df
        self.num_time_steps_before = num_time_steps_before
        self.num_time_steps_after = num_time_steps_after
        self.transform = SysModelTransform()
    

    def __len__(self):
        return len(self.df) - self.num_time_steps_before - self.num_time_steps_after

    def __getitem__(self, idx):
        # idx can be of type int or slice

        # Get a slice of the dataframe
        df = self.df.iloc[idx:idx+self.num_time_steps_before+self.num_time_steps_after].copy()


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

        future_outputs = df.iloc[self.num_time_steps_before:self.num_time_steps_before+self.num_time_steps_after][
            'angle'
        ].to_numpy().astype(np.float32)
        future_inputs = df.iloc[self.num_time_steps_before:self.num_time_steps_before+self.num_time_steps_after][[
            'flex_myobrick_pwm',
            'extend_myobrick_pwm'
        ]].to_numpy().astype(np.float32)
        future_interals = df.iloc[self.num_time_steps_before:self.num_time_steps_before+self.num_time_steps_after][[
            'flex_myobrick_torque_encoder',
            #'flex_myobrick_pos_encoder',
            'extend_myobrick_torque_encoder',
            #'extend_myobrick_pos_encoder'
        ]].to_numpy().astype(np.float32)
                


        # convert to tensors and fix dimensions
        past_inputs = torch.from_numpy(past_inputs).permute(1, 0)
        past_outputs = torch.from_numpy(past_outputs).unsqueeze(0)
        past_interals = torch.from_numpy(past_interals).permute(1, 0)

        future_inputs = torch.from_numpy(future_inputs).permute(1, 0)
        future_outputs = torch.from_numpy(future_outputs).unsqueeze(0)
        future_interals = torch.from_numpy(future_interals).permute(1, 0)

        # Aply transform
        past_inputs, past_outputs, past_interals, future_inputs, future_outputs, future_interals = self.transform(past_inputs, past_outputs, past_interals, future_inputs, future_outputs, future_interals)
        

        return past_inputs, past_outputs, past_interals, future_inputs, future_outputs, future_interals

    
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
    