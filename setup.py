import sys
import os
from setuptools import setup, find_packages
from pip.req import parse_requirements

if sys.version_info.major < 3:
	print("I'm only for python 3, please upgrade")
	sys.exit(1)

install_reqs = parse_requirements(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt'), session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
	name='gooch_maf_tools',
	version='0.1.dev1',
	packages=find_packages(),
	include_package_data=True,
	install_requires=reqs,
	description="tools for working with TCGA MAF files",
	long_description="""\
	Several scripts for working with util files and TSV files. Fixing symbol names, querying large MAF files, etc.
	""",
	author="Michael Gooch",
	author_email="goochmi@gmail.com",
	url="https://github.com/kotoroshinoto/TCGA_MAF_Analysis",
	classifiers=[
		"Programming Language :: Python :: 3 :: Only",
	],
	entry_points={
		'console_scripts': [
		'gooch_maf_tools = gooch_maf_tools.main:gooch_maf_tools'
		]
	}
)
