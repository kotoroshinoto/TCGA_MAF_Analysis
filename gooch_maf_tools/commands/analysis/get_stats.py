import rpy2.robjects.packages as rpackages
import rpy2.robjects as ro
from rpy2.robjects.vectors import StrVector
import click
import csv
import os
import sys
from typing import List
from typing import Dict


def check_r_packages(packagenames: list):
	results = dict()
	for package in packagenames:
		results[package] = rpackages.isinstalled(package)
	return results


def check_and_install_R_dependency(library_name: str):
	required_r_packages = list([library_name])
	required_r_packages_install_status = check_r_packages(required_r_packages)
	need_to_install_r_packages = list()
	for package in required_r_packages_install_status:
		if not required_r_packages_install_status[package]:
			need_to_install_r_packages.append(package)
	if len(need_to_install_r_packages) > 0:
		utils = rpackages.importr('utils')
		utils.chooseCRANmirror(ind=1)
		utils.install_packages(StrVector(need_to_install_r_packages))


def build_position_dicts_from_location_file(csv_file_reader: csv.reader):
	num_key_columns = 4
	positions = dict()
	gene_symbols = list()
	category_labels = dict()
	first_line = True
	for entry in csv_file_reader:
		if first_line:
			first_line = False
			if entry[0] != 'GENE_SYMBOL':
				click.echo("FIRST LINE IS NOT A HEADER:\n\t%s" % '\t'.join(entry), err=True)
				click.echo("First Column of first line: %s" % entry[0])
				exit(-1)  # TODO maybe implement user-defined columns and labels for files with no header
			numcolumns = len(entry)
			category_count = numcolumns - num_key_columns
			for i in range(num_key_columns, num_key_columns + category_count):
				category_labels[entry[i]] = i
				if entry[i] not in positions:
					positions[entry[i]] = dict()
			continue
		gene_symbol = entry[0]
		if gene_symbol not in gene_symbols:
			gene_symbols.append(gene_symbol)
		# click.echo('gene_symbol: %s' % gene_symbol)
		pos_string = "%s|%s|%s" % (entry[1], entry[2], entry[3])
		# click.echo('pos_string: %s' % pos_string)
		for label in category_labels:
			# click.echo('label: %s' % label)
			count_column = category_labels[label]
			# click.echo('count column: %d' % count_column)
			count = int(entry[count_column])
			# click.echo('count: %d' % count)
			if count > 0:
				if gene_symbol not in positions[label]:
					positions[label][gene_symbol] = dict()
				if pos_string in positions[label][gene_symbol]:
					click.echo("[WARNING]: Duplicate position entry detected! %s -> %s" % (gene_symbol, pos_string), err=True)
					exit(-1)
				positions[label][gene_symbol][pos_string] = count
	return positions, gene_symbols, category_labels


def compute_kurtosis_string(label_positions, gene_symbol):
	label_symbol_positions = label_positions[gene_symbol]
	if len(label_symbol_positions.keys()) == 0:
		return None
	if len(label_symbol_positions.keys()) == 1:
		return None
	num_list = list()
	for pos_str in label_symbol_positions:
		count = label_symbol_positions[pos_str]
		split_pos = pos_str.split('|')
		chrom = split_pos[0]
		start = int(split_pos[1])
		end = int(split_pos[2])
		if start != end:  # skip Multi-Nucleotide Mutations
			continue
		if count == 1:
			num_list.append(str(start))
		else:
			num_list.append('rep(%d,%d)' % (start, count))
	if len(num_list) <= 1:
		return None
	return ','.join(num_list)


def compute_kurtosis(kurt_str, label):
	r_command_1 = "%s <- c(%s)" % (label, kurt_str)
	r_command_2 = 'kurtosis(%s)' % label
	ro.r(r_command_1)
	result = ro.r(r_command_2)[0]
	return result


@click.group(name="get_stats", help='perform statistics on tabular data files', no_args_is_help=True)
def cli():
	pass


