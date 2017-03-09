import subprocess
subprocess.run(["python", "generate_lengths_files.py"])
subprocess.run(["python", "name_fixing.py"])
subprocess.run(["python", "parse_symbolchecker.py"])
subprocess.run(["python", "corrected_length_checks.py"])
subprocess.run(["python", "generate_results.py"])
subprocess.run(["python", "fix_symbols.py"])
subprocess.run(["python", "count_and_split.py"])