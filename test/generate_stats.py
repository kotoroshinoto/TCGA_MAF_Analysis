from pathlib import Path
from gooch_test_util import *

test_output_dir = Path(".").joinpath("test_output")
count_analysis_dir = test_output_dir.joinpath("count_analysis")
lowdir = test_output_dir.joinpath("low_group")
highdir = test_output_dir.joinpath("high_group")
length_file = "%s" % test_output_dir.joinpath("lengths", "MAF_NAMES", "COMBINED_LENGTHS", "ucsc_refseq_and_manual_lengths_combined.tsv").absolute()
manual_length_file = "%s" % test_output_dir.joinpath("lengths", "MAF_NAMES", "HAND_CURATED", "lengths.tsv").absolute()
low_gene_count = "%s" % lowdir.joinpath("low.gene.counts").absolute()
high_gene_count = "%s" % highdir.joinpath("high.gene.counts").absolute()

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

low_outlier_file = "%s" % count_analysis_dir.joinpath("low.gene_linreg.tsv").absolute()
high_outlier_file = "%s" % count_analysis_dir.joinpath("high.gene_linreg.tsv").absolute()

low_outlier_cmd = [
	"gooch_maf_tools", "analysis", "get_stats", "Gene_Outliers",
	"--count_file", low_gene_count, "0", "1",
	"--length_file", length_file, "0", "1",
	"--output", low_outlier_file
]
high_outlier_cmd = [
	"gooch_maf_tools", "analysis", "get_stats", "Gene_Outliers",
	"--count_file", high_gene_count, "0", "1",
	"--length_file", length_file, "0", "1",
	"--output", high_outlier_file
]

low_mut_type_per_sample = "%s" % lowdir.joinpath("low.mutation_type.per_sample.counts").absolute()
high_mut_type_per_sample = "%s" % highdir.joinpath("high.mutation_type.per_sample.counts").absolute()
mut_type_t_test_out = "%s" % count_analysis_dir.joinpath("mutation_type_t_test.tsv").absolute()

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

mut_type_t_test_cmd = [
	"gooch_maf_tools", "analysis", "get_stats", "Mutation_Type_T_Test",
	"--file", "LOW", low_mut_type_per_sample,
	"--file", "HIGH",  high_mut_type_per_sample,
	"--output", mut_type_t_test_out
]


# Usage: gooch_maf_tools analysis get_stats locations [OPTIONS]
#
#   Produce kurtosis calculations from mutation locations file
#
# Options:
#   --file FILENAME
#   --output PATH
#   --help           Show this message and exit.

low_location_counts = "%s" % lowdir.joinpath("low.location.counts").absolute()
high_location_counts = "%s" % highdir.joinpath("high.location.counts").absolute()
low_kurt = "%s" % count_analysis_dir.joinpath("low.kurtosis.tsv").absolute()
high_kurt = "%s" % count_analysis_dir.joinpath("high.kurtosis.tsv").absolute()

#gooch_maf_tools analysis get_stats locations
#--file test_output\low_group\low.location.counts
#--output test_output\low.kurtosis.tsv

#gooch_maf_tools analysis get_stats locations
#--file test_output\high_group\high.location.counts
#--output test_output\high.kurtosis.tsv

low_kurtosis_cmd = [
	"gooch_maf_tools", "analysis", "get_stats", "locations",
	"--file", low_location_counts,
	"--output", low_kurt
]

high_kurtosis_cmd = [
	"gooch_maf_tools", "analysis", "get_stats", "locations",
	"--file", high_location_counts,
	"--output", high_kurt
]

runcmd(low_outlier_cmd)
runcmd(high_outlier_cmd)
runcmd(mut_type_t_test_cmd)
runcmd(low_kurtosis_cmd)
runcmd(high_kurtosis_cmd)
