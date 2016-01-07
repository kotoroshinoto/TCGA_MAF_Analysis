#!/usr/bin/env python3
import sys
import os
import click
import csv
import re
import vcf
import vcf.model
import copy
import GenericFormats.MAF
from intervaltree import Interval, IntervalTree


csv.field_size_limit(sys.maxsize)

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

	def __list__(self):
		result = list()
		result.append(str(self.cosmic_id))
		result.append(str(self.chrom))
		result.append(str(self.start))
		result.append(str(self.end))
		result.append(str(self.strand))
		result.append(str(self.ref_seq))
		result.append(str(self.alt_seq))
		result.append(str(self.cds_string))
		result.append(str(self.prediction))
		return result

	def __str__(self):
		str_list = self.__list__()
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
	def record_from_tablefile(cls, record: dict):
		new_record = cls()
		new_record.cosmic_id = record[0]
		new_record.chrom = record[1]
		new_record.start = int(record[2])
		new_record.end = int(record[3])
		new_record.strand = record[4]
		new_record.ref_seq = record[5]
		new_record.alt_seq = record[6]
		new_record.cds_string = record[7]
		new_record.prediction = record[8]

		# if new_record.ref_seq[0] == new_record.alt_seq[0]:
		# 	print("[WARNING] first nucleotides match in record: %s" % new_record)
		return new_record

	@classmethod
	def record_from_vcf(cls, record: vcf.model._Record):
		new_record = cls()
		new_record.cosmic_id = record.ID
		new_record.chrom = fix_chr(record.CHROM)
		new_record.strand = record.INFO["STRAND"]
		new_record.start = int(record.start) + 1
		new_record.end = int(record.end) + 1
		new_record.cds_string = record.INFO["CDS"]
		new_record.ref_seq = str(record.REF).upper().lstrip().rstrip()
		new_record.alt_seq = str(record.ALT[0]).upper().lstrip().rstrip()

		if record.ALT[0].type == "MNV":
			if len(new_record.ref_seq) == 1 and len(new_record.alt_seq) > 1:
				seq1 = new_record.ref_seq[0:1]
				seq2 = new_record.alt_seq[0:1]
				if seq1 != seq2:
					print("[VCF format violation] INS with non-matching initial base", file=sys.stderr)
					sys.exit(-1)
				else:
					new_record.remove_leftmost_nucleotide(update_start=False)
			else:
				seq1 = new_record.ref_seq[0:1]
				seq2 = new_record.alt_seq[0:1]
				if seq1 == seq2:
					new_record.remove_leftmost_nucleotide()

		new_record.replace_empty_nucleotide_with_dash()

		if len(record.ALT) > 1:
			print("[ASSUMPTION BUG] VCF record had more than 1 ALT sequence", file=sys.stderr)
			sys.exit(-1)
		#data that is missing: stop & prediction
		new_record.vcf_input = True
		return new_record

	def replace_empty_nucleotide_with_dash(self):
		if self.ref_seq == "":
			self.ref_seq = "-"
		if self.alt_seq == "":
			self.alt_seq = "-"

	def remove_leftmost_nucleotide(self, update_start=True):
		if update_start:
			self.start += 1
		self.ref_seq = self.ref_seq[1:]
		self.alt_seq = self.alt_seq[1:]
		self.replace_empty_nucleotide_with_dash()


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
			temp_record = copy.deepcopy(vcf_data)
			temp_record.remove_leftmost_nucleotide()
			if temp_record.start == tsv_data.start:
				vcf_data.remove_leftmost_nucleotide()
			return vcf_data.start == tsv_data.start
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
	vcf_data.end = tsv_data.end
	vcf_data.tsv_input = True

COSMIC_DATA = dict()
INTERVAL_TREES = dict()
MAF_DATA = list()


def process_vcf(vcf_file):
	print("Starting to read COSMIC VCF file", file=sys.stderr)
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


