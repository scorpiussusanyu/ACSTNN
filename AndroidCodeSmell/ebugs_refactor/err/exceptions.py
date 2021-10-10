#!/usr/bin/python3

class MonkeyRunningError(Exception):
	"""Exception raised when the a monkey test fails to execute properly

    Attributes:
        app -- the ID of the failing app
        seed -- the seed of the failing test
    """
	def __init__(self, app, seed):
		self.message = "The monkey test with seed " + str(seed) + " failed for app " + str(app)
		super(MonkeyRunningError, self).__init__(self.message)

class NoTestResultsError(Exception):
	"""Exception raised when the a monkey test fails to execute properly

    Attributes:
        app -- the ID of the failing app
        seed -- the seed of the failing test
    """
	def __init__(self, app, seed):
		self.message = "The app " + str(app) + " failed to generate results file for seed " + str(seed)
		super(NoTestResultsError, self).__init__(self.message)

# Missing exceptions:
#	no measures files found
#	no trace file found
#	
