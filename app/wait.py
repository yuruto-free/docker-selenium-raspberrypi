import signal
import time

class ProcessStatus:
    def __init__(self):
        self.__status = True

    def change_status(self, signum, frame):
        self.__status = False

    def get_status(self):
        return self.__status

if __name__ == '__main__':
    process_status = ProcessStatus()
    # setup signal
    signal.signal(signal.SIGTERM, process_status.change_status)
    signal.signal(signal.SIGINT, process_status.change_status)

    # main loop
    while process_status.get_status():
        time.sleep(1)
