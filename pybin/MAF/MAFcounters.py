__author__ = 'mgooch'


class FeatureCounter:
	def __init__(self):
		self.counts = dict()
		self.name = None

	def count(self):
		return 0

	def determineMutation(self, norm1, norm2, tumor1, tumor2):
		return None

	def __appendcount(self, keystring):
		if keystring in self.counts:
			self.counts[keystring] += 1
		else:
			self.counts[keystring] = 1

	def __countif(self, keystring, condition):
		if condition:
			self.__appendcount(keystring)

	def __str__(self):
		return ""

	def writeFile(self, prefix, path):
		return


class GeneMutCounter(FeatureCounter):
	def __init__(self):
		self.hugoIDs = dict()

	def count(self):
		return
	def __str__(self):
		return ""


class SampMutCounter(FeatureCounter):
	def count(self):
		return


class MutTypeCounter(FeatureCounter):
	def count(self):
		return