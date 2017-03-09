import rpy2.robjects.packages as rpackages
import rpy2.robjects as ro
import click
import csv
import sys
from typing import List
from typing import Dict
from ..get_stats.util import *


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


@click.command(name='Mutation_Type_T_Test', help="perform t-test on mutation type data")
@click.option('--file', nargs=2, type=(str, click.File('r')), required=True, multiple=True)
@click.option('--output', nargs=1, required=False, default=None, type=click.Path(dir_okay=False, writable=True))
def cli(file, output):
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

if __name__ == "__main__":
	cli()