#highly negative kurtosis indicates uniform distribution. Highly positive kurtosis implies very thin distributions
@cli.command(name='locations', help='Produce kurtosis calculations from mutation locations file')
@click.option('--file', nargs=1, type=click.File('r'))
@click.option('--output', nargs=1, required=False, default=None, type=click.Path(dir_okay=False, writable=True))
def compute_kurtosis_location(filename, output):
	check_and_install_R_dependency('e1071')
	rpackages.importr('e1071')
	output_file = None
	output_csv_writer = None
	if output is None:
		output_file = sys.stdout
	else:
		output_file = open(output, mode='w', newline='')
	output_csv_writer = csv.writer(output_file, dialect='excel-tab')
	csv_reader = csv.reader(filename, dialect='excel-tab')
	positions, gene_symbol_list, label_list = build_position_dicts_from_location_file(csv_reader)
	# positions = positions_tuple[0]
	# gene_symbol_list = positions_tuple[1]
	# label_list = positions_tuple[2]
	first_line = list()
	first_line.append("GENE_SYMBOL")
	for label in label_list:
		first_line.append(label)
	#write first line
	output_csv_writer.writerow(first_line)
	for gene_symbol in gene_symbol_list:
		output = list()
		output.append(gene_symbol)
		kurtosis_string_list = list()
		for label in label_list:
			if gene_symbol not in positions[label]:
				kurtosis_string_list.append("None (no counts)")
				continue
			label_positions = positions[label]
			kurt_str = compute_kurtosis_string(label_positions, gene_symbol)
			if kurt_str is not None:
				kurtosis_string_list.append(compute_kurtosis(kurt_str, label))
			else:
				kurtosis_string_list.append("None (Not Computable)")
		output += kurtosis_string_list
		output_csv_writer.writerow(output)


def revcomp(nuc: str) -> str:
	if nuc.upper() == 'A':
		return 'T'
	if nuc.upper() == 'T':
		return 'A'
	if nuc.upper() == 'C':
		return 'G'
	if nuc.upper() == 'G':
		return 'C'


