__author__ = 'mgooch'
import os
import sys

from GenericFormats import MAF


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


class SampMutCounter(FeatureCounter):
	def count(self, entry: MAF.Entry):
		self.__appendcount__(entry.data['Tumor_Sample_Barcode'])
		# self.__appendcount__(entry.Tumor_Sample_UUID)


class MutTypeCounter(FeatureCounter):
	def count(self, entry: MAF.Entry):
		mut_type_list = entry.determine_mutation()
		for mut_type in mut_type_list:
			self.__appendcount__(mut_type)
