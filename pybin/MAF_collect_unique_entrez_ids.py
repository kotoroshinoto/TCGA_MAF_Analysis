#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import sys
parser = argparse.ArgumentParser(description="Collect Unique entries from first two columns of MAF file")
parser.add_argument('--maf', type=argparse.FileType('r'), required=True, help="file to collect names from")
parser.add_argument('--out', type=argparse.FileType('w'), required=True, help="file to use for output")
parser.add_argument('--outNoEntrez', type=argparse.FileType('w'), help="file to use for output names lacking entrez IDs")

args = parser.parse_args()
Names = list()
#Entrez_IDs = list()
first_line_skipped = False
for line in args.maf:
	if not first_line_skipped:
		first_line_skipped = True
		continue
	line = line.rstrip()
	if len(line) <= 0:
		continue
	line_split = line.split("\t")
	if len(line_split) < 2:
		continue
	symbol = line_split[0].rstrip()
	entrez_id = line_split[1].rstrip()
#write symbols with no entrez ID to a different file if wanted
	if symbol not in Names:
		Names.append(symbol)
		#Entrez_IDs.append(line_split[1])
		if entrez_id != "0":
			print("%s\t%s" % (line_split[0], line_split[1]), file=args.out)
		else:
			if args.outNoEntrez is not None:
				print("%s\t" % line_split[0], file=args.outNoEntrez)
