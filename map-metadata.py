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


def valid_input(string):
    """Checks if string is a valid input directory"""
    path = os.path.abspath(string)
    if not os.path.exists(path):
        error = f"Directory does not exists: {path}"
        raise argparse.ArgumentTypeError(error)
    if not os.path.isdir(path):
        error = f"Not a directory: {path}"
        raise argparse.ArgumentTypeError(error)
    return path


def valid_output(string):
    """Checks if string is a valid output directory and creates it if needed"""
    path = os.path.abspath(string)
    if not os.path.isdir(path):
        print(f"Creating {path}")
        os.mkdir(path)
    return path


def parse_arguments():
    """Processes the arguments"""
    parser = CustomArgumentParser(usage="%(prog)s [OPTIONS] INPUT OUTPUT")

    parser.add_argument("input_dir", type=valid_input)

    parser.add_argument("output_dir", type=valid_output)

    args = parser.parse_args()
    return args

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    """Main function"""
    # Loop through input folder's contents
    for song_name in os.listdir(args.input_dir):
        # Find matches and process them
        match = SONG_REGEX.match(song_name)
        if match:
            artists, title = get_artists_and_title(match)
            # Process the file
            subprocess.run([
                'ffmpeg', '-y',
                '-i', os.path.join(args.input_dir, song_name),
                '-metadata', 'artist={}'.format(artists),
                '-metadata', 'title={}'.format(title),
                '-c', 'copy',
                os.path.join(args.output_dir, song_name)
            ])

# Entry point
if __name__ == "__main__":
    args = parse_arguments()

    try:
        main()
    except KeyboardInterrupt:
        print("\nUser interrupt", file=sys.stderr)
        sys.exit(1)
