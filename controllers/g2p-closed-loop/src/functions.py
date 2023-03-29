import numpy as np
import sklearn
import rospy
from numpy import matlib
from scipy import signal, stats
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
import os
from copy import deepcopy
from mpl_toolkits.mplot3d import axes3d
import matplotlib.lines as mlines
from copy import deepcopy
from run import *

def optimize_activations(model, cum_kinematics: np.ndarray, cum_activations: np.ndarray, reward_thresh = 7, refinement = False):

	"""
	Apply reinforcement learning by generating feature vectors and running the resulting activations on the test bench.
	These feature vectors contain the activations, kinematics and tendon force for a certain timestep of a particular task.
	The particular task is defined by a) Point to point movement, b) Sin Wave movement.
	The reward is defined by the overall tendon tension from both motors and the distance between the current and desired position.
	The resulting training data which is optimized for activations and tendon force is then used to refine the inverse kinematics model.

	Parameters
	----------
		* model: inverse kinematics model
		* cum_kinematics: kinematics of previous attempts
		* cum_activations: activations of previous attempts
		* reward_thresh: threshold for reward (default: 7)
		* refinement: whether to refine the model after each attempt (default: False)

	Returns
	-------
		* model: inverse kinematics model that has been refined in a closed loop fashion
		* cum_kinematics: kinematics of all attempts
		* cum_activations: activations of all attempts
		* all_rewards: list of all rewards

	"""
	
	# Reward from previous attempt
	prev_reward = np.array([0])
	# Best reward so far
	best_reward = prev_reward
	# Model that yielded best reward
	best_model = model
	# List of all rewards
	all_rewards = []
	# Number of exploitation runs
	exploitation_count = 0
	# Generate first feature vector
	new_features = generate_feature_vector(prev_reward = prev_reward, reward_thresh = reward_thresh, best_reward = best_reward, feat_vec_length = 10)
	# Save best feature vector
	best_features = new_features

	# Run 15 exploitation runs.
	while exploitation_count <= 15:

		# Only increase exploitation count if reward is above threshold
		if best_reward > reward_thresh:
			exploitation_count += 1

		# Generate new feature vector
		new_features = generate_feature_vector(reward_thresh = reward_thresh, best_reward = best_reward, best_features_so_far = best_features)

		[prev_reward, attempt_kinematics, est_attempt_activations, real_attempt_kinematics, real_attempt_activations] = \
			feat_to_run_attempt_fcn(features=new_features, model=model,feat_show=False, model_ver=1)
		
		[cum_kinematics, cum_activations] = \
		concatinate_training_data(
			cum_kinematics, cum_activations, real_attempt_kinematics, real_attempt_activations, throw_percentage = 0.20)
		all_rewards = np.append(all_rewards, prev_reward)

		if prev_reward>best_reward:
			best_reward = prev_reward
			best_features = new_features
			best_model = deepcopy(model)

		if refinement:
			model = inverse_mapping(cum_kinematics, cum_activations, prior_model=model)

		print("best reward so far: ", best_reward)

	input("Learning to walk completed, Press any key to proceed")

	[prev_reward_best, attempt_kinematics_best, est_attempt_activations_best, real_attempt_kinematics_best, real_attempt_activations_best]= \
	feat_to_run_attempt_fcn(features=best_features, model=best_model, feat_show=True)

	print("all_reward: ", all_rewards)
	print("prev_reward_best: ", prev_reward_best)
	return best_reward, all_rewards

def feat_to_run_attempt_fcn(features, model,feat_show=False,Mj_render=False, model_ver=1):
	[q0_filtered, q1_filtered] = feat_to_positions_fcn(features, show=feat_show)
	step_kinematics = positions_to_kinematics_fcn(q0_filtered, q1_filtered, timestep = 0.005)
	attempt_kinematics = step_to_attempt_kinematics_fcn(step_kinematics=step_kinematics)
	est_attempt_activations = estimate_activations(model=model, desired_kinematics=attempt_kinematics)
	[real_attempt_kinematics, real_attempt_activations, chassis_pos]=run_activations(est_attempt_activations, model_ver=model_ver, Mj_render=Mj_render)
	prev_reward = chassis_pos[-1]
	return prev_reward, attempt_kinematics, est_attempt_activations, real_attempt_kinematics, real_attempt_activations