@click.command(help="build table from cosmic VCF and TSV files")
@click.option("--cosmic-vcf", type=click.File('r'), required=True, help="cosmic VCF file")
@click.option("--cosmic-tsv", type=click.Path(exists=True, dir_okay=False, resolve_path=True, readable=True), required=True, help="cosmic TSV file")
@click.option("--output", type=click.Path(dir_okay=False, resolve_path=True, writable=True), required=True, help="path for output file")
def build_cosmic_table(cosmic_vcf, cosmic_tsv, output):
	process_vcf(cosmic_vcf)
	process_tsv(cosmic_tsv)
	with open(output, 'w', newline='') as csvfile:
		table_writer = csv.writer(csvfile, dialect="excel-tab")
		for cosmic_id in COSMIC_DATA:
			record = COSMIC_DATA[cosmic_id]
			if not (record.vcf_input and record.tsv_input):
				print("record was not updated with missing data from tsv: %s" % record, file=sys.stderr)
			else:
				table_writer.writerow(record.__list__());


def process_cosmic_table(cosmic_table):
	#in this mode, COSMIC_DATA will be indexed as follows: COSMIC_DATA["$CHROM"]["$START_$END"]["$REF_$ALT"]
	#initialize the dict with chromosome keys
	print("Starting to read COSMIC table file", file=sys.stderr)
	for i in range(1,23):
		COSMIC_DATA[str(i)] = dict()
		INTERVAL_TREES[str(i)] = IntervalTree()
	COSMIC_DATA["X"] = dict()
	COSMIC_DATA["Y"] = dict()
	COSMIC_DATA["MT"] = dict()
	INTERVAL_TREES["X"] = IntervalTree()
	INTERVAL_TREES["Y"] = IntervalTree()
	INTERVAL_TREES["MT"] = IntervalTree()
	with open(cosmic_table, newline='') as cosmic_table_file:
		cosmic_reader = csv.reader(cosmic_table_file, dialect="excel-tab")
		for record in cosmic_reader:
			cosmic_record = CosmicData.record_from_tablefile(record)
			position_key = "%s_%s" % (cosmic_record.start, cosmic_record.end)
			seq_key = "%s_%s" % (cosmic_record.ref_seq, cosmic_record.alt_seq)
			if position_key not in COSMIC_DATA[cosmic_record.chrom]:
				COSMIC_DATA[cosmic_record.chrom][position_key] = dict()
			if seq_key not in COSMIC_DATA[cosmic_record.chrom][position_key]:
				COSMIC_DATA[cosmic_record.chrom][position_key][seq_key] = list()
			COSMIC_DATA[cosmic_record.chrom][position_key][seq_key].append(cosmic_record)
			i_tree = INTERVAL_TREES[cosmic_record.chrom]  # type: IntervalTree
			i_tree[cosmic_record.start:(cosmic_record.end + 1)] = position_key # range not inclusive of end, needs +1
	print("Finished reading COSMIC table file", file=sys.stderr)


def process_maf_file(maf_file):
	print("Starting to read MAF file", file=sys.stderr)
	global MAF_DATA
	MAF_DATA = GenericFormats.MAF.File.get_all_entries_from_filehandle(maf_file)
	print("Finished reading MAF file", file=sys.stderr)

advanced_search_history = dict()


def compute_mut_type(ref_seq, alt_seq):
	if ref_seq == "-" and alt_seq != "-":
		return "INS"
	if ref_seq != "-" and alt_seq == "-":
		return "DEL"
	if len(ref_seq) == 1 and len(alt_seq) == 1:
		return "SNC"
	return "MNC"


