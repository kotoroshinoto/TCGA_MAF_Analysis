import click
from ..analysis import COUNT_merge
from ..analysis import MAF_counter
from ..analysis import MAF_merge
from ..analysis import MAF_merge_with_label
from ..analysis import get_COSMIC_status
from ..analysis import split_maf_with_counts
from ..analysis import get_stats

# from ._get_stats import main as get_stats


@click.group(name='analysis', help='performing counts and analysis')
def analysis():
	pass

analysis.add_command(MAF_counter.cli, "MAF_counter")
analysis.add_command(COUNT_merge.cli, "COUNT_merge")
analysis.add_command(split_maf_with_counts.cli, "MAF_count_split")
analysis.add_command(MAF_merge.cli, "MAF_merge")
analysis.add_command(MAF_merge_with_label.cli, "MAF_merge_with_label")
analysis.add_command(get_stats.cli, 'get_stats')
analysis.add_command(get_COSMIC_status.cli, "get_COSMIC_status")

if __name__ == "__main__":
	analysis()