def feat_to_positions_fcn(feature_vector: np.ndarray, timestep = 0.005, cycle_duration = 1.3):

	"""
	Converts a given feature vector to a set of joint angles.

	Parameters
	----------
		* feature_vector: vector of features to be converted to joint angles.
		* timestep: timestep duration in seconds.


	"""


	number_of_features = feature_vector.shape[0]
	each_feature_length =  int(np.round((cycle_duration/number_of_features)/timestep))
	feat_angles = np.linspace(0, 2*np.pi*(number_of_features/(number_of_features+1)), number_of_features)
	q0_raw = feature_vector*np.sin(feat_angles)
	q1_raw = feature_vector*np.cos(feat_angles)
	q0_scaled = (q0_raw*np.pi/3)
	q1_scaled = -1*((-1*q1_raw+1)/2)*(np.pi/2) # since the mujoco model goes from 0 to -pi/2
	q0_scaled_extended = np.append(q0_scaled, q0_scaled[0])
	q1_scaled_extended = np.append(q1_scaled, q1_scaled[0])

	q0_scaled_extended_long = np.array([])
	q1_scaled_extended_long = np.array([])
	for ii in range(feature_vector.shape[0]):
		q0_scaled_extended_long = np.append(
			q0_scaled_extended_long, np.linspace(
				q0_scaled_extended[ii], q0_scaled_extended[ii+1], each_feature_length))
		q1_scaled_extended_long = np.append(
			q1_scaled_extended_long, np.linspace(
				q1_scaled_extended[ii], q1_scaled_extended[ii+1], each_feature_length))
	q0_scaled_extended_long_3 = np.concatenate(
		[q0_scaled_extended_long[:-1], q0_scaled_extended_long[:-1], q0_scaled_extended_long])
	q1_scaled_extended_long_3 = np.concatenate(
		[q1_scaled_extended_long[:-1], q1_scaled_extended_long[:-1], q1_scaled_extended_long])

	fir_filter_length = int(np.round(each_feature_length/(1)))
	b=np.ones(fir_filter_length,)/fir_filter_length # a simple moving average filter > users can 
	#change these if they need smoother pattern
	a=1
	q0_filtered_3 = signal.filtfilt(b, a, q0_scaled_extended_long_3)
	q1_filtered_3 = signal.filtfilt(b, a, q1_scaled_extended_long_3)

	q0_filtered = q0_filtered_3[q0_scaled_extended_long.shape[0]:2*q0_scaled_extended_long.shape[0]-1] # length = 1999 (the 
	#very last was ommited since it is going to be the first one on the next cycle)
	q1_filtered = q1_filtered_3[q1_scaled_extended_long.shape[0]:2*q1_scaled_extended_long.shape[0]-1]
	
	return q0_filtered, q1_filtered

def step_to_attempt_kinematics_fcn(step_kinematics, number_of_steps_in_an_attempt = 10):
	attempt_kinematics=np.matlib.repmat(step_kinematics,number_of_steps_in_an_attempt,1)
	return(attempt_kinematics)