class MutationTypeSampleEntry:

	@classmethod
	def get_data_column_labels(cls) -> List[str]:
		result = list()
		result.append('sample_ID')
		nucs = ['A', 'C', 'G', 'T']
		#changes
		for nuc1 in nucs:
			for nuc2 in nucs:
				if nuc1 == nuc2:
					continue
				result.append('%s_%s' % (nuc1, nuc2))
		#insertions
		for nuc in nucs:
			result.append('-_%s' % nuc)
		#deletions
		for nuc in nucs:
			result.append('%s_-' % nuc)
		result.append('MNC')
		return result

	@classmethod
	def get_calculated_column_labels(cls) -> List[str]:
		result = list(['INS', 'DEL', 'INDEL', 'TRANSITIONS', 'TRANSVERSIONS'])
		accounted_for = list()
		nucs = ['A', 'C', 'G', 'T']
		# changes
		for nuc1 in nucs:
			for nuc2 in nucs:
				if nuc1 == nuc2:
					continue
				pair = '%s_%s' % (nuc1, nuc2)
				revcomp_pair = '%s_%s' % (revcomp(nuc1), revcomp(nuc2))
				if pair in accounted_for:
					continue
				result.append('%s|%s' % (pair,revcomp_pair))
				accounted_for.append(pair)
				accounted_for.append(revcomp_pair)
		return result

	@classmethod
	def get_output_column_labels(cls) -> List[str]:
		return cls.get_data_column_labels() + cls.get_calculated_column_labels()

	def __init__(self, csvline: dict):
		self._sample_ID = csvline['sample_ID']  # type: str
		#changes
		self._A_T = int(csvline['A_T'])  # type: int
		self._A_G = int(csvline['A_G'])  # type: int
		self._A_C = int(csvline['A_C'])  # type: int
		self._T_A = int(csvline['T_A'])  # type: int
		self._T_G = int(csvline['T_G'])  # type: int
		self._T_C = int(csvline['T_C'])  # type: int
		self._G_A = int(csvline['G_A'])  # type: int
		self._G_T = int(csvline['G_T'])  # type: int
		self._G_C = int(csvline['G_C'])  # type: int
		self._G_A = int(csvline['G_A'])  # type: int
		self._C_A = int(csvline['C_A'])  # type: int
		self._C_G = int(csvline['C_G'])  # type: int
		self._C_T = int(csvline['C_T'])  # type: int
		#insertions
		self._insA = int(csvline['-_A'])  # type: int
		self._insT = int(csvline['-_T'])  # type: int
		self._insG = int(csvline['-_G'])  # type: int
		self._insC = int(csvline['-_C'])  # type: int
		#deletions
		self._delA = int(csvline['A_-'])  # type: int
		self._delT = int(csvline['T_-'])  # type: int
		self._delG = int(csvline['G_-'])  # type: int
		self._delC = int(csvline['C_-'])  # type: int
		#MNC
		self._mnc = int(csvline['MNC'])  # type: int
		self.func_dict = {  # type: Dict[str, int]
			'sample_ID': self.sample_id,
			'A_T': self.A_T,
			'A_G': self.A_G,
			'A_C': self.A_C,
			'T_A': self.T_A,
			'T_G': self.T_G,
			'T_C': self.T_C,
			'G_T': self.G_T,
			'G_A': self.G_A,
			'G_C': self.G_C,
			'C_A': self.C_A,
			'C_T': self.C_T,
			'C_G': self.C_G,
			'-_A': self.insA,
			'-_T': self.insT,
			'-_G': self.insG,
			'-_C': self.insC,
			'A_-': self.delA,
			'T_-': self.delT,
			'G_-': self.delG,
			'C_-': self.delC,
			'MNC': self.MNC,
			'INS': self.INS,
			'DEL': self.DEL,
			'INDEL': self.INDEL,
			'TRANSITIONS': self.transitions,
			'TRANSVERSIONS': self.transversions,
			'A_C|T_G': self.A_C_or_T_G,
			'A_G|T_C': self.A_G_or_T_C,
			'A_T|T_A': self.A_T_or_T_A,
			'C_A|G_T': self.C_A_or_G_T,
			'C_G|G_C': self.C_G_or_G_C,
			'C_T|G_A': self.C_T_or_G_A
		}

	def sample_id(self) -> str:
		return self._sample_ID

	def A_T(self) -> int:
		return self._A_T

	def A_G(self) -> int:
		return self._A_G

	def A_C(self) -> int:
		return self._A_C

	def T_A(self) -> int:
		return self._T_A

	def T_G(self) -> int:
		return self._T_G

	def T_C(self) -> int:
		return self._T_C

	def G_A(self) -> int:
		return self._G_A

	def G_T(self) -> int:
		return self._G_T

	def G_C(self) -> int:
		return self._G_C

	def C_A(self) -> int:
		return self._C_A

	def C_T(self) -> int:
		return self._C_T

	def C_G(self) -> int:
		return self._C_G

	def insA(self) -> int:
		return self._insA

	def insT(self) -> int:
		return self._insT

	def insG(self) -> int:
		return self._insG

	def insC(self) -> int:
		return self._insC

	def delA(self) -> int:
		return self._delA

	def delT(self) -> int:
		return self._delT

	def delG(self) -> int:
		return self._delG

	def delC(self) -> int:
		return self._delC

	def MNC(self) -> int:
		return self._mnc

	def __getitem__(self, item) -> int:
		return self.func_dict[item]()

	def INS(self) -> int:
		return self._insA + self._insC + self._insG + self._insT

	def DEL(self) -> int:
		return self._delA + self._delC + self._delG + self._delT

	def INDEL(self) -> int:
		return self.INS() + self.DEL()

	#chemically identical mutations (strand insensitive perspective)
	def A_T_or_T_A(self) -> int:
		return self._A_T + self._T_A

	def C_G_or_G_C(self) -> int:
		return self._C_G + self._G_C

	def C_T_or_G_A(self) -> int:
		return self._C_T + self._G_A

	def A_C_or_T_G(self) -> int:
		return self._A_C + self._T_G

	def A_G_or_T_C(self) -> int:
		return self._A_G + self._T_C

	def C_A_or_G_T(self) -> int:
		return self._C_A + self._G_T

	def transitions(self) -> int:
		return self.C_T_or_G_A() + self.A_G_or_T_C()

	def transversions(self) -> int:
		return self.A_T_or_T_A() + self.C_G_or_G_C() + self.C_A_or_G_T() + self.A_C_or_T_G()

	def total_mut_count(self) -> int:
		return self.transitions() + self.transversions() + self.INDEL() + self.MNC()

	def output_dict(self) -> Dict[str, int]:
		outdict = dict()
		outdict['sample_ID'] = self._sample_ID
		outdict['A_C'] = self._A_C
		outdict['A_T'] = self._A_T
		outdict['A_G'] = self._A_G

		outdict['T_A'] = self._T_A
		outdict['T_C'] = self._T_C
		outdict['T_G'] = self._T_G

		outdict['C_A'] = self._C_A
		outdict['C_T'] = self._C_T
		outdict['C_G'] = self._C_G

		outdict['G_A'] = self._G_A
		outdict['G_T'] = self._G_T
		outdict['G_C'] = self._G_C

		outdict['-_A'] = self._insA
		outdict['-_T'] = self._insT
		outdict['-_C'] = self._insC
		outdict['-_G'] = self._insG

		outdict['A_-'] = self._delA
		outdict['T_-'] = self._delT
		outdict['C_-'] = self._delC
		outdict['G_-'] = self._delG

		outdict['MNC'] = self._mnc

		outdict['INS'] = self.INS()
		outdict['DEL'] = self.DEL()
		outdict['INDEL'] = self.INDEL()

		outdict['TRANSITIONS'] = self.transitions()
		outdict['TRANSVERSIONS'] = self.transversions()

		outdict['A_C|T_G'] = self.A_C_or_T_G()
		outdict['A_G|T_C'] = self.A_G_or_T_C()

		outdict['A_T|T_A'] = self.A_T_or_T_A()
		outdict['C_A|G_T'] = self.C_A_or_G_T()

		outdict['C_G|G_C'] = self.C_G_or_G_C()
		outdict['C_T|G_A'] = self.C_T_or_G_A()
		return outdict


