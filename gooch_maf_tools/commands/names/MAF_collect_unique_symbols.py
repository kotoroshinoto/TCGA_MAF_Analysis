#!/usr/bin/env python3
import click
import sys
import csv
__author__ = 'mgooch'


@click.command(help="Collect Unique entries from first column of maf file")
@click.option('--maf', type=click.File('r'), required=True, help="file to collect names from")
@click.option('--out', type=click.File('w+'), default=sys.stdout, help="file to use for output")
def cli(maf, out):
	Names = list()
	#Entrez_IDs = list()
	rdr = csv.reader(maf, dialect='excel-tab')
	for line in rdr:
		if len(line) < 1:
			continue
		symbol = line[0].rstrip()
		if symbol != "Hugo_Symbol" and symbol not in Names:
			Names.append(symbol)
			#Entrez_IDs.append(line_split[1])
			print("%s\t" % line[0], file=out)
	out.write("")
	out.close()
