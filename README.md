TCGA_MAF_Analysis
=================
#object-files:
pybin/Cosmic/TSV.py <br>
pybin/Cosmic/VCF.py <br>
pybin/TCGA/MAFcounters.py <br>
pybin/TCGA/MAF.py <br>
pybin/TCGA/MAFSampleCountsList.py<br>

#functional script files:

##used for name fixes:
check_against_lengths_file.py <br>
exon_sizer.py <br>
MAF_collect_unique_entrez_ids.py <br>
MAF_collect_unique_sumbols.py <br>
parse_symbolcheck_output.py <br>
update_names_entrez.py <br>

##used for counting and grouping (splitting file by size boundaries): 
maf_counter.py <br>
split_maf_with_counts.py<br>

This is a work in progress. Hope to eventually combine these diverse functions into a single command-driven script.<br>

#Current Tasks:
*Complete unified name-fixing script
*Unify all scripts into a single command-driven script
*switch from argparse module to Click module