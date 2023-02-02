import rospy
import threading

class RosLoop:
    def __init__(self):
        rospy.init_node('bench_controller', anonymous=True)

    def _run(self):
        rospy.spin()

    def start(self):
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def stop(self):
        rospy.signal_shutdown('stop')
        self.thread.join()