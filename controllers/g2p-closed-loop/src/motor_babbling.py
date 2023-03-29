from functions import *
import numpy as np

def motor_babbling(babbling_seconds = 300, timestep = 0.01, pass_chance = 0.01, skip_rows = 200, max_in = 1, min_in = 0):

    """
    Implementation of motor babbling to create an inverse kinematics model of the test bench

    Parameters
    ----------
        * babbling_seconds: number of seconds to babble (default: 300)
        * timestep: duration of each timestep in seconds (default: 0.01)
        * pass_chance: probability of activation being passed to motor (default: 0.01)
        * skip_rows: number of rows to skip in babbling data (setup phase) (default: 200)
        * max_in: maximum activation value (default: 1)
        * min_in: minimum activation value (default: 0)

    Returns
    -------
        * babbling_kinematics: kinematics resulting from given activations
        * babbling_activations: activations of babbling generated from generate_activation_values()
    """

    #number of samples to run
    run_samples = int(np.round(babbling_seconds/timestep))

    #generating random activations in range (min_in, max_in) -> These activations could fight against each other but that is okay
    motor1_act = generate_activations(babbling_seconds, pass_chance, max_in, min_in, run_samples)
    motor2_act = generate_activations(babbling_seconds, pass_chance, max_in, min_in, run_samples)

    #concatenate motor activations in one vector with shape (run_samples, num_motors)
    babbling_activations = np.transpose(np.concatenate([[motor1_act],[motor2_act]], axis=0))

    #run babbling activations and map activations to resulting kinematics
    [babbling_kinematics, babbling_activations, _] = run_activations(babbling_activations, timestep)

    #return kinematics to activations mapping after skipping setup phase
    return babbling_kinematics[skip_rows:,:], babbling_activations[skip_rows:, :]

def generate_activations(signal_duration: int, pass_chance: float, max_in: float, min_in: float, run_samples: int):

    """
    Generating random activations for each motor
    
    Parameters
    ----------
        * signal_duration: duration of signal in seconds
        * pass_chance: probability of activation being passed to motor
        * max_in: maximum activation value
        * min_in: minimum activation value
        * run_samples: number of samples to run
    
    Returns
    -------
        * generated_activations: activations that can be run on robot
    """

    #generate evenly spaced samples
    samples = np.linspace(0, signal_duration, run_samples)

    #initialize activations vector
    generated_activations = np.zeros(run_samples,)

	#generating random activations
    for i in range(1, run_samples):
        pass_rand = np.random.uniform(0,1,1)
	
        if pass_rand < pass_chance:
            #generate random activation in range (min_in, max_in)
            generated_activations[i] = ((max_in - min_in) * np.random.uniform(0,1,1)) + min_in
        else:
            #set activation to previous activation
            generated_activations[i] = generated_activations[i-1]

    return generated_activations