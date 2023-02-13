

# phony targets
.PHONY: run_evaluator observe_bench_state observe_controller_next_waypoints observe_bench_motor_control start_controller start_bench start_motors reset_kill_switch start_myobricks

SHELL := /bin/bash

run_evaluator:
	@echo "Running evaluator..."
	@cd evaluator; \
	python3 main.py ./eval_paths/validation_run.csv


observe_bench_state:
# Source bench msg types
	source ~/roboy_team_ws22/w22-test-bench/catkin_ws/devel/setup.bash; \
	rostopic echo /test_bench/BenchState

observe_controller_next_waypoints:
	source ~/roboy_team_ws22/w22-test-bench/catkin_ws/devel/setup.bash; \
	rostopic echo /controller/NextWaypoints

observe_bench_motor_control:
	source ~/roboy_team_ws22/w22-test-bench/catkin_ws/devel/setup.bash; \
	rostopic echo /test_bench/BenchMotorControl

start_controller:
	@echo "Running controller..."
	@cd controllers/base_line; \
	python3 main.py

start_bench:
	@echo "Starting bench..."
	@cd ~/roboy_team_ws22/w22-test-bench/bench; \
	python ./bench_main.py

start_motors:
	@echo "Starting motors..."
	@cd ~/roboy_team_ws22/w22-test-bench/controllers/misc; \
	python ./bench_main.py --start_motors


reset_kill_switch:
	source ~/roboy_team_ws22/w22-test-bench/catkin_ws/devel/setup.bash; \
	rostopic pub /test_bench/BenchMotorControl bench/BenchMotorControl "{reset_kill_switch: true}" -1

start_myobricks:
	source ~/roboy_team_ws22/w22-test-bench/catkin_ws/devel/setup.bash; \
	rostopic pub /test_bench/BenchMotorControl bench/BenchMotorControl "{flex_myobrick_start: true, extend_myobrick_start: true}" -1