class GroupMutationData:
	def __init__(self, label):
		self._data = dict()  # type: Dict[str, MutationTypeSampleEntry]
		self._samples = list()  # type: List[str]
		self.group_label = label

	def __contains__(self, item) -> bool:
		return item in self._data

	def __getitem__(self, item) -> MutationTypeSampleEntry:
		return self._data[item]

	def __setitem__(self, key, value):
		if key in self._data:
			raise ValueError("Sample ID showed up more than once")
		self._data[key] = value
		self._samples.append(key)

	def samples(self) -> List[str]:
		return self._samples

	def get_column(self, mut_type) -> List[int]:
		retlist = list()
		for sample_id in self._samples:
			retlist.append(self._data[sample_id][mut_type])
		return retlist

	def get_normalized_column(self, mut_type) -> List[float]:
		normalized_list = list()
		for sample_id in self._samples:
			countval = float(self._data[sample_id][mut_type])
			totalval = float(self._data[sample_id].total_mut_count())
			normalized_list.append(countval / totalval)
		return normalized_list

	@classmethod
	def __read_file__(cls, file: csv.DictReader, label: str):
		group_data = cls(label)
		for line in file:
			sample_data = MutationTypeSampleEntry(line)
			group_data[sample_data.sample_id()] = sample_data
		return group_data


