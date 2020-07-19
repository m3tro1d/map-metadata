import argparse
import os
import re
import subprocess
import sys


def get_artists_and_title(match):
    """Returns a tuple of artists and title in specified name"""
    # This will correctly display multiple artists in windows
    artists = match.group(1).replace(', ', ';')
    title = match.group(2)
    return (artists, title)


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


# Process input directories
# Check input directory
if not os.path.exists(input_dir):
    print("Directory '{}' does not exist, exiting.".format(input_dir))
    sys.exit(1)
# Check output directory
if not os.path.exists(output_dir):
    print("Specified output directory '{}' does not exist, creating...".format(output_dir))
    os.mkdir(output_dir)
# Make them nice
input_dir = os.path.abspath(input_dir)
output_dir = os.path.abspath(output_dir)


# Loop through input folder's contents
for song_name in os.listdir(input_dir):
    # Find matches and process them
    match = song_regex.match(song_name)
    if match != None:
        artists, title = get_artists_and_title(match)
        # Process the file
        subprocess.run([
            'ffmpeg', '-y',
            '-i', os.path.join(input_dir, song_name),
            '-metadata', 'artist={}'.format(artists),
            '-metadata', 'title={}'.format(title),
            '-c', 'copy',
            os.path.join(output_dir, song_name)
        ])