def generate_feature_vector(reward_thresh: float, best_reward: float, feat_min = 0.4, feat_max = 0.9, **kwargs):

	"""
	Generates a feature vector which describes the particular task.
		a) Policy 1 (Exploration): Generate a random feature vector
		b) Policy 2 (Exploitation): Generate a feature vector based on Multivariate Gaussian Distribution Based Stochastic Search
	The feature vector is used to generate the desired kinematics for the attempt.

	Parameters
	----------
		* reward_thresh: the reward threshold that needs to be reached to generate a new feature vector
		* best_reward_so_far: the best reward so far
		* feat_min: the minimum value for the feature vector values
		* feat_max: the maximum value for the feature vector values
		* kwargs: either "best_features_so_far" or "feat_vec_length" needs to be provided

	Returns
	-------
		* new_features: the new feature vector
	"""

	if ("best_features_so_far" in kwargs):
		#save the best feature vector so far if it is provided to apply Multivariate Gaussian Distribution Based Stochastic Search on it
		best_features_so_far = kwargs["best_features_so_far"]
	elif ("feat_vec_length" in kwargs):
		#generate a random feature vector from uniform distribution if the length is provided
		best_features_so_far = np.random.uniform(feat_min, feat_max, kwargs["feat_vec_length"])
	else:
		raise NameError('Either best_features_so_far or feat_vec_length needs to be provided')
	
	#Policy 1 (Exploration Phase): Generate random kinematics data
	if best_reward < reward_thresh:
		new_features = np.random.uniform(feat_min, feat_max, best_features_so_far.shape[0])

	#Policy 2 (Exploitation Phase): Use Multivariate Gaussian Distribution Based Stochastic Search
	else:
		#standard deviation should be inversly proportional to reward and positive
		sigma = np.max([(12 - best_reward) / 100, 0.01])

		#new feature vector
		new_features = np.zeros(best_features_so_far.shape[0],)

		#Iterate over each feature and generate a new feature based on Multivariate Gaussian Distribution Based Stochastic Search
		for i in range(0, len(new_features)):
			new_features[i] = np.random.normal(loc = best_features_so_far[i], scale = sigma)

		#Make sure that the new feature vector is within the bounds defined by feat_min and feat_max
		new_features = np.maximum(new_features, feat_min * np.ones(best_features_so_far.shape[0],))
		new_features = np.minimum(new_features, feat_max * np.ones(best_features_so_far.shape[0],))

	#return the new feature vector
	return new_features

def execute_refinement(model, scalerIn: MinMaxScaler, scalerOut: MinMaxScaler, particular_kinematics: np.ndarray, input_kinematics: np.ndarray, input_activations: np.ndarray, P: np.ndarray, I: np.ndarray, num_refinements = 10, timestep = 0.005):

	"""
	Refines the ANN model by training the model with optimized training data for the particular kinematics.
	We apply reinforcement learning to optimize for the activations of the training data so that the motors don't fight each other while moving the endeffector to the desired position.
	The activations are applied to the motors in a closed loop fashion using a PI controller.

	Parameters
	----------
		* model: The ANN model to be refined
		* scalerIn: The scaler used to scale the input data
		* scalerOut: The scaler used to scale the output data
		* particular_kinematics: The kinematics of the particular task that is used to optimize the training data
		* input_kinematics: The kinematics of the input data (current Training Data)
		* input_activations: The activations of the intput data (current Training Data)
		* P: The P matrix of the PI controller
		* I: The I matrix of the PI controller
		* num_refinements: The number of times the model is refined
		* timestep: The timestep of the experiment
		
	Returns
	-------
		* model: The refined model
		* scalerIn_new: The new scaler used to scale the input data
		* scalerOut_new: The new scaler used to scale the output data
		* cum_kinematics: The kinematics of the input data and the particular kinematics
		* cum_activations: The activations of the input data and the particular kinematics
		* actual_kinematics: The actual kinematics of the testbench after feedback execution
		* actual_activations: The actual activations of the testbench after feedback execution
		* particular_kinematics: The particular kinematics of the experiment
		* errors: The kinematics errors of the model after each refinement
		* average_error: The average error of the model with the input data
	"""

	#Run closed loop execution on testbench to receive the actual kinematics, activations and tendon tensions for RL
	average_error, actual_kinematics, actual_activations, actual_tendon_forces = feedback_execution(model = model, scalerIn = scalerIn, scalerOut = scalerOut, desired_kinematics = particular_kinematics, P = P, I = I)

	# Errors of the model after each refinement
	errors = []

	#Cumuative kinematics and activations
	cum_kinematics = input_kinematics
	cum_activations = input_activations

	#Refinement loop
	for i in range(num_refinements):
		
		#Concatinate the training data with the data collected during the last refinement
		cum_kinematics, cum_activations = concatinate_training_data(prev_kinematics = input_kinematics, prev_activations = input_activations, new_kinematics = actual_kinematics, new_activations = actual_activations)

		#Retrain the model with the new training data and save the new MinMaxScalers
		refined_model, scalerIn_new, scalerOut_new = inverse_mapping(kinematics = cum_kinematics, activations = cum_activations, prior_model = model)

		#Run closed loop execution on testbench to receive the actual kinematics and activations as well as the average error
		average_error_i, actual_kinematics, actual_activations, actual_tendon_forces = feedback_execution(model = refined_model, scalerIn = scalerIn_new, scalerOut = scalerOut_new, desired_kinematics = particular_kinematics, P = P, I = I, timestep = timestep)
		
		#append the average error
		np.append(errors, average_error_i)

	#calculate the average error of the model with the input data
	average_error = np.mean(errors)

	return refined_model, scalerIn_new, scalerOut_new, cum_kinematics, cum_activations, actual_kinematics, actual_activations, particular_kinematics, errors, average_error

