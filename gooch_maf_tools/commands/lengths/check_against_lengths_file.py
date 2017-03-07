#!/usr/bin/env python3
import click
import re
import sys
import os
__author__ = 'mgooch'


@click.command(help="check MAF names against names in transcript length files")
@click.option('--mafnames', type=click.File('r'), required=True, help="file of names to be translated")
@click.option('--checkcolumn', type=int, default=None, help="check this column instead of oldcolumn")
@click.option('--oldcolumn', type=int, default=0, help="this column is the original name")
@click.option('--genelength', type=click.File('r'), multiple=True, required=True, help="file of gene lengths that has names")#, nargs='+'
@click.option('--matched', type=click.File('w+'), required=True, help="file to write matched names")
@click.option('--unmatched', type=click.File('w+'), required=True, help="file to write unmatched names")
@click.option('--keep', default=False, is_flag=True, help="put checked label in 2nd column even if unmatched")
@click.option('--logok', default=os.devnull, type=click.File('w+'), help="log OK output to this file")
@click.option('--logbad', default=os.devnull, type=click.File('w+'), help="log BAD output to this file")
def cli(mafnames, checkcolumn, oldcolumn, genelength, matched, unmatched, keep, logok, logbad):
	MAF_original_names = dict()
	MAF_names = dict()
	if checkcolumn is None:
		checkcolumn = oldcolumn

	#pull util names from file
	for line in mafnames:
		if len(line) > 0:
			split_line = line.split("\t")
			old_symbol = split_line[oldcolumn].rstrip()
			check_symbol = split_line[checkcolumn].rstrip()
			if len(check_symbol) > 0:
				MAF_names[check_symbol.upper()] = check_symbol
				if len(old_symbol) == 0:
					print("[WARNING] missing original symbol for checked symbol: %s" % check_symbol)
				MAF_original_names[check_symbol.upper()] = old_symbol
	mafnames.close()

	#build list of names from size file if one was given
	Length_File_Name_List = dict()
	for lengthfile in genelength:
		print("reading file: %s" % lengthfile.name)
		for line in lengthfile:
			if len(line) > 0:
				split_line = line.split("\t")
				symbol = split_line[0].rstrip()
				if len(symbol) > 0:
					if symbol.upper() not in Length_File_Name_List:
						Length_File_Name_List[symbol.upper()] = symbol
		lengthfile.close()

	for check_symbol in MAF_names:
		if check_symbol in Length_File_Name_List:
			if oldcolumn != checkcolumn:
				print("checked name OK for: %s -> %s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=logok)
			else:
				print("checked name OK for: %s" % (MAF_names[check_symbol]), file=logok)
			print("%s\t%s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=matched)
		else:
			if oldcolumn != checkcolumn:
				print("checked name BAD for: %s - > %s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=logbad)
			else:
				print("checked name BAD for: %s" % (MAF_names[check_symbol]), file=logbad)
			if keep:
				print("%s\t%s" % (MAF_original_names[check_symbol], MAF_names[check_symbol]), file=unmatched)
			else:
				print("%s\t" % MAF_original_names[check_symbol], file=unmatched)
	matched.close()
	unmatched.close()

if __name__ == "__main__":
	cli()
