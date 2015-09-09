#!/usr/bin/env python
__author__ = 'mgooch'
from biomart import BiomartServer
import argparse

parser = argparse.ArgumentParser(description="Pull Down New Gene Lists from biomart ensembl database")
parser.add_argument('--outFull', type=argparse.FileType('w'), required=True, help="file to write entries that have both HGNC symbol AND entrez IDs")
parser.add_argument('--outEntrez', type=argparse.FileType('w'), help="file to write entries that only have entrez IDS")
parser.add_argument('--outHugo', type=argparse.FileType('w'), help="file to write entries that only have HGNC symbols")
parser.add_argument('--outEnsembl', type=argparse.FileType('w'), help="file to write entries that have neither HGNC symbols nor entrez ids")
args = parser.parse_args()

server = BiomartServer( "http://www.biomart.org/biomart" )
hsapiens_gene = server.datasets['hsapiens_gene_ensembl']

_params = dict()
_params['attributes'] = list()
_params['attributes'].append('ensembl_gene_id')
_params['attributes'].append('hgnc_symbol')
_params['attributes'].append('entrezgene')

#_params['filters'] = dict()
#_params['filters']['gene_id'] = list()
#_params['filters']['gene_id'].append('1')

response = hsapiens_gene.search(params=_params)
for line in response.iter_lines():
	line_split = line.split("\t")
	ensembl_name = line_split[0].rstrip()
	hgnc_name = line_split[1].rstrip()
	entrez_id = line_split[2].rstrip()
	if len(hgnc_name) > 0 and len(entrez_id) > 0:
		args.outFull.write("%s\t%s\t%s\n" % (ensembl_name, hgnc_name, entrez_id))
	elif len(hgnc_name) == 0 and len(entrez_id) > 0:
		args.outEntrez.write("%s\t%s\n" % (ensembl_name, entrez_id))
	elif len(hgnc_name) > 0 and len(entrez_id) == 0:
		args.outHugo.write("%s\t%s\n" % (ensembl_name, hgnc_name))
	else:
		args.outEnsembl.write("%s\n" % ensembl_name)
