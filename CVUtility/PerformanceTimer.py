from timeit import default_timer as timer


class PerformanceTimer:

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