def concatinate_training_data(prev_kinematics: np.ndarray, prev_activations: np.ndarray, new_kinematics: np.ndarray, new_activations: np.ndarray, throw_percentage = 0.20):

	"""
	Concatinates data from previous training with new data from refinment phase of g2p

	Parameters
	----------
		* prev_kinematics: kinematics from previous training
		* prev_activations: activations from previous training
		* new_kinematics: kinematics from refinment phase of g2p
		* new_activations: activations from refinment phase of g2p
		* throw_percentage: percentage of data to throw away from the beginning of the new data

	Returns
	-------
		* cum_kinematics: cumulated kinematics
		* cum_activations: cumulated activations
	"""

	size_of_incoming_data = new_kinematics.shape[0]
	samples_to_throw = int(np.round(throw_percentage*size_of_incoming_data))
	prev_kinematics = np.concatenate([prev_kinematics, new_kinematics[samples_to_throw:,:]])
	prev_activations = np.concatenate([prev_activations, new_activations[samples_to_throw:,:]])
	return prev_kinematics, prev_activations

def inverse_mapping(kinematics: np.ndarray, activations: np.ndarray, early_stopping = False, **kwargs):

	"""
	Trains an MLP that maps activations to kinematics (Inverse Mapping).
	If a prior model is passed, the model will be trained on the new data otherwise a new model will be created and trained on the data.
	As shown in colab notebook (TODO: add link) "model 2" performs the best which is why it is used here

	Parameters
	----------
		* kinematics: kinematics numpy array with shape (n_samples, 3)
		* activations: activations numpy array with shape (n_samples, 2)
		* early_stopping: if True, the model will stop training when the validation loss stops decreasing
		* kwargs: prior_model: if a model is passed, the model will be trained on the new data

	Returns
	-------
		* model: the trained model
		* scalerIn: the scaler used to scale the input data
		* scalerOut: the scaler used to scale the output data -> use scalerOut.inverse_transform(model.predict(input)) to get the predicted activations
	"""

	#Scale training data for better performance
	scalerIn = MinMaxScaler()
	scalerOut = MinMaxScaler()
	kinematics_scaled = scalerIn.fit_transform(kinematics)
	activations_scaled = scalerOut.fit_transform(activations)

	#Keep the model if it is passed as an argument
	if ("prior_model" in kwargs):
		model = kwargs["prior_model"]
	#Create a new model when no model is passed
	else:
		model = MLPRegressor(
			hidden_layer_sizes = (50,2),
      		max_iter = 300,
      		solver = "adam",
			activation = "logistic",
			verbose = True,
			warm_start = True,
			early_stopping = early_stopping)

	#train model
	model.fit(kinematics_scaled, activations_scaled)

	#return trained model and MinMaxScaler
	return (model, scalerIn, scalerOut)

def estimate_activations(model, scalerIn: MinMaxScaler, scalerOut: MinMaxScaler, desired_kinematics: np.ndarray):

	"""
	Estimates the activations from the kinematics using the inverse mapping learned by the model.
	
	Parameters
	----------
		* model: the model that maps kinematics to activations
		* scalerIn: the scaler used to scale the input data
		* scalerOut: the scaler used to scale the output data
		* desired_kinematics: the desired kinematics 

	Returns
	-------
		* estimated_activations: the estimated activations to achieve the desired kinematics
	"""

	#scale kinematics
	desired_kinematics_scaled = scalerIn.transform(desired_kinematics)
	#predict activations
	estimated_activations_scaled = model.predict(desired_kinematics_scaled)
	#inverse scaling so that the activations are in the correct range
	estimated_activations = scalerOut.inverse_transform(estimated_activations_scaled)

	#return estimated activations
	return estimated_activations

