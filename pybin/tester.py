#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import sys
import os
import Annotation.MAF.File_Handlers.MAFreader as MAFreader


def main():
	parser = argparse.ArgumentParser(description="Count # of entries per gene in MAF file")
	parser.add_argument('--maf', type=argparse.FileType('r'), required=True, help="file containing MAF entries")
	args = parser.parse_args()

	#method 1
	# maf_handler = MAFreader.MAFfile()
	# maf_handler.use_filehandle(args.maf)
	# while True:
	# 	entry = maf_handler.get_next_entry()
	# 	if entry is None:
	# 		break
	# 	print("%s\t%s" % (entry.Hugo_Symbol, entry.Entrez_Gene_Id))


	#method 2
	entries = MAFreader.MAFFile.get_all_entries_from_filehandle(args.maf)
	for entry in entries:
		mutlist = entry.determine_mutation()
		print("%s\t%s\t%s" % (entry.Hugo_Symbol, entry.Entrez_Gene_Id, "\t".join(mutlist)))

if __name__ == "__main__":
	main()