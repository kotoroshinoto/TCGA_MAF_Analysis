import os
import sys
import shutil
from pathlib import Path

names_to_not_delete = ["lengths","MAF_NAMES"] # this file contains some files we don't want to remove and some that we do want to remove
names_to_skip_recursion = ["GENE_NAMES_ORG", "HAND_CURATED"] # these files were produced externally, cannot regenerate

for root, dirs, files in os.walk(Path(".").joinpath("test_output")):
	parentpath = Path(root)
	# print("BEFORE root: %s; dirs: %s; files:%s" % (root, dirs, files))
	i =0
	while i < len(dirs):
		dir = dirs[i]
		# sys.stdout.write("dir: %s;" % dir)
		dir_to_remove = "%s" % parentpath.joinpath(dir).absolute()
		if dir in names_to_skip_recursion:
			# print("skip recursion: %s" % dir_to_remove)
			dirs.remove(dir)
		elif dir not in names_to_not_delete:
			print("remove directory tree: %s" % dir_to_remove)
			shutil.rmtree(dir_to_remove)
			dirs.remove(dir)
		else:
			# print("do not remove, recurse into directory: %s" % dir_to_remove)
			i += 1
	for file in files:
		file_to_remove = "%s" % parentpath.joinpath(file).absolute()
		print("remove file: %s" % file_to_remove)
		os.remove(file_to_remove)
	# print(" AFTER root: %s; dirs: %s; files:%s" % (root, dirs, files))