def generate_p2p_kinematics(low: float, high: float, num_positions: int, position_duration: float, timestep: float):

	"""
	Generating random kinematics for a point to point refinement phase of the g2p task. The angle implies the position of the endeffector.

	Parameters
	----------
		* low: lower bound for random angles
		* high: upper bound for random angles
		* num_positions: number of positions to generate
		* position_duration: duration of holding each angle in seconds
		* timestep: timestep of the test bench

	Returns
	-------
		* random_kinematics: random kinematics for the test bench to follow
	"""

	#calculating number of samples for each position
	num_samples = position_duration / timestep

	#array for storing random kinematics
	random_angles = np.zeros(int(np.round(num_positions * num_samples)),)

	#generating random positions
	for i in range(num_positions):
		#generating random value
		random_value = ((high-low) * (np.random.rand(1)[0])) + low
		#repeat random value for number of samples
		random_value_sampled = np.repeat(random_value, num_samples)
		#fill array with random values in the correct interval as described by num_samples
		random_angles[int(i * num_samples) : int((i+1) * num_samples)] = random_value_sampled

	#calculate kinematics from angles
	random_kinematics = calculate_kinematics(random_angles, timestep = timestep)

	return random_kinematics

def generate_sin_kinematics(attempt_length: int , num_cycles: int, timestep = 0.005):

	"""
	Generating continuous kinematics for the refinement phase of the g2p task. The kinematics are generated by a sine wave.

	Parameters
	----------
		* attempt_length: length of the attempt in seconds
		* num_cycles: number of cycles to complete in the attempt
		* timestep: timestep of the kinematics

	Returns
	-------
		* continuous_kinematics: continuous kinematics for the testbench to follow
	"""

	#calculate the number of samples
	num_samples = int(np.round(attempt_length / timestep))

	#initialize the kinematics vector
	q0 = np.zeros(num_samples)

	#loop through the samples and calculate angles
	for i in range(num_samples):
		q0[i]=(np.pi/3)*np.sin(num_cycles*(2*np.pi*i/num_samples))

	#calculate the kinematics from angles
	continuous_kinematics = calculate_kinematics(angles = q0, timestep = timestep)

	#return the kinematics
	return continuous_kinematics

def calculate_kinematics(angles: np.ndarray, timestep = 0.005):

	"""
	Converting joint angles to kinematics (angle, velocity, acceleration)

	Parameters
	----------
		* angles: angles of joint 0
		* timestep: time between two samples

	Returns
	-------
		* kinematics: kinematics numpy array with shape (n_samples, 3) for joint 0. Each row is a sample and the columns are angle, velocity and acceleration
	"""

	#calculating velocity and acceleration
	angular_velocities = np.gradient(angles) / timestep
	angular_accelerations = np.gradient(angular_velocities) / timestep

	#concatenating kinematics into one array with shape (n_samples, 3) with every row being a sample and the columns being angle, velocity and acceleration
	kinematics = np.concatenate(([[angles], [angular_velocities], [angular_accelerations]]), axis = 0)

	#transposing kinematics
	kinematics = np.transpose(kinematics)

	return kinematics

def calculate_kinematics_error(desired_kinematics: np.ndarray, real_kinematics: np.ndarray, error_type = "RMSE"):

    """
    Calculates the error between desired kinematics and actual kinematics
    Either mean abs value or RMSE

    Parameters
    ----------
        * desired_kinematics: desired kinematics (angle, velocity, acceleration)
        * real_kinematics: real kinematics (angle, velocity, acceleration)
        * error_type: type of error to calculate. Either "MAE" or "RMSE"

    Returns
    -------
        * error: error vector between the two kinematic vectors or -1 if error type not recognized
    """

    #local variables
    num_samples = desired_kinematics.shape[0]

    #initializing error vector for all kinematics sample
    error = np.zero(num_samples)

    for i in range(num_samples):
        if(error_type == "MAE"):
            error[i] = np.mean(np.abs(desired_kinematics[i,:] - real_kinematics[i,:]))
        elif(error_type == "RMSE"):
            error[i] = np.sqrt(np.power(desired_kinematics[i,:]-real_kinematics[i,:],2).mean())
        else:
            print("Error type not recognized")
            error = -1

    return error

