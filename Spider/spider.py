# python3 spider.py -h

import argparse
import pathlib
import os
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import signal
import urllib.robotparser

DEBUG = False

# https://docs.python.org/3/library/signal.html
def handle_keyboard_interrupt(signal, frame) -> None:
    """Handles the keyboard interrupt (Ctrl+C) gracefully."""
    print("\n[INFO] Scraping interrupted by the user. Exiting...")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_keyboard_interrupt)

# https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3/library/pathlib.html
def parse_args() -> argparse.Namespace:
    """Parses the command-line arguments."""
    parser = argparse.ArgumentParser(prog='Spider', description='Image scraper that downloads images from a given URL.')
    parser.add_argument('URL', help='URL to download images from')
    parser.add_argument('-r', '--recursive', action='store_true', help='Download images recursively')
    parser.add_argument('-l', '--level', type=int, dest='depth', help='Max. depth level for recursion', default=5)
    parser.add_argument('-p', '--path', type=pathlib.Path, help='Directory to save images', default='./data')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Enable verbose output')
    args = parser.parse_args()
    
    if args.verbose:
        global DEBUG
        DEBUG = True
    
    if DEBUG:
        print(f"[DEBUG] Fetched arguments: {args}")
    
    return args

# https://docs.python.org/3/library/urllib.robotparser.html
def check_robots(url: str) -> None:
    """Checks robots.txt file for the URL."""
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url + "/robots.txt")
    rp.read()
    user_agent = "*"
    if not rp.can_fetch(user_agent, url):
        print(f"Warning: Scraping is forbidden by robots.txt for {url}")
        # sys.exit(1)
    if DEBUG:
        print(f"[DEBUG] Robots.txt checked for {url}")
        

def ensure_directory_exists(path: pathlib.Path) -> pathlib.Path:
    """Checks if the directory exists, creates it if it doesn't."""
    try:
        if os.path.isfile(path):
            raise ValueError(f"The path '{path}' is a file, not a directory.")
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"Error while creating the directory '{path}': {e}")
        sys.exit(1)


def fetch_page_content(url): # what is the return type of this function?  -> Optional[str]:
    """Fetches the content of the URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Failed to fetch: {url} (Status Code: {response.status_code})")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching the URL '{url}': {e}")
        return None


# https://docs.python.org/3/library/re.html
def is_image(url): #  -> Optional[re.Match]:
    """Checks if the URL corresponds to an image."""
    return re.search(r'\.(jpg|jpeg|png|gif|bmp)(\?.*)?$', url, re.IGNORECASE)


# https://docs.python.org/3/library/urllib.parse.html
def parse_image_urls(page, base_url):
    """Parses image URLs from the given page."""
    try:
        soup = BeautifulSoup(page, 'html.parser')
        img_tags = soup.find_all('img')
        img_urls = {urljoin(base_url, tag.get('src')) for tag in img_tags if tag.get('src') and is_image(tag.get('src'))}
        return list(img_urls)
    except Exception as e:
        print(f"[ERROR] Error while parsing image URLs: {e}")
        return []

# https://docs.python.org/3/library/os.html
def download_image(img_url, folder) -> None:
    """Downloads the image from the URL and saves it to the specified folder."""
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            filename = os.path.basename(img_url.split('?')[0])
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as img_file:
                for chunk in response.iter_content(chunk_size=1024):
                    img_file.write(chunk)
            if DEBUG:
                print(f"[DEBUG] Downloaded image: {filepath}")
        else:
            print(f"[ERROR] Failed to download image {img_url}, Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Unexpected error while downloading {img_url}: {e}")


# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
def scrape_images(url, save_path, recursive, depth, visited=None) -> None:
    """Recursively scrapes images from the given URL."""
    if visited is None:
        visited = set()
    
    if url in visited or depth < 0:
        return
    
    visited.add(url)
    page_content = fetch_page_content(url)
    if not page_content:
        return

    img_urls = parse_image_urls(page_content, url)
    for img_url in img_urls:
        download_image(img_url, save_path)

    if recursive:
        soup = BeautifulSoup(page_content, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        for link in links:
            scrape_images(link, save_path, recursive, depth - 1, visited)


def main() -> None:
    try:
        args = parse_args()
        check_robots(args.URL)
        path = ensure_directory_exists(args.path)
        scrape_images(args.URL, path, args.recursive, args.depth)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
