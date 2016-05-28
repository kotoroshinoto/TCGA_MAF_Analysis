import click
import sys
import os
import csv

input_tsv = dict()
input_files = dict()
output_tsv = None
output_file = None

labels = list()


@click.group(help="This program is intended to be used to merge tabular count files produced by different MAF files. Will insert zeroes for missing values", name="COUNT_merge")
@click.option("--in", "infile", nargs=2, type=(str, click.File('r')), required=True, multiple=True, help="string is label to use in output, file is file containing the type of counts you are trying to merge")
@click.option("--out", type=click.Path(dir_okay=False, writable=True), required=True, help="file to write output to")
def cli(infile, out):
	global input_tsv
	global input_files
	global output_tsv
	global output_file
	for in_pair in infile:
		label = in_pair[0]
		in_file = in_pair[1]
		if label in labels:
			raise click.BadOptionUsage("cannot use the same label more than once")
		labels.append(in_pair[0])
		input_files[label] = in_file
		input_tsv[label] = csv.reader(in_file, dialect="excel-tab")
	output_file = open(out, 'w', newline='')
	output_tsv = csv.writer(output_file, dialect="excel-tab")

	pass


@cli.command(name="mutation_type", help="")
def merge_mutation_type():
	global output_tsv
	# click.echo("[merge_mutation_type]")
	column_keys = list()
	column_keys.append("MUTATION_TYPE")
	counts = dict()
	for label in labels:
		# click.echo("[merge_mutation_type] label: %s" % label)
		column_keys.append("%s_COUNT" % label)
		tsv_reader = input_tsv[label]
		for line in tsv_reader:
			#check for header lines
			if line[0] == column_keys[0]:
				continue
			mutation_type = line[0]
			count = line[1]
			# click.echo("[merge_mutation_type] mutation_type: %s | count %s" % (mutation_type, count))
			if mutation_type not in counts:
				counts[mutation_type] = dict()
			counts[mutation_type][label] = count
	output_tsv.writerow(column_keys)
	for mutation_type in counts:
		tsv_row = list()
		tsv_row.append(mutation_type)
		for label in labels:
			if label in counts[mutation_type]:
				tsv_row.append(counts[mutation_type][label])
			else:
				tsv_row.append(0)
		output_tsv.writerow(tsv_row)


@cli.command(name="genes", help="")
def merge_genes():
	global output_tsv
	# click.echo("[merge_genes]")
	column_keys = list()
	column_keys.append("GENE_SYMBOL")
	counts = dict()
	for label in labels:
		# click.echo("[merge_genes] label: %s" % label)
		column_keys.append("%s_COUNT" % label)
		tsv_reader = input_tsv[label]
		for line in tsv_reader:
			# check for header lines
			if line[0] == column_keys[0]:
				continue
			gene_symbol = line[0]
			count = line[1]
			# click.echo("[merge_genes] gene_symbol: %s | count %s" % (gene_symbol, count))
			if gene_symbol not in counts:
				counts[gene_symbol] = dict()
			counts[gene_symbol][label] = count
	output_tsv.writerow(column_keys)
	for gene_symbol in counts:
		tsv_row = list()
		tsv_row.append(gene_symbol)
		for label in labels:
			if label in counts[gene_symbol]:
				tsv_row.append(counts[gene_symbol][label])
			else:
				tsv_row.append(0)
		output_tsv.writerow(tsv_row)


@cli.command(name="locations", help="")
def merge_locations():
	global output_tsv
	# click.echo("[merge_locations]")
	column_keys = list()
	column_keys.append("GENE_SYMBOL")
	column_keys.append("CHROM")
	column_keys.append("START")
	column_keys.append("END")
	counts = dict()
	for label in labels:
		# click.echo("[merge_locations] label: %s" % label)
		column_keys.append("%s_COUNT" % label)
		tsv_reader = input_tsv[label]
		for line in tsv_reader:
			# check for header lines
			# print(','.join(line))
			if line[0] == 'GENE_SYMBOL' and line[1] == 'CHROM' and line[2] == 'START' and line[3] == 'END' and line[4] == 'COUNT':
				# print("HEADER LINE DETECTED")
				continue
			tmp_lst = list(line)
			count = tmp_lst.pop()
			location_key = '|'.join(tmp_lst)
			# click.echo("[merge_locations] location_key: %s | count %s" % (location_key, count))
			if location_key not in counts:
				counts[location_key] = dict()
			counts[location_key][label] = count
	output_tsv.writerow(column_keys)
	for location_key in counts:
		tsv_row = list()
		tsv_row+=location_key.split('|')
		for label in labels:
			if label in counts[location_key]:
				tsv_row.append(counts[location_key][label])
			else:
				tsv_row.append(0)
		output_tsv.writerow(tsv_row)


@cli.command(name="locations_mut_specific", help="")
def merge_mutation_specific_locations():
	global output_tsv
	# click.echo("[merge_mut_specific_locations]")
	column_keys = list()
	column_keys.append("GENE_SYMBOL")
	column_keys.append("CHROM")
	column_keys.append("START")
	column_keys.append("END")
	column_keys.append("MUT_TYPE")
	column_keys.append("VARIANT_TYPE")
	column_keys.append("VARIANT_CLASS")
	counts = dict()
	for label in labels:
		# click.echo("[merge_mut_specific_locations] label: %s" % label)
		column_keys.append("%s_COUNT" % label)
		tsv_reader = input_tsv[label]
		for line in tsv_reader:
			# check for header lines
			# print(','.join(line))
			if line[0] == 'GENE_SYMBOL' and line[1] == 'CHROM' and line[2] == 'START' and line[3] == 'END' and line[4] == 'MUT_TYPE' and line[5] == 'VARIANT_TYPE' and line[6] == 'VARIANT_CLASS' and line[7] == 'COUNT':
				# print("HEADER LINE DETECTED")
				continue
			tmp_lst = list(line)
			count = tmp_lst.pop()
			location_key = '|'.join(tmp_lst)
			# click.echo("[merge_mut_specific_locations] location_key: %s | count %s" % (location_key, count))
			if location_key not in counts:
				counts[location_key] = dict()
			counts[location_key][label] = count
	output_tsv.writerow(column_keys)
	for location_key in counts:
		tsv_row = list()
		tsv_row += location_key.split('|')
		for label in labels:
			if label in counts[location_key]:
				tsv_row.append(counts[location_key][label])
			else:
				tsv_row.append(0)
		output_tsv.writerow(tsv_row)
	pass
