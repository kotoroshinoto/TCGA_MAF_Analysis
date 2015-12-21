__author__ = 'mgooch'
import os
import sys


class Entry:
	column2index = dict()
	index2column = dict()

	@classmethod
	def get_index(cls, heading: 'str') -> 'int':
		if heading in cls.column2index:
			return cls.column2index[heading]
		else:
			return None

	@classmethod
	def get_heading(cls, index: 'int') -> 'str':
		if index in cls.index2column:
			return cls.index2column[index]
		else:
			return None

	@classmethod
	def __register_column__(cls, heading: 'str', index: 'int'):
		cls.column2index[heading] = index
		cls.index2column[index] = heading

	@classmethod
	def __initialize_class__(cls):
		cls.__register_column__('Hugo_Symbol', 0)
		cls.__register_column__('hEntrez_Gene_Id', 1)
		cls.__register_column__('Center', 2)
		cls.__register_column__('Ncbi_Build', 3)
		cls.__register_column__('Chrom', 4)
		cls.__register_column__('Start_Position', 5)
		cls.__register_column__('End_Position', 6)
		cls.__register_column__('Strand', 7)
		cls.__register_column__('Variant_Classification', 8)
		cls.__register_column__('Variant_Type', 9)
		cls.__register_column__('Reference_Allele', 10)
		cls.__register_column__('Tumor_Seq_Allele1', 11)
		cls.__register_column__('Tumor_Seq_Allele2', 12)
		cls.__register_column__('Dbsnp_Rs', 13)
		cls.__register_column__('Dbsnp_Val_Status', 14)
		cls.__register_column__('Tumor_Sample_Barcode', 15)
		cls.__register_column__('Matched_Norm_Sample_Barcode', 16)
		cls.__register_column__('Match_Norm_Seq_Allele1', 17)
		cls.__register_column__('Match_Norm_Seq_Allele2', 18)
		cls.__register_column__('Tumor_Validation_Allele1', 19)
		cls.__register_column__('Tumor_Validation_Allele2', 20)
		cls.__register_column__('Match_Norm_Validation_Allele1', 21)
		cls.__register_column__('Match_Norm_Validation_Allele2', 22)
		cls.__register_column__('Verification_Status', 23)
		cls.__register_column__('Validation_Status', 24)
		cls.__register_column__('Mutation_Status', 25)
		cls.__register_column__('Sequencing_Phase', 26)
		cls.__register_column__('Sequence_Source', 27)
		cls.__register_column__('Validation_Method', 28)
		cls.__register_column__('Score', 29)
		cls.__register_column__('Bam_File', 30)
		cls.__register_column__('Sequencer', 31)
		cls.__register_column__('Tumor_Sample_UUID', 32)
		cls.__register_column__('Matched_Norm_Sample_UUID', 33)
		cls.__register_column__('File_Name', 34)
		cls.__register_column__('Archive_Name', 35)
		cls.__register_column__('Line_Number', 36)
		return

	def __init__(self):
		self.data = dict()

	@classmethod
	def get_header_line(cls):
		return "Hugo_Symbol	Entrez_Gene_Id	Center	Ncbi_Build	Chrom	" \
			"Start_Position	End_Position	Strand	Variant_Classification	Variant_Type	Reference_Allele	" \
			"Tumor_Seq_Allele1	Tumor_Seq_Allele2	Dbsnp_Rs	Dbsnp_Val_Status	Tumor_Sample_Barcode	" \
			"Matched_Norm_Sample_Barcode	Match_Norm_Seq_Allele1	Match_Norm_Seq_Allele2	" \
			"Tumor_Validation_Allele1	Tumor_Validation_Allele2	Match_Norm_Validation_Allele1	" \
			"Match_Norm_Validation_Allele2	Verification_Status	Validation_Status	Mutation_Status	Sequencing_Phase" \
			"	Sequence_Source	Validation_Method	Score	Bam_File	Sequencer	Tumor_Sample_UUID	" \
			"Matched_Norm_Sample_UUID	File_Name	Archive_Name	Line_Number"

	@classmethod
	def process_line(cls, line):
		if line is None or line == "" or line == cls.get_header_line():
			return None
		columns = line.split("\t")
		if len(columns) != 37:
			print("line does not have correct # of columns (37)", file=sys.stderr)
			print("processing line: '%s'" % line, file=sys.stderr)
			sys.exit(-1)
		entry = cls()
		for i in range(0,len(columns)):
			entry.data[cls.get_heading(i)] = columns[i]
		return entry

	def determine_mutation(self):
		tmr = list()
		nrm = list()
		nrm.append(self.data['Match_Norm_Seq_Allele1'])
		nrm.append(self.data['Match_Norm_Seq_Allele2'])
		tmr.append(self.data['Tumor_Seq_Allele1'])
		tmr.append(self.data['Tumor_Seq_Allele2'])

		if len(nrm[0]) > 1 or len(nrm[1]) > 1 or len(tmr[0]) > 1 or len(tmr[1]) > 1:
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
				#1,1 -> 1,1 Don't expect this to be triggered, it shouldn't be in the TCGA file at all
				return ["NO_MUTATION"]
			else:
				#mutation either of both chromosomes or paired with LOH
				#likely LOH + mutation
				#can count the mutation TYPE AND LOH
				#1,1 -> 2,2
				return ["LOH_W_MUT", "%s_%s" % (nrm[0], tmr[0]), "%s_-" % nrm[0]]
		elif nrm_same and (not tmr_same):
			if nrm1_match_tmr1 or nrm1_match_tmr2:
				#one of the tumor alleles matches the normal alleles (which are the same)
				#this means one difference exists
				#log mutation type
				#captures these mutations:
				if nrm1_match_tmr1:
					#1,1 -> 1,2
					return ["%s_%s" % (nrm[0], tmr[1])]
				else:
					#1,1 -> 2,1
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
				return ["%s_%s" % (nrm[1], tmr[1])]
			if nrm2_match_tmr1 and (not (nrm2_match_tmr2 or nrm1_match_tmr2 or nrm1_match_tmr1)):
				# 1,2 -> 2,3
				return ["%s_%s" % (nrm[0], tmr[1])]
			if nrm1_match_tmr2 and (not (nrm2_match_tmr2 or nrm1_match_tmr1 or nrm2_match_tmr1)):
				# 1,2 -> 3,1
				return ["%s_%s" % (nrm[1], tmr[0])]
			if nrm2_match_tmr2 and (not (nrm1_match_tmr1 or nrm1_match_tmr2 or nrm2_match_tmr1)):
				# 1,2 -> 3,2
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
		for i in range(0, 37):
			cols.append(self.data[self.__class__.get_heading(i)])
		return "\t".join(cols)

