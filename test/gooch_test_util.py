import subprocess


def cat_files(file_list, target_file):
	out_handle = open(target_file, "w")
	for file in file_list:
		handle = open(file,"r")
		for line in handle:
			line = line.rstrip()
			if line != "":
				print(line, file=out_handle)


def runcmd(cmd):
	print(" ".join(cmd))
	subprocess.run(cmd)