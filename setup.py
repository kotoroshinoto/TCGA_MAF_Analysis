import sys
from setuptools import setup, find_packages

if sys.version_info.major < 3:
	print("I'm only for python 3, please upgrade")
	sys.exit(1)

setup(
	name='gooch_annotation_tools',
	version='0.1',
	packages=find_packages(),
	include_package_data=True,
	install_requires=['Click>=5.1'],
	description="tools for working with TSV and TCGA files",
	long_description="""\
	Several scripts for working with TCGA files and TSV files. Fixing symbol names, querying large TSV files, etc.
	""",
	author="Michael Gooch",
	author_email="goochmi@gmail.com",
	url="https://github.com/kotoroshinoto/TCGA_MAF_Analysis",
	classifiers=[
		"Programming Language :: Python :: 3 :: Only",
	],
	entry_points='''
		[console_scripts]
		symbolquery=gooch_annotation_tools.pybin.Symbol_query:cli
		''',
)
