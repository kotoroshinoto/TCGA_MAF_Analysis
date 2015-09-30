#!/usr/bin/env python3
__author__ = 'mgooch'

import os
import sys
import io
from contracts import contract


class MAFSampleCountsList:

	def __init__(self):
		self.counts = dict()

	def get_count(self, sample_key: 'str') -> 'int':
		if sample_key in  self.counts:
			return self.counts[sample_key]
		return None

	def set_count(self, sample_key: 'str', count: 'int') -> 'None':
		self.counts[sample_key] = count
		return

	def read_file_handle(self, handle: io.TextIOBase) -> 'None':
		return

	def read_file(self, path: 'str') -> 'None':
		handle = open(path, mode='r')
		self.read_file_handle(handle)
		return

	@staticmethod
	@contract(bound_list='list[>=1](int, >0)', returns='list(int)')
	def fix_boundaries(bound_list: 'list[int]') -> 'list[int]':
		unique_list = list(set(bound_list))
		sorted_list = sorted(unique_list)
		return sorted_list

	@contract(bound_list='list[>=1](int, >0)')
	def split(self, bound_list: 'list[int]') -> 'list[dict[str, int]]':
		if len(bound_list) < 1:
			print()
		bounds_fixed = self.__class__.fix_boundaries(bound_list)
		print("splitting on boundaries: %s" % (", ".join(str(x) for x in bounds_fixed)))
		for boundary in bounds_fixed:
			tmp_list = self.__split_single__(boundary)
		#TODO finish porting internal splitter

		return

	@contract(boundary='int, >0', returns='list[2](type(MAFSampleCountsList))')
	def __split_single__(self, boundary: 'int') -> 'list[MAFSampleCountsList]':
		return

	def __clear__(self):
		self.counts = dict()
		return