import rpy2.robjects.packages as rpackages
import rpy2.robjects as ro
import click
import csv
import sys
from typing import List
from typing import Dict
from ..get_stats.util import *


class GeneNameMap:

	def __init__(self):
		self.name_map = dict()  # type: Dict[str, str]
		self.rev_name_map = dict()  # type: Dict[str, str]
		self.symbols = list()  # type: List[str])

	def register_name(self, nameold: str, namenew: str):
		if nameold in self.name_map:
			raise ValueError("MAF symbol: \"%s\" already has a mapping" % nameold)
		self.name_map[nameold] = namenew
		self.rev_name_map[namenew] = nameold
		self.symbols.append(nameold)

	def replace_name_registration(self, nameold: str, namenew: str):
		if nameold not in self.name_map:
			raise ValueError("MAF symbol: \"%s\" does not have an existing mapping" % nameold)
		self.name_map[nameold] = namenew
		self.rev_name_map[namenew] = nameold

	def get_name_for(self, nameold) -> str:
		if nameold not in self.name_map:
			raise ValueError("MAF symbol: \"%s\" does not have a mapping" % nameold)
		return self.name_map[nameold]

	def is_registered(self, nameold: str):
		return nameold in self.name_map

	def read_name_file(self, filehandle, old_col: int, new_col: int, has_header: bool):
		reader = csv.reader(filehandle, dialect='excel-tab')
		if has_header:
			next(reader)  # skip first line
		for row in reader:
			self.register_name(row[old_col], row[new_col])

	def rev_get_name_for(self, newname:str):
		if newname not in self.rev_name_map:
			raise ValueError("UPDATED symbol: \"%s\" does not have an existing mapping" % newname)
		return self.rev_name_map[newname]

	def rev_is_regstered(self, newname):
		return newname in self.rev_name_map


class GeneLinregEntry:
	def __init__(self, symbol: str):
		self._symbol = symbol
		self._count = 0
		self._length = 0


class GeneLinregData:
	def __init__(self):
		self.data_dict = dict()  # type: Dict[str, GeneLinregEntry]
		self.symbol_list = list()  #type: List[str]
		self.name_map = None  # type: GeneNameMap

	def read_count_file(self, filehandle, name_col: int, count_col: int, has_header: bool):
		reader = csv.reader(filehandle, dialect='excel-tab')
		if has_header:
			next(reader)  # skip first line

		for row in reader:
			if self.name_map is not None:
				oldsymbol = row[name_col]
				newsymbol = self.name_map.get_name_for(oldsymbol)
				if newsymbol not in self.data_dict:
					entry = GeneLinregEntry(newsymbol)  # type: GeneLinregEntry
					self.data_dict[newsymbol] = entry
					self.symbol_list.append(newsymbol)
				else:
					entry = self.data_dict[newsymbol]  # type: GeneLinregEntry
				entry._count = int(row[count_col])
			else:
				symbol = row[name_col]
				if symbol not in self.data_dict:
					entry = GeneLinregEntry(symbol)  # type: GeneLinregEntry
					self.data_dict[symbol] = entry
					self.symbol_list.append(symbol)
				else:
					entry = self.data_dict[symbol]  # type: GeneLinregEntry
				entry._count = int(row[count_col])

	def read_length_file(self, filehandle, name_col: int, length_col: int, has_header: bool):
		reader = csv.reader(filehandle, dialect='excel-tab')
		if has_header:
			next(reader)  # skip first line
		for row in reader:
			if self.name_map is not None:
				oldsymbol = row[name_col]
				if not self.name_map.is_registered(oldsymbol):
					continue  # skip missing names, as they are likely not in the data
				newsymbol = self.name_map.get_name_for(oldsymbol)
				if newsymbol not in self.data_dict:
					continue
					# entry = GeneLinregEntry(newsymbol)  # type: GeneLinregEntry
					# self.data_dict[newsymbol] = entry
					# self.symbol_list.append(newsymbol)
				else:
					entry = self.data_dict[newsymbol]  # type: GeneLinregEntry
				entry._length = int(row[length_col])
			else:
				symbol = row[name_col]
				if (symbol not in self.symbol_list) or (symbol not in self.data_dict):
					continue
				else:
					entry = self.data_dict[symbol]
				entry._length = int(row[length_col])

	def read_name_file(self, filehandle, old_col: int, new_col: int, has_header: bool):
		if filehandle is None:
			return
		self.name_map = GeneNameMap()
		self.name_map.read_name_file(filehandle, old_col, new_col, has_header)

	def generate_count_vector(self) -> ro.IntVector:
		counts = list()
		for symbol in self.symbol_list:
			counts.append(self.data_dict[symbol]._count)
		return ro.IntVector(counts)

	def generate_length_vector(self) -> ro.IntVector:
		lengths = list()
		for symbol in self.symbol_list:
			lengths.append(self.data_dict[symbol]._length)
		return ro.IntVector(lengths)

	def get_symbol_list(self):
		return self.symbol_list


@click.command(name='Gene_Outliers', help="compute studentized residuals for list of gene counts")
@click.option('--count_file', type=(click.File('r'), int, int), default=(None, None, None), required=True, help="count file, symbol column, count column")
@click.option('--length_file', type=(click.File('r'), int, int), default=(None, None, None), required=True, help="length file, symbol column,  length column")
@click.option('--name_map_file', type=(click.File('r'), int, int), default=(None, None, None), help="names file, old name column, new name column")
@click.option('--header_count/--noheader_count', default=True)
@click.option('--header_length/--noheader_length', default=True)
@click.option('--header_name_map/--noheader_name_map', default=True)
@click.option('--output', required=False, default=None, type=click.Path(dir_okay=False, writable=True), help="output file path")
@click.pass_context
def cli(ctx, count_file, length_file, name_map_file, output, header_count, header_length, header_name_map):
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
	print("count_file: %s" % count_file[0].name)
	exit(0)
	check_and_install_R_dependency('MASS')
	rpackages.importr('MASS')
	linreg_data = GeneLinregData()

	#read in name map
	linreg_data.read_name_file(name_map_file[0], name_map_file[1], name_map_file[2], header_name_map)

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
	if name_map_file[0] is not None:
		fieldnames.append('Gene_Symbol[MAF]')
		fieldnames.append('Gene_Symbol[UPDATED]')
	else:
		fieldnames.append('Gene_Symbol')
	fieldnames.append('Length')
	fieldnames.append('Mutation_Count')
	fieldnames.append('Studentized_Residual')
	output_writer = csv.writer(output_file, dialect='excel-tab')
	output_writer.writerow(fieldnames)
	symbol_list = linreg_data.symbol_list
	for i in range(0, len(symbol_list)):
		if name_map_file[0] is not None:
			newsymbol = symbol_list[i]
			oldsymbol = linreg_data.name_map.rev_get_name_for(newsymbol)
			if newsymbol not in linreg_data.data_dict:
				continue
			dataentry = linreg_data.data_dict[newsymbol]  # type: GeneLinregEntry
			row = list()
			row.append(oldsymbol)
			row.append(newsymbol)
			row.append(dataentry._length)
			row.append(dataentry._count)
			row.append(studres_result[i])
			output_writer.writerow(row)
		else:
			symbol = symbol_list[i]
			if (symbol not in linreg_data.symbol_list) or (symbol not in linreg_data.data_dict):
				continue
			dataentry = linreg_data.data_dict[symbol]  # type: GeneLinregEntry
			row = list()
			row.append(symbol)
			row.append(dataentry._length)
			row.append(dataentry._count)
			row.append(studres_result[i])
			output_writer.writerow(row)

if __name__ == "__main__":
	cli()
