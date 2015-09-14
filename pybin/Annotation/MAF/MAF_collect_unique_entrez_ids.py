#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import sys
parser = argparse.ArgumentParser(description="Collect Unique entries from first two columns of MAF file")
parser.add_argument('--maf', type=argparse.FileType('r'), required=True, help="file to collect names from")
parser.add_argument('--out', type=argparse.FileType('w'), default=sys.stdout, help="file to use for output")

args = parser.parse_args()
Names = list()
#Entrez_IDs = list()

for line in args.maf:
	line = line.rstrip()
	if len(line) <= 0:
		continue
	line_split = line.split("\t")
	if len(line_split) < 2:
		continue
	symbol = line_split[0].rstrip()
	entrez_id = line_split[1].rstrip()
	if entrez_id != "0" and symbol not in Names:
		Names.append(symbol)
		#Entrez_IDs.append(line_split[1])
		print("%s\t%s" % (line_split[0], line_split[1]))
#TODO write symbols with no entrez ID to a different file