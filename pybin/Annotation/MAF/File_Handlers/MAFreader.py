__author__ = 'mgooch'
import os
import sys


class MAFentry:
	column2index = dict()
	index2column = dict()

	@staticmethod
	def get_index(heading):
		if heading in MAFentry.column2index:
			return MAFentry.column2index[heading]
		else:
			return None

	@staticmethod
	def get_heading(index):
		if index in MAFentry.index2column:
			return MAFentry.index2column[index]
		else:
			return None

	@staticmethod
	def __register_column__(heading, index):
		MAFentry.column2index[heading] = index
		MAFentry.index2column[index] = heading

	@staticmethod
	def __initialize_class__():
		MAFentry.__register_column__('Hugo_Symbol', 0)
		MAFentry.__register_column__('hEntrez_Gene_Id', 1)
		MAFentry.__register_column__('Center', 2)
		MAFentry.__register_column__('Ncbi_Build', 3)
		MAFentry.__register_column__('Chrom', 4)
		MAFentry.__register_column__('Start_Position', 5)
		MAFentry.__register_column__('End_Position', 6)
		MAFentry.__register_column__('Strand', 7)
		MAFentry.__register_column__('Variant_Classification', 8)
		MAFentry.__register_column__('Variant_Type', 9)
		MAFentry.__register_column__('Reference_Allele', 10)
		MAFentry.__register_column__('Tumor_Seq_Allele1', 11)
		MAFentry.__register_column__('Tumor_Seq_Allele2', 12)
		MAFentry.__register_column__('Dbsnp_Rs', 13)
		MAFentry.__register_column__('Dbsnp_Val_Status', 14)
		MAFentry.__register_column__('Tumor_Sample_Barcode', 15)
		MAFentry.__register_column__('Matched_Norm_Sample_Barcode', 16)
		MAFentry.__register_column__('Match_Norm_Seq_Allele1', 17)
		MAFentry.__register_column__('Match_Norm_Seq_Allele2', 18)
		MAFentry.__register_column__('Tumor_Validation_Allele1', 19)
		MAFentry.__register_column__('Tumor_Validation_Allele2', 20)
		MAFentry.__register_column__('Match_Norm_Validation_Allele1', 21)
		MAFentry.__register_column__('Match_Norm_Validation_Allele2', 22)
		MAFentry.__register_column__('Verification_Status', 23)
		MAFentry.__register_column__('Validation_Status', 24)
		MAFentry.__register_column__('Mutation_Status', 25)
		MAFentry.__register_column__('Sequencing_Phase', 26)
		MAFentry.__register_column__('Sequence_Source', 27)
		MAFentry.__register_column__('Validation_Method', 28)
		MAFentry.__register_column__('Score', 29)
		MAFentry.__register_column__('Bam_File', 30)
		MAFentry.__register_column__('Sequencer', 31)
		MAFentry.__register_column__('Tumor_Sample_UUID', 32)
		MAFentry.__register_column__('Matched_Norm_Sample_UUID', 33)
		MAFentry.__register_column__('File_Name', 34)
		MAFentry.__register_column__('Archive_Name', 35)
		MAFentry.__register_column__('Line_Number', 36)
		return

	def __init__(self):
		self.Hugo_Symbol = ""
		self.Entrez_Gene_Id = ""
		self.Center = ""
		self.Ncbi_Build = ""
		self.Chrom = ""
		self.Start_Position = ""
		self.End_Position = ""
		self.Strand = ""
		self.Variant_Classification = ""
		self.Variant_Type = ""
		self.Reference_Allele = ""
		self.Tumor_Seq_Allele1 = ""
		self.Tumor_Seq_Allele2 = ""
		self.Dbsnp_Rs = ""
		self.Dbsnp_Val_Status = ""
		self.Tumor_Sample_Barcode = ""
		self.Matched_Norm_Sample_Barcode = ""
		self.Match_Norm_Seq_Allele1 = ""
		self.Match_Norm_Seq_Allele2 = ""
		self.Tumor_Validation_Allele1 = ""
		self.Tumor_Validation_Allele2 = ""
		self.Match_Norm_Validation_Allele1 = ""
		self.Match_Norm_Validation_Allele2 = ""
		self.Verification_Status = ""
		self.Validation_Status = ""
		self.Mutation_Status = ""
		self.Sequencing_Phase = ""
		self.Sequence_Source = ""
		self.Validation_Method = ""
		self.Score = ""
		self.Bam_File = ""
		self.Sequencer = ""
		self.Tumor_Sample_UUID = ""
		self.Matched_Norm_Sample_UUID = ""
		self.File_Name = ""
		self.Archive_Name = ""
		self.Line_Number = ""
		return

	@staticmethod
	def process_line(line):
		if line is None or line == "" or line == "Hugo_Symbol	Entrez_Gene_Id	Center	Ncbi_Build	Chrom	" \
			"Start_Position	End_Position	Strand	Variant_Classification	Variant_Type	Reference_Allele	" \
			"Tumor_Seq_Allele1	Tumor_Seq_Allele2	Dbsnp_Rs	Dbsnp_Val_Status	Tumor_Sample_Barcode	" \
			"Matched_Norm_Sample_Barcode	Match_Norm_Seq_Allele1	Match_Norm_Seq_Allele2	" \
			"Tumor_Validation_Allele1	Tumor_Validation_Allele2	Match_Norm_Validation_Allele1	" \
			"Match_Norm_Validation_Allele2	Verification_Status	Validation_Status	Mutation_Status	Sequencing_Phase" \
			"	Sequence_Source	Validation_Method	Score	Bam_File	Sequencer	Tumor_Sample_UUID	" \
			"Matched_Norm_Sample_UUID	File_Name	Archive_Name	Line_Number":
			return None
		columns = line.split("\t")
		if len(columns) != 37:
			print("line does not have correct # of columns (37)", file=sys.stderr)
			print("processing line: '%s'" % line, file=sys.stderr)
			sys.exit(-1)
		entry = MAFentry()
		entry.Hugo_Symbol = columns[0]
		entry.Entrez_Gene_Id = columns[1]
		entry.Center = columns[2]
		entry.Ncbi_Build = columns[3]
		entry.Chrom = columns[4]
		entry.Start_Position = columns[5]
		entry.End_Position = columns[6]
		entry.Strand = columns[7]
		entry.Variant_Classification = columns[8]
		entry.Variant_Type = columns[9]
		entry.Reference_Allele = columns[10]
		entry.Tumor_Seq_Allele1 = columns[11]
		entry.Tumor_Seq_Allele2 = columns[12]
		entry.Dbsnp_Rs = columns[13]
		entry.Dbsnp_Val_Status = columns[14]
		entry.Tumor_Sample_Barcode = columns[15]
		entry.Matched_Norm_Sample_Barcode = columns[16]
		entry.Match_Norm_Seq_Allele1 = columns[17]
		entry.Match_Norm_Seq_Allele2 = columns[18]
		entry.Tumor_Validation_Allele1 = columns[19]
		entry.Tumor_Validation_Allele2 = columns[20]
		entry.Match_Norm_Validation_Allele1 = columns[21]
		entry.Match_Norm_Validation_Allele2 = columns[22]
		entry.Verification_Status = columns[23]
		entry.Validation_Status = columns[24]
		entry.Mutation_Status = columns[25]
		entry.Sequencing_Phase = columns[26]
		entry.Sequence_Source = columns[27]
		entry.Validation_Method = columns[28]
		entry.Score = columns[29]
		entry.Bam_File = columns[30]
		entry.Sequencer = columns[31]
		entry.Tumor_Sample_UUID = columns[32]
		entry.Matched_Norm_Sample_UUID = columns[33]
		entry.File_Name = columns[34]
		entry.Archive_Name = columns[35]
		entry.Line_Number = columns[36]
		return entry

	def determine_mutation(self):
		tmr = list()
		nrm = list()
		nrm.append(self.Match_Norm_Seq_Allele1)
		nrm.append(self.Match_Norm_Seq_Allele2)
		tmr.append(self.Tumor_Seq_Allele1)
		tmr.append(self.Tumor_Seq_Allele2)

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
				#1,1 -> 1,1 Don't expect this to be triggered, it shouldn't be in the MAF file at all
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
MAFentry.__initialize_class__()


class MAFfile:
	@staticmethod
	def __get_all_entries_from_lines__(lines):
		entries = list()
		for line in lines:
			line = line.rstrip()
			if line == "":
				continue
			entry = MAFentry.process_line(line)
			if entry is not None:
				entries.append(entry)
		return entries

	@staticmethod
	def get_all_entries_from_path(path):
		filehandle = open(path, mode='r')
		return MAFfile.get_all_entries_from_filehandle(filehandle)

	@staticmethod
	def get_all_entries_from_filehandle(filehandle):
		lines = filehandle.readlines()
		return MAFfile.__get_all_entries_from_lines__(lines)

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
			entry = MAFentry.process_line(self.next_line)
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
