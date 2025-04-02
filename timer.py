import time


class Timer:
    def __init__(self, duration=1):
        self.duration = duration
        self.start_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.start_time = None

    def is_running(self):
        if self.start_time is None:
            return False
        return (time.perf_counter() - self.start_time) < self.duration

    def stopped(self):
        return not self.is_running()

    def time_left(self):
        if self.start_time is None:
            return 0  # Timer not started
        elapsed = time.perf_counter() - self.start_time
        return max(0, self.duration - elapsed)
