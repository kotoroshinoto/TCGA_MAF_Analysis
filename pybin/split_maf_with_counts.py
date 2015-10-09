#!/usr/bin/env python3
import argparse
import os

import MAFreader as MAFreader
from MAFSampleCountsList import MAFSampleCountsList

__author__ = 'mgooch'


def generate_file_handles(args, parser, bounds, prefix=None):
	handles = list()
	sorted_bounds = sorted(bounds)
	if prefix is None:
		maf_path = args.maf.name
		maf_filename = os.path.split(maf_path)[1]
		prefix = os.path.splitext(maf_filename)[0]
	low = 1
	#3 bounds, 4 groups  x < bound1, bound1 <= x < bound2
	paths = list()
	for i in range(0, len(bounds) + 1):
		if i == len(bounds):
			paths.append("%s.%s-above.maf" % (prefix, low))
			print("%s.%s-above.maf" % (prefix, low))
		else:
			high = bounds[i]
			paths.append("%s.%s-%s.maf" % (prefix, low, high - 1))
			print("%s.%s-%s.maf" % (prefix, low, high - 1))
		low = high
	for path in paths:
		handles.append(open(path, mode='w'))
	return handles


def main():
	parser = argparse.ArgumentParser(description="Count # of entries per gene in MAF file")
	parser.add_argument('--counts', type=argparse.FileType('r'), required=True, help="file containing sample counts")
	parser.add_argument('--boundaries', type=int, nargs='+', required=True, help="list of boundaries for splitting")
	parser.add_argument('--maf', type=argparse.FileType('r'), required=True, help="maf file to split")
	parser.add_argument('--key', type=int, required=True, help="0-based column number to use as key in maf file")
	parser.add_argument('--out_prefix', type=str, required=False, help="output path prefix")
	args = parser.parse_args()

	scl = MAFSampleCountsList()
	fixed_list = MAFSampleCountsList.fix_boundaries(args.boundaries)
	if args.out_prefix:
		handles = generate_file_handles(args, parser, fixed_list, args.out_prefix)
		""":type : list[io.TextIOBase]"""
	else:
		handles = generate_file_handles(args, parser, fixed_list)
		""":type : list[io.TextIOBase]"""
	scl.read_file_handle(args.counts)
	split_list = scl.split(fixed_list)

	entries = MAFreader.MAFFile.get_all_entries_from_filehandle(args.maf)
	args.maf.close()

	for entry in entries:
		target_list = -1
		for i in range(0, len(split_list)):
			if entry.data[MAFreader.MAFEntry.get_heading(args.key)] in split_list[i]:
				if target_list != -1:
					parser.exit(-1, "MAF entry: %s, is in multiple lists\n" % entry.data[
						MAFreader.MAFEntry.get_heading(args.key)])
				target_list = i
				# print("key %s belongs in list # %d" % (entry.data[MAFreader.MAFEntry.get_heading(args.key)], i))
				print("%s" % entry, file=handles[i])
		if target_list == -1:
			parser.exit(-1, "MAF key: %s, doesn't exist in any of the lists\n" % entry.data[
				MAFreader.MAFEntry.get_heading(args.key)])
	# for i in range(0, len(split_list)):
	# 	print("list # %d" % i)
	# 	print("%s" % split_list[i])


if __name__ == "__main__":
	main()