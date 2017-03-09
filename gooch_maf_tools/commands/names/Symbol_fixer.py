#!/usr/bin/env python3
import warnings
import io
import sys
import click
import gooch_maf_tools.formats.MAF as MAF
from typing import Dict, List, Tuple
import csv
#
# @cli.command(name="TSV")
# @click.option('--input', type=(click.File('r'), int), required=True, help="path to file containing names, and the column to read")
# @click.option('--lengths', type=(click.File('r'), int), help="path to lengths file, name column")
# @click.option('--symbolcheck', type=(click.File('r'), int, int, int), help="path to symbolcheck file, input column, match type column, approved symbol column")
# @click.option('--entrez', type=(click.File('r'), int, int), help="path to entrez file, hugo symbol column, entrez id column")
# @click.option('--manual', type=(click.File('r'), int, int), help="path to file containing manually curated names, oldname column, newname column")
# @click.option('--name_to_entrez', type=click.File('r'), help="output from MAF_collect_unique_entrez_ids.py")
# def tsv_command(input, lengths, symbolcheck, entrez, manual, name_to_entrez):
# 	#validate option validity
# 	return
#
#
# @cli.command(name="TSV-ENTREZ")
# @click.option('--input', type=(click.File('r'), int, int), required=True, help="path to file containing names and entrez ids, symbol column, entrez column")
# @click.option('--lengths', type=(click.File('r'), int), help="path to lengths file, name column")
# @click.option('--symbolcheck', type=(click.File('r'), int, int, int), help="path to symbolcheck file, input column, match type column, approved symbol column")
# @click.option('--entrez', type=(click.File('r'), int, int), help="path to entrez file, hugo symbol column, entrez id column")
# @click.option('--manual', type=(click.File('r'), int, int), help="path to file containing manually curated names, oldname column, newname column")
# def tsv_with_entrez_command(input, lengths, symbolcheck, entrez, manual):
# 	#validate option validity
# 	return


class KeptSymbol:
	def __init__(self, symbol=None, source=None):
		self.symbol = symbol
		self.source = source


class KeptSymbols:
	def __init__(self):
		self.old_symbols = list()  # type: List[str]
		self.kept_symbols = dict()  # type: Dict[str, KeptSymbol]

	def register_symbol_pair(self, oldsymbol:str, newsymbol:str, source: str):
		if oldsymbol not in self.old_symbols:
			self.old_symbols.append(oldsymbol)
		if oldsymbol not in self.kept_symbols:
			self.kept_symbols[oldsymbol] = KeptSymbol(newsymbol, source)
		else:
			self.kept_symbols[oldsymbol].symbol = newsymbol
			self.kept_symbols[oldsymbol].source = source

	def update_maf_symbol(self, entry: MAF.Entry):
		oldsymb = entry.get_data(0)
		entry.fieldnames.append("oldsymbol")
		entry.fieldnames.append("symbol_source")
		if (oldsymb in self.old_symbols) and (oldsymb in self.kept_symbols):
			entry.set_data(0, self.kept_symbols[oldsymb].symbol)
			entry.data["oldsymbol"] = oldsymb
			entry.data["symbol_source"] = self.kept_symbols[oldsymb].source
		else:  # (oldsymb not in self.old_symbols) or (oldsymb not in self.kept_symbols)
			warnings.warn(RuntimeWarning("tried to update symbol that wasn't in provided data: %s" % oldsymb))
			entry.data["oldsymbol"] = oldsymb
			entry.data["symbol_source"] = "unmatched"

	def read_lengthcheck_file(self, length_option: Tuple[io.IOBase, int, int], sourcename: str) -> None:
		print(length_option[0].name)
		if length_option[0] is None:
			return
		reader = csv.reader(length_option[0], dialect='excel-tab')
		for entry in reader:
			oldsymb = entry[length_option[1]]
			newsymb = entry[length_option[2]]
			# print("old symbol: %s\tnew symbol: %s" %(oldsymb, newsymb))
			self.register_symbol_pair(oldsymb, newsymb, sourcename)

	def update_maf(self, maf_handle: io.IOBase, out_option: io.IOBase) -> None:
		mafreader = MAF.EntryReader(maf_handle)
		wrote_headers = False
		while mafreader.has_next():
			entry = mafreader.next()
			self.update_maf_symbol(entry)
			if not wrote_headers:
				print("\t".join(entry.fieldnames), file=out_option)
				wrote_headers = True
			print("%s" % entry, file=out_option)


@click.command(name="SymbolFixer")
@click.option('--maf', type=click.File('r'), required=True, help="path to maf file")
@click.option('--original', type=(click.File('r'), int, int), help="path to original lengthcheck file, original_name column index, newname column index")
@click.option('--symbolcheck', type=(click.File('r'), int, int), help="path to symbolcheck lengthcheck file, original_name column index, newname column index")
@click.option('--entrez', type=(click.File('r'), int, int), help="path to entrez lengthcheck file, original_name column index, newname column index")
@click.option('--manual', type=(click.File('r'), int, int), help="path to file containing manually curated symbols, original_name column index, newname column index")
@click.option('--out', type=click.File('w+'), default=sys.stdout, help="output path to write changed maf entries")
def cli(maf, original, symbolcheck, entrez, manual, out):
	"""Create output MAF with updated symbols,
		add additional columns showing what the old symbols were,
		and whether the symbol should be considered up-to-date or not"""
	symbols = KeptSymbols()

	symbols.read_lengthcheck_file(manual, 'manual')
	symbols.read_lengthcheck_file(entrez, 'entrez')
	symbols.read_lengthcheck_file(symbolcheck, 'symbolcheck')
	symbols.read_lengthcheck_file(original, 'original')

	#if entry symbol is in lengths, original name is kept
	#otherwise following priority is used:
	#entrez_ID
	#symbolcheck
	#manual
	#if none of these were matched, signal this in output
	#add columns to data: orig_symbol, kept_from, where kept_from is one of original, symbolcheck, entrez, manual, or "unmatched"
	print("inputfile: %s\noutputfile: %s" % (maf.name, out.name))
	symbols.update_maf(maf, out)
	return


if __name__ == "__main__":
	cli()
