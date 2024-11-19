Exercice 1 - Spider

The spider program allow you to extract all the images from a website, recursively, by providing a url as a parameter.
You have to manage the following program options:
   ./spider [-rlp] URL
• Option -r : recursively downloads the images in a URL received as a parameter.
• Option -r -l [N] : indicates the maximum depth level of the recursive download. If not indicated, it will be 5.
• Option -p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
The program will download the following extensions by default:
• .jpg/jpeg
• .png
• .gif
• .bmp



requirements.txt
contains all the external Python packages your script depends on:
requests – For HTTP requests.
beautifulsoup4 – For parsing HTML and extracting image URLs.
argparse – For handling command-line arguments (which is part of the Python standard library, so no need to install separately).
urllib – For URL parsing (also part of the Python standard library).
pathlib – For handling paths (again, part of Python's standard library).

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip list
deactivate
