import click
from ..names import MAF_collect_unique_entrez_ids
from ..names import MAF_collect_unique_symbols 
from ..names import Symbol_fixer 
from ..names import Symbol_query 
from ..names import cosmic_name_clipper 
from ..names import parse_symbolcheck_output 
from ..names import update_names_entrez  


@click.group(name='names', help="correcting name mismatches")
def names():
	pass

names.add_command(cosmic_name_clipper.cli, "cosmic_name_clipper")
names.add_command(MAF_collect_unique_entrez_ids.cli, "MAF_collect_unique_entrez_ids")
names.add_command(MAF_collect_unique_symbols.cli, "MAF_collect_unique_symbols")
names.add_command(parse_symbolcheck_output.cli, "parse_symbolcheck")
names.add_command(Symbol_query.cli, "symbol_query")
names.add_command(update_names_entrez.cli, "update_names_entrez")
names.add_command(Symbol_fixer.cli, "fix_symbols")

if __name__ == "__main__":
	names()