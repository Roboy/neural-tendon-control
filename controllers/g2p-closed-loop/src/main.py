import numpy as np
from matplotlib import pyplot as plt
from warnings import simplefilter
from tensorflow.keras.models import save_model
from functions import *
from motor_babbling import *

# Make sure we always get the same random data
np.random.seed(0)

# Generate first training data with motor babbling
[babbling_kinematics, babbling_activations] = motor_babbling(babbling_seconds = 300, timestep = 0.01, pass_chance = 0.01, skip_rows = 200, max_in = 1, min_in = 0)

# Create training database initially with babbling data
cum_kinematics = babbling_kinematics
cum_activations = babbling_activations

# Create inverse mapping with babbling data and save MinMaxScaler from input and output
model, scalerIn, scalerOut = inverse_mapping(kinematics = babbling_kinematics, activations = babbling_activations, early_stopping = True)

# Constants for PID Controller
# TODO: Might have to be tuned/adjusted
# TODO: Should we use D as well? -> Make it more responsive to changes in error
P = np.array([10])
I = np.array([2])

# Number of trials to get refined model
trial_number = 1
# Average error of predictions for each trial
average_error = []
# List of all models from each trial
models = []
#Make sure we always get the same random data
np.random.seed(0)

# Iterate over trials and refine model
for i in range(trial_number):

    # Refine model 10 times with optimized training data
    model, errors, cum_kinematics, cum_activations = refine(model = model, scalerIn = scalerIn, scalerOut = scalerOut, babbling_kinematics = babbling_kinematics, babbling_activations = babbling_activations, P = P, I = I, num_refinements = 10, timestep = 0.005)

    # Save model and average error for each trial
    models.append(model)
    average_error.append(np.mean(errors))

# Find model with lowest average error
best_model = models[np.argmin(average_error)]

# Save best model as h5 file. It can be used for inverse mapping!
save_model(best_model, 'model.h5')