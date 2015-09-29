#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import sys
import os
import Annotation.MAF.File_Handlers.MAFreader as MAFreader
import Annotation.MAF.Counters.MAFcounters as MAFcounters

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
	mut_type_counter = MAFcounters.MutTypeCounter()
	samp_counter = MAFcounters.SampMutCounter()
	gene_counter = MAFcounters.GeneMutCounter()
	for entry in entries:
		mut_type_counter.count(entry)
		samp_counter.count(entry)
		gene_counter.count(entry)
	# sys.stdout.write("%s" % mut_type_counter)
	print("# of samples: %d" % len(samp_counter.counts.keys()))
	sys.stdout.write("%s" % samp_counter)
	# sys.stdout.write("%s" % gene_counter)

if __name__ == "__main__":
	main()