def advanced_search(chrom, position_key, seq_key, reason, unmatched_fsock=None):
	# find overlapping ranges
	# in overlapping ranges, see if adjusting start or end
	# by removing any homologous segments from both entries rescues the match
	i_tree = INTERVAL_TREES[chrom]  # type: IntervalTree
	values = position_key.split("_")
	start = int(values[0])
	end = int(values[1])
	mut_values = seq_key.split("_")
	ref_seq = mut_values[0]
	alt_seq = mut_values[1]
	history_key = "%s:%s-%s:%s>%s" % (chrom, start, end, ref_seq, alt_seq)
	if history_key in advanced_search_history:
		return advanced_search_history[history_key]
	else:
		advanced_search_history[history_key] = [["NO_COSMIC_ENTRY"], ["NO_DATA"]]
	query = i_tree.search(start, end + 1)
	overlaps = list()
	for intvl in query:  # type: Interval
		overlaps.append(intvl)
	if len(overlaps) == 0:
		if unmatched_fsock is not None:
			print("[MatchFailure]\t%s\t%s\t%s\t%s" % (chrom, position_key, seq_key, reason), file=unmatched_fsock)
		return [["NO_COSMIC_ENTRY"], ["NO_DATA"]]
	else:
		print("%s:%s-%s:%s>%s" % (chrom, start, end, ref_seq, alt_seq), file=unmatched_fsock)
		for intvl in overlaps:  # type: Interval
			r_start = intvl.begin
			r_end = intvl.end - 1
			mut_list = COSMIC_DATA[chrom][intvl.data].keys()
			for mut in mut_list:
				r_mut_values = mut.split("_")
				r_ref_seq = r_mut_values[0]
				r_alt_seq = r_mut_values[1]
				print("\t%s:%s-%s:%s>%s" % (chrom, r_start, r_end, r_ref_seq, r_alt_seq), file=unmatched_fsock)
				#filter out mutations of different type
				#rules:
				#if search term is MNC, check if it has homologous regions that should be removed
				#   if it is still MNC, only keep MNC
				#if search term is INS, only keep INS & MNC, check if MNC is actually an INS
				#   if MNC is still MNC, do not keep
				#if search term is DEL, only keep DEL & MNC, check if MNC is actually a DEL
				#   if MNC is still MNC, do not keep
		if unmatched_fsock is not None:
			print("[MatchFailure]\t%s\t%s\t%s\t%s" % (chrom, position_key, seq_key, reason), file=unmatched_fsock)
		return [["NO_COSMIC_ENTRY"], ["NO_DATA"]]


@click.command(help="check cosmic prediction for mutation effects")
@click.option("--cosmic-table", type=click.Path(exists=True, dir_okay=False, resolve_path=True, readable=True), required=True, help="cosmic table file generated by this script")
@click.option("--maf", type=click.File('r'), required=True, help="Util file to be checked")
@click.option("--output", type=click.Path(dir_okay=False, resolve_path=True, writable=True), required=True, help="path for output file")
@click.option("--unmatched", type=click.File('w'), help="path for unmatched log")
def check_maf_against_cosmic(cosmic_table, maf, output, unmatched):
	process_cosmic_table(cosmic_table)
	process_maf_file(maf)
	with open(output, 'w', newline='') as csvfile:
		tsv_writer = csv.writer(csvfile, dialect="excel-tab")  # type: csv.DictWriter
		for entry in MAF_DATA:  # type: GenericFormats.MAF.Entry
			output_list = entry.__str__().split("\t")
			chrom = str(entry.data['Chrom']).upper()
			seq_key = entry.determine_mutation(resolve_mnc=True, report_ref_seq=True)[0]
			if seq_key == "LOH_W_MUT":
				print("[WARNING]: Skipping MAF entry due to mutation type: LOH_W_MUT\t%s" % entry, file=sys.stderr)
				continue
			position_key = "%s_%s" % (entry.data['Start_Position'], entry.data['End_Position'])
			if position_key not in COSMIC_DATA[chrom]:
				result_list = advanced_search(chrom, position_key, seq_key, "coordinates_not_present", unmatched_fsock=unmatched)
				output_list.append(";".join(result_list[0]))
				output_list.append(";".join(result_list[1]))
				tsv_writer.writerow(output_list)
				continue
			if seq_key not in COSMIC_DATA[chrom][position_key]:
				result_list = advanced_search(chrom, position_key, seq_key, "mutation_not_present", unmatched_fsock=unmatched)
				output_list.append(";".join(result_list[0]))
				output_list.append(";".join(result_list[1]))
				tsv_writer.writerow(output_list)
				continue
			cosmic_record_list = COSMIC_DATA[chrom][position_key][seq_key]  # type: list

			cosmic_id_list = list()
			prediction_list = list()
			for cosmic_record in cosmic_record_list:  # type: CosmicData

				prediction = cosmic_record.prediction
				if prediction == "":
					prediction = "NO_PREDICTION_PRESENT"
				cosmic_id_list.append(cosmic_record.cosmic_id)
				prediction_list.append(prediction)
			output_list.append(";".join(cosmic_id_list))
			output_list.append(";".join(prediction_list))
			tsv_writer.writerow(output_list)


@click.group(no_args_is_help=True)
def cli():
	pass

cli.add_command(build_cosmic_table, name="prep")
cli.add_command(check_maf_against_cosmic, name="check")

if __name__ == "__main__":
	cli()
