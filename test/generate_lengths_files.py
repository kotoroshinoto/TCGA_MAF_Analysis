from pathlib import Path
from gooch_test_util import *

annotation_path = Path("E:\\dissertation\\data\\downloaded_annotations\\TCGA_Name_annotations\\UCSC_table_browser")
refseq_bed_path = "%s" % annotation_path.joinpath("RefSeq_Human.bed").absolute()
refseq_names_tsv_path = "%s" % annotation_path.joinpath("UCSC_refseq.table.names.tsv").absolute()
ucsc_bed_path = "%s" % annotation_path.joinpath("UCSC_genes.bed").absolute()
ucsc_names_tsv_path = "%s" % annotation_path.joinpath("UCSC_genes.table.names.tsv").absolute()

length_dir = Path(".").joinpath("test_output", "lengths")
length_dir.mkdir(exist_ok=True)

both_out = "%s" % length_dir.joinpath("Gene_Lengths_ucsc_refseq_merged.tsv").absolute()
ucsc_out = "%s" % length_dir.joinpath("Gene_Lengths.ucsc.tsv").absolute()
refseq_out = "%s" % length_dir.joinpath("Gene_Lengths.refseq.tsv").absolute()

ucsc_refseq_merged_cmd = [
	"gooch_maf_tools", "lengths", "exon_sizer",
	"--refseq", refseq_bed_path, refseq_names_tsv_path, "0", "1",
	"--ucsc", ucsc_bed_path, ucsc_names_tsv_path, "0", "1",
	"--out", both_out
]

ucsc_cmd = [
	"gooch_maf_tools", "lengths", "exon_sizer",
	"--ucsc", ucsc_bed_path, ucsc_names_tsv_path, "0", "1",
	"--out", ucsc_out
]

refseq_cmd = [
	"gooch_maf_tools", "lengths", "exon_sizer",
	"--refseq", refseq_bed_path, refseq_names_tsv_path, "0", "1",
	"--out", refseq_out
]

data_directory = Path("E:\\dissertation\\data\\raw_data")
colon_path = data_directory.joinpath("colon")
somatic_colon_mutations = colon_path.joinpath("Somatic_Mutations")
illumina_path = somatic_colon_mutations.joinpath("BCM__IlluminaGA_DNASeq","Level_2")
maf_path = illumina_path.joinpath("hgsc.bcm.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.maf")
maf_names_path = length_dir.joinpath("MAF_NAMES")

runcmd(ucsc_refseq_merged_cmd)
runcmd(ucsc_cmd)
runcmd(refseq_cmd)


