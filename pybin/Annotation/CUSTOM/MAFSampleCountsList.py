#!/usr/bin/env python3
__author__ = 'mgooch'

import os
import sys
import io


class MAFSampleCountsList:
	def __init__(self):
		self.counts = dict()

	def get_count(self, sample_key: str) -> int:
		if sample_key in  self.counts:
			return self.counts[sample_key]
		return None

	def set_count(self, sample_key: str, count: int) -> None:
		self.counts[sample_key] = count
		return

	def read_file_handle(self, handle: io.TextIOBase) -> None:
		return

	def read_file(self, path: str) -> None:
		handle = open(path, mode='r')
		self.read_file_handle(handle)
		return

	@staticmethod
	def fix_boundaries(self, bound_list: list) -> None:
		if len(bound_list) < 1:
			print("No boundary arguments supplied to fixBoundaries", file=sys.stderr)
			sys.exit(-1)
		result = list
		for value in sorted(list(set(bound_list))):
			if value >= 0:
				result.append(value)
			else:
				print("WARNING: %d removed as it is not a valid boundary" % value, file=sys.stderr)
		return result

	def split(self, bound_list: list) -> None:
		if len(bound_list) < 1:
			#TODO left off here
		return

	def __split_single__(self, boundary: int):
		return

	def __clear__(self):
		self.counts = dict()
		return