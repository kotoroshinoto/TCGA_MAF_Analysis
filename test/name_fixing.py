from pathlib import Path
from gooch_test_util import *

colon_illumina_path = Path("E:\\dissertation\\data\\raw_data").joinpath("colon","Somatic_Mutations","BCM__IlluminaGA_DNASeq","Level_2")
maf_path = "%s" % colon_illumina_path.joinpath("hgsc.bcm.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.maf").absolute()
annotation_path = Path("E:\\dissertation\\data\\downloaded_annotations\\TCGA_Name_annotations\\UCSC_table_browser")

lengths_dir = Path(".").joinpath("test_output", "lengths")
maf_names_dir = lengths_dir.joinpath("MAF_NAMES")
maf_names_dir.mkdir(exist_ok=True)

original_dir = maf_names_dir.joinpath("ORIGINAL")
original_dir.mkdir(exist_ok=True)

orig_MAF_names = "%s" % original_dir.joinpath("MAF_names.txt").absolute()

#unique MAF symbols for name fixing
unqiue_maf_cmd = [
	"gooch_maf_tools", "names", "MAF_collect_unique_symbols",
	"--maf", maf_path,
	"--out", orig_MAF_names
]

orig_length_check = original_dir.joinpath("LENGTH_CHECK")
orig_length_check.mkdir(exist_ok=True)

gene_length_file = "%s" % lengths_dir.joinpath("Gene_Lengths_ucsc_refseq_merged.tsv").absolute()
length_matched_out = "%s" % orig_length_check.joinpath("names_ok.txt").absolute()
length_unmatched_out = "%s" % orig_length_check.joinpath("names_bad.txt").absolute()


name_check_cmd = [
	"gooch_maf_tools", "lengths", "name_check_length_file",
	"--mafnames", orig_MAF_names,
	"--genelength", gene_length_file,
	"--matched", length_matched_out,
	"--unmatched", length_unmatched_out
]

entrez_file = "%s" % annotation_path.joinpath("UCSC_entrez.table.names.tsv")

entrez_correction_path = maf_names_dir.joinpath("ENTREZ")
entrez_correction_path.mkdir(parents=True, exist_ok=True)

name_to_entrez_map = "%s" % entrez_correction_path.joinpath("MAF_names_entrez_ids.tsv").absolute()
maf_symb_no_entrez = "%s" % entrez_correction_path.joinpath("MAF_names_noentrez.txt").absolute()

entrez_corrected = "%s" % entrez_correction_path.joinpath("names_corrected.txt").absolute()
entrez_unmatched = "%s" % entrez_correction_path.joinpath("names_unmatched.txt").absolute()

entrez_id_cmd =[
	"gooch_maf_tools", "names", "MAF_collect_unique_entrez_ids",
	"--maf", "%s" % maf_path,
	"--outNoEntrez", maf_symb_no_entrez,
	"--out",  "%s" % name_to_entrez_map
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

#gather unique symbols
runcmd(unqiue_maf_cmd)

#check symbols that are already matched
runcmd(name_check_cmd)

#out of symbols that are not matched, collect unique symbols with entrez ids and unique symbols without entrez ids
runcmd(entrez_id_cmd)

#attempt to update those with entrez ids
runcmd(update_names_entrez_cmd)
