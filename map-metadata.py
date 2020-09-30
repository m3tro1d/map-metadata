import argparse
import os
import re
import subprocess
import sys


# Regexp for files in format "artist - title.mp3"
SONG_REGEX = re.compile(r'(.+) - (.+)\.mp3')


def get_artists_and_title(match):
    """Returns a tuple of artists and title in specified name"""
    # This will correctly display multiple artists in windows
    artists = match.group(1).replace(', ', ';')
    title = match.group(2)
    return (artists, title)


def parse_arguments():
    """Processes the arguments"""
    parser = argparse.ArgumentParser(
        description="""This script maps metadata from files' names, so you don't
        have to enter it manually.""")
    parser.add_argument("input_dir",
                        help="directory to grab mp3 files from")
    parser.add_argument("output_dir",
                        help="directory to place processed files to")
    return parser.parse_args()


def check_dirs(input_dir, output_dir):
    """Checks if the dirs are presented & creates output_dir if necessary"""
    # Check input directory
    if not os.path.exists(input_dir):
        print("Directory '{}' does not exist, exiting.".format(input_dir))
        sys.exit(1)
    # Check output directory
    if not os.path.exists(output_dir):
        print("Creating '{}'...".format(output_dir))
        os.mkdir(output_dir)


def process_files(input_dir, output_dir):
    """Processes the files"""
    # Loop through input folder's contents
    for song_name in os.listdir(input_dir):
        # Find matches and process them
        match = SONG_REGEX.match(song_name)
        if match:
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


def main():
    """Entry point of the script"""
    # Get the input arguments
    args = parse_arguments()
    input_dir = os.path.realpath(args.input_dir)
    output_dir = os.path.realpath(args.output_dir)

    # Check the directories
    check_dirs(input_dir, output_dir)

    # Process the songs
    process_files(input_dir, output_dir)

# Entry point
if __name__ == "__main__":
    main()
