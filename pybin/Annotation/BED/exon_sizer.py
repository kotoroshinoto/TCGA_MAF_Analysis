#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse

def next_bed(line):
	line = line.rstrip()
	split_line = line.split("\t")
	name = split_line[3].rstrip()

	lengths = split_line[10].split(',')
	total_length = 0
	for length in lengths:
		if len(length) > 0:
			total_length += int(length)
	#print("%s\t%s" %(name, total_length))
	return [name, total_length]


def next_name(line, col_from, col_to):
	line = line.rstrip()
	if len(line) == 0:
		return None
	split_line = line.split("\t")
	#print("# of columns: %d" % (len(split_line)))
	if len(split_line) <= col_from or len(split_line) <= col_to:
		return None
	name_from = split_line[col_from].rstrip()
	if len(name_from) == 0:
		return None
	name_to = split_line[col_to].rstrip()
	#print("%s -> %s" %(name_from, name_to))
	return [name_from, name_to]


parser = argparse.ArgumentParser(description="Compute exonic sizes of genes and relate them to HUGO IDs")
parser.add_argument('--bed', type=argparse.FileType('r'), required=True, help="path to a bed file containing genes & exons")
parser.add_argument('--names', type=argparse.FileType('r'), required=True, help="path to a file relating BED file names to desired names")
parser.add_argument('--columns', type=str, required=True, help="CSV pair of values, first column's names match those from the BED file, second names match those to use in the output")
args = parser.parse_args()
splitValues = args.columns.split(',')

fromCol = int(splitValues[0]) - 1
toCol = int(splitValues[1]) - 1
names_fh = args.names

bed_fh = args.bed

Name_Map = dict()

#build map of names
for name in names_fh:
	nametuple = next_name(name, fromCol, toCol)
	if nametuple is not None:
		Name_Map[nametuple[0]] = nametuple[1]

Value_Map = dict()
for bedline in bed_fh:
	bedtuple = next_bed(bedline)
	gene_name = Name_Map[bedtuple[0]]
	length = bedtuple[1]
	if gene_name not in Value_Map:
		Value_Map[gene_name] = list()
	Value_Map[gene_name].append(length)

Lengths = dict()

for gene_name in Value_Map:
	value_list = Value_Map[gene_name]
	average = sum(value_list)/len(value_list)
	print("%s\t%d" % (gene_name, average))

