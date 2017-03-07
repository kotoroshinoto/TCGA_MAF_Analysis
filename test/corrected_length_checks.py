from pathlib import Path
import subprocess

annotation_path = Path("E:\\dissertation\\data\\downloaded_annotations\\TCGA_Name_annotations\\UCSC_table_browser")

out_dir = Path(".").joinpath("test_output", "lengths")
maf_names_dir = out_dir.joinpath("MAF_NAMES")

symbolcheck_dir = maf_names_dir.joinpath("SYMBOLCHECK")
symbolcheck_length_check_dir = symbolcheck_dir.joinpath("LENGTH_CHECK")
symbolcheck_length_check_dir.mkdir(exist_ok=True)
symbolcheck_OK_file = symbolcheck_length_check_dir.joinpath("corrected_names_ok.txt")
symbolcheck_BAD_file = symbolcheck_length_check_dir.joinpath("corrected_names_bad.txt")
symbolcheck_corrected_file = symbolcheck_dir.joinpath("corrected.txt")


ucsc_refseq_file = annotation_path.joinpath("Gene_Lengths_ucsc_refseq_merged.tsv")

#convert to strings
ucsc_refseq_file = "%s" % ucsc_refseq_file.absolute()
symbolcheck_OK_file = "%s" % symbolcheck_OK_file.absolute()
symbolcheck_BAD_file = "%s" % symbolcheck_BAD_file.absolute()
symbolcheck_corrected_file = "%s" % symbolcheck_corrected_file.absolute()

#check symbol_check output
symbolcheck_cmd =[
	"gooch_maf_tools", "lengths", "name_check_length_file",
	"--mafnames", symbolcheck_corrected_file,
	"--genelength", ucsc_refseq_file,
	"--checkcolumn", "1",
	"--oldcolumn", "0",
	"--keep",
	"--matched", symbolcheck_OK_file,
	"--unmatched", symbolcheck_BAD_file
]

entrez_dir = maf_names_dir.joinpath("ENTREZ_CORRECTION")
entrez_corrected_file = entrez_dir.joinpath("names_corrected.txt")
entrez_length_check_dir = entrez_dir.joinpath("LENGTH_CHECK")
entrez_length_check_dir.mkdir(exist_ok=True)
entrez_OK_file = entrez_length_check_dir.joinpath("names_corrected_ok.txt")
entrez_BAD_file = entrez_length_check_dir.joinpath("names_corrected_bad.txt")


#convert to strings
entrez_corrected_file = "%s" % entrez_corrected_file.absolute()
entrez_OK_file = "%s" % entrez_OK_file.absolute()
entrez_BAD_file = "%s" % entrez_BAD_file.absolute()

#check merged UCSC & refseq output
ucsc_refseq_check_cmd = [
	"gooch_maf_tools", "lengths", "name_check_length_file",
	"--mafnames", entrez_corrected_file,
	"--genelength", ucsc_refseq_file,
	"--checkcolumn", "1",
	"--oldcolumn", "0",
	"--keep",
	"--matched", entrez_OK_file,
	"--unmatched", entrez_BAD_file
]


def exec_command(cmd):
	print(" ".join(cmd))
	subprocess.run(cmd)

exec_command(symbolcheck_cmd)
exec_command(ucsc_refseq_check_cmd)
