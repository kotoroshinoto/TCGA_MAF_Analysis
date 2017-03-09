import click
from ..lengths import check_against_lengths_file
from ..lengths import exon_sizer


@click.group(name='lengths', help='work with gene lengths')
def lengths():
	pass

lengths.add_command(exon_sizer.cli, "exon_sizer")
lengths.add_command(check_against_lengths_file.cli, "name_check_length_file")

if __name__ == "__main__":
	lengths()
