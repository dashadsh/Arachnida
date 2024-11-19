The second scorpion program receive image files as parameters and must be able to parse them for EXIF and other metadata, displaying them on the screen.
The program must at least be compatible with the same extensions that spider handles. It display basic attributes such as the creation date, as well as EXIF data. The out-
put format is up to you.
   ./scorpion FILE1 [FILE2 ...]

Python argparse module: For command-line argument parsing.
Pillow library (PIL): To read and extract EXIF and image metadata.
os and datetime modules: To extract creation dates and handle file system operations.
EXIF metadata: This is embedded in some image formats like JPEG and TIFF.


python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip list
deactivate