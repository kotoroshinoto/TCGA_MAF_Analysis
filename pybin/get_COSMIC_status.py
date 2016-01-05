#!/usr/bin/env python3
import sys
import os
import click
import csv
import re
import vcf
import vcf.model

class CdsData:
	def __init__(self):
		self.mut_type = ""
		self.start = 0
		self.end = 0
		self.old_seq = ""
		self.new_seq = ""

tsv_position_matcher = re.compile("([0-9]+):([0-9]+)-([0-9]+)")


def fix_chr(chrstring):
	chr = chrstring.upper()
	chr.replace("CHR", "")
	return str(chr)


chrom_num_to_letter = dict()
chrom_num_to_letter['23'] = 'X'
chrom_num_to_letter['24'] = 'Y'
chrom_num_to_letter['25'] = 'MT'


def fix_sex_mt(chrom):
	if chrom in chrom_num_to_letter:
		return chrom_num_to_letter[chrom]
	else:
		return chrom


def chrom_compare(chr1, chr2):
	c1 = fix_sex_mt(chr1.upper())
	c2 = fix_sex_mt(chr2.upper())
	return c1 == c2


def calc_preceding_identical_bases(seq1, seq2):
	s1 = seq1.upper().rstrip().lstrip()
	s2 = seq2.upper().rstrip().lstrip()
	samecount = 0
	for i in range(0, min(len(seq1), len(seq2))):
		if s1[i] == s2[i]:
			samecount += 1
		else:
			return samecount
	return samecount


class CosmicData:
	def __init__(self):
		self.cosmic_id = None
		self.chrom = None
		self.strand = None
		self.start = None
		self.end = None
		self.prediction = None
		self.cds_string = None
		self.ref_seq = None
		self.alt_seq = None
		self.vcf_input = False
		self.tsv_input = False
		self.pos = None
		self.affected_start = None

	def __str__(self):
		str_list = list()
		str_list.append(str(self.cosmic_id))
		str_list.append(str(self.chrom))
		str_list.append(str(self.start))
		str_list.append(str(self.end))
		str_list.append(str(self.ref_seq))
		str_list.append(str(self.alt_seq))
		str_list.append(str(self.cds_string))
		str_list.append(str(self.prediction))
		return "\t".join(str_list)

	@classmethod
	def record_from_tsv(cls, record: dict):
		method_name = "[record_from_tsv]"
		new_record = cls()
		new_record.cosmic_id = record[16]
		new_record.cds_string = record[17]
		new_record.strand = record[24]
		position_match = tsv_position_matcher.match(record[23])
		if not position_match:
			print("%s TSV formatting fault: %s does not seem to be in correct position format" % (method_name, record[23]), file=sys.stderr)
			sys.exit(-1)
		new_record.chrom = fix_chr(position_match.group(1))
		new_record.start = int(position_match.group(2))
		new_record.end = int(position_match.group(3))
		new_record.prediction = record[26]
		new_record.tsv_input = True
		return new_record

	@classmethod
	def record_from_vcf(cls, record: vcf.model._Record):
		new_record = cls()
		new_record.cosmic_id = record.ID
		new_record.chrom = fix_chr(record.CHROM)
		new_record.strand = record.INFO["STRAND"]
		new_record.pos = int(record.POS)
		new_record.start = int(record.start) + 1
		new_record.end = int(record.end)
		new_record.affected_start = int(record.affected_start) + 1
		new_record.cds_string = record.INFO["CDS"]
		new_record.ref_seq = str(record.REF).upper().lstrip().rstrip()
		new_record.alt_seq = str(record.ALT[0]).upper().lstrip().rstrip()
		if len(record.ALT) > 1:
			print("[ASSUMPTION BUG] VCF record had more than 1 ALT sequence", file=sys.stderr)
			sys.exit(-1)
		#data that is missing: stop & prediction
		new_record.vcf_input = True
		return new_record


