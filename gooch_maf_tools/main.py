import click

from .commands.lengths import exon_sizer
from .commands.lengths import check_against_lengths_file

from .commands.analysis import COUNT_merge
from .commands.analysis import get_COSMIC_status
from .commands.analysis import get_stats
from .commands.analysis import MAF_collect_unique_entrez_ids
from .commands.analysis import MAF_counter
from .commands.analysis import MAF_merge
from .commands.analysis import MAF_merge_variant_callers
from .commands.analysis import split_maf_with_counts


from .commands.names import cosmic_name_clipper
from .commands.names import MAF_collect_unique_symbols
from .commands.names import Symbol_query
from .commands.names import parse_symbolcheck_output
from .commands.names import update_names_entrez
from .commands.names import Symbol_fixer


@click.group(name='gooch_maf_tools', help="collection of tools for working with MAF files and gene annotations")
def cli():
	pass


@cli.group(name='names', help="correcting name mismatches")
def names():
	pass


@cli.group(name='lengths', help='work with gene lengths')
def lengths():
	pass


@cli.group(name='analysis', help='performing counts and analysis')
def analysis():
	pass

analysis.add_command(MAF_counter.cli, "MAF_counter")
analysis.add_command(COUNT_merge.cli, "COUNT_merge")
analysis.add_command(split_maf_with_counts.cli, "MAF_count_split")
analysis.add_command(MAF_merge.cli, "MAF_merge")
analysis.add_command(MAF_merge_variant_callers.cli, "MAF_merge_variant_callers")
analysis.add_command(get_stats.cli, 'get_stats')
analysis.add_command(get_COSMIC_status.cli, "get_COSMIC_status")


lengths.add_command(exon_sizer.cli, "exon_sizer")
lengths.add_command(check_against_lengths_file.cli, "name_check_length_file")

names.add_command(cosmic_name_clipper.cli, "cosmic_name_clipper")
names.add_command(MAF_collect_unique_entrez_ids.cli, "MAF_collect_unique_entrez_ids")
names.add_command(MAF_collect_unique_symbols.cli, "MAF_collect_unique_symbols")
names.add_command(parse_symbolcheck_output.cli, "parse_symbolcheck")
names.add_command(Symbol_query.cli, "symbol_query")
names.add_command(update_names_entrez.cli, "update_names_entrez")
names.add_command(Symbol_fixer.cli, "fix_symbols")


if __name__ == "__main__":
	cli()
