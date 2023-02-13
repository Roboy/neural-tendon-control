#!/bin/bash

# Source bench msg types
source ~/roboy_team_ws22/w22-test-bench/catkin_ws/devel/setup.bash
# The kill switch is set on startup so it need to be reseted.
rostopic pub -1 /test_bench/BenchMotorControl bench/BenchMotorControl "{reset_kill_switch: true}"
# The motors are stopped when the kill switch is set, so start them after resetting the kill switch.
rostopic pub -1 /test_bench/BenchMotorControl bench/BenchMotorControl "{flex_myobrick_start: true, extend_myobrick_start: true}"
