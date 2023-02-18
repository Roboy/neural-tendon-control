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
        self.input_list = []

        # Setup message event callback
        self.subscriber = rospy.Subscriber('/test_bench/BenchMotorControl', BenchMotorControl, self._on_bench_motor_command_callback)


    def _on_bench_motor_command_callback(self, msg):

        self.input_list.append(msg)

        if msg.flex_myobrick_start :
            self.myobrick_flex.start()
        if msg.extend_myobrick_start :
            self.myobrick_extend.start()
        
        if msg.reset_kill_switch :
            self.safety_observer.reset_kill_switch()
        if msg.press_kill_switch :
            self.safety_observer._kill_switch()

    def get_input(self, tick):
        # Get input from queue and remove all older inputs
        input = None
        input_list = self.input_list.copy()
        for i in input_list:
            if i.tick == tick:
                input = i
                self.input_list.remove(i)
            elif i.tick < tick:
                self.input_list.remove(i)

        return input
                
        
