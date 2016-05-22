import click
from .Commands import MAF_counter


@click.group(name='TEST')
def cli():
	print("DERP")
	return

cli.add_command(MAF_counter.cli, "COUNT")

if __name__ == "__main__":
	cli()
