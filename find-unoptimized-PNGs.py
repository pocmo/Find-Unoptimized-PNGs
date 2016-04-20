#!/usr/bin/python

import argparse
import distutils.spawn
import fnmatch
import os
import subprocess
import sys

TEMPORARY_FILE = "./tmp_optimized.png"

def main():
	parser = argparse.ArgumentParser(description='Find PNGs in need of optimization')
	parser.add_argument('--path', dest='path', action='store', help='Path to search for PNGs in (default: .)', default='.')
	parser.add_argument('--command', dest='command', action='store', help='Command to compress PNGs (default: pngcrush)', default='pngcrush')

	args = parser.parse_args()

	if not distutils.spawn.find_executable(args.command):
		sys.exit("Command %s not found" % args.command)

	optimized_files = []
	unoptimized_files = []

	for root, directory, files in os.walk(args.path):
		for item in fnmatch.filter(files, "*.png"):
			path = root + os.sep + item
			original_size = os.path.getsize(path)

			return_code = subprocess.call([args.command, path, TEMPORARY_FILE])
			if return_code is not 0:
				sys.exit("%s returned non-zero return code: %s" % (args.command, return_code))

			optimized_size = os.path.getsize(TEMPORARY_FILE)

			if (optimized_size < original_size):
				unoptimized_files.append((path, original_size, optimized_size))
			else:
				optimized_files.append(path)

			os.remove(TEMPORARY_FILE)

	print "%s file(s) are optimized, %s file(s) are in need of optimization" % (len(optimized_files), len(unoptimized_files))

	total_bytes = 0
	optimized_bytes = 0
	total_saved = 0

	if unoptimized_files:
		for (path, original_size, optimized_size) in unoptimized_files:
			difference = original_size - optimized_size
			percentage = (int) (100 / float(original_size) * float(difference))
			print path
			print "-" + str(percentage) + "% / -" + str(difference) + " bytes   original=" + str(original_size) + " bytes, optimized=" + str(optimized_size) + " bytes"
			print
			total_saved += difference
			total_bytes += original_size
			optimized_bytes += optimized_size

		print "%s files with %s bytes, %s bytes optmized (- %s bytes)" % (len(optimized_files) + len(unoptimized_files), total_bytes, optimized_bytes, total_saved)

if __name__ == '__main__':
    main()
