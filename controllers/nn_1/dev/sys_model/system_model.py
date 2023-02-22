'''
Model for controlling any type of system with a given set of input, output and measured state variables.

Contstraints:
    - fixed sampling rate for measured state variables, input and output


Should I add past desired outputs as input to the model?

'''


import torch
# lightning
import pytorch_lightning as pl




class SysModel(pl.LightningModule):
    def __init__(self, num_past_time_steps, num_input_vars, num_output_vars, num_internal_vars):
        super().__init__()

        self.num_past_time_steps = num_past_time_steps
        self.num_input_vars = num_input_vars
        self.num_output_vars = num_output_vars
        self.num_internal_vars = num_internal_vars


        # Conv 1
        conv1_out_channels = 10
        conv1_kernel_size = 3
        self.conv1 = torch.nn.Conv1d(
            sum([num_output_vars, num_internal_vars]), 
            conv1_out_channels, 
            3
        )
        conv1_out_dim = [conv1_out_channels, num_past_time_steps - 2]

        # Conv 2
        conv2_out_channels = 20
        self.conv2 = torch.nn.Conv1d(
            conv1_out_channels, 
            conv2_out_channels, 
            3
        )
        conv2_out_dim = [conv2_out_channels, conv1_out_dim[1] - 2]

        conv3_out_channels = 10
        self.conv3 = torch.nn.Conv1d(
            sum([
                num_output_vars,
                num_internal_vars,
                conv1_out_channels,
                conv2_out_channels,
                num_input_vars
            ]), 
            conv3_out_channels, 
            15
        )
        conv3_out_dim = [conv3_out_channels, conv2_out_dim[1] - 14]
  

        # Fully connected layers
        fc1_out_dim = 20
        self.fc1 = torch.nn.Linear(
            sum([
                conv3_out_dim[0] * conv3_out_dim[1],
                conv1_out_dim[0] * conv1_out_dim[1],
                num_input_vars * num_past_time_steps,
            ]),
            fc1_out_dim
        )

        fc2_out_dim = 20
        self.fc2 = torch.nn.Linear(
            fc1_out_dim, 
            fc2_out_dim
        )

        self.fc3 = torch.nn.Linear(
            fc2_out_dim, 
            num_output_vars + num_internal_vars
        )


    def forward(self, past_inputs, past_outputs, past_interals):
        '''
        input:
            past_inputs: [batch_size, num_input_vars, num_past_time_steps]
            past_outputs: [batch_size, num_output_vars, num_past_time_steps]
            past_interals: [batch_size, num_internal_vars, num_past_time_steps]

        output:
            next_predicted_output: [batch_size, num_output_vars, 1]
            next_predicted_internal: [batch_size, num_internal_vars, 1]

        '''


        # Conv 1
        past_outputs_internals = torch.cat([past_outputs, past_interals], dim=1)
        x_1 = torch.nn.functional.relu(self.conv1(past_outputs_internals))

        # Conv 2
        x_2 = torch.nn.functional.relu(self.conv2(x_1))

        # Conv 3
        conv3_in = torch.cat([
            past_outputs[:, :, :x_2.shape[2]],
            past_interals[:, :, :x_2.shape[2]],
            x_1[:, :, :x_2.shape[2]],
            x_2,
            past_inputs[:, :, :x_2.shape[2]]
        ], dim=1)
        x_3 = torch.nn.functional.relu(self.conv3(conv3_in))


        # FC 1
        fc1_in = torch.cat([
            x_3.reshape(x_3.shape[0], -1),
            x_1.reshape(x_1.shape[0], -1),
            past_inputs.reshape(past_inputs.shape[0], -1)
        ], dim=1)
        x_4 = torch.nn.functional.relu(self.fc1(fc1_in))


        # FC 2
        x_5 = torch.nn.functional.relu(self.fc2(x_4))

        # FC 3
        x_6 = self.fc3(x_5)

        # Split output
        next_predicted_output_diff = x_6[:, :self.num_output_vars]
        next_predicted_internal_diff = x_6[:, self.num_output_vars:]

        # Add previous output and internal state
        next_predicted_output = next_predicted_output_diff + past_outputs[:, :, -1]
        next_predicted_internal = next_predicted_internal_diff + past_interals[:, :, -1]

        # Fix dimensions
        next_predicted_output = next_predicted_output.unsqueeze(-1)
        next_predicted_internal = next_predicted_internal.unsqueeze(-1)


        return next_predicted_output, next_predicted_internal

    def training_step(self, batch, batch_idx):
        past_inputs, past_outputs, past_interals, next_input, next_output, next_internal = batch
        next_predicted_output, next_predicted_internal = self(past_inputs, past_outputs, past_interals)
        loss = torch.nn.functional.mse_loss(next_predicted_output, next_output) + torch.nn.functional.mse_loss(next_predicted_internal, next_internal)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)

