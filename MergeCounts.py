import click
import os
import sys
import csv

maxInt = sys.maxsize
decrement = True
while decrement:
	decrement = False
	try:
		csv.field_size_limit(maxInt)
	except OverflowError:
		maxInt = int(maxInt/10)
		decrement = True

