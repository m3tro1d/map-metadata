import argparse
import os
import re
import subprocess
import sys


# Regexp for files in format "artist - title.mp3"
song_regex = re.compile(r'(.+) - (.+)\.mp3')


# Parse input parameters
parser = argparse.ArgumentParser(
	description="""This script maps metadata from files' names, so you don't
have to enter it manually.""")

parser.add_argument("input_dir",
	help="directory to grab mp3 files from")

parser.add_argument("output_dir",
	help="directory to place processed files to")

args = parser.parse_args()
input_dir = args.input_dir
output_dir = args.output_dir

# Loop through folders contents
	# Match file regex and process the file
