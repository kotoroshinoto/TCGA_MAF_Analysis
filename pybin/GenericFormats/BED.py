import os
import sys

__author__ = 'mgooch'


class Entry:

	def __init__(self):
		pass

	def __str__(self):
		pass

	def get_column(self, index):
		pass

	def get_number_columns(self):
		pass

class File:

	@staticmethod
	def get_all_entries_from_filehandle(filehandle):
		pass

	@staticmethod
	def get_all_entries_from_path(path):
		pass

	@staticmethod
	def __get_all_entries_from_lines__(lines):
		pass

	def __init__(self):
		pass

	def open(self, path, override=False):
		pass

	def __read_first_line__(self):
		pass

	def has_more_entries(self):
		pass

	def __read_next_line_from_filehandle__(self):
		pass

	def get_next_entry(self):
		pass

	def close(self):
		pass

	def reset(self):
		pass

	def use_filehandle(self, filehandle, override=False):
		pass

	def get_line_count(self):
		pass
