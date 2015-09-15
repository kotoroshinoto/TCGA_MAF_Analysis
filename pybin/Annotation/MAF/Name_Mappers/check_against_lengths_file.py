#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import re
import sys
parser = argparse.ArgumentParser(description="Check MAF names against names in Gene Length files")
parser.add_argument('--mafnames', type=argparse.FileType('r'), required=True, help="file of names to be translated")
parser.add_argument('--checkcolumn', type=int, help="check this column instead of oldcolumn")
parser.add_argument('--oldcolumn', type=int, default=0, help="this column is the original name")
parser.add_argument('--genelength', type=argparse.FileType('r'), required=True, help="file of gene lengths that has names")
parser.add_argument('--matched', type=argparse.FileType('w'), required=True, help="file to write matched names")
parser.add_argument('--unmatched', type=argparse.FileType('w'), required=True, help="file to write unmatched names")
parser.add_argument('--keep', default=False, action='store_true', help="keep newcolumn (or oldcolumn if not set) label in 2nd column if unmatched")

args = parser.parse_args()

MAF_original_names = dict()
MAF_names = dict()

oldcolumn = args.oldcolumn
checkcolumn = oldcolumn

if not hasattr(args, 'newcolumn'):
	checkcolumn = args.checkcolumn

#pull MAF names from file
for line in args.mafnames:
	if len(line) > 0:
		split_line = line.split("\t")
		old_symbol = split_line[oldcolumn].rstrip()
		check_symbol = split_line[checkcolumn].rstrip()
		if len(check_symbol) > 0:
			MAF_names[check_symbol.upper()] = check_symbol
			if len(old_symbol) == 0:
				print("[WARNING] missing original symbol for checked symbol: %s" % check_symbol)
			MAF_original_names[check_symbol.upper()] = old_symbol
args.mafnames.close()

#build list of names from size file if one was given
Length_File_Name_List = dict()

for line in args.genelength:
	if len(line) > 0:
		split_line = line.split("\t")
		symbol = split_line[0].rstrip()
		if len(symbol) > 0:
			Length_File_Name_List[symbol.upper()] = symbol
args.genelength.close()

for check_symbol in MAF_names:
	if check_symbol in Length_File_Name_List:
		if oldcolumn != checkcolumn:
			print("checked name OK for: %s -> %s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=sys.stderr)
		else:
			print("checked name OK for: %s" % (MAF_names[check_symbol]), file=sys.stderr)
		print("%s\t%s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=args.matched)
	else:
		if oldcolumn != checkcolumn:
			print("checked name BAD for: %s - > %s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=sys.stderr)
		else:
			print("checked name BAD for: %s" % (MAF_names[check_symbol]), file=sys.stderr)
		if args.keep:
			print("%s\t%s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=args.unmatched)
		else:
			print("%s\t" % MAF_original_names[check_symbol], file=args.unmatched)
args.matched.close()
args.unmatched.close()
