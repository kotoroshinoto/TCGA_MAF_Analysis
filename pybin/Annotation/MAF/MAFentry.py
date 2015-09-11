__author__ = 'mgooch'
class MAF_format_exception(Exception):
	def __init__(self, errmsg):
		self.errmsg = errmsg
	def __str__(self):
		return "Exception occurred: %s" % self.errmsg
class MAFentry:
	def getIndex(self, colname):
		return 0
	def __initcol2index(self):

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

	def process_line(self, line):
		columns = line.split("\t")
		if len(columns) != 37:
			raise MAF_format_exception("line does not have correct # of columns (37)")
		newobj = MAFentry()
		newobj.Hugo_Symbol = columns[0]
		newobj.Entrez_Gene_Id = columns[1]
		newobj.Center = columns[2]
		newobj.Ncbi_Build = columns[3]
		newobj.Chrom = columns[4]
		newobj.Start_Position = columns[5]
		newobj.End_Position = columns[6]
		newobj.Strand = columns[7]
		newobj.Variant_Classification = columns[8]
		newobj.Variant_Type = columns[9]
		newobj.Reference_Allele = columns[10]
		newobj.Tumor_Seq_Allele1 = columns[11]
		newobj.Tumor_Seq_Allele2 = columns[12]
		newobj.Dbsnp_Rs = columns[13]
		newobj.Dbsnp_Val_Status = columns[14]
		newobj.Tumor_Sample_Barcode = columns[15]
		newobj.Matched_Norm_Sample_Barcode = columns[16]
		newobj.Match_Norm_Seq_Allele1 = columns[17]
		newobj.Match_Norm_Seq_Allele2 = columns[18]
		newobj.Tumor_Validation_Allele1 = columns[19]
		newobj.Tumor_Validation_Allele2 = columns[20]
		newobj.Match_Norm_Validation_Allele1 = columns[21]
		newobj.Match_Norm_Validation_Allele2 = columns[22]
		newobj.Verification_Status = columns[23]
		newobj.Validation_Status = columns[24]
		newobj.Mutation_Status = columns[25]
		newobj.Sequencing_Phase = columns[26]
		newobj.Sequence_Source = columns[27]
		newobj.Validation_Method = columns[28]
		newobj.Score = columns[29]
		newobj.Bam_File = columns[30]
		newobj.Sequencer = columns[31]
		newobj.Tumor_Sample_UUID = columns[32]
		newobj.Matched_Norm_Sample_UUID = columns[33]
		newobj.File_Name = columns[34]
		newobj.Archive_Name = columns[35]
		newobj.Line_Number = columns[36]
		return newobj

	def __str__(self):
		retstr = list()
		retstr.append(self.Hugo_Symbol)
		retstr.append(self.Entrez_Gene_Id)
		retstr.append(self.Center)
		retstr.append(self.Ncbi_Build)
		retstr.append(self.Chrom)
		retstr.append(self.Start_Position)
		retstr.append(self.End_Position)
		retstr.append(self.Strand)
		retstr.append(self.Variant_Classification)
		retstr.append(self.Variant_Type)
		retstr.append(self.Reference_Allele)
		retstr.append(self.Tumor_Seq_Allele1)
		retstr.append(self.Tumor_Seq_Allele2)
		retstr.append(self.Dbsnp_Rs)
		retstr.append(self.Dbsnp_Val_Status)
		retstr.append(self.Tumor_Sample_Barcode)
		retstr.append(self.Matched_Norm_Sample_Barcode)
		retstr.append(self.Match_Norm_Seq_Allele1)
		retstr.append(self.Match_Norm_Seq_Allele2)
		retstr.append(self.Tumor_Validation_Allele1)
		retstr.append(self.Tumor_Validation_Allele2)
		retstr.append(self.Match_Norm_Validation_Allele1)
		retstr.append(self.Match_Norm_Validation_Allele2)
		retstr.append(self.Verification_Status)
		retstr.append(self.Validation_Status)
		retstr.append(self.Mutation_Status)
		retstr.append(self.Sequencing_Phase)
		retstr.append(self.Sequence_Source)
		retstr.append(self.Validation_Method)
		retstr.append(self.Score)
		retstr.append(self.Bam_File)
		retstr.append(self.Sequencer)
		retstr.append(self.Tumor_Sample_UUID)
		retstr.append(self.Matched_Norm_Sample_UUID)
		retstr.append(self.File_Name)
		retstr.append(self.Archive_Name)
		retstr.append(self.Line_Number)
		return "\t".join(retstr)
