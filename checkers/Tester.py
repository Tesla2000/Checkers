import time

class Tester:
	counter = 0

	def restCounter(self):
		self.counter = 0

	def measureTimeSince(self, startTime=0):
		return round(time.time() - startTime, 2)

	def incrementCounter(self):
		self.counter += 1








