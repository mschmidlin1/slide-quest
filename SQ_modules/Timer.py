import time



class Timer:
    """
    A class which allows you to set a timer and then check if time is up.
    """
    length_s: int
    start_time: float
    end_time: float
    def __init__(self, length_s: int):
        self.length_s = length_s
    
    def start(self):
        """
        Starts the timer.
        """
        self.start_time = time.time()
        self.end_time = self.start_time + self.length_s
    
    def time_is_up(self) -> bool:
        """
        Returns if time is up for the timer.
        """
        return time.time() > self.end_time


    



