
import threading
import subprocess
import rospy
from roboy_middleware_msgs.msg import MotorState, MotorCommand

class Watchdog:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback
        self.timer = None
        self.process = None

    def start(self):
        self.process = threading.Thread(target=self.run)
        self.process.start()

    def run(self):
        self.timer = threading.Timer(self.timeout, self.callback)
        self.timer.start()

    def stop(self):
        if self.timer and self.timer.is_alive():
            self.timer.cancel()

        if self.process and self.process.is_alive():
            self.process.join()

    def reset(self):
        self.stop()
        self.start()


class MyoBrick:
    def __init__(self, motor_id):
        self.motor_id = motor_id

        # Set motor to pwm mode
        subprocess.check_call("./set_control_mode.sh %s" % (str(motor_id)), shell=True)

        # Setup message event callback
        self.subscriber = rospy.Subscriber('/roboy/pinky/middleware/MotorState', MotorState, self._on_motor_state_callback)
        self.publisher = rospy.Publisher('/roboy/pinky/middleware/MotorCommand', MotorCommand, queue_size=10)
        self.motor_state_lock = threading.Lock()

        # motor state variables
        self.pv_pos_encoder = 0
        self.pv_torque_encoder = 0
        self.pv_current = 0
        self.sp_pwm = 0

        # Start watchdog
        self.wd = Watchdog(0.5, self._set_pwm_watchdog_callback)

        self.is_running = False

    def _on_motor_state_callback(self, msg):
        with self.motor_state_lock:
            #self.motor_state = msg
            self.pv_pos_encoder = msg.encoder0_pos[self.motor_id]
            self.pv_torque_encoder = msg.displacement[self.motor_id]
            self.pv_current = msg.current[self.motor_id]

    def _set_pwm_watchdog_callback(self):
        self.set_pwm(0)

    def set_pwm(self, pwm):
        if not self.is_running:
            return

        self.wd.reset()
        msg = MotorCommand()
        msg.global_id = [self.motor_id]
        msg.setpoint = [pwm]
        self.publisher.publish(msg)
        self.sp_pwm = pwm

    def get_state(self):
        with self.motor_state_lock:

            return {
                'pv_pos_encoder' : self.pv_pos_encoder,
                'pv_torque_encoder' : self.pv_torque_encoder,
                'pv_current' : self.pv_current
            }
        
    def start(self):
        self.is_running = True
    
    def stop(self):
        msg = MotorCommand()
        msg.global_id = [self.motor_id]
        msg.setpoint = [0]
        self.publisher.publish(msg)
        self.sp_pwm = 0

        self.is_running = False

    def terminate(self):
        self.stop()
        self.wd.stop()