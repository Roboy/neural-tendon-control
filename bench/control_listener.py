import rospy

from bench.msg import BenchState, BenchMotorControl, BenchRecorderControl


class ControlListener:
    def __init__(self, 
            myobrick_flex,
            myobrick_extend,
            safety_observer,
        ):
        self.myobrick_flex = myobrick_flex
        self.myobrick_extend = myobrick_extend
        self.safety_observer = safety_observer

        # Input storage
        self.input = {}

        # Setup message event callback
        self.subscriber = rospy.Subscriber('/test_bench/BenchMotorControl', BenchMotorControl, self._on_bench_motor_command_callback)


    def _on_bench_motor_command_callback(self, msg):
        self.myobrick_flex.set_pwm(msg.flex_myobrick_pwm)
        self.myobrick_extend.set_pwm(msg.extend_myobrick_pwm)

        if msg.flex_myobrick_start :
            self.myobrick_flex.start()
        if msg.extend_myobrick_start :
            self.myobrick_extend.start()
        
        if msg.reset_kill_switch :
            self.safety_observer.reset_kill_switch()
        if msg.press_kill_switch :
            self.safety_observer._kill_switch()