#!/usr/bin/env python3
import sys
import os
import MAFreader
import click

#global args
output_file = None
unmatched_log_file = None
symbol_dict = dict()


def log_unmatched_symbols():
	"""get list of unmatched symbols from global var: symbol_dict"""
	if unmatched_log_file is None:
		print("not logging unmatched symbols")
		return
	print("begin logging unmatched symbols")
	unmatched = list()
	for symbol in symbol_dict:
		if not symbol_dict[symbol]:
			unmatched.append(symbol)
	print("%s" % ("\n".join(sorted(unmatched))), file=unmatched_log_file)


@click.group(no_args_is_help=True)
@click.option('--out', type=click.File('w'), required=False, default=sys.stdout, help='path to file for query output, defaults to <stdout>')
@click.option('--unmatched', type=click.File('w'), required=False, default=None, help='if defined, write unmatched symbols to file')
def cli(out, unmatched):
	"""Query MAF file for entries that have desired gene symbols"""
	# click.echo("output file %s" % out.name, err=True)
	global output_file
	output_file = out
	if unmatched is not None:
		global unmatched_log_file
		unmatched_log_file = unmatched
		click.echo("logging unmatched symbols to: %s" % unmatched_log_file.name, err=True)
	return


@click.group(no_args_is_help=True)
@click.argument('query', type=click.File('r'), required=True)
@click.argument('column', type=int, required=False)
def input_file(query, column):
	"""query using data from a file

	\b
	QUERY\tpath to file to use for query
	COLUMN\tif file is a TSV, provide this argument to select symbol column"""
	# click.echo("query from file %s" % query.name, file=sys.stderr)
	if column is not None:
		# click.echo("file is TSV, using column %d" % column, err=True)
		#pull symbols from file splitting by tab and taking only the desired column
		for line in query:
			if len(line) == 0 or line[0] == "#":
				continue
			split_line = line.split("\t")
			symbol = split_line[column].upper().rstrip()
			if len(symbol) == 0:
				continue
			if symbol not in symbol_dict:
				symbol_dict[symbol] = False
	else:
		#pull symbols from file treating entire line as symbol
		for line in query:
			if len(line) == 0 or line[0] == "#":
				continue
			line = line.rstrip().upper()
			if len(line) == 0:
				continue
			if line not in symbol_dict:
				symbol_dict[line] = False
	# click.echo("query from list:\n%s" % ("\n".join(sorted(symbol_dict.keys()))), err=True)
	return


@click.group(no_args_is_help=True)
@click.argument('query', type=str, required=True)
def input_list(query):
	"""query using a list from commandline

	\b
	QUERY\tlist of symbols to use for query in CSV format
	"""
	query_list = query.split(",")
	for symbol in query_list:
		symbol_upper = symbol.upper()
		if symbol_upper not in symbol_dict:
			symbol_dict[symbol_upper] = False
	# click.echo("query from list:\n%s" % (", ".join(sorted(symbol_dict.keys()))), err=True)
	return


@click.command(add_help_option=True)
@click.argument('database', type=click.File('r'), required=True)
def query_maf(database):
	"""query an MAF file

	\b
	 DATABASE\tfile to be queried containing MAF entries
	"""
	# click.echo("maf file to be queried: %s" % database.name, err=True)
	#read MAF lines from file, spit them out to output stream if their symbol matches one of the queries
	maf_file_reader = MAFreader.MAFFile()
	maf_file_reader.use_filehandle(database)
	while maf_file_reader.has_more_entries():
		entry = maf_file_reader.get_next_entry()
		if entry.data['Hugo_Symbol'].upper() in symbol_dict:
			print("%s" % entry, file=output_file)
	log_unmatched_symbols()
	return


@click.command(add_help_option=True)
@click.argument('database', type=click.File('r'), required=True)
@click.argument('column', type=int, required=True)
def query_tsv(database, column):
	"""query a generic TSV file based on contents in designated column

	\b
	DATABASE\tpath to a TSV file
	COLUMN  \tzero-based column index
	"""
	# click.echo("tsv file to be queried: %s" % database.name, err=True)
	# click.echo("using column %d" % column, err=True)
	for line in database:
		if len(line) == 0 or line[0] == "#":
			continue
		split_line = line.split("\t")
		if len(split_line) < column+1:
			click.echo("line doesn't have enough columns: \"%s\"" % line, err=True)
			continue
		symbol = split_line[column].upper().rstrip()
		if len(symbol) == 0:
			click.echo("no symbol entry for line: %s" % line, err=True)
			continue
		if symbol in symbol_dict:
			symbol_dict[symbol] = True
			print("%s" % line.rstrip('\n'), file=output_file)
	log_unmatched_symbols()
	return

input_file.add_command(query_maf, name="maf")
input_file.add_command(query_tsv, name="tsv")

input_list.add_command(query_maf, name="maf")
input_list.add_command(query_tsv, name="tsv")

cli.add_command(input_file, name="file")
cli.add_command(input_list, name="list")


if __name__ == "__main__":
	cli()
