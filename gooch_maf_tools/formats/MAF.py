import os
import sys
from io import TextIOBase
import csv
import re
from typing import re
__author__ = 'mgooch'


class Entry:

	def __init__(self, dict_from_dict_reader=None, fieldnames=None):
		self.data = None  # type: dict[str, str]
		if dict_from_dict_reader is None:
			self.data = dict()
		else:
			if fieldnames is None:
				raise RuntimeError("[Entry::__init__] fieldnames not supplied with dict from dictreader")
			self.data = dict_from_dict_reader
			self.fieldnames = fieldnames

	# def determine_mutation(self):
		# cds_text = self.data['HGVSc']
	def get_data(self, index: int) -> str:
		return self.data[self.fieldnames[index]]

	def get_heading(self, index: int) -> str:
		return self.fieldnames[index]

	def has_index(self, index: int) -> bool:
		return 0 > index < len(self.fieldnames)

	def determine_mutation(self, resolve_mnc=False, report_ref_seq=False):
		tmr = list()
		nrm = list()
		nrm.append(self.data['Match_Norm_Seq_Allele1'])
		nrm.append(self.data['Match_Norm_Seq_Allele2'])
		tmr.append(self.data['Tumor_Seq_Allele1'])
		tmr.append(self.data['Tumor_Seq_Allele2'])
		ref_seq = self.data['Reference_Allele']
		if len(nrm[0]) > 1 or len(nrm[1]) > 1 or len(tmr[0]) > 1 or len(tmr[1]) > 1:
			if not resolve_mnc:
				return ['MNC']

		if len(nrm[0]) == 0:
			nrm[0] = '-'
		if len(nrm[1]) == 0:
			nrm[1] = '-'
		if len(tmr[0]) == 0:
			tmr[0] = '-'
		if len(tmr[1]) == 0:
			tmr[1] = '-'

		nrm_same = nrm[0] == nrm[1]
		tmr_same = tmr[0] == tmr[1]

		nrm1_match_tmr1 = nrm[0] == tmr[0]
		nrm2_match_tmr2 = nrm[1] == tmr[1]

		nrm1_match_tmr2 = nrm[0] == tmr[1]
		nrm2_match_tmr1 = nrm[1] == tmr[0]

		if nrm_same and tmr_same:
			if nrm[0] == tmr[0]:
				#no mutation
				#1,1 -> 1,1 Don't expect this to be triggered, it shouldn't be in the util file at all
				return ["NO_MUTATION"]
			else:
				#mutation either of both chromosomes or paired with LOH
				#likely LOH + mutation
				#can count the mutation TYPE AND LOH
				#1,1 -> 2,2
				if report_ref_seq:
					return ["LOH_W_MUT", "%s_%s" % (ref_seq, tmr[0]), "%s_-" % ref_seq]
				else:
					return ["LOH_W_MUT", "%s_%s" % (nrm[0], tmr[0]), "%s_-" % nrm[0]]
		elif nrm_same and (not tmr_same):
			if nrm1_match_tmr1 or nrm1_match_tmr2:
				#one of the tumor alleles matches the normal alleles (which are the same)
				#this means one difference exists
				#log mutation type
				#captures these mutations:
				if nrm1_match_tmr1:
					#1,1 -> 1,2
					if report_ref_seq:
						return ["%s_%s" % (ref_seq, tmr[1])]
					else:
						return ["%s_%s" % (nrm[0], tmr[1])]
				else:
					#1,1 -> 2,1
					if report_ref_seq:
						return ["%s_%s" % (ref_seq, tmr[0])]
					else:
						return ["%s_%s" % (nrm[0], tmr[0])]
			else:
				#both tumor alleles are different from normal alleles (which match each other), but don't match each other what do?
				#LIKELY_ARTIFACT_ERROR
				#1,1 -> 2,3
				return ["LIKELY_ARTIFACT_ERROR", "DOUBLE_MUTATION"]

		elif (not nrm_same) and tmr_same:
			if nrm1_match_tmr1 or nrm2_match_tmr1:
				#one of the normal alleles matches the tumor alleles (which are the same)
				#this means one difference exists
				#likely LOH without mutation
				#captures these mutations:
				#1,2 -> 1,1
				#1,2 -> 2,2
				return ["LOH_NO_MUT"]
			else:
				#tumor alleles (which match each other) are different from both normal alleles, what do?
				#likely LOH + mutation
				#1,2 -> 3,3
				return ["LOH_W_MUT", "INDETERMINATE_MUTATION", "INDETERMINATE_INDEL"]

		else:  # (not nrm_name) and (not tmr_same)
			#not sure what can be done to identify this situation, which allele changed to which other allele?
			#at LEAST 2 differences exist
			# check for a match between one of tumors and normals
			# if 1,2	3,4 signal likely error
			if not(nrm1_match_tmr1 or nrm1_match_tmr2 or nrm2_match_tmr1 or nrm2_match_tmr2):
				#1,2	3,4 case
				#signal likely error
				return ["LIKELY_ARTIFACT_ERROR"]
			#capture these mutations:
			if nrm1_match_tmr1 and (not (nrm2_match_tmr2 or nrm1_match_tmr2 or nrm2_match_tmr1)):
				# 1,2 -> 1,3
				if report_ref_seq:
					return ["%s_%s" % (ref_seq, tmr[1])]
				else:
					return ["%s_%s" % (nrm[1], tmr[1])]
			if nrm2_match_tmr1 and (not (nrm2_match_tmr2 or nrm1_match_tmr2 or nrm1_match_tmr1)):
				# 1,2 -> 2,3
				if report_ref_seq:
					return ["%s_%s" % (ref_seq, tmr[1])]
				else:
					return ["%s_%s" % (nrm[0], tmr[1])]
			if nrm1_match_tmr2 and (not (nrm2_match_tmr2 or nrm1_match_tmr1 or nrm2_match_tmr1)):
				# 1,2 -> 3,1
				if report_ref_seq:
					return ["%s_%s" % (ref_seq, tmr[0])]
				else:
					return ["%s_%s" % (nrm[1], tmr[0])]
			if nrm2_match_tmr2 and (not (nrm1_match_tmr1 or nrm1_match_tmr2 or nrm2_match_tmr1)):
				# 1,2 -> 3,2
				if report_ref_seq:
					return ["%s_%s" % (ref_seq, tmr[0])]
				else:
					return ["%s_%s" % (nrm[0], tmr[0])]
			if nrm1_match_tmr1 and nrm2_match_tmr2 and not(nrm1_match_tmr2 or nrm2_match_tmr1):
				#1,2 -> 1,2
				return ["NO_MUTATION"]
			if nrm1_match_tmr2 and nrm2_match_tmr1 and not(nrm1_match_tmr1 or nrm2_match_tmr2):
				#1,2 -> 2,1
				return ["NO_MUTATION"]
			#signal unrecognized condition via a None in a list should not be logically possible
			return [None]

	def __str__(self):
		cols = list()
		for i in range(0, len(self.fieldnames)):
			cols.append(self.data[self.fieldnames[i]])
		return "\t".join(cols)


