import argparse
import pathlib
from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime
import sys


DEBUG = False
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}


# https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3/library/pathlib.html
def parse_args() -> argparse.Namespace:
	"""Parses the command-line arguments."""
	parser = argparse.ArgumentParser(prog='Scorpion', description='Metadata viewer')
	parser.add_argument('image', type=pathlib.Path, nargs = '+', help='Image to view metadata') # each input will be converted to a pathlib.Path object
	parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Enable verbose output')
	args = parser.parse_args() # args is a Namespace object
	
	if args.verbose:
		global DEBUG
		DEBUG = True
	
	if DEBUG:
		print(f"[DEBUG] Fetched arguments: {args}")
	
	return args


def view_filedata(image_path: pathlib.Path) -> None:
    """Displays basic file attributes, such as creation date."""
    try:
        stats = os.stat(image_path)
        creation_time = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  File: {image_path}")
        print(f"  Creation Date: {creation_time}")
        print(f"  Size: {stats.st_size} bytes")
    except Exception as e:
        print(f"Error retrieving attributes for {image_path}: {e}")


def view_metadata(image_path: pathlib.Path) -> None:
    """Displays metadata of the given image."""
    if DEBUG:
        print(f"[DEBUG] Reading data for {image_path}")
    view_filedata(image_path)

    try:
        with Image.open(image_path) as img:
            if DEBUG:
                print(f"[DEBUG] Image opened: {image_path}")

            # formats with EXIF metadata
            exif_data = img._getexif()  # Extract EXIF metadata
            if exif_data:
                print(f"Metadata for {image_path}:")
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)  # Map tag ID to tag name
                    print(f"  {tag}: {value}")
            else:
                print(f"No metadata found for {image_path}.")
    except Exception as e:
        print(f"Error reading metadata for {image_path}: {e}")



def validate_images(image_paths):
    """Validates that all input paths are existing files with supported extensions."""
    for image in image_paths:
        if not image.exists():
            print(f"Error: {image} does not exist.")
            sys.exit(1)
        if not image.is_file():
            print(f"Error: {image} is not a valid file.")
            sys.exit(1)
        if image.suffix.lower() not in SUPPORTED_FORMATS:
            print(f"Error: {image} has an unsupported file extension.")
            sys.exit(1)


def main() -> None:
    args = parse_args()
    validate_images(args.image)
    
    for image in args.image:
          print(f"\nProcessing file: {image}")
          view_metadata(image)
    
if __name__ == '__main__':
    main()