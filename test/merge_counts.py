from pathlib import Path
from gooch_test_util import *
# Usage: gooch_maf_tools analysis COUNT_merge [OPTIONS] COMMAND [ARGS]...
#
#   This program is intended to be used to merge tabular count files produced
#   by different MAF files. Will insert zeroes for missing values
#
# Options:
#   --in <TEXT FILENAME>...  string is label to use in output, file is file
#                            containing the type of counts you are trying to
#                            merge  [required]
#   --out PATH               file to write output to  [required]
#   --help                   Show this message and exit.
#
# Commands:
#   genes
#   locations
#   locations_mut_specific
#   mutation_type

outdir = Path(".").joinpath("test_output")
count_merge_dir = outdir.joinpath("count_analysis")
count_merge_dir.mkdir(parents=True, exist_ok=True)

lowdir = outdir.joinpath("low_group")
highdir = outdir.joinpath("high_group")

genecnt_merge_cmd = [
	"gooch_maf_tools", "analysis", "COUNT_merge",
	"--in", "LOW", "%s" % lowdir.joinpath("low.gene.counts").absolute(),
	"--in", "HIGH", "%s" % highdir.joinpath("high.gene.counts").absolute(),
	"--out", "%s" % count_merge_dir.joinpath("gene_counts_merged.tsv"),
	"genes"
]

locationscnt_merge_cmd = [
	"gooch_maf_tools", "analysis", "COUNT_merge",
	"--in", "LOW", "%s" % lowdir.joinpath("low.location.counts").absolute(),
	"--in", "HIGH", "%s" % highdir.joinpath("high.location.counts").absolute(),
	"--out", "%s" % count_merge_dir.joinpath("location_counts_merged.tsv"),
	"locations"
]

locations_mutspecif_cnt_merge_cmd = [
	"gooch_maf_tools", "analysis", "COUNT_merge",
	"--in", "LOW", "%s" % lowdir.joinpath("low.mutation_type.at.location.counts").absolute(),
	"--in", "HIGH", "%s" % highdir.joinpath("high.mutation_type.at.location.counts").absolute(),
	"--out", "%s" % count_merge_dir.joinpath("mut_specific_location_counts_merged.tsv"),
	"locations_mut_specific"
]

mutation_type_cnt_merge_cmd = [
	"gooch_maf_tools", "analysis", "COUNT_merge",
	"--in", "LOW", "%s" % lowdir.joinpath("low.mutation_type.counts").absolute(),
	"--in", "HIGH", "%s" % highdir.joinpath("high.mutation_type.counts").absolute(),
	"--out", "%s" % count_merge_dir.joinpath("mutation_type_counts_merged.tsv"),
	"mutation_type"
]

runcmd(genecnt_merge_cmd)
runcmd(locationscnt_merge_cmd)
runcmd(locations_mutspecif_cnt_merge_cmd)
runcmd(mutation_type_cnt_merge_cmd)
