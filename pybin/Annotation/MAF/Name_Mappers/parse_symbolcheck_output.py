#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import re
import sys
parser = argparse.ArgumentParser(description="Compute exonic sizes of genes and relate them to HUGO IDs")
parser.add_argument('--symbolcheck', type=argparse.FileType('r'), required=True, help="TSV output from http://www.genenames.org/cgi-bin/symbol_checker")
parser.add_argument('--outApproved', type=argparse.FileType('w'), required=True, help="file to write approved symbols to")
parser.add_argument('--outUnmatched', type=argparse.FileType('w'), required=True, help="file to write unmatched symbols to")
parser.add_argument('--outCorrected', type=argparse.FileType('w'), required=True, help="file to write symbols that were corrected to")
args = parser.parse_args()

#build map of names from symbolcheck file
symbolcheck_approved = dict()
symbolcheck_unmatched = list()
symbolcheck_updated = dict()
symbolcheck_synonyms = dict()
symbolcheck_withdrawn = list()

first_line = True
if args.symbolcheck is not None:
	for line in args.symbolcheck:
		if first_line:
			first_line = False
			continue
		split_line = line.split("\t")
		category = split_line[1].rstrip()
		old_symbol = split_line[0].rstrip()
		if category == "Unmatched":
			symbolcheck_unmatched.append(old_symbol)
			continue
		elif category == "Withdrawn":
			symbolcheck_withdrawn.append(old_symbol)
			continue
		new_symbol = split_line[2].rstrip()
		if category == "Approved symbol":
			symbolcheck_approved[old_symbol] = new_symbol
		elif category == "Previous symbol":
			symbolcheck_updated[old_symbol] = new_symbol
		elif category == "Synonyms":
			symbolcheck_synonyms[old_symbol] = new_symbol
		else:
			print("unrecognized category: %s" % category, file=sys.stderr)

for symbol in symbolcheck_approved:
	print("%s\t%s" % (symbol, symbolcheck_approved[symbol]), file=args.outApproved)
for symbol in symbolcheck_unmatched:
	print("%s\t" % symbol, file=args.outUnmatched)
for symbol in symbolcheck_updated:
	print("%s\t%s" % (symbol, symbolcheck_updated[symbol]), file=args.outCorrected)
for symbol in symbolcheck_synonyms:
	if symbol not in symbolcheck_approved and symbol not in symbolcheck_updated:
		print("%s\t%s" % (symbol, symbolcheck_synonyms[symbol]), file=args.outCorrected)
for symbol in symbolcheck_withdrawn:
	print("[WARNING] symbol withdrawn: %s ", file=sys.stderr)