Entry.__initialize_class__()


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
		self.next_line = self.file_handle.readline()
		if self.next_line:
			self.next_line = self.next_line.rstrip()
		if self.next_line and self.next_line == "Hugo_Symbol	Entrez_Gene_Id	Center	Ncbi_Build	Chrom	" \
			"Start_Position	End_Position	Strand	Variant_Classification	Variant_Type	Reference_Allele	" \
			"Tumor_Seq_Allele1	Tumor_Seq_Allele2	Dbsnp_Rs	Dbsnp_Val_Status	Tumor_Sample_Barcode	" \
			"Matched_Norm_Sample_Barcode	Match_Norm_Seq_Allele1	Match_Norm_Seq_Allele2	" \
			"Tumor_Validation_Allele1	Tumor_Validation_Allele2	Match_Norm_Validation_Allele1	" \
			"Match_Norm_Validation_Allele2	Verification_Status	Validation_Status	Mutation_Status	Sequencing_Phase" \
			"	Sequence_Source	Validation_Method	Score	Bam_File	Sequencer	Tumor_Sample_UUID	" \
			"Matched_Norm_Sample_UUID	File_Name	Archive_Name	Line_Number":
			print("First line in $self->{_fn} was a header line, ignoring it\n", file=sys.stderr)
			self.next_line = self.file_handle.readline()
			if self.next_line:
				self.next_line = self.next_line.rstrip()
			self.line_count += 1

	def has_more_entries(self):
		if self.next_line:
			return True
		else:
			return False

	def __read_next_line_from_filehandle__(self):
		self.next_line = self.file_handle.readline()
		if self.next_line == "":
			self.next_line = None
			return
		self.next_line = self.next_line.rstrip()
		self.line_count += 1
		if self.next_line == "":
			print("line was empty: '%s'" % self.next_line)
			self.__read_next_line_from_filehandle__()

	def get_next_entry(self):
		if self.next_line is not None:
			entry = Entry.process_line(self.next_line)
		else:
			return None
		self.__read_next_line_from_filehandle__()
		return entry

	def close(self):
		if self.allow_close_handle:
			self.file_handle.close()
		return

	def reset(self):
		self.close()
		self.line_count = 0
		self.next_line = None
		self.file_handle = None
		self.allow_close_handle = False

	def use_filehandle(self, filehandle, override=False):
		if self.file_handle is not None:
			if override:
				self.reset()
			else:
				return
		self.file_handle = filehandle
		self.allow_close_handle = False
		self.__read_first_line__()
		return

	def get_line_count(self):
		return self.line_count
