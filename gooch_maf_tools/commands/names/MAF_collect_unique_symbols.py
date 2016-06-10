#!/usr/bin/env python3
import click
import sys
__author__ = 'mgooch'


@click.command(help="Collect Unique entries from first column of util file")
@click.option('--maf', type=click.File('r'), required=True, help="file to collect names from")
@click.option('--out', type=click.File('w'), default=sys.stdout, help="file to use for output")
def cli(maf, out):
	Names = list()
	#Entrez_IDs = list()

	for line in maf:
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
			print("%s\t" % line_split[0], file=out)
