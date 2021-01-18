from textwrap import dedent
import argparse
import os
import re
import subprocess
import sys

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Globals
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Regexp for files in format "artist - title.mp3"
SONG_REGEX = re.compile(r'(.+) - (.+)\.mp3')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CustomArgumentParser(argparse.ArgumentParser):
    """Override ArgumentParser's help message"""
    def format_help(self):
        help_text = dedent(f"""\
        map-metadata is a script for quickly mapping mp3 metadata
        with ffmpeg.

        Usage: {self.prog} [OPTIONS] INPUT OUTPUT

        INPUT:
          Directory containing files for mapping

        OUTPUT:
          Directory to place the processed files in

        Options:
          -h,  --help     show help

        For more information visit:
        https://github.com/m3tro1d/map-metadata
        """)
        return help_text

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_artists_and_title(match):
    """Returns a tuple of artists and title in specified name"""
    # This will correctly display multiple artists in windows
    artists = match.group(1).replace(', ', ';')
    title = match.group(2)
    return (artists, title)


def parse_arguments():
    """Processes the arguments"""
    parser = CustomArgumentParser(usage="%(prog)s [OPTIONS] INPUT OUTPUT")

    parser.add_argument("input_dir")

    parser.add_argument("output_dir")

    args = parser.parse_args()
    return args


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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    """Main function"""
    # Check the directories
    check_dirs(args.input_dir, args.output_dir)
    # Process the songs
    process_files(args.input_dir, args.output_dir)

# Entry point
if __name__ == "__main__":
    args = parse_arguments()

    main()
