#!/usr/bin/env python3
import sys
import os
import click
import csv
import re

def check_vcf_cosmic_quirk(vcf):
	for line in vcf:
		if not line.startswith("#"):
			tabsplit = line.split("\t")
			# print("%s" % tabsplit[7])
			semisplit = tabsplit[7].split(";")
			entries = dict()
			for record in semisplit:
				if "=" in record:
					eqsplit = record.split("=")

					if eqsplit[0] not in entries:
						entries[eqsplit[0]] = list()
					entries[eqsplit[0]].append(eqsplit[1])
				else:
					if record not in entries:
						entries[record] = list()
					entries[record].append(True)
			if "GENE" in entries:
				gene_list = entries["GENE"]
				if len(gene_list) != 2:
					if len(gene_list) > 2:
						print("# GENE VALUEs: %d" % len(gene_list))
				else:
					if gene_list[0] != gene_list[1]:
						print("%s doesn't match %s" % (gene_list[0], gene_list[1]))
			if "STRAND" in entries:
				strand_list = entries["STRAND"]
				if len(strand_list ) != 2:
					if len(strand_list ) > 2:
						print("# STRAND VALUEs: %d" % len(strand_list))
				else:
					if strand_list[0] != strand_list[1]:
						print("%s doesn't match %s" % (strand_list[0], strand_list[1]))
	#RESULT: turns out, the doubled entries aren't ever different. Very strange.
	#It appears 3 of the entries are universal, and the rest only get added to coding records,
	# without regard for duplication
#@click.option("--vcf", type=click.File('r'), required=True, help="cosmic VCF file")

one_number_indel_regex = re.compile("^c\\.([0-9?+-]+)del[ ]*(\S*)ins[ ]*(\S+)$")
two_number_indel_regex = re.compile("^c\\.([0-9?+-]+)[_+-]([cC][.])*([0-9?+-]+)del[ ]*(\S*)ins[ ]*(\S+)$")

one_number_ins_regex = re.compile("^c\\.([0-9?+-]+)ins[ ]*(\S+)$")
two_number_ins_regex = re.compile("^c\\.([0-9?+-]+)[_+-]([cC][.])*([0-9?+-]+)ins[ ]*(\S+)$")

one_number_del_regex = re.compile("^c\\.([0-9?+-]+)del[ ]*(\S*)$")
two_number_del_regex = re.compile("^c\\.([0-9?+-]+)[_+-]([cC][.])*([0-9?+-]+)del[ ]*(\S*)$")

one_number_dup_regex = re.compile("^c\\.([0-9?+-]+)dup$")
two_number_dup_regex = re.compile("^c\\.([0-9?+-]+)[_+-]([cC][.])*([0-9?+-]+)dup$")

qmark_regex = re.compile("^c\\.[?]$")

one_number_regex = re.compile("^c\\.([0-9?+-]+)(\S*)>(\S+)$")
two_number_regex = re.compile("^c\\.([0-9?+-]+)[_+-]([cC][.])*([0-9?+-]+)(\S*)>(\S+)$")


class cds_data:
	def __init__(self):
		self.mut_type = ""
		self.start = 0
		self.end = 0
		self.old_seq = ""
		self.new_seq = ""


def cds_matching(cds, record):

	stripped_cds = cds.translate(str.maketrans('', '', '()'))
	if stripped_cds == "c.?":
		pass
	elif "ins" in stripped_cds and "del" in stripped_cds:
		match_obj = two_number_indel_regex.match(stripped_cds)
		if match_obj:
			pass
		else:
			match_obj = one_number_indel_regex.match(stripped_cds)
			if not match_obj:
				print("failed cds match [indel]: %s\n%s" % (stripped_cds, "\t".join(record)), file=sys.stderr)
				sys.exit(-1)
	elif "ins" in stripped_cds:
		match_obj = two_number_ins_regex.match(stripped_cds)
		if match_obj:
			pass
		else:
			match_obj = one_number_ins_regex.match(stripped_cds)
			if not match_obj:
				print("failed cds match [ins]: %s\n%s" % (stripped_cds, "\t".join(record)), file=sys.stderr)
				sys.exit(-1)
	elif "del" in stripped_cds:
		match_obj = two_number_del_regex.match(stripped_cds)
		if match_obj:
			pass
		else:
			match_obj = one_number_del_regex.match(stripped_cds)
			if not match_obj:
				print("failed cds match [del]: %s\n%s" % (stripped_cds, "\t".join(record)), file=sys.stderr)
				sys.exit(-1)
	elif "dup" in stripped_cds:
		match_obj = two_number_dup_regex.match(stripped_cds)
		if match_obj:
			pass
		else:
			match_obj = one_number_dup_regex.match(stripped_cds)
			if not match_obj:
				print("failed cds match [dup]: %s\n%s" % (stripped_cds, "\t".join(record)), file=sys.stderr)
				sys.exit(-1)
	else:
		match_obj = two_number_regex.match(stripped_cds)
		if match_obj:
			pass
		else:
			match_obj = one_number_regex.match(stripped_cds)
			if not match_obj:
				print("failed cds match [mut]: %s\n%s" % (stripped_cds, "\t".join(record)), file=sys.stderr)
				sys.exit(-1)


@click.command(help="check cosmic prediction for mutation effects")
@click.option("--cosmic", type=click.Path(exists=True), required=True, help="cosmic TSV file")
@click.option("--maf", type=click.File('r'), required=True, help="Util file to be checked")
def cli(cosmic, maf):
	#CDS column: 18
	#genome version: 23
	#Genome position: 24    Format: CHR:START-END
	#Strand: 25
	#FATHMM prediction: 27

	position_matcher = re.compile("([0-9]+):([0-9]+)-([0-9]+)")
	COSMIC_IDS = dict()
	with open(cosmic, newline='') as cosmic_file:
		cosmic_reader = csv.reader(cosmic_file, dialect="excel-tab")
		first_line = next(cosmic_reader)
		for record in cosmic_reader:
			if record[16] in COSMIC_IDS:
				continue
			else:
				COSMIC_IDS[record[16]] = True
			skip_report = False
			cds = record[17]
			genome_version = record[22]
			position = record[23]
			strand = record[24]
			prediction = record[26]
			position_match_obj = position_matcher.match(position)
			if not position_match_obj:
				if len(position) != 0:
					print("failed match on position for %s" % position, file=sys.stderr)
				else:
					print("no position for entry: %s" % "\t".join(record), file=sys.stderr)
				skip_report = True
			cds_matching(cds, record)

			# if not skip_report:
			# 	report = list()
			# 	report.append(position_match_obj.group(1))
			# 	report.append(position_match_obj.group(2))
			# 	report.append(position_match_obj.group(3))
				# report.append(cds_match_obj.group(1))
				# report.append(cds_match_obj.group(2))
				# print("%s" % "\t".join(report))

if __name__ == "__main__":
	cli()
