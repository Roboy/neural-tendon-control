# Joint test bench

# SW

## Bench node

The bench node acts a middle layer between the hardware and the controller. It's tasks are:

- Initilization of motors and sensors after system startup.
- Protecting the hardware from overload by overriding controller.
- Recording variables and saving the dataset to a file.
- Exposing a standardised interface to controller via ROS topics.
- Setting different load scenarios by controlling "Load control MyoBrick"

## Controller node

The controller node controls the angle of the joint by reading and writing to the different ROS topics exposed by the bench node. The controller node itself exposes a ROS topic interface for setting waypoints.

## Evaluation node

The evaluation node sends waypoints to the controller node and evaluates it's performance.


## ROS topics
- /bench/

# HW

## Connection diagram

<p align="center">
<img src="./misc/docs/connections_setup.png" alt="drawing" width="700"/>
</p>

## Mechanical setup

<p align="center">
<img src="./misc/docs/mechanical_setup.png" alt="drawing" width="500"/>
</p>

