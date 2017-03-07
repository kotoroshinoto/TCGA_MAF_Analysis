import click
import os
import sys
from gooch_maf_tools.formats import MAF
from typing import Tuple


@click.command(help="Merge MAF files from multiple sources, with associated labels")
@click.option("--maf", type=(str, click.File('r')), required=True, multiple=True, help="label for file and path to file containing MAF entries")
@click.option('--out', type=click.File('w'), required=False, default=sys.stdout, help='path to use for output files')
# @click.option('--noheader', type=bool, required=False, default=False, help="disable header line in output")
def cli(maf: 'list[Tuple[str, click.File]]', out: 'click.File'):
	# if not noheader:
	# 	print(MAF.Entry.get_header_line(), file=out)
	for maf_file in maf:
		reader = MAF.EntryReader(maf_file[1])
		print("fields: '%s'" % reader.get_header_line())
		entries = MAF.EntryReader.get_all_entries_from_filehandle(maf_file[1])
		for entry in entries:
			print(entry, file=out)

if __name__ == "__main__":
	cli()
