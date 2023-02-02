import time
import rospy
import csv
import pandas as pd
import threading
import asyncio
import argparse
from bokeh.plotting import figure, output_file, save
import os
import json

from waypoints_sender import WaypointsSender
from bench_observer import BenchObserver

import sys
sys.path.append("../catkin_ws/devel/lib/python3/dist-packages")


from ros_loop import RosLoop



def run_evaluator_node():
    print("Starting controller node.")


    # Init ros loop thread
    print('Init ROS loop.')
    ros_loop = RosLoop()


    # Use argparse to get --name argument, if not specified, use None
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, default=None)
    parser.add_argument('--name', type=str, default=None)
    args = parser.parse_args()

    path_to_csv_file = args.path


    print('Reading path from: ' + path_to_csv_file)
    # Read file as pandas dataframe
    waypoints_df = pd.read_csv(path_to_csv_file)

    
    # Init bench observer
    print('Init bench observer.')
    bench_observer = BenchObserver()


    # Init waypoint sender
    print('Init waypoint sender.')
    waypoints_sender = WaypointsSender(waypoints_df)


    # Start ROS loop
    print('Starting ROS loop.')
    ros_loop.start()


    # Start sending waypoints
    print('Starting sending waypoints.')
    waypoints_sender.start()


     # Run until keyboard interrupt
    print('Press q then enter to quit.')
    while True:
        key = sys.stdin.read(1)

        # Check if the user pressed "q"
        if key == "q":
            print("q was pressed")
            break

    waypoints_sender.terminate()


    # Terminating ROS loop
    print('Terminating controller ROS loop.')
    ros_loop.stop()




    run_name = args.name
    # If --name argument is specified, save results to csv file
    if run_name is None:
        # Set to current date
        run_name = time.strftime("%Y-%m-%d_%H-%M-%S")
    

    # Get the file name for path_to_csv_file and drop the extension
    path_file_name = path_to_csv_file.split('/')[-1].split('.')[0]
    
    # Check if a outpit folder exists with that name in ./outputs, if not create it
    output_folder = './outputs/' + path_file_name
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Check if therese exsists a json dile names (path_file_name).json, if not create it
    json_file_path = output_folder + '/' + path_file_name + '.json'
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as f:
            f.write('{}')

    # Write results to the JSON file
    print('Writing results to json file.')
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        data[run_name] = {
            'run_name' : run_name,
            'date' : time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    


    # Print results
    print('Printing results.')
    bench_observer.get_recorded_bench_state().to_csv(f'{output_folder}/{run_name}_bench_states.csv')
    waypoints_sender.get_sent_waypoints().to_csv(f'{output_folder}/{run_name}_waypoints.csv')

    # Save results to bokeh hmtl file
    print('Saving results to bokeh html file.')
    output_file(filename=f"{output_folder}/{run_name}.html", title=run_name)

    # full screen
    p = figure(title="Run", x_axis_label='time', y_axis_label='angle', width=1400, height=900)
    p.line(bench_observer.get_recorded_bench_state()['timestamp'], bench_observer.get_recorded_bench_state()['angle'], legend_label="bench angle", line_width=2, line_color="blue")
    p.line(waypoints_sender.get_sent_waypoints()['timestamp'], waypoints_sender.get_sent_waypoints()['angle'], legend_label="waypoint angle", line_width=2, line_color="red")
    save(p)





if __name__ == "__main__":
    print("Starting evaluator node.")

    run_evaluator_node()


    print("evaluator node exited.")

