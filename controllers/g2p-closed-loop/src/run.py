import numpy as np
import sklearn
import rospy

def run_activations(activations: np.ndarray, timestep: int):

	"""
	Running activations on test bench

	Parameters
	----------
		* activations: activations to run on test bench
		* timestep: duration of each timestep in seconds

	Returns
	-------
		* actual_kinematics: kinematics resulting from given activations
		* actual_activations: activations that were run on test bench
		* actual_tendon_forces: tendon forces that were measured on test bench
	"""

	#number of activations
	num_activations = activations.shape[0]

	#actual angles of test bench joint
	actual_angles = np.zeros((num_activations,1))

	#actual tendon forces of test bench tendons (felx, extend)
	actual_tendon_forces = np.zeros((num_activations,2))

	#actual activations of test bench motors (felx, extend)
	actual_activations = np.zeros((num_activations,2))

	#iterate over activations and run test bench with it
	for i in range(num_activations):

		#TODO: Send activation to test bench
		#Here we would run the test bench with the activation
		#Check Nils code for how to do that
		#Current problem: Motors are not backdrivable -> How can we avoid tendon slackness? Valero Lab had backdrivable motors

		msg = BenchMotorControl()
		msg.flex_myobrick_pwm = activations[i,0]
		msg.extend_myobrick_pwm = activations[i,1]
		publisher.publish(msg)

		#appending positions and activations to arrays
		actual_angles[i,:] = 0 # Todo get angle from test bench

		pass

	#calculate kinematics from angles
	actual_kinematics = calculate_kinematics(angles = actual_angles, timestep = timestep)

	return actual_kinematics, actual_activations, actual_tendon_forces