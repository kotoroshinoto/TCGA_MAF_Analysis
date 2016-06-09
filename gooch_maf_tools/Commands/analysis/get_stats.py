import rpy2.robjects.packages as rpackages
import rpy2.robjects as ro
from rpy2.robjects.vectors import StrVector
import click
import csv
import os
import sys


def check_r_packages(packagenames: list):
	results = dict()
	for package in packagenames:
		results[package] = rpackages.isinstalled(package)
	return results


def check_and_install_dependencies():
	required_r_packages = list(['e1071', 'MASS'])
	required_r_packages_install_status = check_r_packages(required_r_packages)
	need_to_install_r_packages = list()
	for package in required_r_packages_install_status:
		if not required_r_packages_install_status[package]:
			need_to_install_r_packages.append(package)
	if len(need_to_install_r_packages) > 0:
		utils = rpackages.importr('utils')
		utils.chooseCRANmirror(ind=1)
		utils.install_packages(StrVector(need_to_install_r_packages))

check_and_install_dependencies()
rpackages.importr('e1071')
rpackages.importr('MASS')


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
@click.argument('filename', nargs=1, type=click.File('r'))
@click.argument('output', nargs=1, required=False, default=None, type=click.Path(dir_okay=False, writable=True))
def compute_kurtosis_location(filename, output):
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


class GeneData4Linreg:
	def __init__(self, symbol, count, length):
		self.symbol = str(symbol)
		self.count = int(count)
		self.length = int(length)


def read_gene_counts_into_dict(in_file: csv.DictReader):
	data = dict()
	for line in in_file:
		entry = GeneData4Linreg(line['Gene_Symbol'], line['Count'], line['Length'])
		data[entry.symbol] = entry
	return data


@cli.command(name='Gene_Outliers', help="compute studentized residuals for list of gene counts")
@click.argument('filename', nargs=1, type=click.File('r'))
@click.argument('output', nargs=1, required=False, default=None, type=click.Path(dir_okay=False, writable=True))
def compute_studentized_residuals_genes(filename, output):
	fields = list(['Gene_Symbol', 'Count', 'Length'])
	gene_file_reader = csv.DictReader(filename, fieldnames=fields, dialect='excel-tab')
	data = read_gene_counts_into_dict(gene_file_reader)
	output_file = open(output, newline='', mode='w')
	output_writer = csv.writer(output_file, dialect='excel-tab')
	pass


@cli.command(name='Mutation_Type_T_Test', help="perform t-test on mutation-type files")
@click.argument('file1', nargs=2, type=(str, click.File('r')))
@click.argument('file2', nargs=2, type=(str, click.File('r')))
@click.argument('output', nargs=1, required=False, default=None, type=click.Path(dir_okay=False, writable=True))
def compute_mutation_type_t_test(file1,file2, output):
	file1_reader = csv.reader(file1[1], dialect='excel-tab')
	file2_reader = csv.reader(file2[1], dialect='excel-tab')
	output_file = open(output, newline='', mode='w')
	output_writer = csv.writer(output_file, dialect='excel-tab')
	pass
#https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html

if __name__ == "__main__":
	cli()

