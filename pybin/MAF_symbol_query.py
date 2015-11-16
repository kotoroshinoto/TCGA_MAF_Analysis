#!/usr/bin/env python3
import sys
import os
import argparse
import MAFreader

def get_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Query MAF file for entries that have desired gene symbols")
	parser.add_argument('--maf', type=argparse.FileType('r'), required=True, help="file containing MAF entries")
	parser.add_argument('--out', type=argparse.FileType('w'), required=False, default=sys.stdout, help='path to file for output')
	query_mutex_group = parser.add_mutually_exclusive_group(required=True)
	query_mutex_group.add_argument('--query_list', type=str, nargs='+', help="list of gene symbols to use in query")
	query_mutex_group.add_argument('--query_file', type=argparse.FileType('r'), help="path to file containing list of gene symbols to use in query")
	parser.add_argument("--query_file_column", type=int, help="if query_file is TSV, select a column with this argument")
	return parser


def get_query_symbols(args, parser: argparse.ArgumentParser):
	symbols = dict()
	if args.query_list is not None:
		# print("list given")
		if args.query_file_column is not None:
			parser.error("--query_file_column cannot be specified when using --query_list")
			parser.print_help()
			parser.exit(-1)
		#pull symbols from command line args
		for symbol in args.query_list:
			if symbol not in symbols:
				symbols[symbol] = False
	if args.query_file is not None:
		# print("file given")
		if args.query_file_column is not None:
			# print("file column was given")
			#pull symbols from file splitting by tab and taking only the desired column
			for line in args.query_file:
				if line[0] == "#":
					continue
				line = line.rstrip()
				split_line = line.split("\t")
				symbol = split_line[args.query_file_column]
				if symbol not in symbols:
					symbols[symbol] = False
		else:
			# print("file column not given")
			#pull symbols from file treating entire line as symbol
			for line in args.query_file:
				if line[0] == "#":
					continue
				line = line.rstrip()
				if line not in symbols:
					symbols[line] = False
	return symbols


def main():
	parser = get_parser()
	args = parser.parse_args()
	symbols = get_query_symbols(args, parser)
	# for symbol in symbols:
	# 	print("%s" % (symbol))
	maf_file = args.maf
	out_file = args.out

	#read MAF lines from file, spit them out to output stream if their symbol matches one of the queries
	maf_file_reader = MAFreader.MAFFile()
	maf_file_reader.use_filehandle(maf_file)
	while maf_file_reader.has_more_entries():
		entry = maf_file_reader.get_next_entry()
		if entry.data['Hugo_Symbol'] in symbols:
			print("%s" % entry, file=args.out)
	return


if __name__ == "__main__":
	main()
