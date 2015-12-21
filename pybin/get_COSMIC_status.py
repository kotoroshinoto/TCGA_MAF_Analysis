import sys
import os
import click
import abc
import Cosmic


@click.command(help="check cosmic prediction for mutation effects")
@click.option("--vcf", type=click.File('r'), required=True, help="cosmic VCF file")
@click.option("--cosmic", type=click.File('r'), required=True, help="cosmic TSV file")
@click.option("--maf", type=click.File('r'), required=True, help="TCGA file to be checked")
def cli(vcf, cosmic, maf):
	pass



if __name__ == "__main__":
	cli()
