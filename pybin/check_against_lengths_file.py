#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import re
import sys
import os

parser = argparse.ArgumentParser(description="Check Util names against names in Gene Length files")
parser.add_argument('--mafnames', type=argparse.FileType('r'), required=True, help="file of names to be translated")
parser.add_argument('--checkcolumn', type=int, help="check this column instead of oldcolumn")
parser.add_argument('--oldcolumn', type=int, default=0, help="this column is the original name")
parser.add_argument('--genelength', type=argparse.FileType('r'), required=True, help="file of gene lengths that has names", nargs='+')
parser.add_argument('--matched', type=argparse.FileType('w'), required=True, help="file to write matched names")
parser.add_argument('--unmatched', type=argparse.FileType('w'), required=True, help="file to write unmatched names")
parser.add_argument('--keep', default=False, action='store_true', help="put checked label in 2nd column even if unmatched")
parser.add_argument('--logOK', default=os.devnull, type=argparse.FileType('w'), help="log OK output to this file")
parser.add_argument('--logBAD', default=os.devnull, type=argparse.FileType('w'), help="log BAD output to this file")

args = parser.parse_args()

MAF_original_names = dict()
MAF_names = dict()

oldcolumn = args.oldcolumn
checkcolumn = oldcolumn
if args.checkcolumn is not None:
	checkcolumn = args.checkcolumn

#pull Util names from file
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
for lengthfile in args.genelength:
	print("reading file: %s" % lengthfile.name)
	for line in lengthfile:
		if len(line) > 0:
			split_line = line.split("\t")
			symbol = split_line[0].rstrip()
			if len(symbol) > 0:
				if symbol.upper() not in Length_File_Name_List:
					Length_File_Name_List[symbol.upper()] = symbol
	lengthfile.close()

for check_symbol in MAF_names:
	if check_symbol in Length_File_Name_List:
		if oldcolumn != checkcolumn:
			print("checked name OK for: %s -> %s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=args.logOK)
		else:
			print("checked name OK for: %s" % (MAF_names[check_symbol]), file=args.logOK)
		print("%s\t%s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=args.matched)
	else:
		if oldcolumn != checkcolumn:
			print("checked name BAD for: %s - > %s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=args.logBAD)
		else:
			print("checked name BAD for: %s" % (MAF_names[check_symbol]), file=args.logBAD)
		if args.keep:
			print("%s\t%s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=args.unmatched)
		else:
			print("%s\t" % MAF_original_names[check_symbol], file=args.unmatched)
args.matched.close()
args.unmatched.close()
