import time


class TimerError(Exception):

    _start_error = 'Timer already started. Call .stop() before starting a new timer.'

    _stop_error = 'Timer is not running. Call .start() to start a timer'

    _runtime_error = 'No runtime has been calculated. timer needs a .start() then .stop() call to determine runtime'

class timer:

    def __init__(self):
        self.start_time = None
        self.finish_time = None
    
    def start(self):
        if self.start_time:
            raise TimerError(TimerError._start_error)
        
        self.start_time = time.perf_counter()
        self.finish_time = None
    
    def stop(self):
        if not self.start_time:
            raise TimerError(TimerError._stop_error)
        
        self.finish_time = f'{(time.perf_counter() - self.start_time):.8f}'
        self.start_time = None
    
    def runtime(self):
        if not self.finish_time:
            raise TimerError(TimerError._runtime_error)
        
        return self.finish_time