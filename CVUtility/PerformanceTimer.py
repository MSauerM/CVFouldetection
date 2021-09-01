from timeit import default_timer as timer


class PerformanceTimer:
    """
        Class for measuring consumed time of a certain process
        ......

        Attributes
        -----------------
            _startTime
                timestamp at execution of start()
            _endTime
                timestamp at execution of end()
            _usage_label
                information for more specific print displaying
        Methods
        -----------------
            start()
                set _startTime to current time
            end()
                set _endTime to current time
            get_time()
                returns the time a specific part of code has consumed by
                calculating the difference between _endTime and _startTime
        """
    def __init__(self, usage_label: str = None):
        self._startTime = None
        self._endTime = None
        self._usage_label = usage_label

    def start(self):
        self._startTime = timer()

    def end(self):
        self._endTime = timer()

    def get_time(self):
        return self._endTime - self._startTime

    def __str__(self):
        return 'Passed Time: {passedTime}  {usage_label}'.format(passedTime=self.get_time(), usage_label=self._usage_label)