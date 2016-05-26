#!/usr/bin/env python3
import click
import os
import sys
from ..Formats import MAF
from ..Util import MAFcounters

__author__ = 'mgooch'


def generate_file_handles(maf, nameprefix, muttype, sample, gene, muttypepersample, location, muttypeatlocation, outpath):
	maf_path = maf.name
	maf_path_split = os.path.split(maf_path)
	if nameprefix == "":
		prefix = maf_path_split[1]
	else:
		split_nameprefix = os.path.split(nameprefix)
		if split_nameprefix[0] != "":
			print("Name prefix may not contain path separators! %s\n" % nameprefix, file=sys.stderr)
			sys.exit(-1)
		prefix = nameprefix
	print()
	out_handles = dict()
	if muttype:
		out_handles["MUT_TYPE"] = open(os.path.join(outpath, (prefix + ".mutation_type.counts")), mode='w')
	if sample:
		out_handles["SAMPLE"] = open(os.path.join(outpath, (prefix + ".sample.counts")), mode='w')
	if gene:
		out_handles["GENE"] = open(os.path.join(outpath, (prefix + ".gene.counts")), mode='w')
	if muttypepersample:
		out_handles["MUT_TYPE_PER_SAMPLE"] = open(os.path.join(outpath, (prefix + ".mutation_type.per_sample.counts")), mode='w')
	if location:
		out_handles["LOCATION"] = open(os.path.join(outpath, (prefix + ".location.counts")), mode='w')
	if muttypeatlocation:
		out_handles['MUT_TYPE_AT_LOCATION'] = open(os.path.join(outpath, (prefix + ".mutation_type.at.location.counts")), mode='w')
	return out_handles


def handle_outpath_arg(maf, out, nameprefix, muttype, sample, gene, muttypepersample, location, muttypeatlocation):
	if out == "":
		if nameprefix:
			print("[WARNING] argument --nameprefix does nothing if outpath is not defined, script will use stdout for all output", file=sys.stderr)
		out_handles = dict()
		if muttype:
			out_handles["MUT_TYPE"] = sys.stdout
		if sample:
			out_handles["SAMPLE"] = sys.stdout
		if gene:
			out_handles["GENE"] = sys.stdout
		if muttypepersample:
			out_handles["MUT_TYPE_PER_SAMPLE"] = sys.stdout
		if location:
			out_handles["LOCATION"] = sys.stdout
		if muttypeatlocation:
			out_handles["MUT_TYPE_AT_LOCATION"] = sys.stdout
		return out_handles
	else:
		outpath = os.path.realpath(os.path.abspath(out))
		parent_outpath = os.path.realpath(os.path.abspath(os.path.join(outpath, "..")))
		if not os.path.exists(parent_outpath):
			if outpath != out:
				print("parent path of %s [absolute real path: %s], which resolves to %s, does not exist\n" % (out, outpath, parent_outpath), file=sys.stderr)
				sys.exit(-1)
			else:
				print("parent path of %s, which resolves to %s does not exist\n" % (out, outpath), file=sys.stderr)
				sys.exit(-1)
		if os.path.exists(outpath) and os.path.isdir(outpath):
			#craft default filename from maf file + countype.counts
			return generate_file_handles(maf, nameprefix, muttype, sample, gene, muttypepersample, location, muttypeatlocation, outpath)
		elif not os.path.exists(outpath):
			#path does not yet exist, but parent path does
			#create path automatically, then create the filehandles
			os.mkdir(outpath)
			return generate_file_handles(maf, nameprefix, muttype, sample, gene, muttypepersample, location, muttypeatlocation, outpath)
		else:
			#file exists and is not a directory
			if nameprefix:
				print("[WARNING] argument --nameprefix does nothing if outpath points to a path that exists and is not a directory , script will use defined path for all output", file=sys.stderr)
			if outpath != out:
				print("[WARNING] %s [absolute real path: %s] points to an existing file, not a directory" % (out, outpath), file=sys.stderr)
			else:
				print("[WARNING] %s points to an existing file, not a directory" % outpath, file=sys.stderr)
			out_handles = dict()
			out_handle = open(outpath, 'w')
			if muttype:
				out_handles["MUT_TYPE"] = out_handle
			if sample:
				out_handles["SAMPLE"] = out_handle
			if gene:
				out_handles["GENE"] = out_handle
			if muttypepersample:
				out_handles["MUT_TYPE_PER_SAMPLE"] = out_handle
			if location:
				out_handles["LOCATION"] = out_handle
			if muttypeatlocation:
				out_handles["MUT_TYPE_AT_LOCATION"] = out_handle
			return out_handles


def handle_action_args(muttype, sample, gene, muttypepersample, location, muttypeatlocation):
	counters = dict()
	if not(muttype or sample or gene or muttypepersample or location or muttypeatlocation):
		print("must activate at least one counting mode: --muttype --sample --gene --muttypepersample --location --muttypeatlocation", file=sys.stderr)
		sys.exit(-1)
	if muttype:
		counters["MUT_TYPE"] = MAFcounters.MutTypeCounter()
	if sample:
		counters["SAMPLE"] = MAFcounters.SampMutCounter()
	if gene:
		counters["GENE"] = MAFcounters.GeneMutCounter()
	if muttypepersample:
		counters["MUT_TYPE_PER_SAMPLE"] = MAFcounters.MutTypePerSampCounter()
	if location:
		counters["LOCATION"] = MAFcounters.LocMutCounter()
	if muttypeatlocation:
		counters["MUT_TYPE_AT_LOCATION"] = MAFcounters.MutTypeAtLocCounter()
	return counters


@click.command(help="Count # of entries per gene in Util file")
@click.option('--maf', type=click.File('r'), required=True, help="file containing Util entries")
@click.option('--out', type=str, required=False, default="", help='path to use for output files')
@click.option('--nameprefix', type=str, required=False, default="", help='use this prefix in output names instead of automatically generating one')
@click.option('--muttype', is_flag=True, default=False, required=False, help="activate counting according to mutation types")
@click.option('--sample', is_flag=True, default=False, required=False, help="activate counting according to sample ID")
@click.option('--gene', is_flag=True, default=False, required=False, help="activate counting according to gene symbol")
@click.option('--muttypepersample', is_flag=True, default=False, required=False, help="activate counting according to mutation type, but also tracking sample_id")
@click.option('--location', is_flag=True, default=False, required=False, help="activate counting according to genomic location")
@click.option('--muttypeatlocation', is_flag=True, default=False, required=False, help="count more specifically than location does, divides counts by mutation type at each location (probably won't condense data file very much)")
def cli(maf, out, nameprefix, muttype, sample, gene, muttypepersample, location, muttypeatlocation):
	counters = handle_action_args(muttype, sample, gene, muttypepersample, location, muttypeatlocation)
	out_handles = handle_outpath_arg(maf, out, nameprefix, muttype, sample, gene, muttypepersample, location, muttypeatlocation)

	entries = MAF.File.get_all_entries_from_filehandle(maf)
	maf.close()

	for entry in entries:
		for counter in counters:
			counters[counter].count(entry)
	for handle in out_handles:
		out_handles[handle].write("%s" % counters[handle])

if __name__ == "__main__":
	cli()