##### Feedback Functions #####

def feedback_execution(model, scalerIn: MinMaxScaler, scalerOut: MinMaxScaler, desired_kinematics: np.ndarray, P: np.ndarray, I: np.ndarray, delay_timesteps = 0, timestep = 0.005):

	"""
	Executes desired_kinematics in closed loop with the given model on the testbench

	Parameters
	----------
		* model: pre-trained model from motor babbling
		* scalerIn: scaler for input data
		* scalerOut: scaler for output data
		* desired_kinematics: desired kinematics for the joints
		* P: proportional gain for each joint
		* I: integral gain for each joint
		* delay_timesteps: delay between desired and actual kinematics
		* timestep: timestep of the curent kinematics

	Returns
	-------
		* average_kinematics_error: average error of the joint kinematics
		* actual_kinematics: real kinematics of the joint
		* actual_activations: real activations of motors [flex, extend]
		* actual_tendon_forces: real tendon forces of the motor tendons [flex, extend]
	"""

	#estimate activations for desired kinematics. These will be the initial activations which will be corrected in the feedback loop
	est_activations = estimate_activations(model = model, scalerIn = scalerIn, scalerOut = scalerOut,  desired_kinematics = desired_kinematics)

	#number of task samples
	num_samples = desired_kinematics.shape[0]
	#initialize input kinematics vector
	input_kinematics = np.zeros(desired_kinematics.shape)
	#initialize actual angles vector
	actual_angles = np.zeros([num_samples,1])
	#initialize actual activations vector
	actual_activations = np.zeros([num_samples,2])
	#initialize actual kinematics vector
	actual_kinematics = np.zeros([num_samples,1])
	#initialize actual tendon forces vector
	actual_tendon_forces = np.zeros([num_samples,2])
	#initialize cumulative error vector
	q_error_cum = np.zeros([num_samples,1])
	#defines how many timesteps (samples) we need to look back to calculate the gradient with feedback
	gradient_edge_order = 1

	#calculate activations based on kinematics with feedback for every sample in a feedback loop
	for i in range(num_samples):

		#input kinematics = desired_kinematics for sample i when no feedback is available yet at beginning
		if i < max(gradient_edge_order, delay_timesteps + 1):
			input_kinematics[i,:] = desired_kinematics[i,:]

		#calculate input kinematics for sample i with respect to feedback of previous sample
		else:
			[input_kinematics[i,:], q_error_cum] = calculate_input_kinematics(
				step_number = i,
				actual_angles = actual_angles,
				desired_kinematics = desired_kinematics,
				q_error_cum = q_error_cum,
				P = P,
				I = I,
				delay_timesteps = delay_timesteps,
				gradient_edge_order = gradient_edge_order,
				timestep = timestep)

		#update estimated activations after feedback. The input kinematics has been updated with the feedback
		est_activations[i,:] = estimate_activations(model = model, scalerIn = scalerIn, scalerOut = scalerOut, desired_kinematics = [input_kinematics[i,:]])[0,:]

		#Execute the estimated activations on the testbench and save the actual kinematics, activations and tendon forces as feedback for the next timestep
		actual_kinematics[i,:], actual_activations[i,:], actual_tendon_forces[i,:] = run_activations(activations = est_activations[i,:], timestep = timestep)

		#save actual angles for feedback
		actual_angles[i,:] = actual_kinematics[i,0]

	#calculate error for every joint and average error over all joints (here only one joint)
	kinematics_errors = calculate_kinematics_error(desired_kinematics[:,0], actual_kinematics[:,0], error_type = "RMSE")
	average_kinematics_error = np.mean([kinematics_errors])

	return average_kinematics_error, actual_kinematics, actual_activations, actual_tendon_forces

