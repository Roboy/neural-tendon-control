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
            freq = 20
        ):
        self.angel_sensor = angel_sensor
        self.myobrick_flex = myobrick_flex
        self.myobrick_extend = myobrick_extend
        self.safety_observer = safety_observer

        # Setup message event callback
        self.pub = rospy.Publisher('/test_bench/BenchState', BenchState, queue_size=10)

        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._loop)

        self.stop_event = threading.Event()

        self.freq = freq
        self.tick = 0

    def _loop(self):
        while not self.stop_event.is_set():

            # Start loop timer
            start_loop_time = time.time()

            msg = BenchState()
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
            msg.extend_myobrick_pwm = self.myobrick_extend.sp_pwm
            msg.extend_myobrick_in_running_state = self.myobrick_extend.is_running


            # Get current tick input

            # Set current tick output
            # self.myobrick_flex.set_pwm(msg.flex_myobrick_pwm)
            # self.myobrick_extend.set_pwm(msg.extend_myobrick_pwm)


            # Broadcast current tick variables
            self.pub.publish(msg)

            # Increment tick
            self.tick += 1

            # Sleep until next tick
            time.sleep(1/self.freq - (time.time() - start_loop_time))

    def start(self):
        self.thread.start()

    def terminate(self):
        self.stop_event.set()
        self.thread.join()