class GroupedMutationData:
	def __init__(self):
		self._groups = list()
		self._data = dict()

	def __contains__(self, item) -> bool:
		return item in self._groups

	def __getitem__(self, item) -> GroupMutationData:
		return self._data[item]

	def __setitem__(self, key, value):
		if key in self._data:
			raise click.BadArgumentUsage("Cannot use same label more than once")
		self._data[key] = value
		self._groups.append(key)

	def groups(self) -> List[str]:
		return self._groups

	def read_file(self, file: csv.DictReader, label: str):
		group_data = GroupMutationData.__read_file__(file, label)
		self[label] = group_data


def perform_t_test(data: GroupedMutationData, use_proportions=False) -> Dict[str, Dict[str, int]]:
	#first index str will be mut_type, 2nd will be according to the dictwriter's rules
	mut_type_keys = MutationTypeSampleEntry.get_output_column_labels()
	mut_type_values = dict()  # type: Dict[str, Dict[str, ro.IntVector]]
	# create int vectors for use with R
	for group_label in data.groups():
		group = data[group_label]
		mut_type_values[group_label] = dict()
		for mut_type_str in mut_type_keys:
			if mut_type_str == 'sample_ID':
				continue
			# print(column)
			if use_proportions:
				column = group.get_normalized_column(mut_type_str)
				r_vector = ro.FloatVector(column)
			else:
				column = group.get_column(mut_type_str)
				r_vector = ro.IntVector(column)
			mut_type_values[group_label][mut_type_str] = r_vector
	# perform t test
	# get R object for t test function:
	r_t_test = ro.r['t.test']
	# iterate over pairs of vectors, calling t test function for each and storing results.
	t_test_result_dict = dict()  # type: Dict[str, Dict]
	htest_components = ['statistic', 'parameter', 'p.value', 'conf.int', 'estimate', 'null.value', 'alternative', 'method']
	result_dict = dict()
	for mut_type_str in mut_type_keys:
		if mut_type_str == 'sample_ID':
			continue
		out_row = dict()
		out_row['mut_type'] = mut_type_str
		vals_group1 = mut_type_values[data.groups()[0]]
		vals_group2 = mut_type_values[data.groups()[1]]
		v_1 = vals_group1[mut_type_str]
		v_2 = vals_group2[mut_type_str]
		# print(v_1)
		# print(v_2)
		r_result = r_t_test(v_1, v_2)
		# print(r_result)
		for str_key in htest_components:
			tmp = r_result.rx(str_key)

			print_str = str_key + '\t'
			if str_key == 'conf.int' or str_key == 'estimate':
				# print_str += str(tmp[0][0])
				# print_str += '\t'
				# print_str += str(tmp[0][1])
				out_row[str_key + '_%s' % data.groups()[0]] = tmp[0][0]
				out_row[str_key + '_%s' % data.groups()[1]] = tmp[0][1]
			else:
				out_row[str_key] = tmp[0][0]
			# print_str += str(tmp[0][0])
		result_dict[mut_type_str] = out_row
	return result_dict


@cli.command(name='Mutation_Type_T_Test', help="perform t-test on mutation type data")
@click.option('--file', nargs=2, type=(str, click.File('r')), required=True, multiple=True)
@click.option('--output', nargs=1, required=False, default=None, type=click.Path(dir_okay=False, writable=True))
def compute_mutation_type_t_test(file, output):

	#handle args and read files
	if len(file) != 2:
		raise click.BadArgumentUsage("require --file option 2 times for t-test")
	file1 = file[0]
	file2 = file[1]
	file1_reader = csv.DictReader(file1[1], dialect='excel-tab')
	file2_reader = csv.DictReader(file2[1], dialect='excel-tab')
	data = GroupedMutationData()
	data.read_file(file1_reader, file1[0])
	data.read_file(file2_reader, file2[0])
	#pull list of strings to use as keys
	mut_type_keys = MutationTypeSampleEntry.get_output_column_labels()
	output_file = None
	if output is None:
		output_file = sys.stdout
	else:
		output_file = open(output, newline='', mode='w')
	field_names_output = ['mut_type', 'statistic', 'parameter', 'p.value', 'conf.int_%s' % data.groups()[0], 'conf.int_%s' % data.groups()[1], 'estimate_%s' % data.groups()[0], 'estimate_%s' % data.groups()[1], 'null.value', 'alternative', 'method']
	print('Raw Counts', file=output_file)
	print('\t'.join(field_names_output), file=output_file)
	output_writer = csv.DictWriter(output_file, fieldnames=field_names_output, dialect='excel-tab')

	t_test_dict = perform_t_test(data)
	for mut_type_str in mut_type_keys:
		if mut_type_str == 'sample_ID':
			continue
		output_writer.writerow(t_test_dict[mut_type_str])

	print('\nNormalized Counts', file=output_file)
	print('\t'.join(field_names_output), file=output_file)
	normal_t_test_dict = perform_t_test(data, use_proportions=True)
	for mut_type_str in mut_type_keys:
		if mut_type_str == 'sample_ID':
			continue
		output_writer.writerow(normal_t_test_dict[mut_type_str])


