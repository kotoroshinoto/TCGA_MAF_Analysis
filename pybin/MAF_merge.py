import click
import os
import sys
import GenericFormats.MAF


@click.command(help="Count # of entries per gene in Util file")
@click.option("--maf", type=click.File('r'), required=True, multiple=True, help="file containing Util entries")
@click.option('--out', type=click.File('w'), required=False, default=sys.stdout, help='path to use for output files')
def main(maf, out):
	print(GenericFormats.MAF.Entry.get_header_line(), file=out)
	for maf_file in maf:
		entries = GenericFormats.MAF.File.get_all_entries_from_filehandle(maf_file)
		maf_file.close()
		for entry in entries:
			print(entry, file=out)

if __name__ == "__main__":
	main()