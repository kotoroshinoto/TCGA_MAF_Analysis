#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import sys
import os
# import Annotation.MAF.File_Handlers.MAFreader as MAFreader
# import Annotation.MAF.Counters.MAFcounters as MAFcounters

from Annotation.CUSTOM.MAFSampleCountsList import MAFSampleCountsList

def main():
	# parser = argparse.ArgumentParser(description="Count # of entries per gene in MAF file")
	# parser.add_argument('--counts', type=argparse.FileType('r'), required=True, help="file containing sample counts")
	# parser.add_argument('--boundaries', type=int, nargs='+', required=True, help="list of boundaries for splitting")
	# args = parser.parse_args()

	scl = MAFSampleCountsList()
	fixed_list = MAFSampleCountsList.fix_boundaries([1, 2, 1, 2])
	scl.split(fixed_list)


if __name__ == "__main__":
	main()