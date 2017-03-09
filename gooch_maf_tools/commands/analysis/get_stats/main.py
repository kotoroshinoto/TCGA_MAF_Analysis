import click
from ..get_stats import mut_location_kurtosis
from ..get_stats import mut_type_t_test
from ..get_stats import mutcount_length_linreg


@click.group(name="get_stats", help='perform statistics on tabular data files', no_args_is_help=True)
def get_stats():
	pass

get_stats.add_command(mut_location_kurtosis.cli, "locations")
get_stats.add_command(mut_type_t_test.cli, "Mutation_Type_T_Test")
get_stats.add_command(mutcount_length_linreg.cli, "Gene_Outliers")

if __name__ == "__main__":
	get_stats()

