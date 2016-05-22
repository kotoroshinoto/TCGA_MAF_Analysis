import click
from .Commands import MAF_counter
from .Commands import exon_sizer
from .Commands import get_COSMIC_status


@click.group(name='TEST')
def cli():
	pass

cli.add_command(MAF_counter.cli, "MAF_counter")
cli.add_command(exon_sizer.cli, "exon_sizer")
cli.add_command(get_COSMIC_status.cli, "get_COSMIC_status")

if __name__ == "__main__":
	cli()
