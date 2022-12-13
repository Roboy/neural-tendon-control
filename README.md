# Joint test bench

# SW

## Bench node

### Desc

The bench node acts a middle layer between the hardware and the controller. It's tasks are:

- Initilization of motors and sensors after system startup.
- Protecting the hardware from overload by overriding controller.
- Recording variables and saving the dataset to a file.
- Exposing a standardised interface to controller via ROS topics.
- Setting different load scenarios by controlling "Load control MyoBrick"

### How to start
1. Power up:
    - power supply
    - fpga computer
    - prophet computer
2. Connect to Roboy wifi.
3. Start ROS master on prophet computer
    ```
    roscore
    ```
4. Start ROS slave on fpga computer
    ```
    ./roboy_plexus pinky.yaml
    ```
5. Activate roboy conda envireonment on prophet
    ```
    activate_conda
    ```
6. Start bench program
    ```
    cd ~/roboy_team_ws22/w22-test-bench/catkin_ws
    python ./bench_main.py
    ```
    

### ROS topics
- /test_bench/BenchMotorControl
  - float32 flex_myobrick_pwm
  - float32 extend_myobrick_pwm
  - bool flex_myobrick_start
  - bool extend_myobrick_start
  - bool reset_kill_switch 
  - bool press_kill_switch
- /test_bench/BenchState
  - float32 angle
  - bool safety_switch_pressed
  - float32 flex_myobrick_pos_encoder
  - float32 flex_myobrick_torque_encoder
  - float32 flex_myobrick_current
  - float32 flex_myobrick_pwm
  - bool flex_myobrick_in_running_state
  - float32 extend_myobrick_pos_encoder
  - float32 extend_myobrick_torque_encoder
  - float32 extend_myobrick_current
  - float32 extend_myobrick_pwm
  - bool extend_myobrick_in_running_state


## Controller node

### Desc

The controller node controls the angle of the joint by reading and writing to the different ROS topics exposed by the bench node. The controller node itself exposes a ROS topic interface for setting waypoints.

## Evaluation node

### Desc

The evaluation node sends waypoints to the controller node and evaluates it's performance.




# HW

## Connection diagram

<p align="center">
<img src="./misc/docs/connections_setup.png" alt="drawing" width="700"/>
</p>

## Mechanical setup

<p align="center">
<img src="./misc/docs/mechanical_setup.png" alt="drawing" width="500"/>
</p>

