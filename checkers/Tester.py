import time
from typing import Union

from protocols.protocols import Tester as Tester_

class Tester(Tester_):
    counter = 0

    def restCounter(self):
        self.counter = 0

    def measureTimeSince(self, startTime: Union[complex, float, int]=0):
        return round(time.time() - startTime, 2)

    def incrementCounter(self):
        self.counter += 1
