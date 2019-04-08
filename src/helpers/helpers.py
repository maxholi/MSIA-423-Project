import datetime


class Timer:
    """Times the code within the with statement and logs the elapsed time when it closes.

           Args:
               function (string): Name of function being timed
               logger (`logging.logger`): Logger to have elapsed time logged to
   """
    def __init__(self, function, logger):
        self.logger = logger
        self.function = function

    def __enter__(self):
        self.start = datetime.datetime.now()

        return self

    def __exit__(self, *args):
        self.end = datetime.datetime.now()
        self.interval = self.end - self.start
        self.logger.info("%s took %0.2f seconds", self.function, self.interval.total_seconds())