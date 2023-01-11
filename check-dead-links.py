import requests
from bs4 import BeautifulSoup
import urllib.parse
from collections import deque

session = requests.Session()

def check_link(url, base_url):
    try:
        if url.startswith("#"):
            url = urllib.parse.urljoin(base_url, url)
        r = session.head(url, allow_redirects=True)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False
def crawl_site(url):
    queue = deque([url])
    visited = set()
    dead_links = []
    session = requests.Session()
    while queue:
        current_url = queue.popleft()
        parsed_url = urllib.parse.urlparse(current_url)
        try:
            r = session.get(current_url)
        except requests.exceptions.RequestException as e:
            # Log the error for debugging purposes
            print(f'Error: {e}')
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href.startswith('/'):
                href = urllib.parse.urljoin(current_url, href)
            elif href.startswith('http'):
                pass
            else:
                continue 
            if not check_link(href, parsed_url):
                dead_links.append((href, current_url))
                print(f'Dead link {href} found on page {current_url}')
        for link in links:
            href = link.get('href')
            if parsed_url.hostname == urllib.parse.urlparse(href).hostname and href not in visited:
                queue.append(href)
                visited.add(href)
    session.close()

url = 'https://url/'
crawl_site(url)
