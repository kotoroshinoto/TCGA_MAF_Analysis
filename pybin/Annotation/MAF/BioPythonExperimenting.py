#!/usr/bin/env python3
__author__ = 'mgooch'
import sys
from Bio import Entrez
Entrez.email = "goochmi@gmail.com"
handle = Entrez.esearch(db="gene", term="txid9606[Orgn] AND %s[sym]" % "TCP10L2", retmode="xml")
records = Entrez.read(handle)
handle.close()
for record in records['IdList']:
	print(record)
	geneHandle = Entrez.efetch(db="gene", id=record, retmode="xml")
	geneRecords = Entrez.read(geneHandle)[0]
	# for key in geneRecords:
		# print(key)
		#print(geneRecords[key])
	print(geneRecords['Entrezgene_gene'])
	geneHandle.close()