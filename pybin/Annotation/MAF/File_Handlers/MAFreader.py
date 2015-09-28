__author__ = 'mgooch'
import os
import sys


class MAFentry:
	column2index = dict()

	@staticmethod
	def __init__():


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
		columns = line.split("\t")
		if len(columns) != 37:
			print("line does not have correct # of columns (37)", file=sys.stderr)
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


class MAFfile:
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
		self.next_line =self.file_handle.readline()
		if self.next_line:
			self.next_line =self.next_line.rstrip()
		if self.next_line and self.next_line == "Hugo_Symbol	Entrez_Gene_Id	Center	Ncbi_Build	Chrom	Start_Position	End_Position	Strand	Variant_Classification	Variant_Type	Reference_Allele	Tumor_Seq_Allele1	Tumor_Seq_Allele2	Dbsnp_Rs	Dbsnp_Val_Status	Tumor_Sample_Barcode	Matched_Norm_Sample_Barcode	Match_Norm_Seq_Allele1	Match_Norm_Seq_Allele2	Tumor_Validation_Allele1	Tumor_Validation_Allele2	Match_Norm_Validation_Allele1	Match_Norm_Validation_Allele2	Verification_Status	Validation_Status	Mutation_Status	Sequencing_Phase	Sequence_Source	Validation_Method	Score	Bam_File	Sequencer	Tumor_Sample_UUID	Matched_Norm_Sample_UUID	File_Name	Archive_Name	Line_Number":
			print("First line in $self->{_fn} was a header line, ignoring it\n", file=sys.stderr);
			self.next_line =self.file_handle.readline()
			if self.next_line:
				self.next_line =self.next_line.rstrip()
			self.line_count += 1

	def has_more_entries(self):
		if self.next_line:
			return True
		else:
			return False

	def get_next_entry(self):
		entry = MAFentry.process_line(self.next_line)
		self.next_line =self.file_handle.readline()
		if self.next_line:
			self.next_line =self.next_line.rstrip()
		self.line_count += 1
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

	def use_filehandle(self, filehandle, override = False):
		if self.file_handle is not None:
			if override:
				self.reset()
			else:
				return
		self.file_handle = filehandle
		self.allow_close_handle = False
		self.__read_first_line__()
		return
