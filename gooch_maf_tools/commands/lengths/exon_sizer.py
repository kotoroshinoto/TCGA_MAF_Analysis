#!/usr/bin/env python3
__author__ = 'mgooch'
import click
import sys


def next_bed(line):
	line = line.rstrip()
	split_line = line.split("\t")
	name = split_line[3].rstrip()

	lengths = split_line[10].split(',')
	total_length = 0
	for length in lengths:
		if len(length) > 0:
			total_length += int(length)
	#print("%s\t%s" %(name, total_length))
	return [name, total_length]


def next_name(line, col_from, col_to):
	line = line.rstrip()
	if len(line) == 0:
		return None
	split_line = line.split("\t")
	#print("# of columns: %d" % (len(split_line)))
	if len(split_line) <= col_from or len(split_line) <= col_to:
		return None
	name_from = split_line[col_from].rstrip()
	if len(name_from) == 0:
		return None
	name_to = split_line[col_to].rstrip()
	#print("%s -> %s" %(name_from, name_to))
	return [name_from, name_to]


def read_bed_and_map_names(bed_handle, name_map):
	bed_exon_length_map = dict()
	for bedline in bed_handle:
		bedtuple = next_bed(bedline)
		gene_name = name_map[bedtuple[0]]
		length = bedtuple[1]
		if gene_name not in bed_exon_length_map:
			bed_exon_length_map[gene_name] = list()
		bed_exon_length_map[gene_name].append(length)
	return bed_exon_length_map


def merge_and_write_bed_dicts(primary, secondary, outfilehandle):

	if (primary is None) and (secondary is None):
		return

	#warning, the names from both dicts should be mapped prior to doing this
	#primary names will take priority, taking entries from secondary only if they don't already exist within the dict
	merged = dict()

	def do_output_for_dict(current_dict, merged_dict):
		for entry in current_dict:
			if entry in merged_dict:
				continue
			else:
				merged_dict[entry] = True
			value_list = current_dict[entry]
			average = sum(value_list) / len(value_list)
			print("%s\t%d" % (entry, average), file=outfilehandle)
	if primary is not None:
		do_output_for_dict(primary, merged)
	if secondary is not None:
		do_output_for_dict(secondary, merged)
	return


def read_namefile(handlelist):
	from_col = handlelist[2]
	to_col = handlelist[3]
	name_map = dict()
	#build map of names
	for name in handlelist[1]:
		nametuple = next_name(name, from_col, to_col)
		if nametuple is not None:
			name_map[nametuple[0]] = nametuple[1]
	return name_map


def read_files_and_map_names(handlelist):
	name_map = read_namefile(handlelist)
	return read_bed_and_map_names(handlelist[0], name_map)


def argcheck(parser):
	args = parser.parse_args()
	ucsc_files = args.ucsc is not None
	ucsc_col = args.ucsc_col is not None
	refseq_files = args.refseq is not None
	refseq_col =args.refseq_col is not None
	ucsc_both_missing = (not ucsc_files) and (not ucsc_col)
	refseq_both_missing = (not refseq_files) and (not refseq_col)

	ucsc_missing_cols = ucsc_files and (not ucsc_col)
	ucsc_missing_files = (not ucsc_files) and ucsc_col

	refseq_missing_cols = refseq_files and (not refseq_col)
	refseq_missing_files = (not refseq_files) and refseq_col

	err_msg = ""
	if ucsc_both_missing and refseq_both_missing:
		err_msg += "\nMust provide at least one set of files and column entries"
	if ucsc_missing_cols:
		err_msg += "\nmissing --ucsc_col argument, must provide both column argument and files argument or neither"
	if refseq_missing_cols:
		err_msg += "\nmissing --refseq_col argument, must provide both column argument and files argument or neither"
	if ucsc_missing_files:
		err_msg += "\nmissing --ucsc argument, must provide both column argument and files argument or neither"
	if refseq_missing_files:
		err_msg += "\nmissing --refseq argument, must provide both column argument and files argument or neither"
	if err_msg != "":
		parser.error(err_msg)
	return args


# @click.option('--ucsc_col', type=int, nargs=2, help="")
# @click.option('--refseq_col', type=int, nargs=2, help="")
@click.command(help="Compute exonic sizes of genes and relate them to HUGO IDs")
@click.option('--ucsc', type=(click.File('r'), click.File('r'), int, int), help="first path is to a bed file containing genes & exons from UCSC, \n2nd path is to path to a file relating BED file names to desired names. \nInts are a pair of 0-based index values for parsing the names file, first column's names match those from the BED file, second names match those to use in the output")
@click.option('--refseq', type=(click.File('r'), click.File('r'), int, int), help="first path is to a bed file containing genes & exons from REFSEQ, \n2nd path is to path to a file relating BED file names to desired names. \nInts are a pair of 0-based index values for parsing the names file, first column's names match those from the BED file, second names match those to use in the output")
@click.option('--out', type=click.File('w'), default=sys.stdout, help="output file")
def cli(ucsc, refseq, out):
	if len(refseq) == 0 and len(ucsc) == 0:
		raise click.BadArgumentUsage("Must give at least one of the following: --ucsc --refseq")
	if len(ucsc) == 4:
		ucsc_bed = read_files_and_map_names(ucsc)
	else:
		ucsc_bed = None
	if len(refseq) == 4:
		refseq_bed = read_files_and_map_names(refseq)
	else:
		refseq_bed = None

	return merge_and_write_bed_dicts(ucsc_bed, refseq_bed, out)


if __name__ == "__main__":
	cli()
