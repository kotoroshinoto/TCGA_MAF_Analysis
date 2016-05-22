#!/usr/bin/env python3
import os
import sys
import click
import re

@click.command()
@click.argument('cosmic_file', type=click.File('r'), required=True)
@click.argument('output_file', type=click.File('w'), required=False, default=sys.stdout)
def cli(cosmic_file, output_file):
	"""replaces SYMBOL_JUNK with SYMBOL in column 0 of COSMIC entries where _JUNK matches the following formats:

	\b
	_ENST*
	_HUMAN
	_NEW
	_NM_*
	_same_name
	_cluster

	\b
	COSMIC_FILE\tpath to COSMIC TSV file
	OUTPUT_FILE\tpath to write output to [defaults to <stdin>]"""

	# formats
	# SYMBOL_ENST*
	# SYMBOL_HUMAN
	# SYMBOL_NEW
	# SYMBOL_NM_*
	# SYMBOL_same_name
	# SYMBOL_cluster
	non_empty_non_whitespace_word = "\S+"
	possibly_empty_non_whitespace_word = "\S*"
	enst_case = "_ENST"
	human_case = "_HUMAN"
	new_case = "_NEW"
	nm_case = "_NM_"
	same_name_case = "_SAME_NAME"
	cluster_case = "_CLUSTER"
	combined_cases = "|".join([enst_case, human_case, new_case, nm_case, same_name_case, cluster_case])
	regex_string ="(%s)(%s)(%s)" % (non_empty_non_whitespace_word, combined_cases, possibly_empty_non_whitespace_word)
	# print(regex_string)
	compiled_regex = re.compile(regex_string)
	first_line = True
	# input_line_count = 0
	# output_line_count = 0
	for line in cosmic_file:
		# input_line_count += 1
		assert(isinstance(line, str))
		if first_line:
			first_line = False
			if line.startswith("Gene name"):
				print(line.rstrip("\n"), file=output_file)
				# output_line_count += 1
				continue
		split_line = line.split("\t")
		gene_name = split_line[0].upper().rstrip()
		match_obj = compiled_regex.match(gene_name)
		if match_obj:
			# print(match_obj.group(1))
			split_line[0] = split_line[0][0:len(match_obj.group(1))]
			print(("\t".join(split_line)).rstrip("\n"), file=output_file)
			# output_line_count += 1
		else:
			print(line.rstrip("\n"), file=output_file)
			# output_line_count += 1

if __name__ == "__main__":
	cli()
