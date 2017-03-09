import click
from .commands.analysis.main import analysis
from .commands.lengths.main import lengths
from .commands.names.main import names


@click.group(name='gooch_maf_tools', help="collection of tools for working with MAF files and gene annotations")
def gooch_maf_tools():
	pass

gooch_maf_tools.add_command(analysis, "")
gooch_maf_tools.add_command(lengths, "")
gooch_maf_tools.add_command(names, "")

if __name__ == "__main__":
	gooch_maf_tools()
