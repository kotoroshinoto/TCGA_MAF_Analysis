import click
import os
import sys
import Formats.MAF


@click.command(help="Count # of entries per gene in Util file")
@click.option("--maf", type=click.File('r'), required=True, multiple=True, help="file containing Util entries")
@click.option('--out', type=click.File('w'), required=False, default=sys.stdout, help='path to use for output files')
@click.option('--noheader', type=bool(), required=False, default=False, help="disable header line in output")
def main(maf, out, noheader):
	if not noheader:
		print(Formats.MAF.Entry.get_header_line(), file=out)
	for maf_file in maf:
		entries = Formats.MAF.File.get_all_entries_from_filehandle(maf_file)
		maf_file.close()
		for entry in entries:
			print(entry, file=out)

if __name__ == "__main__":
	main()