def calculate_input_kinematics(step_number: int, actual_angles: np.ndarray, desired_kinematics: np.ndarray, q_error_cum: np.ndarray, P: np.ndarray, I: np.ndarray, delay_timesteps: int, gradient_edge_order = 1, timestep = 0.005):

    """
    PI controller like function that calculates K_p * error + K_i * integral(error).
    This returns the input kinematics for the next timestep

    Parameters
    ----------
        * step_number: current timestep
        * actual_angle: actual angle of the joint at current timestep
        * desired_kinematics: desired kinematics of the joint at current timestep
        * q_error_cum: cumulative error of the joint at current timestep
        * P: proportional gain for each joint
        * I: integral gain for each joint
        * delay_timesteps: delay between desired and actual kinematics
        * gradient_edge_order: defines how many timesteps we need to look back to calculate the gradient with feedback
        * timestep: duration of each timestep in seconds

    Returns
    -------
        * input_kinematics: input kinematics for the next timestep
        * q_error_cum: cumulative error of the joint
    """

    #desired kinematics (angle and velocity) stacking together kinematcis of every joint (for now only one joint)
    q_desired =  desired_kinematics[step_number, np.ix_([0])][0]
    q_dot_desired = desired_kinematics[step_number, np.ix_([1])][0]

    #calculating errors between desired and actual angles using feedback from previous timestep
    q_plant = actual_angles[step_number - gradient_edge_order - delay_timesteps, :]
    q_error = q_desired - q_plant
    q_error_cum[step_number, :] = q_error

    #Implementing PI controller (K_p * error + K_i * integral(error)) to adapt the input velocity
    q_dot_in = q_dot_desired + P * q_error + I * (q_error_cum.sum(axis = 0) * timestep)

    #calculating input angle and acceleration
    q_in = q_desired
    q_double_dot_in = calculate_kinematics(q_0 = q_in, timestep = timestep)[-1]
    #q_double_dot_in = [np.gradient(desired_kinematics[step_number - gradient_edge_order:step_number + 1, 1], edge_order = gradient_edge_order)[-1] / timestep]

    input_kinematics = [q_in[0], q_dot_in[0], q_double_dot_in[0]]
    
    return input_kinematics, q_error_cum


#### Refinement Functions ####

def refine(model, scalerIn: MinMaxScaler, scalerOut: MinMaxScaler, babbling_kinematics: np.ndarray, babbling_activations: np.ndarray, P: np.ndarray, I: np.ndarray, num_refinements = 10, timestep = 0.005):

	"""
	Refines the ANN model by collecting more training data that is optimized for tendon force so that the motors don't fight each other while achiving predefined kinematic tasks.
	In this case the task is to move the endeffector precisely according to the RL Experiments:
		a) P2P: The endeffector is moved to random non consecutive positions
		b) sin: The endeffector is moved to consecutive positions that are a sin function of time
	The optimized Training data is then used to refine the model. #TODO: Maybe completly retrain the model with the optimized data instead of refining it. -> Test
	
	Please note: The idea to combine both RL experiments is what I came up with. In case it will worsen the performance we can just use one of them -> Probably the P2P experiment.
	Just recently I realized that we need to optimize the training data itself which is why apply the Reinforcement Learning to the motor activations in order to achive less tendon force and not to the kinematics.

	Parameters
	----------
		* model: The ANN model to be refined
		* scalerIn: The scaler for the input data
		* scalerOut: The scaler for the output data
		* babbling_kinematics: The kinematics of the babbling data
		* babbling_activations: The activations of the babbling data
		* P: The P matrix of the PI Controller
		* I: The I matrix of the PI Controller
		* num_refinements: The number of times the model is refined
		* timestep: The duration of one timestep in seconds
		
	Returns
	-------
		* refined_model: The refined model refined after both RL experiments
		* errors: The kinematics errors of the model after each refinement
		* cum_kinematics: The kinematics of the babbling data and the data collected during the refinements
		* cum_activations: The activations of the babbling data and the data collected during the refinements
	"""

	# Refine the model by optimizing data from the P2P experiment for less tendon force
	p2p_refined_model, scalerIn_p2p, scalerOut_p2p, errors, cum_kinematics, cum_activations = refine_p2p_task(model = model, scalerIn = scalerIn, scalerOut = scalerOut, input_kinematics = babbling_kinematics, input_activations = babbling_activations, P = P, I = I, num_refinements = num_refinements, timestep = timestep)

	# Refine the p2p refined model by optimizing data from the sin experiment for less tendon force
	refined_model, scalerIn_sin, scalerOut_sin, errors, cum_kinematics, cum_activations = refine_sin_task(model = p2p_refined_model, scalerIn = scalerIn_p2p, scalerOut = scalerOut_p2p, input_kinematics = cum_kinematics, input_activations = cum_activations, P = P, I = I, num_refinements = num_refinements, timestep = timestep)

	# Return the refined model with the optimized data from both experiments
	return refined_model, scalerIn_sin, scalerOut_sin, errors, cum_kinematics, cum_activations

