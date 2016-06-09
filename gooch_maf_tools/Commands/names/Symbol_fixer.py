#!/usr/bin/env python3
import sys
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
# TODO make name fixer scripts work on either actual util files or custom files with numbered columns


class AbstractSymbolFixContext:
	# __metaclass__ = abc.ABCMeta

	def __init__(self):
		return

	# @abc.abstractmethod
	def getSymbol(self, index):
		return


# class SymbolFixContextTSV(AbstractSymbolFixContext):
# 	def __init__(self):
# 		super(SymbolFixContextTSV, self).__init__()
# 		return
#
#
# class SymbolFixContextMAF(AbstractSymbolFixContext):
# 	def __init__(self):
# 		super(SymbolFixContextMAF, self).__init__()
# 		return

def prep_steps(context: AbstractSymbolFixContext):
	#prep steps
	#read in all lists, many will need columns to be specified
	#symbolcheck file
	#^produced by giving output from MAF_collect_unique_symbols.py to http://www.genenames.org/cgi-bin/symbol_checker
	#entrez ID -> hugo symbol file
	#lengths file (produced by exon_sizer.py)
	#manual curation file
	return


def prep_tsv_with_entrez(context: AbstractSymbolFixContext):
	return


def prep_maf(context: AbstractSymbolFixContext):
	return


def prep_tsv(context: AbstractSymbolFixContext):
	return


def fix_names(context: AbstractSymbolFixContext):

	#keep a list of the names that have been corrected or were already fine in a dict
	#the dict value should tell us which category they fell into
	#use classes with standard API for handling util vs more generic TSV input
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


@click.group(name='SymbolFixer')
def cli():
	pass


@cli.command(name="TSV")
@click.option('--input', type=(click.File('r'), int), required=True, help="path to file containing names, and the column to read")
@click.option('--lengths', type=(click.File('r'), int), help="path to lengths file, name column")
@click.option('--symbolcheck', type=(click.File('r'), int, int, int), help="path to symbolcheck file, input column, match type column, approved symbol column")
@click.option('--entrez', type=(click.File('r'), int, int), help="path to entrez file, hugo symbol column, entrez id column")
@click.option('--manual', type=(click.File('r'), int, int), help="path to file containing manually curated names, oldname column, newname column")
@click.option('--name_to_entrez', type=click.File('r'), help="output from MAF_collect_unique_entrez_ids.py")
def tsv_command(input, lengths, symbolcheck, entrez, manual, name_to_entrez):
	#TODO validate option validity
	return


@cli.command(name="TSV-ENTREZ")
@click.option('--input', type=(click.File('r'), int, int), required=True, help="path to file containing names and entrez ids, symbol column, entrez column")
@click.option('--lengths', type=(click.File('r'), int), help="path to lengths file, name column")
@click.option('--symbolcheck', type=(click.File('r'), int, int, int), help="path to symbolcheck file, input column, match type column, approved symbol column")
@click.option('--entrez', type=(click.File('r'), int, int), help="path to entrez file, hugo symbol column, entrez id column")
@click.option('--manual', type=(click.File('r'), int, int), help="path to file containing manually curated names, oldname column, newname column")
def tsv_with_entrez_command(input, lengths, symbolcheck, entrez, manual):
	#TODO validate option validity
	return


@cli.command(name="util")
@click.option('--input', type=click.File('r'), required=True, help="path to maf file")
@click.option('--lengths', type=(click.File('r'), int), help="path to lengths file, name column")
@click.option('--symbolcheck', type=(click.File('r'), int, int, int), help="path to symbolcheck file, input column, match type column, approved symbol column")
@click.option('--entrez', type=(click.File('r'), int, int), help="path to entrez file, hugo symbol column, entrez id column")
@click.option('--manual', type=(click.File('r'), int, int), help="path to file containing manually curated names, oldname column, newname column")
def maf_command(input, lengths, symbolcheck, entrez, manual):
	#TODO validate option validity
	return


if __name__ == "__main__":
	cli()
