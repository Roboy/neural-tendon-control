import threading
import time
import csv


TOP_ANGLE_VALUE = 2050.0
BOT_ANGLE_VALUE = 1223.0

class SafetyObserver:
    def __init__(
            self,
            myobrick_flex,
            myobrick_extend,
            angle_sensor
        ):
        self.myobrick_flex = myobrick_flex
        self.myobrick_extend = myobrick_extend
        self.angle_sensor = angle_sensor

        self.freq = 20 # Run safety loop at this freq.
        self.kill_switch_flag = False

        self.stop_event = threading.Event()

    def _run(self):
        while not self.stop_event.is_set():
            time.sleep(1/self.freq)

            if self.kill_switch_flag:
                self.myobrick_extend.stop()
                self.myobrick_flex.stop()
                continue

            flex_state = self.myobrick_flex.get_state()
            extend_state = self.myobrick_extend.get_state()

            # Check joint range
            if self.angle_sensor.get_value() < BOT_ANGLE_VALUE + 50:
                self._kill_switch()
            if self.angle_sensor.get_value() > TOP_ANGLE_VALUE - 50:
                self._kill_switch()


            

    def _kill_switch(self):
        self.myobrick_extend.stop()
        self.myobrick_flex.stop()
        self.kill_switch_flag = True
        print('Motor kill swtich pressed!')

    def get_kill_switch_state(self):
        return self.kill_switch_flag

    def reset_kill_switch(self):
        self.kill_switch_flag = False
    
    def start(self):
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()