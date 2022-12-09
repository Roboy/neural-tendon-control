import threading
import time
import csv

class DataRecorder:
    def __init__(
            self,
            freq,
            path, 
            myobrick_flex,
            myobrick_extend,
            angle_sensor
        ):
        self.freq = freq
        self.path = path
        self.myobrick_flex = myobrick_flex
        self.myobrick_extend = myobrick_extend
        self.angle_sensor = angle_sensor


        self.stop_event = threading.Event()

    def _run(self):
        with open(self.path, 'a') as csvfile:
            writer = csv.writer(csvfile)
            while not self.stop_event.is_set():
                flex_state = self.myobrick_flex.get_state()
                extend_state = self.myobrick_extend.get_state()

                writer.writerow([
                    time.time(),
                    self.angle_sensor.get_value(),
                    flex_state['pv_pos_encoder'],
                    flex_state['pv_torque_encoder'],
                    flex_state['pv_current'],
                    self.myobrick_flex.sp_pwm,
                    extend_state['pv_pos_encoder'],
                    extend_state['pv_torque_encoder'],
                    extend_state['pv_current'],
                    self.myobrick_extend.sp_pwm,

                ])

                time.sleep(1/self.freq)
    
    def start(self):
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()