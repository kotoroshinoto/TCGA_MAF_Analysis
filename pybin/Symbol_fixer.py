#!/usr/bin/env python3
import sys
import os
import click


class GeneSymbolMapper:
	def __init__(self):
		self.__symbols = dict()

	def map_symbol(self, key, symbol):
		if key in self.__symbols:
			print("you attempted to map an already mapped key: %s, which is mapped to %s, tried to map it to %s" % (
			key, symbol, self.__symbols[key]), file=sys.stderr);
			exit(-1)
		self.__symbols[key] = symbol

	def get_mapped_name(self, oldname):
		if oldname not in self.__symbols:
			return ""
		return self.__symbols[oldname]


class MappingInputFile:
	def __init__(self):
		self.__raw_lines = list()
		self.__encoded_lines = list()

	def add_line(self, raw, encoded):
		self.__raw_lines.append(raw)
		self.__encoded_lines.append(encoded)

	def get_encoded(self, index):
		return self.__encoded_lines[index]

	def get_raw(self, index):
		return self.__raw_lines

	def get_encoded_list(self):
		return self.__encoded_lines

	def get_raw_list(self):
		return self.__raw_lines


# TODO merge functionality of all the name fixer scripts into one file for ease of use
# TODO make name fixer scripts work on either actual MAF files or custom files with numbered columns


def prep_steps():
	#prep steps
	#read in all lists, many will need columns to be specified
	#symbolcheck file
	#^produced by giving output from MAF_collect_unique_symbols.py to http://www.genenames.org/cgi-bin/symbol_checker
	#entrez ID -> hugo symbol file
	#lengths file (produced by exon_sizer.py)
	#manual curation file
	return


def fix_names():

	#keep a list of the names that have been corrected or were already fine in a dict
	#the dict value should tell us which category they fell into
	#use classes with standard API for handling MAF vs more generic TSV input
	#output only corrected or already-correct entries into main output file, have a separate file for non-fixed entries

	#name fix steps:
	#check against lengths file -- pre-screen names that already match

	#attempt fix using entrez IDs
	#check against lengths file  -- mark as corrected using entrez
	#REMINDER: ignore zeroes

	#attempt fix using symbolchecker output
	#check against lengths file -- mark as corrected using symbolcheck

	#attempt fix using manual curation file
	#check against lengths file -- mark as corrected using manual curation

	#print to output files and logs
	return


# def get_parser() -> argparse.ArgumentParser:
# 	parser = argparse.ArgumentParser(description="Fix names in TCGA MAF file to match names in newer annotations")
# 	#TODO subcommands for MAF filetype and TSV with selected columns
# 	#TODO flag values for specific fixing steps
# 	#TODO input for manually curated names
# 	#TODO option for logging as when done manually
# 	return parser

@click.group()
def cli():
	pass


@click.command()
@click.option('--input', type=(click.File('r'), int), required=True, help="path to file containing names, and the column to read")
@click.option('--lengths', type=(click.File('r'), int), help="path to lengths file, name column")
@click.option('--symbolcheck', type=(click.File('r'), int, int, int), help="path to symbolcheck file, input column, match type column, approved symbol column")
@click.option('--entrez', type=(click.File('r'), int, int), help="path to entrez file, hugo symbol column, entrez id column")
@click.option('--name_to_entrez', type=click.File('r'), required=True, help="output from MAF_collect_unique_entrez_ids.py")
def tsv_input():
	return

@click.command()
@click.option('--input', type=(click.File('r'), int, int), required=True, help="path to file containing names, symbol column, entrez column")
@click.option('--lengths', type=(click.File('r'), int), help="path to lengths file, name column")
@click.option('--symbolcheck', type=(click.File('r'), int, int, int), help="path to symbolcheck file, input column, match type column, approved symbol column")
@click.option('--entrez', type=(click.File('r'), int, int), help="path to entrez file, hugo symbol column, entrez id column")
def tsv_with_entrez_input():
	return

@click.command()
@click.option('--input', type=click.File('r'), required=True, help="path to maf file")
@click.option('--lengths', type=(click.File('r'), int), help="path to lengths file, name column")
@click.option('--symbolcheck', type=(click.File('r'), int, int, int), help="path to symbolcheck file, input column, match type column, approved symbol column")
@click.option('--entrez', type=(click.File('r'), int, int), help="path to entrez file, hugo symbol column, entrez id column")
def maf_input():
	return

cli.add_command(maf_input, name="MAF")
cli.add_command(tsv_input, name="TSV")
cli.add_command(tsv_with_entrez_input, name="TSV-ENTREZ")
if __name__ == "__main__":
	cli()
