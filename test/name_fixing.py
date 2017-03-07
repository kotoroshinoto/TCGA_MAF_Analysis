from pathlib import Path
import subprocess

data_directory = Path("E:\\dissertation\\data\\raw_data")
colon_path = data_directory.joinpath("colon")
somatic_colon_mutations = colon_path.joinpath("Somatic_Mutations")
illumina_path = somatic_colon_mutations.joinpath("BCM__IlluminaGA_DNASeq","Level_2")
maf_path = illumina_path.joinpath("hgsc.bcm.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.maf")

annotation_path = Path("E:\\dissertation\\data\\downloaded_annotations\\TCGA_Name_annotations\\UCSC_table_browser")
lengths_dir = Path(".").joinpath("test_output", "lengths")
maf_names_dir = lengths_dir.joinpath("MAF_NAMES")
maf_names_dir.mkdir(exist_ok=True)

original_dir = maf_names_dir.joinpath("ORIGINAL")
original_dir.mkdir(exist_ok=True)

orig_length_check = original_dir.joinpath("LENGTH_CHECK")
orig_length_check.mkdir(exist_ok=True)

orig_MAF_names = "%s" % original_dir.joinpath("MAF_names.txt").absolute()
gene_length_file = "%s" % lengths_dir.joinpath("Gene_Lengths_ucsc_refseq_merged.tsv").absolute()
length_matched_out = "%s" % orig_length_check.joinpath("names_ok.txt").absolute()
length_unmatched_out = "%s" % orig_length_check.joinpath("names_bad.txt").absolute()

# entrez_mafnames = orig_length_check.joinpath()
name_to_entrez_map = "%s" % maf_names_dir.joinpath("ENTREZ_REF","MAF_names_entrez_ids.tsv").absolute()
entrez_file = "%s" % annotation_path.joinpath("UCSC_entrez.table.names.tsv")
entrez_correction_path = maf_names_dir.joinpath("ENTREZ_CORRECTION")
entrez_correction_path.mkdir(exist_ok=True)
entrez_corrected = "%s" % entrez_correction_path.joinpath("names_corrected.txt").absolute()
entrez_unmatched = "%s" % entrez_correction_path.joinpath("names_unmatched.txt").absolute()

#unique MAF symbols for name fixing
unqiue_maf_cmd = [
	"gooch_maf_tools", "names", "MAF_collect_unique_symbols",
	"--maf", "%s" % maf_path,
	"--out", "%s" % orig_MAF_names
]

name_check_cmd = [
	"gooch_maf_tools", "lengths", "name_check_length_file",
	"--mafnames", orig_MAF_names,
	"--genelength", gene_length_file,
	"--matched", length_matched_out,
	"--unmatched", length_unmatched_out
]

update_names_entrez_cmd = [
	"gooch_maf_tools", "names", "update_names_entrez",
	"--mafnames", length_unmatched_out,
	"--name_to_entrez", name_to_entrez_map,
	"--entrez", entrez_file,
	"--col-entrez", "3",
	"--col-symbol", "1",
	"--outcorrected", entrez_corrected,
	"--outunmatched", entrez_unmatched
]


def exec_command(cmd):
	print(" ".join(cmd))
	subprocess.run(cmd)

exec_command(unqiue_maf_cmd)
exec_command(name_check_cmd)
exec_command(update_names_entrez_cmd)
