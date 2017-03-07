import click
import os
import sys
from gooch_maf_tools.formats import MAF


@click.command(help="Merge MAF files")
@click.option("--maf", type=click.File('r'), required=True, multiple=True, help="file containing maf entries")
@click.option('--out', type=click.File('w'), required=False, default=sys.stdout, help='path to use for output files')
@click.option('--noheader', type=bool, required=False, default=False, help="disable header line in output")
def cli(maf, out, noheader):
	printed_header = False
	for maf_file in maf:
		entries = MAF.EntryReader.get_all_entries_from_filehandle(maf_file)
		maf_file.close()
		for entry in entries:
			if (not noheader) and (not printed_header):
				print("\t".join(entry.fieldnames))
				printed_header = True
			print(entry, file=out)

if __name__ == "__main__":
	cli()