import threading
import serial

class AngleSensor:
    def __init__(self, serial_port):
        self.ser = serial.Serial(serial_port, baudrate=9600)
        self.ser.flush()
        try:
            line = self.ser.readline()
        except:
            pass

        self.angle = 0

        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._run)

        self.stop_event = threading.Event()

    def _run(self):
        while not self.stop_event.is_set():
            line = self.ser.readline()
            try:
                value = float(line.strip())

                with self.lock:
                    self.angle = value
            except:
                pass

    def get_value(self):
        with self.lock:
            return self.angle

    def start(self):
        self.thread.start()

    def terminate(self):
        self.stop_event.set()
        self.thread.join()
        self.ser.close()
