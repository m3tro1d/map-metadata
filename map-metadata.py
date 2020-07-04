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

args = parser.parse_args()

# Loop through folders contents
	# Match file regex and process the file