def validate_vcf_against_tsv(vcf_data: CosmicData, tsv_data: CosmicData):
	method_name = "validate_vcf_against_tsv"
	if ((not vcf_data.vcf_input) or vcf_data.tsv_input) or ((not tsv_data.tsv_input) or tsv_data.vcf_input):
		print("%s invalid inputs, either a merged record was given or the arguments were in incorrect order" % method_name, file=sys.stderr)
		sys.exit(-1)
	if vcf_data.cosmic_id != tsv_data.cosmic_id:
		print("%s COSMIC ids do not match '%s' vs '%s'" % (method_name, vcf_data.cosmic_id, tsv_data.cosmic_id), file=sys.stderr)
		return False
	if not chrom_compare(vcf_data.chrom, tsv_data.chrom):
		print("%s chr field does not match, '%s' vs '%s' " % (method_name, vcf_data.chrom, tsv_data.chrom), file=sys.stderr)
		return False
	if vcf_data.strand != tsv_data.strand:
		print("%s strand strings do not match '%s' vs '%s'" % (method_name, vcf_data.strand, tsv_data.strand), file=sys.stderr)
		return False
	if vcf_data.cds_string != tsv_data.cds_string:
		print("%s CDS strings do not match '%s' vs '%s'" % (method_name, vcf_data.cds_string, tsv_data.cds_string), file=sys.stderr)
		return False
	if vcf_data.start != tsv_data.start:
		# 1116 AAT  ATG
		# 1117 AT   TG
		if vcf_data.start < tsv_data.start:
			difference = tsv_data.start - vcf_data.start
			subseq1 = vcf_data.ref_seq[0:difference]
			subseq2 = vcf_data.ref_seq[0:difference]
			# print("'%s' vs '%s'" % (subseq1, subseq2))
			return subseq1 == subseq2
		print("%s start field does not match, '%s' vs '%s' " % (method_name, vcf_data.start, tsv_data.start), file=sys.stderr)
		return False
	#VCF file lacks prediction
	#fill in missing data
	return True


def merge_records(vcf_data: CosmicData, tsv_data: CosmicData):
	if not validate_vcf_against_tsv(vcf_data, tsv_data):
		print("[merge_records] Validation failure\nVCF:\n%s\nTSV\n%s" % (vcf_data, tsv_data), file=sys.stderr)
		sys.exit(-1)
	vcf_data.prediction = tsv_data.prediction
	vcf_data.tsv_input = True

COSMIC_DATA = dict()
MAF_DATA = dict()


def process_vcf(vcf_file):
	print("Starting to read VCF file", file=sys.stderr)
	vcf_rdr = vcf.Reader(fsock=vcf_file, strict_whitespace=True)
	for record in vcf_rdr:
		cosmic_id = record.ID
		# print("cosmic ID: %s" % cosmic_id)
		if cosmic_id not in COSMIC_DATA:
			new_data = CosmicData.record_from_vcf(record)
			COSMIC_DATA[new_data.cosmic_id] = new_data
	print("finished reading COSMIC VCF file", file=sys.stderr)


def process_tsv(tsv_file):
	#CDS column: 18
	#genome version: 23
	#Genome position: 24    Format: CHR:START-END
	#Strand: 25
	#FATHMM prediction: 27
	print("Starting to read COSMIC TSV file", file=sys.stderr)
	with open(tsv_file, newline='') as cosmic_file:
		cosmic_reader = csv.reader(cosmic_file, dialect="excel-tab")
		first_line = next(cosmic_reader)
		if str(first_line[0]) != "Gene name":
			# print("first line not headers")
			cosmic_id = first_line[16]
			if cosmic_id not in COSMIC_DATA:
				# print("first line not in COSMIC_DATA %s %s" % (cosmic_id, "\t".join(COSMIC_DATA.keys())))
				pass
			elif COSMIC_DATA[cosmic_id].tsv_input:
				# print("first line corresponding entry already has tsv input")
				pass
			else:
				tsv_record = CosmicData.record_from_tsv(first_line)
				merge_records(COSMIC_DATA[cosmic_id], tsv_record)
		for record in cosmic_reader:
			cosmic_id = record[16]
			if cosmic_id not in COSMIC_DATA:
				continue
			if COSMIC_DATA[cosmic_id].tsv_input:
				continue
			tsv_record = CosmicData.record_from_tsv(record)
			merge_records(COSMIC_DATA[cosmic_id], tsv_record)
	print("finished reading COSMIC TSV file", file=sys.stderr)


@click.command(help="check cosmic prediction for mutation effects")
@click.option("--cosmic-vcf", type=click.File('r'), required=True, help="cosmic VCF file")
@click.option("--cosmic-tsv", type=click.Path(exists=True), required=True, help="cosmic TSV file")
@click.option("--maf", type=click.File('r'), required=True, help="Util file to be checked")
def cli(cosmic_vcf, cosmic_tsv, maf):
	process_vcf(cosmic_vcf)
	process_tsv(cosmic_tsv)
	for cosmic_id in COSMIC_DATA:
		record = COSMIC_DATA[cosmic_id]
		if not (record.vcf_input and record.tsv_input):
			print("record was not updated with missing data from tsv: %s" % record, file=sys.stderr)

if __name__ == "__main__":
	cli()
