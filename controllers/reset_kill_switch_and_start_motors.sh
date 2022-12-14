
# Source bench msg types
. ~/roboy_team_ws22/w22-test-bench/catkin_ws/devel/setup.bash
# The kill switch is set on startup so it need to be reseted.
rostopic pub /test_bench/BenchMotorControl bench/BenchMotorControl "{reset_kill_switch: true}" -1
# The motors are stopped when the kill switch is set, so start them after resetting the kill switch.
rostopic pub /test_bench/BenchMotorControl bench/BenchMotorControl "{flex_myobrick_start: true, extend_myobrick_start: true}" -1
# Test the motors, this command will make the joint flex. A watchdog sets the motor pwm to 0 after 0.5 seconds the last pwm command.