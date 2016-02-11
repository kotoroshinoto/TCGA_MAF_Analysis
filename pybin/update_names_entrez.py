#!/usr/bin/env python3
__author__ = 'mgooch'
import re
import sys
import click

# parser = argparse.ArgumentParser(description="Compute exonic sizes of genes and relate them to HUGO IDs")
# parser.add_argument('--mafnames', type=argparse.FileType('r'), required=True, help="file of names to be translated")
# parser.add_argument('--name_to_entrez', type=argparse.FileType('r'), required=True, help="output from MAF_collect_unique_entrez_ids.py")
# parser.add_argument('--entrez', type=argparse.FileType('r'), required=True, help="file containing symbols and entrez ids")
# parser.add_argument('--col-entrez', type=int, required=True, help="column that has entrez ids")
# parser.add_argument('--col-symbol', type=int, required=True, help="column that has symbols")
#
# parser.add_argument('--outCorrected', type=argparse.FileType('w'), required=True, help="file to use for output")
# parser.add_argument('--outUnmatched', type=argparse.FileType('w'), required=True, help="file to use for output")
#
# args = parser.parse_args()


@click.command()
@click.option('--mafnames', type=click.File('r'), required=True, help="file of names to be translated")
@click.option('--name_to_entrez', type=click.File('r'), required=True, help="output from MAF_collect_unique_entrez_ids.py")
@click.option('--entrez', type=click.File('r'), required=True, help="file containing symbols and entrez ids")
@click.option('--col-entrez', type=int, required=True, help="column that has entrez ids")
@click.option('--col-symbol', type=int, required=True, help="column that has symbols")
@click.option('--outCorrected', type=click.File('w'), required=True, help="file to use for output")
@click.option('--outUnmatched', type=click.File('w'), required=True, help="file to use for output")
def cli(mafnames,name_to_entrez, entrez, col_entrez, col_symbol, outCorrected, outUnmatched):
	MAF_names = dict()

	#pull TCGA names from file
	for line in mafnames:
		if len(line) > 0:
			split_line = line.split("\t")
			symbol = split_line[0].rstrip()
			MAF_names[symbol.upper()] = symbol
	mafnames.close()

	Name2EntrezID = dict()

	for line in name_to_entrez:
		# line = line.rstrip()
		if len(line) > 0:
			line_split = line.split("\t")
			symbol = line_split[0].upper().rstrip()
			entrez_id = line_split[1].rstrip()
			if symbol not in Name2EntrezID:
				if len(symbol) > 0 and len(entrez_id) > 0 and entrez_id != "0":
					Name2EntrezID[symbol] = entrez_id
			# else:
			# 	print("Duplicate entry in symbol->entrez file for symbol: %s" % symbol, file=sys.stderr)
	name_to_entrez.close()

	EntrezID2ModernSymbol = dict()

	for line in entrez:
		if len(line) > 0:
			line_split = line.split("\t")
			symbol = line_split[col_symbol].upper().rstrip()
			entrez_id = line_split[col_entrez].rstrip()
			if entrez_id not in EntrezID2ModernSymbol:
				if len(symbol) > 0 and len(entrez_id) > 0:
					EntrezID2ModernSymbol[entrez_id] = symbol
			# else:
			# 	print("Duplicate entry in entrez->symbol file for entrez_id: %s" % entrez_id, file=sys.stderr)

	# print("#Old_Symbol\tNew_Symbol", file=args.outCorrected)
	for name in MAF_names:
		#get entrez_id
		if name in Name2EntrezID:
			entrez_id = Name2EntrezID[name]
			if entrez_id in EntrezID2ModernSymbol:
				symbol = EntrezID2ModernSymbol[entrez_id]
				print("%s\t%s" % (MAF_names[name], symbol), file=outCorrected)
			else:
				print("%s\t" % (MAF_names[name]), file=outUnmatched)
		else:
			print("%s\t" % (MAF_names[name]), file=outUnmatched)
		#convert entrez_id back to symbol
	outCorrected.close()
	outUnmatched.close()

if __name__ == "__main__":
	cli()