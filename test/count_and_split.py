from pathlib import Path
import subprocess
data_directory = Path("E:\\dissertation\\data\\raw_data")
colon_path = data_directory.joinpath("colon")
somatic_colon_mutations = colon_path.joinpath("Somatic_Mutations")
illumina_path = somatic_colon_mutations.joinpath("BCM__IlluminaGA_DNASeq")
illumina_path = illumina_path.joinpath("Level_2")
maf_path = illumina_path.joinpath("hgsc.bcm.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.maf")

output_dir = Path(".")
output_dir = output_dir.joinpath("test_output")
output_dir.mkdir(exist_ok=True)

print("%s" % maf_path.absolute())
# Usage: gooch_maf_tools analysis MAF_counter [OPTIONS]
#
#   Count # of entries per gene in util file
#
# Options:
#   --maf FILENAME       file containing util entries  [required]
#   --out TEXT           path to use for output files
#   --nameprefix TEXT    use this prefix in output names instead of
#                        automatically generating one
#   --muttype            activate counting according to mutation types
#   --sample             activate counting according to sample ID
#   --gene               activate counting according to gene symbol
#   --muttypepersample   activate counting according to mutation type, but also
#                        tracking sample_id
#   --location           activate counting according to genomic location
#   --muttypeatlocation  count more specifically than location does, divides
#                        counts by mutation type at each location (probably
#                        won't condense data file very much)
#   --help               Show this message and exit.
count_cmd = ["gooch_maf_tools", "analysis", "MAF_counter",
             "--maf", "%s" % maf_path.absolute(),
             "--out", "%s" % output_dir.absolute(),
             "--nameprefix", "test_run_count",
             "--muttype",
             "--sample",
             "--gene",
             "--muttypepersample",
             "--location",
             "--muttypeatlocation"
             ]

# Usage: gooch_maf_tools analysis MAF_count_split [OPTIONS]
#
#   Count # of entries per gene in util file
#
# Options:
#   --counts FILENAME  file containing sample counts  [required]
#   --maf FILENAME     maf file to split  [required]
#   --key INTEGER      0-based column number to use as key in maf file
#                      [required]
#   --out_prefix TEXT  output path prefix
#   --boundaries TEXT  list of boundaries for splitting  [required]
#   --help             Show this message and exit.

count_file = output_dir.joinpath("test_run_count.sample.counts")

split_cmd = ["gooch_maf_tools", "analysis", "MAF_count_split",
             "--counts","%s" %count_file.absolute(),
             "--maf", "%s" % maf_path.absolute(),
             "--key", "15",
             "--out_prefix", "test_output\\test_split",
             "--boundaries", "1000"
             ]


low_maf_file = output_dir.joinpath("test_split.1-999.maf")
low_outdir = output_dir.joinpath("low_group")
high_maf_file = output_dir.joinpath("test_split.1000-above.maf")
high_outdir = output_dir.joinpath("high_group")

low_count_cmd = ["gooch_maf_tools", "analysis", "MAF_counter",
             "--maf", "%s" % low_maf_file.absolute(),
             "--out", "%s" % low_outdir.absolute(),
             "--nameprefix", "low",
             "--muttype",
             "--sample",
             "--gene",
             "--muttypepersample",
             "--location",
             "--muttypeatlocation"
             ]

high_count_cmd = ["gooch_maf_tools", "analysis", "MAF_counter",
             "--maf", "%s" % high_maf_file.absolute(),
             "--out", "%s" % high_outdir.absolute(),
             "--nameprefix", "high",
             "--muttype",
             "--sample",
             "--gene",
             "--muttypepersample",
             "--location",
             "--muttypeatlocation"
             ]

# subprocess.run(count_cmd)
# subprocess.run(split_cmd)
# subprocess.run(low_count_cmd)
# subprocess.run(high_count_cmd)

# Usage: gooch_maf_tools lengths exon_sizer [OPTIONS]
#
#   Compute exonic sizes of genes and relate them to HUGO IDs
#
# Options:
#   --ucsc <FILENAME FILENAME INTEGER INTEGER>...
#                                   first path is to a bed file containing genes
#                                   & exons from UCSC,
#                                   2nd path is to path to a
#                                   file relating BED file names to desired
#                                   names.
#                                   Ints are a pair of 0-based index
#                                   values for parsing the names file, first
#                                   column's names match those from the BED
#                                   file, second names match those to use in the
#                                   output
#   --refseq <FILENAME FILENAME INTEGER INTEGER>...
#                                   first path is to a bed file containing genes
#                                   & exons from REFSEQ,
#                                   2nd path is to path to
#                                   a file relating BED file names to desired
#                                   names.
#                                   Ints are a pair of 0-based index
#                                   values for parsing the names file, first
#                                   column's names match those from the BED
#                                   file, second names match those to use in the
#                                   output
#   --out FILENAME                  output file
#   --help                          Show this message and exit.

exon_sizer_cmd = ["gooch_maf_tools", "lengths", "exon_sizer",
                  
                  ]
