from pathlib import Path
import subprocess
lengths_dir = Path(".").joinpath("test_output", "lengths")
maf_names_dir = lengths_dir.joinpath("MAF_NAMES")

symbolcheck_out_dir = maf_names_dir.joinpath("SYMBOLCHECK")
symbolcheck_out_dir.mkdir(exist_ok=True)
approved = "%s" % symbolcheck_out_dir.joinpath("approved.txt").absolute()
unmatched = "%s" % symbolcheck_out_dir.joinpath("unmatched.txt").absolute()
corrected = "%s" % symbolcheck_out_dir.joinpath("corrected.txt").absolute()

symbolcheck_file = "%s" % maf_names_dir.joinpath("GENE_NAMES_ORG", "entrez_unmatched_symbol_check.tsv").absolute()

symbolcheck_cmd = [
	"gooch_maf_tools", "names", "parse_symbolcheck",
	"--symbolcheck", symbolcheck_file,
	"--outApproved", approved,
	"--outUnmatched", unmatched,
	"--outCorrected", corrected
]


def exec_command(cmd):
	print(" ".join(cmd))
	subprocess.run(cmd)

exec_command(symbolcheck_cmd)
