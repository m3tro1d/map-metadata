# Map-metadata
This is a simple program that simplifies metadata mapping for mp3 files.

# Requirements
* Python 3
* [FFmpeg](https://ffmpeg.org)

# Usage
```
Usage: map-metadata.py [OPTIONS] INPUT OUTPUT

INPUT:
  Directory containing files for mapping

OUTPUT:
  Directory to place the processed files in

Options:
  -h,  --help     show help
```

By default it will process files named as `artist - title.mp3` and write the corresponding metadata.
