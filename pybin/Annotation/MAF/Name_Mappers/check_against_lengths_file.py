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
mafnames_fh = args.mafnames
MAF_names = list()

#pull MAF names from file
for line in mafnames_fh:
	line = line.rstrip()
	if len(line) > 0:
		MAF_names.append(line)
mafnames_fh.close()

#build list of names from size file if one was given
Length_File_Name_List = list()

for line in args.genelength:
	line = line.rstrip()
	if len(line) > 0:
		split_line = line.split("\t")
		name = split_line[0]
		Length_File_Name_List.append(name)
		#print("added name: %s" % name)
args.genelength.close()

for name in MAF_names:
	if name in Length_File_Name_List:
		print("original name OK for: %s" % name, file=sys.stderr)
		print(name, file=args.matched)
	else:
		print("original name BAD for: %s" % name, file=sys.stderr)
		print(name, file=args.unmatched)
args.matched.close()
args.unmatched.close()
