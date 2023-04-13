# Test bench
The test bench is a development platform for trying out different control algorithms for tendon driven robots. It was specifically design to enable

- fast iterations of different control algorithms for faster development cycles,
- a safe environment for testing control algorithms by adding additional safety mechanisms,
- not risking breaking the high cost Roboy when trying out novel techniques,
- a good learning stepping stone by letting the user get a feel for ROS in a relatively simple system.


More documentation can be found at https://devanthro.atlassian.net/wiki/spaces/WS2223/pages/2739437602/NTC+Documentation

# Installation

1. Clone this repository
    
    ```bash
    git clone git@github.com:Roboy/neural-tendon-control.git
    ```
    
2. Create a new python environment 
    
    ```bash
    conda create --name roboy python
    ```
    
3. Activate the new python environment
    
    ```bash
    conda activate roboy
    ```
    
4. Install python dependencies
    
    ```bash
    conda install -c conda-forge ros-rospy
    pip3 install torch
    conda install numpy
    conda install matplotlib
    ```
    
# Build

Build the catkin workspace by

1. Navigate to the catkin_ws directory in the repo's root directory
    
    ```bash
    cd ./neural-tendon-control/catkin_ws
    ```
    
2. Build
    
    ```bash
    catkin_make
    ```
    
3. Source the newly built workspace to your environment
    
    ```bash
    source ./neural-tendon-control/catkin_ws/devel/setup.bash
    ```
    

To change or add new ROS messages in the workspace, follow these steps:

1. Add the new message files in the directory `./catkin_ws/src/[package_name]/msg`. Message files needs to end with `.msg` and follow the ROS syntax. Example:
    
    ```
    float32 angle
    float32 flex_myobrick_pwm
    bool flex_myobrick_in_running_state
    ```
    
2. Add the new message file names to the CMakeLists.txt file
    
    ```bash
    vi ./neural-tendon-control/catkin_ws/src/[package_name]/CMakeLists.txt
    ```
    
    This is how it can look like:
    
    ```
    add_message_files(
      FILES
      BenchState.msg
      BenchMotorControl.msg
      BenchRecorderControl.msg
    )
    ```
    
3. Rebuild the package by running `catkin_make` in the workspace directory.
    
    ```bash
    cd /neural-tendon-control/catkin_ws
    catkin_make
    ```
    
4. Source newly built workspace to your environment
    
    ```bash
    source ./neural-tendon-control/catkin_ws/devel/setup.bash
    ```
    
5. The msg type should now be visible when running rosmsg list
    
    ```python
    rosmsg list | grep [package_name]
    ```
    
6. Use them in python by adding the path to generated modules
    
    For example:
    
    ```python
    import sys
    sys.path.append("../catkin_ws/devel/lib/python3/dist-packages")
    
    # Change bench to the package name and BenchState to the message file name
    from bench.msg import BenchState
    ```

# Nodes and their usage

## Bench node

### Description

The bench node acts as a middle layer between the hardware and the controller along with the rest of the ROS nodes that need to communicate with the MyoBricks and angle sensor. Its tasks are:

- initialization of motors and sensors after system startup to put them in the correct configuration,
- protect the hardware by making sure the joint is operating within safe limits,
- set the system into a safe state if a controller malfunction is detected,
- expose a standardized interface to the sensors and actuators for the different controllers and other nodes via ROS topics.

### Usage

Before starting the bench node, make sure that

1. you have started the ROS master service by running the command
    
    ```bash
    roscore
    ```
    
2. You have applied 24 V to the MyoBricks.
3. You have powered up the FPGA single board computer and started the pinky ROS node on it by running the command
    
    ```bash
    # This command should be run on the FPGA computer board
    ./roboy_plexus pinky.yaml
    ```
    

When you have completed the previous steps you are ready to start the actual bench node. Do this by:

1. Enable the “roboy” python environment
    
    ```bash
    conda activate roboy
    ```
    
2. Run the bench node program
    
    ```bash
    cd ~/roboy_team_ws22/w22-test-bench/bench
    python ./bench_main.py
    ```
    
    Change the bench node root folder path to your own.
    
3. For safety reasons, the bench node is started with both MyoBricks in a stopped state. To activate them, run the following script
    
    ```bash
    # Activate robot python environment
    conda activate roboy
    # Navigate to the repo directroy
    cd ~/roboy_team_ws22/w22-test-bench/
    # Run the controller that resets the kill switch and activates the motors
    ./controllers/misc/reset_kill_switch_and_start_motors.sh
    ```
    
    The MyoBricks needs to be restarted each time the bench goes into safe mode. This is a safety mechanism and can happen for example if the joint goes out of range.
    

To stop the controller, simply press q followed by enter. This will quit the system in a safe manner and set the PWM of the MyoBricks to zero before closing.

### Location within repo

The source code for the bench node is located in `neural-tendon-control/bench/`.

### ROS interface

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


## Data recorder node

### Description

The data recorder records the state of the bench to a specified CSV file.

### Usage

Before you start the data recorder node, make sure that the bench node is running properly. When the bench node is running, you can start the recorder node by:

1. Activate the “roboy” python environment
    
    ```bash
    conda acivate python
    ```
    
2. Run the data recorder program. Change the `recorded_data.csv` to any path you want the data recorder to save to. If the file already exists, the data recorder will append new rows at the bottom of the file and not override it.
    
    ```bash
    cd ~/roboy_team_ws22/w22-test-bench/data_recorder
    python ./data_recorder.py ./recorded_data.csv
    ```
    
3. To stop recording of data, simply hit `Ctrl+C`.

### Location within repo

The source code for the data recorded node is located in `neural-tendon-control/data_recorded/`.

### CSV file format

- timestamp
- angle
- safety_switch_pressed
- flex_myobrick_pos_encoder
- flex_myobrick_torque_encoder
- flex_myobrick_current
- flex_myobrick_pwm
- flex_myobrick_in_running_state
- extend_myobrick_pos_encoder
- extend_myobrick_torque_encoder
- extend_myobrick_current
- extend_myobrick_pwm
- extend_myobrick_in_running_state

## Controller node

### Description

The controller node controls the angle of the joint by reading and writing to the different ROS topics exposed by the bench node.

Example of available controllers:

- controllers/misc/babble.py
    
    Makes the joint babble up and down.
    
- controllers/misc/go_to_middle_pos.py
    
    Makes the joint go to the middle position, then exits.
    
- controllers/misc/go_up_and_down.py
    
    Makes the joint go up and down full range until once presses CTRL+C, then exits.
    
- controllers/misc/reset_kill_switch_and_start_motors.sh
    
    Resets the kill switch and starts the motors, then exits.
    
- controllers/nn_follow_sinus/main.py
    
    Makes the joint go up and down in a sinus motion based on the MPC technique.
    
- controllers/g2p-closed-loop/src/main.py
    
    Implementation of the closed loop g2p controller approach.
    

### Usage

The usage of the controller node depends how the controller is implemented. However, all controllers needs to be able to talk the the bench node so make sure the bench node is running before starting a controller.

To start the “babble controller”, run:

```bash
conda activate roboy
python ./controllers/misc/babble.py
```

To run the “nn follow sinus controller”, run:

```bash
conda activate roboy
python ./controllers/nn_follow_sinus/main.py
```

### Location within repo

The source for the controller nodes are located in `neural-tendon-control/controllers/`.




