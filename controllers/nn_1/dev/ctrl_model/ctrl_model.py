'''
Model for controlling any type of system with a given set of input, output and measured state variables.

Contstraints:
    - fixed sampling rate for measured state variables, input and output


Should I add past desired outputs as input to the model?

'''


import torch
# lightning
import pytorch_lightning as pl




class CtrlModel(pl.LightningModule):
    def __init__(self, num_past_time_steps, num_future_time_steps, num_input_vars, num_output_vars, num_internal_vars):
        super().__init__()

        self.num_past_time_steps = num_past_time_steps
        self.num_future_time_steps = num_future_time_steps
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

        # Conv f1
        conv_f1_out_channels = 3
        conv_f1_kernel_size = 3
        self.conv_f1 = torch.nn.Conv1d(
            num_output_vars, 
            conv_f1_out_channels, 
            conv_f1_kernel_size
        )
        conv_f1_out_dim = [conv_f1_out_channels, num_future_time_steps - 2]

        # Conv f2
        conv_f2_out_channels = 3
        conv_f2_kernel_size = 3
        self.conv_f2 = torch.nn.Conv1d(
            conv_f1_out_channels, 
            conv_f2_out_channels, 
            conv_f2_kernel_size
        )
        conv_f2_out_dim = [conv_f2_out_channels, conv_f1_out_dim[1] - 2]


        # fc new2
        fc_new2_out_dim = 30
        self.fc_new2 = torch.nn.Linear(
            sum([
                fc1_out_dim,
                num_past_time_steps * (num_output_vars + num_internal_vars),
                num_future_time_steps * num_output_vars,
                conv_f1_out_dim[0] * conv_f1_out_dim[1],
                conv_f2_out_dim[0] * conv_f2_out_dim[1]
            ]),
            fc_new2_out_dim
        )

        fc_new3_out_dim = 20
        self.fc_new3 = torch.nn.Linear(
            fc_new2_out_dim, 
            fc_new3_out_dim
        )

        self.fc_new4 = torch.nn.Linear(
            fc_new3_out_dim, 
            num_input_vars
        )



    def forward(self, past_inputs, past_outputs, past_interals, future_outputs):
        '''
        input:
            past_inputs: [batch_size, num_input_vars, num_past_time_steps]
            past_outputs: [batch_size, num_output_vars, num_past_time_steps]
            past_interals: [batch_size, num_internal_vars, num_past_time_steps]
            future_outputs: [batch_size, num_output_vars, num_future_time_steps]

        output:
            next_predicted_input: [batch_size, num_input_vars, 1]

        '''

        # Common with sys model START

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

        # Common with sys model END


        # Conv f1
        x_f1 = torch.nn.functional.relu(self.conv_f1(future_outputs))

        # Conv f2
        x_f2 = torch.nn.functional.relu(self.conv_f2(x_f1))

        # FC new2
        x_new2_in = torch.cat([
            x_4,
            past_outputs.reshape(past_outputs.shape[0], -1),
            past_interals.reshape(past_interals.shape[0], -1),
            future_outputs.reshape(future_outputs.shape[0], -1),
            x_f1.reshape(x_f1.shape[0], -1),
            x_f2.reshape(x_f2.shape[0], -1)
        ], dim=1)
        x_new2 = torch.nn.functional.relu(self.fc_new2(x_new2_in))

        # FC new3
        x_new3 = torch.nn.functional.relu(self.fc_new3(x_new2))

        # FC new4
        next_predicted_input = self.fc_new4(x_new3)

        # Fix dimensions
        next_predicted_input = next_predicted_input.unsqueeze(-1)

        return next_predicted_input

    def training_step(self, batch, batch_idx):
        past_inputs, past_outputs, past_interals, future_outputs, next_input = batch
        next_predicted_input = self(past_inputs, past_outputs, past_interals, future_outputs)
        loss = torch.nn.functional.mse_loss(next_predicted_input, next_input)
        self.log('train_loss', loss)
        return loss

    def test_step(self, batch, batch_idx):
        past_inputs, past_outputs, past_interals, future_outputs, next_input = batch
        next_predicted_input = self(past_inputs, past_outputs, past_interals, future_outputs)
        loss = torch.nn.functional.mse_loss(next_predicted_input, next_input)
        self.log('test_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)