class EntryReader:
	def __init__(self, file, fieldnames=None):
		self.file = file
		self.reader = None
		if fieldnames is None:
			#make sure to skip comment lines if fieldnames is not defined
			self.fieldnames = None
			for line in self.file:  # type: str
				if line == "":
					break
				if line.lstrip().startswith("#"):
					continue
				else:
					self.fieldnames = line.lstrip().rstrip().split("\t")
					break
			if self.fieldnames is None:
				raise IOError("file contains no lines with fields, is either empty or entirely composed of comments")
		else:
			# pass fieldnames to reader if available
			self.fieldnames = fieldnames
		self.reader = csv.DictReader(self.file, fieldnames=self.fieldnames, dialect='excel-tab')
		self.num_cols = len(self.reader.fieldnames)
		self.entry_count = 0
		self.next_entry = next(self.reader)

	def next(self) -> Entry:
		if not self.has_next():
			return None
		entry = Entry(self.next_entry, self.reader.fieldnames)
		try:
			self.next_entry = next(self.reader)
		except StopIteration:
			# print("StopIteration exception encountered", file=sys.stderr)
			self.next_entry = None
		self.entry_count += 1
		return entry

	def has_next(self)-> 'bool':
		return self.next_entry is not None

	def get_index(self, heading: 'str') -> 'int':
		if heading in self.reader.fieldnames:
			return self.reader.fieldnames.index(heading)
		else:
			return None

	def get_heading(self, index: 'int') -> 'str':
		if index < self.num_cols:
			return self.reader.fieldnames[index]

	def get_header_line(self) -> 'str':
		return "\t".join(self.reader.fieldnames)

	def get_entry_count(self):
		return self.entry_count

	def get_line_count(self):
		return self.get_line_count()

	def get_remaining(self) -> 'list[Entry]':
		entries = list()  # type: 'list[Entry]'
		while self.has_next():
			entries.append(self.next())
		return entries

	@classmethod
	def get_all_entries_from_filehandle(cls, file) -> 'list[Entry]':
		reader = cls(file)
		return reader.get_remaining()
