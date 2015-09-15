#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import re
import sys
parser = argparse.ArgumentParser(description="Check MAF names against names in Gene Length files")
parser.add_argument('--mafnames', type=argparse.FileType('r'), required=True, help="file of names to be translated")
parser.add_argument('--genelength', type=argparse.FileType('r'), required=True, help="file of gene lengths that has names")
parser.add_argument('--matched', type=argparse.FileType('w'), required=True, help="file to write matched names")
parser.add_argument('--unmatched', type=argparse.FileType('w'), required=True, help="file to write unmatched names")

args = parser.parse_args()

MAF_names = dict()

#pull MAF names from file
for line in args.mafnames:
	if len(line) > 0:
		split_line = line.split("\t")
		symbol = split_line[0].rstrip()
		if len(symbol) > 0:
			MAF_names[symbol.upper()] = symbol
args.mafnames.close()

#build list of names from size file if one was given
Length_File_Name_List = dict()

for line in args.genelength:
	if len(line) > 0:
		split_line = line.split("\t")
		name = split_line[0].rstrip()
		if len(name) > 0:
			Length_File_Name_List[name.upper()] = name
args.genelength.close()

for name in MAF_names:
	if name in Length_File_Name_List:
		print("original name OK for: %s" % MAF_names[name], file=sys.stderr)
		print("%s\t%s" % (MAF_names[name], MAF_names[name]), file=args.matched)
	else:
		print("original name BAD for: %s" % MAF_names[name], file=sys.stderr)
		print("%s\t" % MAF_names[name], file=args.unmatched)
args.matched.close()
args.unmatched.close()