#https://stat.ethz.ch/R-manual/R-devel/library/stats/html/# t.test.html


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
			raise ValueError("UPDATED  symbol: \"%s\" does not have an existing mapping" % nameold)
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
		self.name_map = GeneNameMap()  # type: GeneNameMap

	def read_count_file(self, filehandle, name_col: int, count_col: int, has_header: bool):
		reader = csv.reader(filehandle, dialect='excel-tab')
		if has_header:
			next(reader)  # skip first line

		for row in reader:
			oldsymbol = row[name_col]
			newsymbol = self.name_map.get_name_for(oldsymbol)
			if newsymbol not in self.data_dict:
				entry = GeneLinregEntry(newsymbol)  # type: GeneLinregEntry
				self.data_dict[newsymbol] = entry
				self.symbol_list.append(newsymbol)
			else:
				entry = self.data_dict[newsymbol]  # type: GeneLinregEntry
			entry._count = int(row[count_col])

	def read_length_file(self, filehandle, name_col: int, length_col: int, has_header: bool):
		reader = csv.reader(filehandle, dialect='excel-tab')
		if has_header:
			next(reader)  # skip first line
		for row in reader:
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

	def read_name_file(self, filehandle, old_col: int, new_col: int, has_header: bool):
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


@cli.command(name='Gene_Outliers', help="compute studentized residuals for list of gene counts")
@click.option('--count_file', type=(click.File('r'), int, int), default=(None, None, None), required=True, help="count file, symbol column, count column")
@click.option('--length_file', type=(click.File('r'), int, int), default=(None, None, None), required=True, help="length file, symbol column,  length column")
@click.option('--name_map_file', type=(click.File('r'), int, int), default=(None, None, None), required=True, help="names file, old name column, new name column")
@click.option('--header_count/--noheader_count', default=True)
@click.option('--header_length/--noheader_length', default=True)
@click.option('--header_name_map/--noheader_name_map', default=True)
@click.option('--output', required=False, default=None, type=click.Path(dir_okay=False, writable=True), help="output file path")
@click.pass_context
def compute_studentized_residuals_genes(ctx, count_file, length_file, name_map_file, output, header_count, header_length, header_name_map):
	errormsg=list()
	if count_file[0] is None:
		errormsg.append("--count_file is required")
	if length_file[0] is None:
		errormsg.append("--length_file is required")
	if name_map_file[0] is None:
		errormsg.append("--name_map_file is required")
	if len(errormsg) > 0:
		print(compute_studentized_residuals_genes.get_help(ctx))
		raise click.UsageError(', '.join(errormsg))
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
	fieldnames.append('Gene Symbol[MAF]')
	fieldnames.append('Gene Symbol[UPDATED]')
	fieldnames.append('Length')
	fieldnames.append('Mutation Count')
	fieldnames.append('Studentized Residual')
	output_writer = csv.writer(output_file, dialect='excel-tab')
	output_writer.writerow(fieldnames)
	symbol_list = linreg_data.symbol_list
	for i in range(0, len(symbol_list)):
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

if __name__ == "__main__":
	cli()

