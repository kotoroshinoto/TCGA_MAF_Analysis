import rpy2.robjects.packages as rpackages
import rpy2.robjects as ro
import click
import csv
import sys
from typing import List
from typing import Dict
from ..get_stats.util import *


class GeneLinregEntry:
	def __init__(self, symbol: str):
		self.symbol = symbol
		self.symbol_key = symbol.casefold()
		self.count = 0
		self.length = 0


class GeneLinregData:
	def __init__(self):
		self.data_dict = dict()  # type: Dict[str, GeneLinregEntry]
		self.symbol_list = list()  #type: List[str]

	def read_count_file(self, filehandle, name_col: int, count_col: int, has_header: bool):
		reader = csv.reader(filehandle, dialect='excel-tab')
		if has_header:
			next(reader)  # skip first line
		for row in reader:
			symbol = row[name_col]
			symbol_key = symbol.casefold()
			if symbol_key not in self.data_dict:
				entry = GeneLinregEntry(symbol)  # type: GeneLinregEntry
				self.data_dict[symbol_key] = entry
				self.symbol_list.append(symbol_key)
			else:
				entry = self.data_dict[symbol_key]  # type: GeneLinregEntry
			entry.count = int(row[count_col])

	def read_length_file(self, filehandle, name_col: int, length_col: int, has_header: bool):
		reader = csv.reader(filehandle, dialect='excel-tab')
		if has_header:
			next(reader)  # skip first line
		for row in reader:
			symbol = row[name_col]
			symbol_key = symbol.casefold()
			if (symbol_key not in self.symbol_list) or (symbol_key not in self.data_dict):
				continue
			entry = self.data_dict[symbol_key]
			entry.length = int(row[length_col])

	def generate_count_vector(self) -> ro.IntVector:
		counts = list()
		for symbol in self.symbol_list:
			counts.append(self.data_dict[symbol].count)
		return ro.IntVector(counts)

	def generate_length_vector(self) -> ro.IntVector:
		lengths = list()
		for symbol in self.symbol_list:
			lengths.append(self.data_dict[symbol].length)
		return ro.IntVector(lengths)

	def get_symbol_list(self):
		return self.symbol_list


@click.command(name='Gene_Outliers', help="compute studentized residuals for list of gene counts")
@click.option('--count_file', type=(click.File('r'), int, int), default=(None, None, None), required=True, help="count file, symbol column, count column")
@click.option('--length_file', type=(click.File('r'), int, int), default=(None, None, None), required=True, help="length file, symbol column,  length column")
@click.option('--header_count/--noheader_count', default=True)
@click.option('--header_length/--noheader_length', default=True)
@click.option('--header_name_map/--noheader_name_map', default=True)
@click.option('--output', required=False, default=None, type=click.Path(dir_okay=False, writable=True), help="output file path")
@click.pass_context
def cli(ctx, count_file, length_file, output, header_count, header_length, header_name_map):
	#TODO find out why some lengths are not matching and are being given a size of zero
	errormsg=list()
	if count_file[0] is None:
		errormsg.append("--count_file is required")
	if length_file[0] is None:
		errormsg.append("--length_file is required")
	# if name_map_file[0] is None:
	# 	errormsg.append("--name_map_file is required")
	if len(errormsg) > 0:
		print(cli.get_help(ctx))
		raise click.UsageError(', '.join(errormsg))
	check_and_install_R_dependency('MASS')
	rpackages.importr('MASS')
	linreg_data = GeneLinregData()

	#read in counts file
	linreg_data.read_count_file(count_file[0], count_file[1], count_file[2], header_count)

	#read in length file
	linreg_data.read_length_file(length_file[0], length_file[1], length_file[2], header_length)

	length_vector = linreg_data.generate_length_vector()
	count_vctr = linreg_data.generate_count_vector()

	ro.r('x=' + str(length_vector.r_repr()))
	ro.r('y=' + str(count_vctr.r_repr()))

	linreg_result = ro.r('lm(y~x)')

	studres_func = ro.r('studres')

	studres_result = studres_func(linreg_result)

	if output is None:
		output_file = sys.stdout
	else:
		output_file = open(output, newline='', mode='w')
	fieldnames = list()
	fieldnames.append('Gene_Symbol')
	fieldnames.append('Length')
	fieldnames.append('Mutation_Count')
	fieldnames.append('Studentized_Residual')
	output_writer = csv.writer(output_file, dialect='excel-tab')
	output_writer.writerow(fieldnames)
	symbol_list = linreg_data.symbol_list
	for i in range(0, len(symbol_list)):
		symbol = symbol_list[i]
		if (symbol not in linreg_data.symbol_list) or (symbol not in linreg_data.data_dict):
			continue
		dataentry = linreg_data.data_dict[symbol]  # type: GeneLinregEntry
		row = list()
		row.append(dataentry.symbol)
		row.append(dataentry.length)
		row.append(dataentry.count)
		row.append(studres_result[i])
		output_writer.writerow(row)

if __name__ == "__main__":
	cli()
