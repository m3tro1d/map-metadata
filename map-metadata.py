import os
import re
import suprocess
import sys


# Regexp for files in format "artist - title.mp3"
song_regex = re.compile(r'(.+) - (.+)\.mp3')

# Parse input parameters

# Loop through folders contents
	# Match file regex and process the file
