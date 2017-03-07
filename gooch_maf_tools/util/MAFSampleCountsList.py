#!/usr/bin/env python3
import os
import sys
import io

__author__ = 'mgooch'


class MAFSampleCountsList:

	def __init__(self):
		self.counts = dict()

	def __contains__(self, item):
		return item in self.counts

	def get_count(self, sample_key: 'str') -> 'int':
		if sample_key in self.counts:
			return self.counts[sample_key]
		return None

	def set_count(self, sample_key: 'str', count: 'int') -> 'None':
		self.counts[sample_key] = count
		return

	def read_file_handle(self, handle) -> 'None':
		lines = handle.readlines()
		""":type : list[str]"""
		for line in lines:
			splitline = line.rstrip().split("\t")
			if len(splitline) != 2:
				continue
			self.counts[splitline[0]] = int(splitline[1])
		return

	def read_file(self, path: 'str') -> 'None':
		handle = open(path, mode='r')
		self.read_file_handle(handle)
		return

	@staticmethod
	def fix_boundaries(bound_list: 'list[int]') -> 'list[int]':
		unique_list = list(set(bound_list))
		sorted_list = sorted(unique_list)
		return sorted_list

	def split(self, bound_list: 'list[int]') -> 'list[dict[str, int]]':
		result_lists = list()
		if len(bound_list) < 1:
			print()
		bounds_fixed = self.__class__.fix_boundaries(bound_list)
		print("splitting on boundaries: %s" % (", ".join(str(x) for x in bounds_fixed)), file=sys.stderr)
		remaining_list = self
		for boundary in bounds_fixed:
			# print("splitting on boundary: %d" % boundary)
			tmp_list = remaining_list.__split_single__(boundary)
			result_lists.append(tmp_list[0])
			remaining_list = tmp_list[1]
		result_lists.append(remaining_list)
		return result_lists

	def __split_single__(self, boundary: 'int') -> 'list[MAFSampleCountsList]':
		#TODO finish porting internal splitter
		# print("[__split_single__] boundary: %d" % boundary)
		splitlists = list()
		""":type : list[MAFSampleCountsList]"""

		splitlists.append(MAFSampleCountsList())#lower
		splitlists.append(MAFSampleCountsList())#higher & equal
		for item in self.counts:
			count = self.counts[item]
			if count >= boundary:
				splitlists[1].set_count(item, count)
			else:
				splitlists[0].set_count(item, count)
		return splitlists

	def __clear__(self):
		self.counts = dict()
		return

	def __str__(self):
		s = str("")
		for item in self.counts:
			s += "%s\t%d\n" % (item, self.counts[item])
		return s
