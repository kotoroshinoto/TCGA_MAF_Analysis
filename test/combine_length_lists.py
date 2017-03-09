from pathlib import Path
from gooch_test_util import *

length_dir = Path(".").joinpath("test_output","lengths")
browser_length_file = "%s" % length_dir.joinpath("Gene_Lengths_ucsc_refseq_merged.tsv").absolute()
manual_length_file = "%s" % length_dir.joinpath("MAF_NAMES","HAND_CURATED","lengths.tsv").absolute()
output_dir = length_dir.joinpath("MAF_NAMES", "COMBINED_LENGTHS")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = "%s" % output_dir.joinpath("ucsc_refseq_and_manual_lengths_combined.tsv")
cat_files([browser_length_file, manual_length_file], output_file)