def refine_p2p_task(model, scalerIn: MinMaxScaler, scalerOut: MinMaxScaler, input_kinematics: np.ndarray, input_activations: np.ndarray, P: np.ndarray, I: np.ndarray, num_refinements = 10, timestep = 0.005):

	"""
	Refines the ANN model by collecting optimized training data that is particlar to the task of Point to Point movement before training the model with the newly generated and optimized data.
	In this case the task is to move the endeffector precisely to random non consecutive positions.

	Parameters
	----------
		* model: The ANN model to be refined
		* input_kinematics: The kinematics of the input data
		* input_activations: The activations of the intput data
		* P: The P matrix of the PI controller
		* I: The I matrix of the PI controller
		* num_refinements: The number of times the model is refined
		* timestep: The timestep of the experiment
		
	Returns
	-------
		* model: The refined model
		* scalerIn: The scaler for the input data
		* scalerOut: The scaler for the output data
		* errors: The kinematics errors of the model after each refinement
		* cum_kinematics: The kinematics of the input data and the data collected during the refinement
		* cum_activations: The activations of the input data and the data collected during the refinement
	"""

	# Generate random non continuous kinematics for point to point experiment
	particular_kinematics = generate_p2p_kinematics(low = -(np.pi / 3), high = np.pi / 3, num_positions = 10, position_duration = 2.5, timestep = timestep)

	# Execute refinement with the particular kinematics to optimize the training data
	refined_model, scalerIn_new, scalerOut_new, errors, cum_kinematics, cum_activations = execute_refinement(model = model, scalerIn = scalerIn, scalerOut = scalerOut, particular_kinematics = particular_kinematics, input_kinematics = input_kinematics, input_activations = input_activations, P = P, I = I, num_refinements = num_refinements)

	# Return the refined model with the optimized data from the P2P experiment
	return refined_model, scalerIn_new, scalerOut_new, errors, cum_kinematics, cum_activations

def refine_sin_task(model, scalerIn: MinMaxScaler, scalerOut: MinMaxScaler, input_kinematics: np.ndarray, input_activations: np.ndarray, P: np.ndarray, I: np.ndarray, num_refinements = 10, timestep = 0.005):

	"""
	Refines the ANN model by collecting more training data that is particlar to the task of sin movements befor training the model with the newly generated and optimized data.
	In this case the task is to move the endeffector precisely to consecutive positions that are a sin function of time

	Parameters
	----------
		* model: The ANN model to be refined
		* scalerIn: The scaler used to scale the input data
		* scalerOut: The scaler used to scale the output data
		* input_kinematics: The kinematics of the input data
		* input_activations: The activations of the input data
		* P: The P matrix of the PI Controller
		* I: The I matrix of the PI Controller
		* num_refinements: The number of times the model is refined
		* timestep: The duration of one timestep in seconds
		
	Returns
	-------
		* model: The refined model
		* scalerIn: The scaler for the input data
		* scalerOut: The scaler for the output data
		* errors: The kinematics errors of the model after each refinement
		* cum_kinematics: The kinematics of the input data and the data collected during the refinement
		* cum_activations: The activations of the input data and the data collected during the refinement
	"""

	# Generate continuous sin kinematics for sin experiment
	particular_kinematics = generate_sin_kinematics(attempt_length = 10, num_cycles = 7 )

	# Execute refinement with the particular kinematics to optimize the training data
	refined_model, scalerIn_new, scalerOut_new, errors, cum_kinematics, cum_activations = execute_refinement(model = model, scalerIn = scalerIn, scalerOut = scalerOut, particular_kinematics = particular_kinematics, input_kinematics = input_kinematics, input_activations = input_activations, P = P, I = I, num_refinements = num_refinements)

	# Return the refined model with the optimized data from the Sin experiment
	return refined_model, scalerIn_new, scalerOut_new, errors, cum_kinematics, cum_activations