from pathlib import Path
from gooch_test_util import *

# Usage: gooch_maf_tools names fix_symbols [OPTIONS]
#
#   Create output MAF with updated symbols, add additional columns showing
#   what the old symbols were, and whether the symbol should be considered up-
#   to-date or not
#
# Options:
#   --maf FILENAME                  path to maf file  [required]
#   --original <FILENAME INTEGER INTEGER>...
#                                   path to original lengthcheck file,
#                                   original_name column index, newname column
#                                   index
#   --symbolcheck <FILENAME INTEGER INTEGER>...
#                                   path to symbolcheck lengthcheck file,
#                                   original_name column index, newname column
#                                   index
#   --entrez <FILENAME INTEGER INTEGER>...
#                                   path to entrez lengthcheck file,
#                                   original_name column index, newname column
#                                   index
#   --manual <FILENAME INTEGER INTEGER>...
#                                   path to file containing manually curated
#                                   symbols, original_name column index, newname
#                                   column index
#   --out FILENAME                  output path to write changed maf entries
#   --help                          Show this message and exit.
data_directory = Path("E:\\dissertation\\data\\raw_data")
colon_path = data_directory.joinpath("colon")
somatic_colon_mutations = colon_path.joinpath("Somatic_Mutations")
illumina_path = somatic_colon_mutations.joinpath("BCM__IlluminaGA_DNASeq")
illumina_path = illumina_path.joinpath("Level_2")
maf_path = illumina_path.joinpath("hgsc.bcm.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.maf")

maf_name_dir = Path(".").joinpath("test_output", "lengths", "MAF_NAMES")
original_path = maf_name_dir.joinpath("ORIGINAL", "LENGTH_CHECK", "names_ok.txt")
entrez_path = maf_name_dir.joinpath("ENTREZ", "LENGTH_CHECK", "names_corrected_ok.txt")
symbchk_path = maf_name_dir.joinpath("SYMBOLCHECK", "LENGTH_CHECK", "corrected_names_ok.txt")
manual_path = maf_name_dir.joinpath("HAND_CURATED", "names.tsv")


fixed_symbols_dir = Path(".").joinpath("test_output", "fixed_symbols")
fixed_symbols_dir.mkdir(exist_ok=True)
out_path = fixed_symbols_dir.joinpath("hgsc.bcm.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.maf")

symbol_fixer_cmd = [
	"gooch_maf_tools", "names", "fix_symbols",
	"--maf", "%s" % maf_path.absolute(),
	"--original", "%s" % original_path.absolute(), "0", "1",
	"--symbolcheck", "%s" % symbchk_path.absolute(), "0", "1",
	"--entrez", "%s" % entrez_path.absolute(), "0", "1",
	"--manual", "%s" % manual_path.absolute(), "0", "1",
	"--out", "%s" % out_path.absolute()
]

runcmd(symbol_fixer_cmd)
