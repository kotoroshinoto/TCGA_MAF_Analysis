#!/usr/bin/env python3
import argparse
import os
import sys

import GenericFormats.MAF
import Util.MAFcounters

__author__ = 'mgooch'


def generate_file_handles(args, outpath, parser):
	maf_path = args.maf.name
	maf_path_split = os.path.split(maf_path)
	if args.nameprefix == "":
		prefix = maf_path_split[1]
	else:
		split_nameprefix = os.path.split(args.nameprefix)
		if split_nameprefix[0] != "":
			parser.exit("Name prefix may not contain path separators! %s\n" % args.nameprefix)
		prefix = args.nameprefix
	print()
	out_handles = dict()
	if args.muttype:
		out_handles["MUT_TYPE"] = open(os.path.join(outpath, (prefix + ".mutation_type.counts")), mode='w')
	if args.sample:
		out_handles["SAMPLE"] = open(os.path.join(outpath, (prefix + ".sample.counts")), mode='w')
	if args.gene:
		out_handles["GENE"] = open(os.path.join(outpath, (prefix + ".gene.counts")), mode='w')
	return out_handles


def handle_outpath_arg(args, parser):
	if args.out == "":
		if args.nameprefix:
			print("[WARNING] argument --nameprefix does nothing if outpath is not defined, script will use stdout for all output", file=sys.stderr)
		out_handles = dict()
		if args.muttype:
			out_handles["MUT_TYPE"] = sys.stdout
		if args.sample:
			out_handles["SAMPLE"] = sys.stdout
		if args.gene:
			out_handles["GENE"] = sys.stdout
		return out_handles
	else:
		outpath = os.path.realpath(os.path.abspath(args.out))
		parent_outpath = os.path.realpath(os.path.abspath(os.path.join(outpath, "..")))
		if not os.path.exists(parent_outpath):
			if outpath != args.out:
				parser.exit(-1, "parent path of %s [absolute real path: %s], which resolves to %s, does not exist\n" % (args.out, outpath, parent_outpath))
			else:
				parser.exit(-1, "parent path of %s, which resolves to %s does not exist\n" % (args.out, outpath))
		if os.path.exists(outpath) and os.path.isdir(outpath):
			#craft default filename from maf file + countype.counts
			return generate_file_handles(args, outpath, parser)
		elif not os.path.exists(outpath):
			#path does not yet exist, but parent path does
			#create path automatically, then create the filehandles
			os.mkdir(outpath)
			return generate_file_handles(args, outpath, parser)
		else:
			#file exists and is not a directory
			if args.nameprefix:
				print("[WARNING] argument --nameprefix does nothing if outpath points to a path that exists and is not a directory , script will use defined path for all output", file=sys.stderr)
			if outpath != args.out:
				print("[WARNING] %s [absolute real path: %s] points to an existing file, not a directory" % (args.out, outpath), file=sys.stderr)
			else:
				print("[WARNING] %s points to an existing file, not a directory" % outpath, file=sys.stderr)
			out_handles = dict()
			out_handle = open(outpath, 'w')
			if args.muttype:
				out_handles["MUT_TYPE"] = out_handle
			if args.sample:
				out_handles["SAMPLE"] = out_handle
			if args.gene:
				out_handles["GENE"] = out_handle
			return out_handles


def handle_action_args(args, parser):
	counters = dict()
	if not(args.muttype or args.sample or args.gene):
		parser.exit(-1, "must activate at least one counting mode: --muttype --sample --gene\n")
	if args.muttype:
		counters["MUT_TYPE"] = Util.MAFcounters.MutTypeCounter()
	if args.sample:
		counters["SAMPLE"] = Util.MAFcounters.SampMutCounter()
	if args.gene:
		counters["GENE"] = Util.MAFcounters.GeneMutCounter()
	return counters


def get_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Count # of entries per gene in Util file")
	parser.add_argument('--maf', type=argparse.FileType('r'), required=True, help="file containing Util entries")
	parser.add_argument('--out', type=str, required=False, default="", help='path to use for output files')
	parser.add_argument('--nameprefix', type=str, required=False, default="", help='use this prefix in output names instead of automatically generating one')
	parser.add_argument('--muttype', action='store_true', default=False, required=False, help="activate counting according to mutation types")
	parser.add_argument('--sample', action='store_true', default=False, required=False, help="activate counting according to sample ID")
	parser.add_argument('--gene', action='store_true', default=False, required=False, help="activate counting according to gene symbol")
	return parser


def main():
	parser = get_parser()
	args = parser.parse_args()

	counters = handle_action_args(args, parser)
	out_handles = handle_outpath_arg(args, parser)

	entries = GenericFormats.MAF.File.get_all_entries_from_filehandle(args.maf)
	args.maf.close()

	for entry in entries:
		for counter in counters:
			counters[counter].count(entry)
	for handle in out_handles:
		out_handles[handle].write("%s" % counters[handle])

if __name__ == "__main__":
	main()