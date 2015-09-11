#!/usr/bin/env python3
__author__ = 'mgooch'
import argparse
import re
import sys
parser = argparse.ArgumentParser(description="Compute exonic sizes of genes and relate them to HUGO IDs")
parser.add_argument('--mafnames', type=argparse.FileType('r'), required=True, help="file of names to be translated")
parser.add_argument('--names', type=argparse.FileType('r'), required=True, help="file of names from annotation lists")
parser.add_argument('--size', type=argparse.FileType('r'), required=False, help="file of sizes that has names")
parser.add_argument('--column', type=int, required=True, help="column where desired name is found")
parser.add_argument('--symbolcheck', type=argparse.FileType('r'), required=True, help="TSV output from http://www.genenames.org/cgi-bin/symbol_checker")
args = parser.parse_args()
toCol = int(args.column) - 1
mafnames_fh = args.mafnames
MAF_names = list()

#pull MAF names from file
for line in mafnames_fh:
	line = line.rstrip()
	MAF_names.append(line)
mafnames_fh.close()

#build map of names from symbolcheck file
symbolcheck_map = dict()
if args.symbolcheck is not None:
	for line in args.symbolcheck:
		line = line.rstrip()
		split_line = line.split("\t")
		if len(split_line) > 3:
			symbolcheck_map[split_line[0]] = split_line[2]

#build list of lines from names file
names_fh = args.names
name_lines = list()
for line in names_fh:
	line = line.rstrip()
	if len(line) > 0:
		name_lines.append(str(line.rstrip()))


#build list of names from size file if one was given
Size_File_Name_List = list()
if args.size is not None:
	for line in args.size:
		line = line.rstrip()
		if len(line) > 0:
			split_line = line.split("\t")
			name = split_line[0]
			Size_File_Name_List.append(name)
			#print("added name: %s" % name)

#build list of names from names file for quick check
Easy_List = list()
for line in name_lines:
	line = line.rstrip()
	if len(line) > 0:
		split_line = line.split("\t")
		Easy_List.append(split_line[toCol])

Name_Map = dict()
for name in MAF_names:
	if name not in Name_Map:
		if name in Size_File_Name_List:
			print("original name OK for: %s" % name, file=sys.stderr)
			Name_Map[name] = name
for name in MAF_names:
	if name not in Name_Map:
		if name in Easy_List:
			print("original name OK for: %s" % name, file=sys.stderr)
			Name_Map[name] = name
for name in MAF_names:
	if name in Name_Map:
		if name in symbolcheck_map:
			if Name_Map[name] != symbolcheck_map[name]:
				print("symbolcheck name conflicts with existing choice for: %s | %s; %s" % (name, Name_Map[name], symbolcheck_map[name]), file=sys.stderr)
	else:
		if name in symbolcheck_map:
			Name_Map[name] = symbolcheck_map[name]

for name in MAF_names:
	match_found = False
	if name in Name_Map:
		match_found = True
	else:
		sys.stderr.write("searching for a match for %s; " % name)
		for line in name_lines:
			regex_matcher_str = "[\s]" + name + "[,\s]"
			matchobj = re.search(regex_matcher_str, line)
			if matchobj:
				match_found = True
				print("line: %s" % line, file=sys.stderr)
				split_line = line.split("\t")
				to_name = split_line[toCol]
				Name_Map[name] = to_name
				# print("%s\t%s" % (name, to_name))
	if not match_found:
		print("no match was found for: %s" % name, file=sys.stderr)
for name in Name_Map:
	print("%s\t%s" % (name, Name_Map[name]))