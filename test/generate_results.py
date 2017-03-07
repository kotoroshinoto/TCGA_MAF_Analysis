from pathlib import Path
from shutil import copyfile
out_dir = Path(".").joinpath("test_output","lengths","MAF_NAMES")
out_dir = out_dir
def cat_files(file_list, target_file):
	out_handle = open(target_file, "w")
	for file in file_list:
		handle = open(file,"r")
		for line in handle:
			line = line.rstrip()
			print(line, file=out_handle)
original = out_dir.joinpath("ORIGINAL","LENGTH_CHECK")
symbolcheck = out_dir.joinpath("SYMBOLCHECK","LENGTH_CHECK")
entrez_correction = out_dir.joinpath("ENTREZ_CORRECTION","LENGTH_CHECK")

original_ok = original.joinpath("names_ok.txt")
symbolcheck_ok = symbolcheck.joinpath("corrected_names_ok.txt")
entrez_correction_ok = entrez_correction.joinpath("names_corrected_ok.txt")

symbolcheck_approved = out_dir.joinpath("SYMBOLCHECK","approved.txt")
symbolcheck_bad = symbolcheck.joinpath("corrected_names_bad.txt")
entrez_correction_bad = entrez_correction.joinpath("names_corrected_bad.txt")

symbolcheck_unmatched = out_dir.joinpath("SYMBOLCHECK","unmatched.txt")

result_dir = Path(".").joinpath("RESULTS")
result_dir.mkdir(exist_ok=True)
approved_in = result_dir.joinpath("approved_symbols_in_UCSC_genes.txt")
approved_not_in = result_dir.joinpath("approved_symbols_not_in_UCSC_genes.txt")

unrecognized_symbols = result_dir.joinpath("unrecognized_symbols.txt")

cat_files([
	original_ok,
	symbolcheck_ok,
	entrez_correction_ok
], approved_in)

cat_files([
	symbolcheck_approved,
	symbolcheck_bad,
	entrez_correction_bad
], approved_not_in)

copyfile("%s" % symbolcheck_unmatched.absolute(), "%s" % unrecognized_symbols.absolute())
