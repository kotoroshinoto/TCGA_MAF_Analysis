#!/usr/bin/env python3
__author__ = 'mgooch'

#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import sys
import os
# import Annotation.MAF.File_Handlers.MAFreader as MAFreader
# import Annotation.MAF.Counters.MAFcounters as MAFcounters

from Annotation.CUSTOM.MAFSampleCountsList import MAFSampleCountsList

def main():
	parser = argparse.ArgumentParser(description="Count # of entries per gene in MAF file")
	parser.add_argument('--counts', type=argparse.FileType('r'), required=True, help="file containing sample counts")
	parser.add_argument('--boundaries', type=int, nargs='+', required=True, help="list of boundaries for splitting")
	args = parser.parse_args()

	scl = MAFSampleCountsList()
	scl.read_file_handle(args.counts)
	fixed_list = MAFSampleCountsList.fix_boundaries(args.boundaries)
	split_list = scl.split(fixed_list)
	for i in range(0,len(split_list)):
		print("list # %d" % i)
		print("%s" % split_list[i])


if __name__ == "__main__":
	main()