import rospy
import threading
import time

from bench.msg import BenchState, BenchMotorControl, BenchRecorderControl


class TickLoop:
    def __init__(self,
            angel_sensor,
            myobrick_flex,
            myobrick_extend,
            safety_observer,
            control_listener,
            freq,
        ):
        self.angel_sensor = angel_sensor
        self.myobrick_flex = myobrick_flex
        self.myobrick_extend = myobrick_extend
        self.safety_observer = safety_observer
        self.control_listener = control_listener

        # Setup message event callback
        self.pub = rospy.Publisher('/test_bench/BenchState', BenchState, queue_size=10)

        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._loop)

        self.stop_event = threading.Event()

        self.freq = freq
        self.tick = 0

    def _loop(self):
        time_to_sleep = 0
        while not self.stop_event.is_set():

            # Start loop timer
            t_0 = time.time()

            msg = BenchState()
            msg.tick = self.tick

            # Get current tick internal and output variables
            msg.angle = self.angel_sensor.get_value()

            msg.safety_switch_pressed = self.safety_observer.get_kill_switch_state()

            flex_state_dict = self.myobrick_flex.get_state()

            msg.flex_myobrick_pos_encoder = flex_state_dict['pv_pos_encoder']
            msg.flex_myobrick_torque_encoder = flex_state_dict['pv_torque_encoder']
            msg.flex_myobrick_current = flex_state_dict['pv_current']
            msg.flex_myobrick_pwm = self.myobrick_flex.sp_pwm
            msg.flex_myobrick_in_running_state = self.myobrick_flex.is_running

            extend_state_dict = self.myobrick_extend.get_state()

            msg.extend_myobrick_pos_encoder = extend_state_dict['pv_pos_encoder']
            msg.extend_myobrick_torque_encoder = extend_state_dict['pv_torque_encoder']
            msg.extend_myobrick_current = extend_state_dict['pv_current']
            msg.extend_myobrick_in_running_state = self.myobrick_extend.is_running

            t_1 = time.time()

            # Get current tick input
            input_msg = self.control_listener.get_input(self.tick)

            t_2 = time.time()

            # Set current tick output
            if input_msg is not None:
                self.myobrick_flex.set_pwm(input_msg.flex_myobrick_pwm)
                self.myobrick_extend.set_pwm(input_msg.extend_myobrick_pwm)
                msg.flex_myobrick_pwm = input_msg.flex_myobrick_pwm
                msg.extend_myobrick_pwm = input_msg.extend_myobrick_pwm
            else :
                self.myobrick_flex.set_pwm(0)
                self.myobrick_extend.set_pwm(0)
                msg.flex_myobrick_pwm = 0
                msg.extend_myobrick_pwm = 0

            t_3 = time.time()

            # Publish tick variables
            self.pub.publish(msg)

            t_4 = time.time()

            # Increment tick
            self.tick += 1

            # Sleep until next tick
            time_to_sleep = 1/self.freq - (time.time() - t_0)
            if time_to_sleep < 0:
                time_to_sleep = 0
                print('tick loop is too slow')
                print('time to get state: ', t_1 - t_0)
                print('time to get input: ', t_2 - t_1)
                print('time to set output: ', t_3 - t_2)
                print('time to publish: ', t_4 - t_3)
            time.sleep(time_to_sleep)
        print('last time to sleep: ', time_to_sleep)


    def start(self):
        self.thread.start()

    def terminate(self):
        self.stop_event.set()
        self.thread.join()