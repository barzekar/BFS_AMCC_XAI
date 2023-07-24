import time
import signal


class Timeout:
    """
    Context manager to set a timeout for a block of code.
    """
    def __init__(self, seconds):
        self.seconds = seconds
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.time()
        signal.signal(signal.SIGALRM, self.timeout_handler)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        self.end_time = time.time()
        signal.alarm(0)  # Disable the alarm

    @property
    def elapsed_time(self):
        if self.start_time is not None and self.end_time is not None:
            return self.end_time - self.start_time
        return None

    @staticmethod
    def timeout_handler(signum, frame):
        raise TimeoutError("Code block timed out!")
