'''
Model for controlling any type of system with a given set of input, output and measured state variables.

Contstraints:
    - fixed sampling rate for measured state variables, input and output


Should I add past desired outputs as input to the model?

'''


import torch
# lightning
import pytorch_lightning as pl




class SystemControllerModel(pl.LightningModule):
    def __init__(self, num_past_time_steps, num_future_time_steps, num_input_vars, num_output_vars, num_internal_vars):
        super().__init__()

        self.num_past_time_steps = num_past_time_steps
        self.num_future_time_steps = num_future_time_steps
        self.num_input_vars = num_input_vars
        self.num_output_vars = num_output_vars
        self.num_internal_vars = num_internal_vars

        # Convolute over past states
        past_conv1_out_channels = 5
        self.past_conv1 = torch.nn.Conv1d(num_input_vars + num_output_vars + num_internal_vars, past_conv1_out_channels, 3)
        past_conv2_out_channels = 10
        self.past_conv2 = torch.nn.Conv1d(past_conv1_out_channels, past_conv2_out_channels, 3)
        past_conv2_out_dim = [past_conv2_out_channels, num_past_time_steps - 4]


        # Convolute over desired outputs
        future_conv1_out_channels = 5
        self.future_desired_output_conv1 = torch.nn.Conv1d(num_output_vars, future_conv1_out_channels, 2)
        future_conv2_out_channels = 5
        self.future_desired_output_conv2 = torch.nn.Conv1d(future_conv2_out_channels, future_conv2_out_channels, 2)
        future_conv2_out_dim = [future_conv2_out_channels, num_future_time_steps - 2]

        # Fully connected layers
        fc1_out_dim = 20
        self.fc1 = torch.nn.Linear(
            180, # Got from debugging
            num_future_time_steps * fc1_out_dim
        )

        self.fc2 = torch.nn.Linear(
            num_future_time_steps * fc1_out_dim, 
            num_future_time_steps * num_input_vars
        )


    def forward(self, past_inputs, past_outputs, past_interals, future_desired_outputs):
        '''
        input:
            past_inputs: [batch_size, num_input_vars, num_past_time_steps]
            past_outputs: [batch_size, num_output_vars, num_past_time_steps]
            past_interals: [batch_size, num_internal_vars, num_past_time_steps]
            future_desired_outputs: [batch_size, num_output_vars, num_future_time_steps]

        output:
            future_predicted_inputs: [batch_size, num_input_vars, num_future_time_steps]
        '''


        past_combined = torch.cat((past_inputs, past_outputs, past_interals), dim=1)

        # Convolute over past combined
        x_1 = torch.nn.functional.relu(self.past_conv1(past_combined))
        x_2 = torch.nn.functional.relu(self.past_conv2(x_1))

        # Convolute over desired outputs
        x_2 = torch.nn.functional.relu(self.future_desired_output_conv1(future_desired_outputs))
        x_2 = torch.nn.functional.relu(self.future_desired_output_conv2(x_2))

        # Flatten and feed into fully connected layers
        x_1 = torch.flatten(x_1, start_dim=1)
        x_2 = torch.flatten(x_2, start_dim=1)

        x = torch.cat((x_1, x_2), dim=1)
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))

        # Reshape to [batch_size, num_input_vars, num_future_time_steps]
        future_predicted_inputs = x.reshape(x.shape[0], -1, self.num_future_time_steps)

        

        return future_predicted_inputs

    def training_step(self, batch, batch_idx):
        past_inputs, past_outputs, past_interals, future_desired_outputs, future_predicted_inputs = batch
        y_hat = self(past_inputs, past_outputs, past_interals, future_desired_outputs)
        loss = torch.nn.functional.mse_loss(y_hat, future_predicted_inputs)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)

