import click
import os
import sys

import gooch_maf_tools.MAF_counter

@click.group(name='TEST')
def cli():
	print("DERP")
	return

cli.add_command(gooch_maf_tools.MAF_counter.main, "COUNT")

if __name__ == "__main__":
	cli()
