#!/usr/bin/env bash
COMMAND_PATH=''
ANNOTATION_PATH=$COMMAND_PATH/downloaded_annotations/TCGA_Name_annotations
SET COUNT_PATH=$COMMAND_PATH/tabular_data/counts/hgsc.bcm.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.maf.counts.0-999.gene.counts
python -m gooch_maf_tools.main analysis get_stats Gene_Outliers --length_file $ANNOTATION_PATH/gene_lengths.tsv 0 1 --name_map_file $ANNOTATION_PATH/maf_to_official_translated.txt 0 1 --count_file $COUNT_PATH 0 1