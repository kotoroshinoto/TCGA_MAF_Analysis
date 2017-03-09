#!/usr/bin/env python3
__author__ = 'mgooch'
import click
import sys


@click.command(help="Collect Unique entries from first two columns of util file")
@click.option('--maf', type=click.File('r'), required=True, help="file to collect names from")
@click.option('--out', type=click.File('w'), required=True, help="file to use for output")
@click.option('--outNoEntrez', type=click.File('w'), help="file to use for output names lacking entrez IDs")
def cli(maf, out, outnoentrez):
	Names = list()
	#Entrez_IDs = list()
	first_line_skipped = False
	for line in maf:
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
			if entrez_id != "0" and entrez_id != "":
				print("%s\t%s" % (line_split[0], line_split[1]), file=out)
			else:
				if outnoentrez is not None:
					print("%s\t" % line_split[0], file=outnoentrez)
	if outnoentrez is not None:
		outnoentrez.write("")
		outnoentrez.close()
	out.write("")
	out.close()
if __name__ == "__main__":
	cli()
