import click
from .Commands import MAF_counter
from .Commands import exon_sizer
from .Commands import get_COSMIC_status
from .Commands import check_against_lengths_file
from .Commands import cosmic_name_clipper
from .Commands import MAF_collect_unique_entrez_ids
from .Commands import MAF_collect_unique_symbols
from .Commands import MAF_merge
from .Commands import parse_symbolcheck_output
# from .Commands import Symbol_fixer
from .Commands import Symbol_query
from .Commands import split_maf_with_counts
from .Commands import update_names_entrez


@click.group(name='gooch_maf_tools')
def cli():
	pass

cli.add_command(MAF_counter.cli, "MAF_counter")
cli.add_command(exon_sizer.cli, "exon_sizer")
cli.add_command(get_COSMIC_status.cli, "get_COSMIC_status")
cli.add_command(check_against_lengths_file.cli, "name_check_length_file")
cli.add_command(cosmic_name_clipper.cli, "cosmic_name_clipper")
cli.add_command(MAF_collect_unique_entrez_ids.cli, "MAF_collect_unique_entrez_ids")
cli.add_command(MAF_collect_unique_symbols.cli, "MAF_collect_unique_symbols")
cli.add_command(MAF_merge.cli, "MAF_merge")
cli.add_command(parse_symbolcheck_output.cli, "parse_symbolcheck")
cli.add_command(Symbol_query.cli,"symbol_query")
# cli.add_command(Symbol_fixer.cli,"")
cli.add_command(split_maf_with_counts.cli, "MAF_count_split")
cli.add_command(update_names_entrez.cli,"update_names_entrez")

if __name__ == "__main__":
	cli()
