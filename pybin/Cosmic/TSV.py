import sys
import os


class Entry:

	def __init__(self):
		pass

	@classmethod
	def process_line(cls, line):
		pass

	def __str__(self):
		return ""


class File:

	def __init__(self):
		pass

	@staticmethod
	def __get_all_entries_from_lines__(lines):
		pass

	@staticmethod
	def get_all_entries_from_path(path):
		pass

	@staticmethod
	def get_all_entries_from_filehandle(filehandle):
		pass

	def open(self, path, override=False):
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