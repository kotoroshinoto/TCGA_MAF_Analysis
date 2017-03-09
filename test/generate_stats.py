from pathlib import Path
from gooch_test_util import *

# Usage: gooch_maf_tools analysis get_stats Gene_Outliers [OPTIONS]
#
#   compute studentized residuals for list of gene counts
#
# Options:
#   --count_file <FILENAME INTEGER INTEGER>...
#                                   count file, symbol column, count column
#                                   [required]
#   --length_file <FILENAME INTEGER INTEGER>...
#                                   length file, symbol column,  length column
#                                   [required]
#   --name_map_file <FILENAME INTEGER INTEGER>...
#                                   names file, old name column, new name column
#   --header_count / --noheader_count
#   --header_length / --noheader_length
#   --header_name_map / --noheader_name_map
#   --output PATH                   output file path
#   --help                          Show this message and exit.

#gooch_maf_tools analysis get_stats Gene_Outliers
#--count_file test_output\low_group\low.gene.counts 0 1
#--length_file test_output\lengths\Gene_Lengths_ucsc_refseq_merged.tsv 0 1
#--output test_output\gene_linreg.tsv

# Usage: gooch_maf_tools analysis get_stats Mutation_Type_T_Test
#            [OPTIONS]
#
#   perform t-test on mutation type data
#
# Options:
#   --file <TEXT FILENAME>...  [required]
#   --output PATH
#   --help                     Show this message and exit.

#gooch_maf_tools analysis get_stats Mutation_Type_T_Test
#--file LOW test_output\low_group\low.mutation_type.per_sample.counts
#--file HIGH test_output\high_group\high.mutation_type.per_sample.counts
#--output test_output\mutation_type_t_test.tsv

# Usage: gooch_maf_tools analysis get_stats locations [OPTIONS]
#
#   Produce kurtosis calculations from mutation locations file
#
# Options:
#   --file FILENAME
#   --output PATH
#   --help           Show this message and exit.

#gooch_maf_tools analysis get_stats locations --file test_output\low_group\low.location.counts --output test_output\low.kurtosis.tsv
#gooch_maf_tools analysis get_stats locations --file test_output\high_group\high.location.counts --output test_output\high.kurtosis.tsv