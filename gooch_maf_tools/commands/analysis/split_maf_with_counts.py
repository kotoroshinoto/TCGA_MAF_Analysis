#!/usr/bin/env python3
import click
import os
import sys
from gooch_maf_tools.formats import MAF
from gooch_maf_tools.util.MAFSampleCountsList import MAFSampleCountsList

__author__ = 'mgooch'


def generate_file_handles(maf, bounds, prefix=None):
	handles = list()
	for i in range(len(bounds)):
		bounds[i] = int(bounds[i])

	sorted_bounds = sorted(bounds)
	if prefix is None:
		maf_path = maf.name
		maf_filename = os.path.split(maf_path)[1]
		prefix = os.path.splitext(maf_filename)[0]
	low = 1
	#3 bounds, 4 groups  x < bound1, bound1 <= x < bound2
	paths = list()
	for i in range(0, len(sorted_bounds) + 1):
		if i == len(sorted_bounds):
			paths.append("%s.%s-above.maf" % (prefix, low))
			print("%s.%s-above.maf" % (prefix, low))
		else:
			high = sorted_bounds[i]
			paths.append("%s.%s-%s.maf" % (prefix, low, high - 1))
			print("%s.%s-%s.maf" % (prefix, low, high - 1))
		low = high
	for path in paths:
		handles.append(open(path, mode='w'))
	return handles


@click.command(help="Split MAF file based on # of counts for categories in a column")
@click.option('--counts', type=click.File('r'), required=True, help="file containing sample counts")
@click.option('--maf', type=click.File('r'), required=True, help="maf file to split")
@click.option('--key', type=int, required=True, help="0-based column number to use as key in maf file")
@click.option('--out_prefix', default="", type=str, required=False, help="output path prefix")
@click.option('--boundaries', type=str, required=True, help="list of boundaries for splitting")
def cli(counts, boundaries, maf, key, out_prefix):
	scl = MAFSampleCountsList()
	fixed_list = MAFSampleCountsList.fix_boundaries(boundaries.split(","))
	if out_prefix is not None:
		handles = generate_file_handles(maf, fixed_list, out_prefix)
		""":type : list[io.TextIOBase]"""
	else:
		handles = generate_file_handles(maf, fixed_list)
		""":type : list[io.TextIOBase]"""
	scl.read_file_handle(counts)
	split_list = scl.split(fixed_list)

	entries = MAF.EntryReader.get_all_entries_from_filehandle(maf)
	maf.close()

	#write initial header line to all output files
	#TODO use CSV handler or a built in function to the class to do this more elegantly
	for handle in handles:
		print("\t".join(entries[0].fieldnames), file=handle)

	for entry in entries:
		target_list = -1
		for i in range(0, len(split_list)):
			if entry.get_data(key) in split_list[i]:
				if target_list != -1:
					print("util entry: %s, is in multiple lists\n" % entry.get_data(key), file=sys.stderr)
					sys.exit(-1)
				target_list = i
				# print("key %s belongs in list # %d" % (entry.data[MAF.Entry.get_heading(key)], i))
				print("%s" % entry, file=handles[i])
		if target_list == -1:
			print("util key: %s, doesn't exist in any of the lists\n" % entry.get_data(key), file=sys.stderr)
			sys.exit(-1)
	# for i in range(0, len(split_list)):
	# 	print("list # %d" % i)
	# 	print("%s" % split_list[i])


if __name__ == "__main__":
	cli()