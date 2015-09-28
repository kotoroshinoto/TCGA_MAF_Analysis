__author__ = 'mgooch'

import Annotation.MAF.File_Handlers.MAFreader as MAFreader

class FeatureCounter:
	def __init__(self):
		self.counts = dict()
		self.name = None

	def count(self):
		return 0

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