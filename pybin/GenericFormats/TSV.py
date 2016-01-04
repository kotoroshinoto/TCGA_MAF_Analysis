import os
import sys

__author__ = 'mgooch'


class Entry:

	def __init__(self):
		self.data = list()

	def __str__(self):
		return "\t".join(self.data)

	def get_column(self, index):
		return self.data[index]

	def get_number_columns(self):
		return len(self.data)

	@classmethod
	def process_line(cls, line):
		entry = cls()

		entry.data = line.split("\t")

		return entry


class File:
	@staticmethod
	def __get_all_entries_from_lines__(lines):
		entries = list()
		for line in lines:
			line = line.rstrip()
			if line == "":
				continue
			entry = Entry.process_line(line)
			if entry is not None:
				entries.append(entry)
		return entries

	@staticmethod
	def get_all_entries_from_path(path):
		filehandle = open(path, mode='r')
		return File.get_all_entries_from_filehandle(filehandle)

	@staticmethod
	def get_all_entries_from_filehandle(filehandle):
		lines = filehandle.readlines()
		return File.__get_all_entries_from_lines__(lines)

	def __init__(self):
		self.allow_close_handle = False
		self.file_handle = None
		self.next_line = None
		self.line_count = 0
		return

	def open(self, path, override=False):
		if self.file_handle is not None:
			if override:
				self.reset()
			else:
				return
		self.file_handle = open(path, mode='r')
		self.__read_first_line__()
		return

	def __read_first_line__(self):
		rstrip_chars = list()
		rstrip_chars.append('\n')
		rstrip_chars.append('\r')
		lstrip_chars = list()
		lstrip_chars.append(' ')
		none_count = 0
		failure_condition = False
		while True:
			if none_count > 5:
				failure_condition = True
				break
			line = self.file_handle.readline()
			if line is None:
				none_count += 1
			else:
				self.line_count += 1
				if len(line) > 0:
					line = line.rstrip(rstrip_chars)
					if line.lstrip(lstrip_chars).startswith('#'):
						continue
		if failure_condition:
			print("failed to read from file", file=sys.stderr)
			sys.exit(-1)

		pass

	def has_more_entries(self):
		if self.next_line:
			return True
		else:
			return False

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
