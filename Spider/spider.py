# python3 spider.py -h

import argparse
import pathlib
import os
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin # to resolve relative path


DEBUG = True

# https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3/howto/argparse.html
def parse_args():
    parser = argparse.ArgumentParser(prog='Spider', description='A simple image scraper that downloads images from a given URL.')
    parser.add_argument('URL', help='The URL to download images from')
    parser.add_argument('-r', '--recursive', action='store_true', help='Download images recursively')
    parser.add_argument('-l', '--level', type=int, dest='depth', help='Maximum depth level for recursion', default=5)
    parser.add_argument('-p', '--path', type=pathlib.Path, help='Directory to save downloaded images', default='./data')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Enable verbose output')
    args = parser.parse_args()
    if DEBUG:
        print("[DEBUG] Parsed arguments:", args)
    return args



# https://docs.python.org/3/library/os.html
# https://docs.python.org/3/library/os.path.html#module-os.path
# https://docs.python.org/3/library/exceptions.html
def create_directory(path):
    try:
        if os.path.isfile(path):
            raise ValueError(f"The path '{path}' is a file, not a directory.")
        if not os.path.exists(path):
            os.makedirs(path)  
        if DEBUG:
            print(f"[DEBUG] Created directory: {path}")
        return path
    
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"Error while creating the directory '{path}': {e}") # for uncaght exceptions
        sys.exit(1)




# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
# https://www.w3schools.com/python/module_requests.asp
# https://docs.python.org/3/tutorial/errors.html
def fetch_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if DEBUG:
                print(f"[DEBUG] Successfully fetched: {url}")
                #print(f"[DEBUG] Page content (first 500 characters):\n{response.text[:500]}")
            return response.text
        else:
            print(f"Error: Failed to fetch: {url} (Status Code: {response.status_code})")
            return None
        
    # requests.exceptions.RequestException - base class for all exceptions raised by the requests library    
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching the URL '{url}': {e}")
        return None # we continue
# probably no exit here bc one page may fail, but we need to fetch more ???????




# https://pypi.org/project/beautifulsoup4/
def parse_img_urls(page, base_url): # add base_url
    try:
        soup = BeautifulSoup(page, 'html.parser')
        img_tags = soup.find_all('img') # tag to embed images in a webpage. ResultSet object(like list)
        if DEBUG:
            print(f"[DEBUG] Found img tags: {img_tags}")
            
        img_urls = [] # avoid duplicates
        for tag in img_tags:
            src = tag.get('src')
            if DEBUG:
                print(f"[DEBUG] Found image URL: {src}")
            if not src:
                continue
            
            src = urljoin(base_url, src) # resolve relative path if needed (handles both absolute and relative paths)
            img_urls.append(src) # add to set
            
        if DEBUG:
            print(f"[DEBUG] Parsed image URLs: {img_urls}")
            
        return img_urls # convert set to list just in case
        
    except Exception as e:
        print(f"Error while parsing image URLs: {e}")
        return []


# https://docs.python.org/3/library/os.path.html#os.path.basename
def download_img(img_url, path):
    try:
        img = requests.get(img_url).content
        img_name = sanitize_filename(img_url)
        img_path = os.path.join(path, img_name)

        
    except Exception as e:
        print(f"[ERROR] Unexpected error while downloading {img_url}: {e}")


        
# https://docs.python.org/3/library/sys.html
if __name__ == "__main__":
    try:
        args = parse_args()
        path = create_directory(args.path)
        page = fetch_page(args.URL)
        img_urls = parse_img_urls(page, args.URL)


    
    except Exception as e: # any uncaught exceptions
        print(f"Error: {e}")
        sys.exit(1)
        

# https://docs.python.org/3/library/functions.html#open
# https://pypi.org/project/beautifulsoup4/