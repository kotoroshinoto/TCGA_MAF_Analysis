__author__ = 'mgooch'
import os
import sys

from Formats import MAF


class FeatureCounter:
	def __init__(self):
		self.counts = dict()
		self.name = None

	def count(self, entry: MAF.Entry):
		return 0

	def __appendcount__(self, keystring):
		if keystring is None:
			return
		if keystring in self.counts:
			self.counts[keystring] += 1
		else:
			self.counts[keystring] = 1

	def __countif__(self, keystring, condition):
		if condition:
			self.__appendcount__(keystring)

	def __str__(self):
		str_val = ""
		for key in sorted(self.counts.keys()):
			str_val += "%s\t%s\n" % (key, self.counts[key])
		return str_val

	def write_file(self, path, prefix=None):
		realpath = os.path.realpath(os.path.relpath(prefix, start=path))
		if self.name is not None and len(self.name) > 0:
			out_file_name = ""
			if prefix is not None and len(prefix) > 0:
				out_file_name = os.path.realpath(os.path.relpath("%s_%s.txt" % (prefix, self.name), start=path))
				#$ofname=$path.'/'.$prefix.'_'.$self->{name}.".txt";
			else:
				out_file_name = os.path.realpath(os.path.relpath("%s.txt" % self.name, start=path))
				#$ofname=$path.'/'.$self->{name}.".txt";
	#		print "$ofname\n";
			out_file_handler = open(out_file_name, mode='w')
			out_file_handler.write("%s" % self)
			out_file_handler.close()
		else:
			print("writeFile used on counter with no name", file=sys.stderr)
			sys.exit(-1)


class GeneMutCounter(FeatureCounter):
	def count(self, entry: MAF.Entry):
		self.__appendcount__(entry.data['Hugo_Symbol'])


class LocMutCounter(FeatureCounter):
	def count(self, entry: MAF.Entry):
		#count according to GENE_CHROM_START_END
		self.__appendcount__("%s|%s|%s|%s|%s|%s" % (entry.data['Hugo_Symbol'], entry.data['Chrom'], entry.data['Start_Position'], entry.data['End_Position'], entry.data['Variant_Type'], entry.data['Variant_Classification']))

	def __str__(self):
		str_rep = "GENE_SYMBOL\t\CHROM\tSTART\tEND\tVARIANT_TYPE\tVARIANT_CLASS\tCOUNT\n"
		for item in self.counts:
			str_rep += "%s\t%d" % (item.replace("|", "\t"), self.counts[item])
			str_rep += "\n"
		return str_rep


class SampMutCounter(FeatureCounter):
	def count(self, entry: MAF.Entry):
		self.__appendcount__(entry.data['Tumor_Sample_Barcode'])
		# self.__appendcount__(entry.Tumor_Sample_UUID)


class MutTypeCounter(FeatureCounter):
	def count(self, entry: MAF.Entry):
		mut_type_list = entry.determine_mutation()
		for mut_type in mut_type_list:
			self.__appendcount__(mut_type)


class MutTypeAtLocCounter(FeatureCounter):
	def count(self, entry: MAF.Entry):
		mut_type_list = entry.determine_mutation()
		for mut_type in mut_type_list:
			self.__appendcount__("%s|%s|%s|%s|%s" % (entry.data['Hugo_Symbol'], entry.data['Chrom'], entry.data['Start_Position'], entry.data['End_Position'], mut_type))

	def __str__(self):
		str_rep = "GENE_SYMBOL\t\CHROM\tSTART\tEND\tMUT_TYPE\tCOUNT\n"
		for item in self.counts:
			str_rep += "%s\t%d" % (item.replace("|", "\t"), self.counts[item])
			str_rep += "\n"
		return str_rep


class MutTypePerSampCounter(FeatureCounter):
	def count(self, entry: MAF.Entry):
		mut_type_list = entry.determine_mutation()
		for mut_type in mut_type_list:
			combin_str = "%s_|_%s" % (entry.data['Tumor_Sample_Barcode'], mut_type)
			self.__appendcount__(combin_str)

	@staticmethod
	def prep_nuc_key_list():
		nuc_characters = list("ACTG")
		combo_keys = list()
		for nuc1 in nuc_characters:
			for nuc2 in nuc_characters:
				if nuc1 != nuc2:
					combo_keys.append(("%s_%s" % (nuc1, nuc2)))
			combo_keys.append(("-_%s" % nuc1))
			combo_keys.append(("%s_-" % nuc1))
		combo_keys.append("MNC")
		return combo_keys

	@staticmethod
	def initialize_sample_dictionary(sample_list):
		nuc_keys = MutTypePerSampCounter.prep_nuc_key_list()
		grid_dict = dict()
		for sample in sample_list:
			if sample not in grid_dict:
				grid_dict[sample] = dict()
				for key in nuc_keys:
					grid_dict[sample][key] = 0
		return grid_dict

	def get_grid_dict(self):
		samples = list()
		split_entries = list()
		for key in sorted(self.counts.keys()):
			key_split = list(key.split('_|_'))
			key_split.append(self.counts[key])
			split_entries.append(key_split)
			if key_split[0] not in samples:
				samples.append(key_split[0])
		grid_dict = MutTypePerSampCounter.initialize_sample_dictionary(samples)
		for entry in split_entries:
			grid_dict[entry[0]][entry[1]] = entry[2]
		return grid_dict

	def __str__(self):
		str_val = ""
		grid_dict = self.get_grid_dict()
		nuc_keys = MutTypePerSampCounter.prep_nuc_key_list()
		first_line = "sample_ID"
		for nuc_pair in nuc_keys:
			first_line += "\t" + nuc_pair
		first_line += "\n"
		for sample in grid_dict:
			entry_str = str(sample)
			for nuc_pair in nuc_keys:
				entry_str += "\t" + str(grid_dict[sample][nuc_pair])
			entry_str += "\n"
			str_val += entry_str
			# str_val += "%s\t%s\t%s\n" % (key_split[0], key_split[1], key_split[2])
		return first_line + str_val
